import protocolbase
from packet import TibiaPacket
import os
import otcrypto
import config
import socket
import time
import pickle
import sys

if os.path.exists('IP_CACHE') and os.path.getmtime('IP_CACHE') > time.time() - 2400:
    IPS = pickle.load(open('IP_CACHE', 'rb'))
else:
    IPS = {}

class LoginProtocol(protocolbase.TibiaProtocol):
    tcpNoDelay = True

    @gen.engine
    def onFirstPacket(self, packet):
        global IPS
        try:
            packet.uint8()
        except:
            return


        if config.letGameServerRunTheLoginServer:
            pos = packet.pos
            packet.pos = 0
            packetType = packet.uint8()
            if packetType == 0xFF:
                if packetType == 0xFF:
                    if packet.getX(4) == "info":
                        try:
                            sendPlayers == packet.uint8()
                        except:
                            sendPlayers = False

                        data = ""
                        # TODO: Send XML format.

                elif packetType == 0x01:
                    # Silly status protocol. No multi world support...
                    reqInfo = packet.uint16()

                    pkg = TibiaPacket()

                    if reqInfo & 0x01: # REQUEST_BASIC_SERVER_INFO
                        pkg.uint8(0x10)
                        pkg.string(config.server[0][0])
                        pkg.string(config.server[0][1])
                        pkg.uint16(4)
                        pkg.uint32(config.loginPort)

                    if reqInfo & 0x02: # REQUEST_SERVER_OWNER_INFO
                        pkg.uint8(0x11)
                        pkg.string(config.ownerName)
                        pkg.string(config.ownerEmail)

                    if reqInfo & 0x04: # REQUEST_MISC_SERVER_INFO
                        pkg.uint8(0x12)
                        pkg.string(config.motd)
                        pkg.string(config.location)
                        pkg.string(config.url)
                        pkg.uint64(time.time() - SERVER_START + config.tibiaTimeOffset)

                    if reqInfo & 0x08: # REQUEST_PLAYERS_INFO
                        pkg.uint8(0x20)
                        pkg.uint32(len(core.game.allPlayers))
                        pkg.uint32(config.gameMaxConnections)
                        pkg.uint32(len(core.game.allPlayers)) # TODO: Track record.

                    if reqInfo & 0x10: # REQUEST_SERVER_MAP_INFO
                        pkg.uint8(0x30)
                        pkg.string(core.game.map.mapInfo.description)
                        pkg.string(core.game.map.mapInfo.author)
                        pkg.uint16(core.game.map.mapInfo.width)
                        pkg.uint16(core.game.map.mapInfo.height)

                    # 0x20 and 0x40 is unimplanted.

                    if reqInfo & 0x80:
                        pkg.uint8(0x23)
                        pkg.string("PyOT")
                        pkg.string(SERVER_VERSION)
                        pkg.string("%s-%s" % (config.versionMin, config.versionMax))

                    pkg.send(self)
                    return

            packet.pos = pos

        packet.pos += 2
        #packet.uint16() # OS 0x00 and 0x01
        version = packet.uint16() # Version int

        if version >= 971:
            version = packet.uint32()
            packet.uint8() # Client type.

        packet.pos += 12 # Checksum for files

        if (len(packet.data) - packet.pos) == 128: # RSA 1024 is always 128
            packet.data = otcrypto.decryptRSA(packet.getData())
            packet.pos = 0 # Reset position

        else:
            print("RSA, length != 128 (it's %d)" % (len(packet.data) - packet.pos))
            self.transport.loseConnection()
            return

        v = packet.uint8()
        if not len(packet.data) or v != 0: # RSA needs to decrypt just fine, so we get the data, and the first byte should be 0
            print("RSA, first char != 0 ")
            self.transport.loseConnection()
            return
        # Set the XTEA key
        k = (packet.uint32(), packet.uint32(), packet.uint32(), packet.uint32())
        sum = 0
        self.xtea = [0] * 64
        for x in range(32):
            self.xtea[x] = sum + k[sum & 3] & 0xffffffff
            sum = (sum + 0x9E3779B9) & 0xffffffff
            self.xtea[32 + x] = sum + k[sum>>11 & 3] & 0xffffffff

        # If cffi, cast this.
        if otcrypto.ffi:
            self.xtea = otcrypto.ffi.new("const uint32_t[]", self.xtea)

        # Check if version is correct
        if version > config.versionMax or version < config.versionMin:
            self.exitWithError(config.versionError)
            print("Version incorrect")
            return


        # Check if there is a username (and a password)

        username = packet.string()
        password = packet.string()

        if not username and not config.anyAccountWillDo:
            self.exitWithError("You must enter your account number")
            return

        # Initialize the packet to send
        pkg = TibiaPacket()

        if username:
            # Our funny way of doing async SQL
            account = yield sql.runQuery("SELECT `id`, `premdays` FROM `accounts` WHERE `name` = %s AND `password` = SHA1(CONCAT(`salt`, %s))", username, password)

            if account:
                characters = yield sql.runQuery("SELECT `name`,`world_id` FROM `players` WHERE account_id = %s", account[0]['id'])

        if not username or not account:
            if config.anyAccountWillDo:
                account = ((0,0),)
                characters = config.anyAccountPlayerMap
            else:
                self.exitWithError("Invalid username or password")
                return

        if config.letGameServerRunTheLoginServer:
            import game.scriptsystem
            game.scriptsystem.get("preSendLogin").run(client=self, characters=characters, account=account, username=username, password=password)

        # Send motd
        pkg.uint8(0x14)
        pkg.string(config.motd)

        # Add character list
        pkg.uint8(0x64)
        pkg.uint8(len(characters))
        for character in characters:
            ip = config.servers[character['world_id']][0]
            port = config.gamePort

            if ':' in ip:
                ip, port = ip.split(':')
                port = int(port)
            if self.address == '127.0.0.1':
                ip = '127.0.0.1'
            elif ip in IPS:
                ip = IPS[ip]
            elif ip != 'auto':
                _ip = ip
                ip = socket.gethostbyname(ip)
                IPS[_ip] = ip
            else:
                import urllib.request, urllib.error, urllib.parse
                try:
                    ip = urllib.request.urlopen("http://vapus.net/ip.php").read()
                except:
                    ip = ""

                if not ip:
                    raise Exception("[ERROR] Automatic IP service is down!")


                IPS['auto'] = ip
                # Save IPS here.
                pickle.dump(IPS, open('IP_CACHE', 'wb'), 2)

            pkg.string(character['name'])
            pkg.string(config.servers[character['world_id']][1])
            pkg.raw(socket.inet_aton(ip if type(ip) == str else ip.decode('utf-8')))
            pkg.length += 4
            pkg.uint16(port)

            if version >= 980:
                pkg.uint8(0)
        # Add premium days
        pkg.uint16(account[0]['premdays'])
        pkg.send(self) # Send

    def exitWithError(self, message, error = 0x0A):
        packet = TibiaPacket()
        packet.uint8(error) # Error code
        packet.string(message) # Error message
        packet.send(self)
        self.loseConnection()

class LoginFactory(protocolbase.TibiaFactory):
    __slots__ = ()
    protocol = LoginProtocol

    def __repr__(self):
        return "<Login Server Factory>"
