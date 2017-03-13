import time
import sys
import os
sys.path.insert(0, '.')
sys.path.insert(0, '..')
sys.path.insert(1, 'game')
sys.path.insert(2, '../game')
import config
config.loadEntierMap = False # Force false on this one.
import packet
import random
import string
import game.functions
import game.loading
import builtins
from tornado import gen
from game.service import gameserver
from tornado import gen, ioloop
builtins.IS_IN_TEST = True
# Some config.
SERVER = None
TEST_PROTOCOL = 963
TEST_PLAYER_ID = random.randint(10, 0x7FFFFFFF)
TEST_PLAYER_NAME = "__TEST__"

builtins.PYOT_RUN_SQLOPERATIONS = False

import os, time, functools, types, unittest
io_loop = ioloop.IOLoop().instance()
builtins.IOLoop = io_loop

def async_test(func):
    def _async_test(self):
        loop = ioloop.IOLoop.instance()
             
        loop.run_sync(lambda: gen.coroutine(func)(self), 3)
    return _async_test
 
async_test.__test__ = False # Nose otherwise mistakes it for a test

class Client:
    """ This is both the transport, and the connection for tests. """
    def __init__(self):
        self.server = self
        self.xtea = None
        self.address = '127.0.0.1'
        self.connected = True
        self._packets = []
        self.socket = DummySocket()
        self.transport = self
        self.ready = True
        self.protocol = game.protocol.getProtocol(TEST_PROTOCOL)
        self.version = TEST_PROTOCOL
        self.webSocket = False        
    def sendPacket(self, format, *argc, **kwargs):
        import packet as p
        import otcrypto
        from struct import pack
        from zlib import adler32
        
        packet = p.TibiaPacket()
        i = 0
        for c in format:
            if c == "b":
                packet.uint8(argc[i])
            elif c == "h":
                packet.uint16(argc[i])
            elif c == "i":
                packet.uint32(argc[i])
            elif c == "q":
                packet.uint64(argc[i])
            elif c == "P":
                packet.uint16(argc[i].x)
                packet.uint16(argc[i].y)
                packet.uint8(argc[i].z)
            elif c == "s":
                packet.string(argc[i])

            i += 1
            
        

        if self.client.xtea:
            length = sum(map(len, packet.data))
            packet.data[0] = bytes(str(length))
            data = otcrypto.encryptXTEA(packet.data, self.client.xtea, length)
        else:
            packet.data[0] = b''
            try:
                data = b''.join(packet.data)
            except:
                print((packet.data))
                
        data = pack("<I", adler32(data) & 0xffffffff)+data
        if kwargs:
            return p.TibiaPacketReader(data)
        else:
            self.client.handlePacketData(data)
                
    def write(self, data):
        # From server. Never use directly on the test side!
        self._data = data
        self._packets.append(packet.TibiaPacketReader(data))
        self._packets[-1].pos += 8

        
    def set_close_callback(self, callback):
        pass # Ignore.
        
    def read_bytes(*argc):
        pass 

class DummySocket:
    def setsockopt(*argc):
        pass        
class FrameworkTest(unittest.TestCase):
    def setUp(self):
        self._overrideConfig = {}
        self.initializeClient()
        io_loop.run_sync(self.initializeEngine)
        self.addCleanup(self.clear)
        self.addCleanup(self.restoreConfig)
        
        self.init()

    def get_new_ioloop(self):
        return ioloop.IOLoop.instance()
    
    def init(self):
        pass
    def cleanup(self):
        pass
    def initializeClient(self):
        self.client = Client()
        
        self.tr = self.client
    def clear(self):
        # Clear all players.
        for player in list(game.player.allPlayers.values()):
            self.destroyPlayer(player)
            
        self.cleanup()
        
    def overrideConfig(self, name, value):
        self._overrideConfig[name] = getattr(config, name)
        
        setattr(config, name, value)
        
    def restoreConfig(self, key=None):
        if key:
            setattr(config, key, self._overrideConfig[key])
        else:
            for key in self._overrideConfig:
                setattr(config, key, self._overrideConfig[key])
            
    @gen.coroutine
    def initializeEngine(self):
        global SERVER
        if not SERVER:
            startTime = time.time()
            
            # Load the core stuff!
            # Note, we use 0 here so we don't begin to load stuff before the reactor is free to do so, SQL require it, and anyway the logs will get fucked up a bit if we don't
            SERVER = gameserver.GameProtocol
            self.server = SERVER(self.client, '127.0.0.1', None)
            yield game.loading.loader(startTime)

        self.server = SERVER(self.client, '127.0.0.1', None)
        self.client.client = self.server
    def destroyPlayer(self, player):
        # Despawn.
        player.despawn()
        # Force remove.
        del game.player.allPlayers[player.name()]
        del game.creature.allCreatures[player.cid]
        
        try:
            self.trackPlayers.remove(player)
        except:
            pass
        
