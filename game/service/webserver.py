import tornado.web
import builtins
import config
from packet import TibiaPacket, TibiaPacketReader
from tornado.websocket import WebSocketHandler
from tornado import gen
import socket 
import game.protocol
import time
from position import Position
import sql
try:
    Web
except:
    # Web server also deals with the web-client interface.
    interface = [(r'/static/(.*)$', tornado.web.StaticFileHandler, {'path': config.dataDirectory + '/web_static/'})]
    if config.webClient:
        IPS = {}
        class WebClientSocket(WebSocketHandler):
            version = 860
            webSocket = True
            def open(self):
                # Set TCP no delay.
                self.set_nodelay(True)
                
                # Unlike Tibia, we don't send a first packet.
                # This is also encryption free. If we at some point choose to support ecnryption, it will be SSL, aka wss protocol, NOT XTEA!!!
                self.player = None
                self.protocol = game.protocol.getProtocol(860)
                self.ready = False
                self.xtea = None
                self.gotFirst = False
                self.username = ""
                self.address = self.request.remote_ip
                print("Opening")
            def check_origin(self, origin):
                return True
                
            def on_message(self, message):
                packet = TibiaPacketReader(message)
                if not self.gotFirst:
                    self.firstPacketLoginAccount(packet)
                elif not self.player:
                    self.firstPacketLoginChar(packet)
                else:
                    self.protocol.handle(self.player, packet)
                    
            def on_close(self):
                self.ready = False
                print("WebSocket closed")

            @gen.engine
            def firstPacketLoginAccount(self, packet):
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
                        # pickle.dump(IPS, open('IP_CACHE', 'wb'), 2)

                    pkg.string(character['name'])
                    pkg.string(config.servers[character['world_id']][1])
                    pkg.raw(socket.inet_aton(ip if type(ip) == str else ip.decode('utf-8')))
                    pkg.length += 4
                    pkg.uint16(port)

                # Add premium days
                pkg.uint16(account[0]['premdays'])
                pkg.send(self) # Send
                
                self.username = username
                self.password = password
                self.gotFirst = True
                

            @gen.engine
            def firstPacketLoginChar(self, packet):
                characterName = packet.string()

                if (not self.username and not config.anyAccountWillDo) or not characterName:
                    self.exitWithError("Could not get your account name, or character name")
                    return

                packet.pos += 6 # I don't know what this is

                # Our funny way of doing async SQL
                account = yield sql.runQuery("SELECT `id`,`language` FROM `accounts` WHERE `name` = %s AND `password` = SHA1(CONCAT(`salt`, %s))", self.username, self.password)

                if not account:
                    account = game.scriptsystem.get("loginAccountFailed").run(client=self, username=username, password=self.password)
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

                self.packet = self.player.packet
                self.player.sendFirstPacket()
                self.ready = True # We can now accept other packages

                # Call the login script
                game.scriptsystem.get("login").run(creature=self.player)
                
            def exitWithError(self, message, error = 0x14):
                packet = TibiaPacket()
                packet.uint8(error) # Error code
                packet.string(message) # Error message
                packet.send(self)
                self.close()
                        
            def send_error(self, code, exc_info):
                self.close()
                
        interface.append((config.webClientPath, WebClientSocket))
    Web = tornado.web.Application(interface);
    builtins.Web = Web
