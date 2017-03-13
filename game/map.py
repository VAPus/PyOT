from game.item import Item
import game.item
from . import scriptsystem
import config
import time
import struct
import sys
import importlib

try:
    mapInfo = importlib.import_module('%s.%s.info' % (config.dataDirectory, config.mapDirectory))
except ImportError:
    print("[ERROR] Map got no info.py file in %s/%s/" % (config.dataDirectory, config.mapDirectory))
    sys.exit()

sectorX, sectorY = mapInfo.sectorSize
sectorShiftX = 0
sectorShiftY = 0

dummyItems = {}

knownMap = {} # sectorSum -> {posSum}

instances = {}

houseTiles = {}

houseDoors = {}

dummyTiles = {}

sectors = set()

for n in range(12):
    if sectorX == 2**n:
        sectorShiftX = n
    if sectorY == 2**n:
        sectorShiftY = n

if sectorShiftX == sectorShiftY == 0:
    print("Sector size (%d, %d) are not a power of two." % (sectorX, sectorY))
    sys.exit()

##### Position class ####
def __uid():
    idsTaken = 1
    while True:
        idsTaken += 1
        yield idsTaken
newInstanceId = __uid().__next__

if config.loadEntierMap:
    # We don't need to call loader.
    def getTile(pos, knownMap=knownMap):
        """ Returns the Tile on this position. """
        posSum = pos.hash

        if posSum in knownMap:
            return knownMap[posSum]

else:
    def getTile(pos, knownMap=knownMap):
        """ Returns the Tile on this position. """
        posSum = pos.hash
    
        if posSum in knownMap:
            return knownMap[posSum]
        elif loadTiles(pos.x, pos.y, pos.instanceId, (pos.instanceId, pos.x >> sectorShiftX, pos.y >> sectorShiftY)):
            return knownMap[posSum] if posSum in knownMap else None

def getTileIfExist(pos, _knownMap=knownMap):
    """ Returns the Tile on this position, but doesn't load non-existing tiles. """
    posSum = pos.hash
    if posSum in _knownMap:
        return _knownMap[posSum]
    else:
        return None

def setTile(pos, tile, knownMap = knownMap):
    """ Set the tile on this position. """
    posSum = pos.hash

    knownMap[posSum] = tile
    return True

def getTileConst(x,y,z,instanceId):
    """ Return the tile on this (unpacked) position. """
    posSum = instanceId << 40 | x << 24 | y << 8 | z
    if posSum in knownMap:
        return knownMap[posSum]
    elif loadTiles(x, y, instanceId, (instanceId, x >> sectorShiftX, y >> sectorShiftY)):
        return knownMap[posSum] if posSum in knownMap else None

if config.loadEntierMap:
     # We don't have to do loading.
     def getTileConst2(posSum, secSum, x, y, instanceId, knownMap = knownMap):
        """ Used by floorDescription """
        if posSum in knownMap:
            return knownMap[posSum]
else:
    def getTileConst2(posSum, secSum, x, y, instanceId, knownMap = knownMap):
        """ Used by floorDescription """
        if posSum in knownMap:
            return knownMap[posSum]
        elif loadTiles(x, y, instanceId, secSum):
             return knownMap[posSum] if posSum in knownMap else None

def getHouseId(pos):
    """ Returns the houseId on this position, or False if none """
    try:
        return getTile(pos).houseId
    except:
        return False

def placeCreature(creature, pos):
    """ Place a creature on this position. """
    try:
        return getTile(pos).placeCreature(creature)
    except:
        return False

def removeCreature(creature, pos):
    """ Remove the creature on this position. """
    try:
        return getTile(pos).removeCreature(creature)
    except:
        return False

def newInstance(base=None):
    """ Returns a new instanceId """
    instance = newInstanceId()
    if base:
        instances[instance] = base + '/'
    else:
        instances[instance] = ''

    return instance