class FrameworkTestGame(unittest.TestCase):
    destroyPlayer = FrameworkTest.destroyPlayer
    initializeEngine = FrameworkTest.initializeEngine
    restoreConfig = FrameworkTest.restoreConfig
    overrideConfig = FrameworkTest.overrideConfig
    clear = FrameworkTest.clear
    initializeClient = FrameworkTest.initializeClient
    
    
    def get_new_ioloop(self):
        return ioloop.IOLoop.instance()
        
    def init(self):
        pass
    def cleanup(self):
        pass
    def setUp(self):
        self.initializeClient()
        self.player = None
        io_loop.run_sync(self.initializeEngine)
        self.trackPlayers = []
        self.fixConnection()
        self.setupPlayer(TEST_PLAYER_ID, TEST_PLAYER_NAME, True)
        

        
        self._overrideConfig = {}
        self.addCleanup(self.clear)
        self.addCleanup(self.restoreConfig)
        
        self.init()

    def clear(self, recreate = False):
        if self.player: # Tests might clear us already. Etc to test clearing!
            self.destroyPlayer(self.player)

        for player in self.trackPlayers[:]:
            self.destroyPlayer(player)
        
        # Clear deathlists.
        deathlist.byKiller = {}
        deathlist.byVictim = {}
        deathlist.loadedDeathIds = set()
        
        if recreate:
            self.setupPlayer(TEST_PLAYER_ID, TEST_PLAYER_NAME, True)
            
        # Cleanup.
        tile = getTile(Position(1000, 1000, 7))
        if tile and len(tile):
            for thing in tile[:]:
                if isinstance(thing, Item) and not thing.fromMap:
                    tile.removeItem(thing)
                
        # Cleanup.
        tile = getTile(Position(1000, 1001, 7))
        if tile and len(tile):
            for thing in tile[:]:
                if isinstance(thing, Item) and not thing.fromMap:
                    tile.removeItem(thing)
                
        # Cleanup.
        tile = getTile(Position(1000, 999, 7))
        if tile and len(tile):
            for thing in tile[:]:
                if isinstance(thing, Item) and not thing.fromMap:
                    tile.removeItem(thing)
                
        # Clear instances.
        for instance in game.map.instances.copy():
            if instance != 0:
                del game.map.instances[instance]
                # Might not be set if we never load anything.
                try:
                    del game.map.knownMap[instance]
                except:
                    pass

        # Clear open bags.
        try:
            self.player.openContainers.clear()
        except:
            pass
    def virtualPlayer(self, id, name):
        # Setup a virtual player.
        # No network abilities, or spawning or such.
        
        # Data must be valid, just random.
        data = {"id": id, "name": name, "world_id": 0, "group_id": 6, "account_id": 0, "vocation": 6, "health": 100, "mana": 100, "soul": 100, "manaspent": 10000, "experience": 5000, "posx": 1000, "posy": 1000, "posz": 7, "instanceId": None, "sex": 0, "looktype": 100, "lookhead": 100, "lookbody": 100, "looklegs": 100, "lookfeet": 100, "lookaddons": 0, "lookmount": 100, "town_id": 1, "skull": 0, "stamina": 100000, "storage": "", "inventory": "", "depot": "", "conditions": "", 'fist': 10, 'sword': 10, 'club': 10, 'axe': 10, 'distance': 10, 'shield': 10, 'fishing': 10, 'fist_tries': 0, 'sword_tries': 0, 'club_tries': 0, 'axe_tries': 0, 'distance_tries': 0, 'shield_tries': 0, 'fishing_tries': 0, "language":"en_EN", "guild_id":0, "guild_rank":0, "balance":0}

        # Add player as if he was online.
        try:
            self.client
        except:
            self.initializeClient()
        else:
            if self.client == None:
                self.initializeClient()

        player = game.player.Player(self.client, data)
        game.player.allPlayers[name] = player

        # Disable saving.
        player.doSave = False
        
        return player
        
    def setupPlayer(self, id=None, name=None, clientPlayer = False):
        if id is None:
            id = random.randint(1, 0x7FFFFFFF)
        if name is None:
            name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))

        # A virtual player with network abilities and spawning.
        player = self.virtualPlayer(id, name)
        
        # Add him to the position.
        tile = getTile(player.position)
        tile.placeCreature(player)

        # Game server does this.
        if clientPlayer:
            self.player = player
            self.client.packet = self.player.packet
            self.player._packet = self.client.protocol.Packet()
            self.player._packet.stream = self.client
            self.client.player = player
            
        # Track it.
        self.trackPlayers.append(player)
        
        # Note, we do not send firstLoginPacket, or even packet for our spawning. Thats for a test to do.
        
        return player
        
    def fixConnection(self):
        # Imagine we already sent the login packet. And all is well.
        self.server.gotFirst = True
        self.server.player = self.player
        self.server.ready = True
        self.server.version = TEST_PROTOCOL
        self.server.protocol = game.protocol.getProtocol(TEST_PROTOCOL)
