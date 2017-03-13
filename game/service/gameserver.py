import protocolbase
import game.protocol
from collections import deque
import config
import otcrypto
import game.scriptsystem
from packet import TibiaPacket
import game.player
from game.map import getTile,removeCreature
from game.functions import updateTile
import struct
import time
from tornado import gen

waitingListIps = deque()
lastChecks = {}
class GameProtocol(protocolbase.TibiaProtocol):
    connections = 0
    tcpNoDelay = True

    def onInit(self):
        self.player = None
        self.protocol = None
        self.ready = False
        self.version = 0
        self.firstConnection = 0
        self.ping = 0

    def onConnect(self):
        pkg = TibiaPacket()
        pkg.uint8(0x1F)
        pkg.uint32(0xFFFFFFFF) # Used for?
        pkg.uint8(0xFF) # Used for?
        pkg.send(self)
        self.firstConnection = time.time()

    def exitWithError(self, message):
        packet = TibiaPacket(0x14)
        packet.string(message) # Error message
        packet.send(self)
        self.loseConnection()

    def exitWaitingList(self, message, slot):
        packet = TibiaPacket(0x16)
        packet.string(message) # Error message
        packet.uint8(15 + (2 * slot))
        packet.send(self)
        self.loseConnection()

    @gen.engine
    def onFirstPacket(self, packet):
        packetType = packet.uint8()
        IN_TEST = False

        if packetType == 0xFF:
            # Special case for tests.
            IN_TEST = True

        if packetType == 0x0A and not self.ready:
            #linux = 0x01 windows = 0x02 flash = 0x03 
            #otc_linux = 0x0A otc_windows = 0x0B otc_mac = 0x0C
            self.OSType = packet.uint16() # os type
            version = packet.uint16() # Version int

            # Calculate ping.
            self.ping = time.time() - self.firstConnection
            print("Ping: ", self.ping * 1000, "ms")
            if version >= 972:
                version = packet.uint32()
                packet.uint8() # Client type.

            self.protocol = game.protocol.getProtocol(version)
            self.version = version
            print(("Client protocol version %d" % version))

            if not self.protocol:
                print("Trying to load a invalid protocol")
                self.transport.loseConnection()
                return

            if not IN_TEST:
                if (len(packet.data) - packet.pos) == 128: # RSA 1024 is always 128
                    packet.data = otcrypto.decryptRSA(packet.getData()) # NOTICE: Should we do it in a seperate thread?
                    packet.pos = 0 # Reset position

                else:
                    print("RSA, length != 128 (it's %d)" % (packet.length - packet.pos))
                    self.transport.loseConnection()
                    return

                if not packet.data or packet.uint8(): # RSA needs to decrypt just fine, so we get the data, and the first byte should be 0
                    print("RSA, first char != 0")
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

            ip = self.address

            # Ban check.
            if game.ban.ipIsBanned(ip):
                self.exitWithError("Your ip is banned.\n %s" % game.ban.banIps[ip].message())
                return

            if config.gameMaxConnections <= (self.connections + len(waitingListIps)):
                if ip in waitingListIps:
                    i = waitingListIps.index(ip) + 1
                    lastChecks[ip] = time.time()
                    # Note: Everyone below this threshhold might connect. So even if your #1 on the list and there is two free slots, you can be unlucky and don't get them.
                    if i + self.connections > config.gameMaxConnections:
                        self.exitWaitingList("Too many players online. You are at place %d on the waiting list." % i, i)
                        return
                else:
                    waitingListIps.append(ip)
                    lastChecks[ip] = time.time()
                    self.exitWaitingList("Too many players online. You are at place %d on the waiting list." % len(waitingListIps), len(waitingListIps))
                    return
            self.connections += 1
            try:
                waitingListIps.remove(ip)
                del lastChecks[ip]
            except:
                pass

            # "Gamemaster" mode?
            gamemaster = packet.uint8()

            # Check if version is correct
            if version > config.versionMax or version < config.versionMin:
                self.exitWithError(config.versionError)
                return

            # Some weird thing with 9.7.
            try:
                # Check if there is a username (and a password)
                username = packet.string()

                characterName = packet.string()

                password = packet.string()
            except:
                self.exitWithError("Try again.")
                return

            if (not username and not config.anyAccountWillDo) or not characterName:
                self.exitWithError("Could not get your account name, or character name")
                return

            packet.pos += 6 # I don't know what this is

            # Our funny way of doing async SQL
            account = yield sql.runQuery("SELECT `id`,`language` FROM `accounts` WHERE `name` = %s AND `password` = SHA1(CONCAT(`salt`, %s))", username, password)

            if not account:
                account = game.scriptsystem.get("loginAccountFailed").run(client=self, username=username, password=password)
                if not account or account == True:
                    self.exitWithError("Invalid username or password")
                    return

            account = account[0]

            # Ban check.
            if game.ban.accountIsBanned(account['id']):
                self.exitWithError("Your account is banned.\n %s" % game.ban.banAccounts[account['id']].message())
                return

            if not len(account) >= 2 or not account['language']:
                language = config.defaultLanguage
            else:
                language = account['language']

            character = yield sql.runQuery("SELECT p.`id`,p.`name`,p.`world_id`,p.`group_id`,p.`account_id`,p.`vocation`,p.`health`,p.`mana`,p.`soul`,p.`manaspent`,p.`experience`,p.`posx`,p.`posy`,p.`posz`,p.`instanceId`,p.`sex`,p.`looktype`,p.`lookhead`,p.`lookbody`,p.`looklegs`,p.`lookfeet`,p.`lookaddons`,p.`lookmount`,p.`town_id`,p.`skull`,p.`stamina`, p.`storage`, p.`inventory`, p.`depot`, p.`conditions`, s.`fist`,s.`fist_tries`,s.`sword`,s.`sword_tries`,s.`club`,s.`club_tries`,s.`axe`,s.`axe_tries`,s.`distance`,s.`distance_tries`,s.`shield`,s.`shield_tries`,s.`fishing`, s.`fishing_tries`, g.`guild_id`, g.`guild_rank`, p.`balance` FROM `players` AS `p` LEFT JOIN player_skills AS `s` ON p.`id` = s.`player_id` LEFT JOIN player_guild AS `g` ON p.`id` = g.`player_id` WHERE p.account_id = %s AND p.`name` = %s AND p.`world_id` = %s", account['id'], characterName, config.worldId)

            if not character:
                character = game.scriptsystem.get("loginCharacterFailed").run(client=self, account=account, name=characterName)
                if not character or character == True:
                    self.exitWithError("Character can't be loaded")
                    return

            character = character[0]
            if gamemaster and character['group_id'] < 3:
                self.exitWithError("You are not gamemaster! Turn off gamemaster mode in your IP changer.")
                return

            # Ban check.
            if isinstance(character, game.player.Player):
                if game.ban.playerIsBanned(character):
                    self.exitWithError("Your player is banned.\n %s" % game.ban.banAccounts[character.data["id"]].message())
                    return
            elif game.ban.playerIsBanned(character['id']):
                self.exitWithError("Your player is banned.\n %s" % game.ban.banAccounts[character['id']].message())
                return

            # If we "made" a new character in a script, character = the player.
            player = None
            if isinstance(character, game.player.Player):
                player = character
                game.player.allPlayers[player.name()] = player
            elif character['name'] in game.player.allPlayers:
                player = game.player.allPlayers[character['name']]
                if player.client:
                    self.exitWithError("This character is already logged in!")
                    return
            if player:
                self.player = player
                if self.player.data["health"] <= 0:
                    self.player.onSpawn()
                self.player.client = self
                tile = getTile(self.player.position)
                tile.placeCreature(self.player)
                # Send update tile to refresh all players. We use refresh because it fixes the order of things as well.
                updateTile(self.player.position, tile)

            else:
                # Load deathlist.
                yield deathlist.loadDeathList(character['id'])
                character["language"] = language
                game.player.allPlayers[character['name']] = game.player.Player(self, character)
                self.player = game.player.allPlayers[character['name']]
                if self.player.data["health"] <= 0:
                    self.player.onSpawn()

                try:
                    tile = getTile(self.player.position)
                    tile.placeCreature(self.player)
                    # Send update tile to refresh all players. We use refresh because it fixes the order of things as well.
                    updateTile(self.player.position, tile)

                except AttributeError:
                    self.player.position = Position(*game.map.mapInfo.towns[1][1])
                    tile = getTile(self.player.position)
                    tile.placeCreature(self.player)
                    # Send update tile to refresh all players. We use refresh because it fixes the order of things as well.
                    updateTile(self.player.position, tile)

            # Update last login
            sql.runOperation("UPDATE `players` SET `lastlogin` = %s WHERE `id` = %s", int(time.time()), character['id'])

            #notifies to otclient that this server can receive extended game protocol opcodes
            self.player.sendExtendedOpcode(0x00, "")

            self.packet = self.player.packet
            self.player.sendFirstPacket()
            self.ready = True # We can now accept other packages

            # Call the login script
            game.scriptsystem.get("login").run(creature=self.player)

            # If we got a waiting list, now is a good time to verify the list
            if lastChecks:
                checkTime = time.time()
                for entry in lastChecks:
                    if checkTime - lastChecks[entry] > 3600:
                        waitingListIps.remove(entry)
                        del lastChecks[entry]

        elif packetType == 0x00 and self.transport.address in config.executeProtocolIps:
            self.gotFirst = False
            t = TibiaPacket()
            if not config.executeProtocolAuthKeys:
                self.ready = 2
            try:
                while True:
                    op = packet.string()
                    print(op)
                    if op == "CALL" and self.ready == 2:
                        print("do this")
                        result = yield game.functions.executeCode(packet.string())

                        t.string(result)
                    elif op == "AUTH":
                        print("auth")
                        result = packet.string() in config.executeProtocolAuthKeys
                        if result:
                            t.string("True")
                            self.ready = 2
                        else:
                            t.string("False")
            except struct.error:
                pass # End of the line
            t.send(self)

    def onPacket(self, packet):
        packet.data = otcrypto.decryptXTEA(packet.getData(), self.xtea)
        packet.pos = 2

        return self.protocol.handle(self.player, packet)

    def onConnectionLost(self):
        if self.player:
            print(("Lost connection on, ", self.player.position))
            self.player.client = None

            if self.player.alive and not self.player.prepareLogout():
                logoutBlock = self.player.getCondition(CONDITION_INFIGHT)
                call_later(logoutBlock.length, self.onConnectionLost)
                return

            self.player.knownCreatures = set()
            self.player.knownBy = set()
            for x in list(game.player.allPlayers.values()):
                if x.client and self.player.data["id"] in x.getVips():
                    stream = x.packet()
                    stream.vipLogout(self.player.data["id"])
                    stream.send(x.client)

            game.scriptsystem.get("logout").run(creature=self.player)
            self.player.despawn()

    """def packet(self, type=None):
        if self.player:
            return (type)"""

class GameFactory(protocolbase.TibiaFactory):
    __slots__ = ()
    protocol = GameProtocol

    def __repr__(self):
        return "<Game Server Factory>"