class Tile(list):
    __slots__ = 'flags',
    def __init__(self, items, flags=0):
        if items:
            super().__init__(items)
          
        # 64bit optimize. 8 first for flags, 12 bit for top count, 12 bit for creature count and 12 bit for bottom count. 
        self.flags = flags

        if items and flags < 0xff: # No upper bits.
            for thing in items[1:]:
                if isinstance(thing, Creature):
                    self.flags += 1 << 20
                elif thing.ontop:
                    self.flags += 1 << 8
                else:
                    self.flags += 1 << 32

    def getCreatureCount(self):
        """ Returns the number of creatures on this tile. """
        return (self.flags >> 20) & 0xfff

    def getItemCount(self):
        """ Returns the number of items (:class:`game.item.Item`) (minus the ground) on this tile. """
        return len(self) - self.getCreatureCount()

    def getTopItemCount(self):
        """ Return the number of ontop items (:class:`game.item.Item`) (minus the ground) on this tile. """
        return 1+(self.flags >> 8) & 0xfff
        
    def getBottomItemCount(self):
        """ Return the number of non-ontop items (:class:`game.item.Item`) (minus the ground) on this tile. """
        return (self.flags >> 32) & 0xfff

    def getFlags(self):
        """ Return the tile flags """
        return self.flags

    def setFlag(self, flag):
        """ Set a flag on the tile """
        flags = self.getFlags()
        if not flags & flag:
            self.flags = flags | flag

    def unsetFlag(self, flag):
        """ Unset a flag on the tile """
        if self.getFlags() & flag:
            self.flags -= flag

    def placeCreature(self, creature):
        """ Place a Creature (subclass of :class:`game.creature.Creature`) on the tile. """
        self.flags += 1 << 20

        pos = len(self) - self.getBottomItemCount()

        self.insert(pos, creature)
        return pos

    def removeCreature(self,creature):
        """ Remove a Creature (subclass of (:class:`game.creature.Creature`) on the tile. """

        self.remove(creature)
        self.flags -= 1 << 20
        
    def placeItem(self, item):
        """ Place an Item (:class:`game.item.Item`) on the tile. This automatically deals with ontop etc. """
        if item.ontop:
            pos = 1 #self.getTopItemCount()
            self.insert(pos, item)
            self.flags += 1 << 8
        else:
            pos = self.getTopItemCount() + self.getCreatureCount() #len(self)
            self.insert(pos, item)
            self.flags += 1 << 32
        return pos

    def placeItemEnd(self, item):
        """ Place an idea at the end of the item stack. This function should NOT usually be used with ontop items. """
        self.flags += 1 << 32

        self.append(item)
        return len(self)

    def bottomItems(self):
        """ Returns a list or tuple with bottom items. """
        bottomItems = self.getBottomItemCount()

        if not bottomItems:
            return

        return self[len(self) - bottomItems:]

    def topItems(self):
        """ Returns an iterator over top items (including the ground). """
        return self[:self.getTopItemCount()]

    def getItems(self):
        """ Returns an iterator over all items on this tile. """

        for thing in self:
            if thing.isItem():
                yield thing

    def creatures(self):
        """ Returns an iterator over all creatures on this tile. """
        creatureCount = self.getCreatureCount()
        if creatureCount:
            topCount = self.getTopItemCount()
            return self[topCount:topCount+creatureCount]
        else:
            return []

    def hasCreatures(self):
        """ Returns True if the tile holds any creatures (:class:`game.creature.Creature`). """
        return self.getCreatureCount() > 0

    def topCreature(self):
        """ Returns the top (first) creature (subclass of :class:`game.creature.Creature`) on the tile. """
        # XXX: This is actually a constant of things[topitemcount]
        for thing in self:
            if isinstance(thing, Creature):
                return thing

    def removeItem(self, item):
        """ Remove the `item` (:class:`game.item.Item`)  from the tile. """
        item.stopDecay()
        self.remove(item)
        if item.ontop:
            self.flags -= 1 << 8
        else:
            self.flags -= 1 << 32

    def removeItemWithId(self, itemId):
        """ Remove items with id equal `itemId` on this tile. """
        for i in self.getItems():
            if i.itemId == itemId:
                self.removeItem(i)


    def getThing(self, stackpos):
        """ Returns the thing on this stack position. """
        try:
            return self[stackpos]
        except:
            return None

    def setThing(self, stackpos, item):
        """ Set the item (can be either a creature or a item) to this stack position. stackpos is one less due to ground. """
        self[stackpos+1] = item

    def findItem(self, itemId):
        """ returns the first item with id equal to `itemId` """
        for x in self.bottomItems():
            if x.itemId == itemId:
                return x

    def findStackpos(self, thing):
        """ Returns the stackposition of that `thing` on this tile. """
        return self.index(thing)

    def findClientItem(self, cid, stackpos=None):
        """ (DON'T USE THIS) """
        for x in self.bottomItems():
            if x.itemId == cid:
                if stackpos:
                    return (self.index(x), x)
                return x


    def copy(self):
        """ Returns a copy of this tile. Used internally for unstacking. """
        items = []
        for item in self:
            if item.isItem():
                items.append(item.copy())

        flags = self.flags
        if flags & TILEFLAGS_STACKED:
            flags -= TILEFLAGS_STACKED
        flags -= self.getCreatureCount() << 20
        return Tile(items, flags)

class HouseTile(Tile):
    __slots__ = ('houseId', 'position')


def loadTiles(x,y, instanceId, sectorSum):
    """ Load the sector witch holds this x,y position. Returns the result. """
    if sectorSum in sectors: return None
    if x > mapInfo.height or y > mapInfo.width or x < 0 or y < 0:
        return None

    return load(sectorSum[1], sectorSum[2], instanceId, sectorSum)

### Start New Map Format ###

attributeIds = ('actions', 'count', 'solid','blockprojectile','blockpath','usable','pickable','movable','stackable','ontop','hangable','rotatable','animation', 'doorId', 'depotId', 'text', 'written', 'writtenBy', 'description', 'teledest')

# Format (Work in Progress)
# Note: Max sector size in PyOt is 1024.
"""
    <uint8>floor_level
    floorLevel < 60
        <loop>

        <uint16>itemId
        <uint8>attributeCount / other

        itemId >= 100:
            every attributeCount (
                See attribute format
            )

        itemId == 50:
            <int32> Tile flags

        itemId == 51:
            <uint32> houseId

        itemId == 0:
            skip attributeCount fields

        {
            ; -> go to next tile
            | -> skip the remaining y tiles (if itemId = 0, and attrNr, skip attrNr x tiles)
            ! -> skip the remaining x and y tiles
            , -> more items
        }

    floorLevel == 60:
        <uint16>center X
        <uint16>center Y
        <uint8>center Z
        <uint8> Radius from center creature might walk
        <uint8> count (
            <uint8> type (61 for Monster, 62 for NPC)
            <uint8> nameLength
            <string> Name

            <int8> X from center
            <int8> Y from center

            <uint16> spawntime in seconds

            }
        )
    Attribute format:

    {
        <uint8>attributeId
        <char>attributeType
        {
            attributeType == i (
                <int32>value
            )
            attributeType == s (
                <uint16>valueLength
                <string with length valueLength>value
            )
            attributeType == T
            attributeType == F

            attributeType == l (
                <uint8>listItems
                <repeat this block for listItems times> -> value
            )
        }


    }
"""

_l_unpack = struct.Struct("<HB").unpack
_long_unpack = struct.Struct("<i").unpack
_creature_unpack = struct.Struct("<bbI").unpack
_spawn_unpack = struct.Struct("<HHBBB").unpack

def loadSectorMap(code, instanceId, baseX, baseY):
    """ Parse the `code` (sector data) starting at baseX,baseY. Returns the sector. """
    global dummyItems, dummyTiles
    thisSectorMap = {}
    pos = 0
    codeLength = len(code)
    skip = False
    skip_remaining = False
    houseId = 0

    # Bind them locally, this is suppose to make a small speedup as well, local things can be more optimized :)
    # Pypy gain nothing, but CPython does.

    l_Item = game.item.makeItem
    l_Tile = Tile
    l_HouseTile = HouseTile
    l_Position = Position
    l_attributes = attributeIds

    # Spawn commands
    l_getNPC = game.npc.getNPC
    l_getMonster = game.monster.getMonster

    # Local reference (for CPython)
    lord = int
    l_unpack = _l_unpack
    long_unpack = _long_unpack
    creature_unpack = _creature_unpack
    spawn_unpack = _spawn_unpack
    boundX, boundY = mapInfo.sectorSize
    globalProtection = config.globalProtectionZone
    protectedZones = config.protectedZones
    stackTiles = config.stackTiles
    l_dummyItems = dummyItems
    l_dummyTiles = dummyTiles
    l_houseData = game.house.houseData

    # This is the Z loop (floor), we read the first byte
    while pos < codeLength:
        # First byte where we're at.
        level = lord(code[pos])

        pos += 1

        if level == 60:
            centerX, centerY, centerZ, centerRadius, creatureCount = spawn_unpack(code[pos:pos+7])
            pos += 7

            # Mark a position
            centerPoint = l_Position(centerX, centerY, centerZ, instanceId)

            # Here we use attrNr as a count for
            for numCreature in range(creatureCount):
                creatureType = lord(code[pos])

                nameLength = lord(code[pos+1])

                name = code[pos+2:pos+nameLength+2].decode('utf-8')
                pos += 8 + nameLength
                spawnX, spawnY, spawnTime = creature_unpack(code[pos-6:pos])

                if creatureType == 61:
                    creature = l_getMonster(name)
                else:
                    creature = l_getNPC(name)
                if creature:
                    creature.spawn(l_Position(centerX+spawnX, centerY+spawnY, centerZ, instanceId), radius=centerRadius, spawnTime=spawnTime, radiusTo=centerPoint)
                else:
                    print("Spawning of %s '%s' failed, it doesn't exist!" % ("Monster" if creatureType == 61 else "NPC", name))
                
            continue

        # Loop over the mapInfo.sectorSize[0] x rows
        for xr in range(boundX):
            # Since we need to deal with skips we need to deal with counts and not a static loop (pypy will have a problem unroll this hehe)
            yr = 0

            while yr < boundY:
                # The items array and the flags for the Tile.
                items = []
                flags = 0

                # We have no limit on the amount of items that a Tile might have. Loop until we hit a end.
                while True:
                    # uint16 itemId / type
                    # uint8 attrNr / count
                    itemId, attrNr = l_unpack(code[pos:pos+3])

                    # Do we have a positive id? If not its a blank tile
                    if itemId:
                        # Tile flags
                        if itemId == 50:
                            pos += 2
                            # int32
                            flags = long_unpack(code[pos:pos+4])[0]

                            pos += 5

                        # HouseId?
                        elif itemId == 51:
                            pos += 2
                            # int32
                            houseId = long_unpack(code[pos:pos+4])[0]

                            pos += 5

                        elif attrNr:
                            pos += 3
                            attr = {}
                            for n in range(attrNr):
                                name = l_attributes[lord(code[pos])]


                                opCode = code[pos+1]
                                pos += 2
                                value = None
                                if opCode == 105: # = i
                                    pos += 4
                                    value = long_unpack(code[pos-4:pos])[0]
                                elif opCode == 115: # = s
                                    valueLength = long_unpack(code[pos:pos+4])[0]
                                    pos += valueLength + 4
                                    value = code[pos-valueLength:pos]
                                elif opCode == 84: # = T
                                    value = True
                                elif opCode == 70: # = F
                                    value = False
                                elif opCode == 108: # = l
                                    value = []
                                    length = lord(code[pos])

                                    pos += 1
                                    for i in range(length):
                                        opCode = code[pos]
                                        pos += 1
                                        if opCode == 105: # = i
                                            pos += 4
                                            item = long_unpack(code[pos-4:pos])[0]
                                        elif opCode == 115: # = s
                                            valueLength = long_unpack(code[pos:pos+4])[0]
                                            pos += valueLength + 4
                                            item = code[pos-valueLength:pos]
                                        elif opCode ==84:  # = T
                                            item = True
                                        elif opCode == 70: # = F
                                            item = False
                                        value.append(item)
                                else:
                                    raise Exception("attr opCode %d not found!" % opCode)
                                attr[name] = value

                            pos += 1
                            attr['fromMap'] = True
                            item = l_Item(itemId, **attr)
                            items.append(item)
                        else:
                            pos += 4
                            try:
                                items.append(l_dummyItems[itemId])
                            except KeyError:
                                try:
                                    item = l_Item(itemId)
                                except KeyError:
                                    pass # Item does not exist.
                                else:
                                    item.tileStacked = True
                                    item.fromMap = True
                                    l_dummyItems[itemId] = item
                                    items.append(item)



                    else:
                        pos += 4
                        if attrNr:
                            yr += attrNr -1



                    v = code[pos-1]
                    if v == 59: break # v == ;
                    elif v ==124: # v == |
                        skip = True
                        if attrNr:
                            xr += attrNr -1
                        break
                    elif v == 33: # v == !
                        skip = True
                        skip_remaining = True
                        break

                    # otherwise it should be ",", we don't need to verify this.

                if len(items):
                    ySum = instanceId << 40 | (xr + baseX) << 24 | (yr + baseY) << 8 | level
                    # For the PvP configuration option, yet allow scriptability. Add/Remove the flag.
                    if globalProtection and not flags & TILEFLAGS_PROTECTIONZONE:
                        flags += TILEFLAGS_PROTECTIONZONE
                    elif not protectedZones and flags & TILEFLAGS_PROTECTIONZONE:
                        flags -= TILEFLAGS_PROTECTIONZONE

                    if houseId:
                        # Fix flags if necessary, TODO: Move this to map maker!
                        if protectedZones and not flags & TILEFLAGS_PROTECTIONZONE:
                            flags += TILEFLAGS_PROTECTIONZONE

                        tile = l_HouseTile(items, flags)
                        tile.houseId = houseId
                        tile.position = ySum


                        # Find and cache doors
                        for i in tile.getItems():
                            if i.hasAction(b"houseDoor"):
                                try:
                                    houseDoors[houseId].append(ySum)
                                    break
                                except:
                                    houseDoors[houseId] = [ySum]


                        if houseId in houseTiles:
                            houseTiles[houseId].append(tile)
                        else:
                            houseTiles[houseId] = [tile]

                        try:
                            for item in l_houseData[houseId].data["items"][ySum]:
                                tile.placeItem(item)
                        except KeyError:
                            pass

                        houseId = 0
                        thisSectorMap[ySum] = tile

                    elif stackTiles:
                        ok = False
                        for i in items:
                            if i.solid:
                                ok = True
                                break
                        if ok:
                            # Constantify items on stacked tiles. This needs some workarounds w/transform. But prevents random bug.
                            if items:
                                hash = []
                                for i in items:
                                    hash = i.itemId 
                                hash = tuple(items)

                            try:
                                thisSectorMap[ySum] = _dummyTiles[hash]
                            except:
                                tile = l_Tile(items, flags + TILEFLAGS_STACKED)
                                l_dummyTiles[hash] = tile
                                thisSectorMap[ySum] = tile

                        else:
                            thisSectorMap[ySum] = l_Tile(items, flags)

                    else:
                        thisSectorMap[ySum] = l_Tile(items, flags)
                yr += 1

                if skip:
                    skip = False
                    break

            if skip_remaining:
                skip_remaining = False
                break

    return thisSectorMap
### End New Map Format ###

def load(sectorX, sectorY, instanceId, sectorSum, verbose=True):
    """ Load sectorX.sectorY.sec. Returns True/False """

    t = time.time()

    # Attempt to load a sector file
    try:
        with open("%s/%s/%s%d.%d.sec" % (config.dataDirectory, config.mapDirectory, instances.get(instanceId, ''), sectorX, sectorY), "rb") as f:
            map = loadSectorMap(f.read(), instanceId, sectorX << sectorShiftX, sectorY << sectorShiftY)
            knownMap.update(map)
        sectors.add(sectorSum)
    except IOError:
        # No? Mark it as empty
        sectors.add(sectorSum)
        return False

    if verbose:
        print("Loading of %d.%d.sec took: %fs" % (sectorX, sectorY, time.time() - t))

    if config.performSectorUnload:
        call_later(config.performSectorUnloadEvery, _unloadMap, sectorX, sectorY, instanceId)

    scriptsystem.get('postLoadSector').run("%d.%d" % (sectorX, sectorY), sector=map, instanceId=instanceId)

    return True

# Map cleaner
def _unloadCheck(sectorX, sectorY, instanceId):
    # Calculate the x->x and y->y ranges
    # We're using a little higher values here to avoid reloading again

    xMin = (sectorX << sectorShiftX) + 14
    xMax = (xMin + mapInfo.sectorSize[0]) + 14
    yMin = (sectorY << sectorShiftY) + 11
    yMax = (yMin + mapInfo.sectorSize[1]) + 11
    try:
        for player in game.player.allPlayers.values():
            pos = player.position # Pre get this one for sake of speed, saves us a total of 4 operations per player

            # Two cases have to match, the player got to be within the field, or be able to see either end (x or y)
            if instanceId == pos.instanceId and (pos[0] < xMax or pos[0] > xMin) and (pos[1] < yMax or pos[1] > yMin):
                return False # He can see us, cancel the unloading
    except:
        return False # Players was changed.

    return True

def _unloadMap(sectorX, sectorY, instanceId):
    print("Checking %d.%d.sec (instanceId %s)" % (sectorX, sectorY, instanceId))
    t = time.time()
    if _unloadCheck(sectorX, sectorY, instanceId):
        print("Unloading....")
        unload(sectorX, sectorY, instanceId)
        print("Unloading took: %fs" % (time.time() - t))
    else:
        call_later(config.performSectorUnloadEvery, _unloadMap, sectorX, sectorY, instanceId)

def unload(sectorX, sectorY, instanceId, knownMap=knownMap):
    """ Unload sectorX.sectorY, loaded into instanceId """
    sectorSum = (instanceId, sectorX, sectorY)
    sectors.remove(sectorSum)

    for z in range(16):
        for x in range(sectorX << sectorShiftX, (sectorX + 1) << sectorShiftX):
            for y in range(sectorY << sectorShiftY, (sectorY + 1) << sectorShiftY):
                 try:
                     del knownMap[instanceId << 40 | x << 24 | y << 8 | z]
                 except:
                     pass
