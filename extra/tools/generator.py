import copy
import sys
sys.path.append('../')
import struct
import io
import math
import json
### Load all solid and movable items
topitems = set()
movable = set()

parse = json.load(io.open("../../data/items.json", 'r'))
for item in parse:
    flags = str(item.get('flags', ''))
    if not flags: continue

    id = item.get('id')
    
    if type(id) != int and '-' in id:
        start, end = map(int, id.split('-'))
        ids = set(range(start, end+1))
    else:
        ids = set((int(id),))

    if 't' in flags:
        topitems |= ids
    if 'm' in flags:
        movable |= ids
    try:
        flags = int(flags)
    except:
        continue

    if flags & (1 << 13):
        topitems |= ids
    if flags & (1 << 6):
        movable |= ids

    
# Format (Work in Progress):
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
            | -> skip the remaining y tiles
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

### Behavior
def replacer(old, new):
    if new:
        return new
    return old
    
def keeper(old, new):
    if old:
        return old
    return new

def merger(old, new):
    for i in new:
        old.append(i)
    return old
    
# I replace ground, and put old stuff onto new ground
def iReplacer(old, new):
    old[0] = new[0]
    if len(new) > 1:
        for i in new[1:]:
            old.append(i)
    return old

class Map(object):
    def __init__(self, xA, yA, ground=100, zs=16):
        self.levels = zs
        self.size = [xA, yA]
        self._author = ""
        self._description = ""
        self.towns = {}
        self.waypoints = {}
        self.houses = {}
        self.flags = {}
        
        self.area = {}
        """for x in range(0, xA+1):
            self.area[7].append([])
            for y in range(0, yA+1):
                self.area[7][x].append([])
                if ground == None:
                    self.area[7][x][y] = None
                elif isinstance(ground, int):
                    self.area[7][x][y] = [Item(ground)]
                else:
                    self.area[7][x][y] = [ground]"""


    def author(self, name):
        self._author = name
    
    def description(self, desc):
        self._description = desc
        
    def town(self, id, name, pos):
        self.towns[id] = (name, pos)
        
    def waypoint(self, name, pos):
        self.waypoints[name] = pos
        
    def merge(self, obj, offsetX, offsetY, overrideLevel=None):
        xO = offsetX
        yO = offsetY
        if not (7 if not overrideLevel else overrideLevel) in self.area:
            self.area[7 if not overrideLevel else overrideLevel] = []
        for x in obj.area:
            for y in x:
                for z in y:
                    self.area[7 if not overrideLevel else overrideLevel][xO][yO] = y[z]

                yO += 1
            yO = offsetY
            xO += 1

    def _ensureRange(self, x,y,z):
        try:
            self.area[x][y][z]
            return
        except:
            if not x in self.area:
                areaX = {}
                self.area[x] = areaX
            else:
                areaX = self.area[x]

            if not y in areaX:
                areaY = {}
                areaX[y] = areaY
            else:
                areaY = areaX[y]

            if not z in areaY:
                areaY[z] = []
            
            if self.size[0] < x:
                self.size[0] = x
                
            if self.size[1] < y:
                self.size[1] = y
            
    def addTo(self,x,y,thing,level=7):
        self._ensureRange(x,y,level)
        
        if type(thing) != list:
            self.area[x][y][level].append(thing)
        else:
            self.area[x][y][level] = thing
                
    def _levelsTo(self, x, y):
        return list(self.area[x][y].keys())
        """levels = []
        for level in list(self.area.keys()):
            try:
                if self.area[level][x][y]: # Raise a error, then it's skipped
                    levels.append(level)
            except:
                pass

        return levels"""
    def compile(self, areas=(32,32)):
        print("--Begin compilation")
        areaXSize = 0
        areaYSize = 0
        toX = int(math.ceil(self.size[0] / float(areas[0])))
        toY = int(math.ceil(self.size[1] / float(areas[1])))
        nothingness = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        doubleNull = chr(0) + chr(0)
        trippelNull = chr(0) * 3
        HiFormat = struct.Struct("<Hi")
        
        for xA in range(areaXSize, toX):
            for yA in range(areaYSize, toY):
                
                sector = {}
                extras = []
                
                for xS in range(0, areas[0]):
                    xPos = (xA*areas[0])+xS

                    if xPos > self.size[0]:
                        break

                    areaX = self.area[xPos] if xPos in self.area else None
                    if not areaX:
                        continue
                    
                    for yS in range(0, areas[1]):
                        yPos = (yA*areas[1])+yS

                        if yPos > self.size[1]:
                            break

                        areaY = areaX[yPos] if yPos in areaX else None
                        if not areaY:
                            continue

                        for level in areaY:
                            """if len(areaY[level]) > 1:
                                # Reorder
                                insert = 0
                                on = 0
                                for thing in areaY[level][:]:
                                    if isinstance(thing, Item):
                                        if thing.id in topitems and on != insert:
                                            areaY[level].remove(thing)
                                            areaY[level].insert(insert, thing)
                                            insert += 1
                                    on += 1"""
                            sectorY = None
                            for thing in areaY[level]:
                                e,extras = thing.gen(xPos, yPos,level,xS,yS, extras)
                                if e:
                                    if not sectorY:
                                        if not level in sector:
                                            sectorZ = {}
                                            sector[level] = sectorZ
                                        else:
                                            sectorZ = sector[level]
 
                                        if not xS in sectorZ:
                                            sectorX = {}
                                            sectorZ[xS] = sectorX
                                        else:
                                            sectorX = sectorZ[xS]

                                        if not yS in sectorX:
                                            sectorY = []
                                            sectorX[yS] = sectorY
                                        else:
                                            sectorY = sectorX[yS]
                                    sectorY.append(e)

                # Begin by rebuilding ranges of tiles in x,y,z
                       
                # Level 3, y compare:
                def yComp(xCom, z, x):
                    output = []
                    nullRows = 0
                    
                    for row in range(areas[1]):
                        pos = (x+(xA*areas[0]),row+(yA*areas[1]),z)
                        y = xCom[row] if row in xCom else None
                        if y:
                            if nullRows:
                                while nullRows > 0:
                                    # Pack 255 at a time.
                                    pack = min(255, nullRows)
                                    output.append(doubleNull + chr(pack))
                                    nullRows -= pack
                                
                            if pos in self.houses:
                                y.append(HiFormat.pack(50, self.houses[pos]))
                                if not pos in self.flags:
                                    self.flags[pos] = 1
                                elif not self.flags[pos] & 1:
                                    self.flags[pos] += 1
                                    
                            if pos in self.flags:
                                y.append(HiFormat.pack(51, self.flags[pos]))

                            output.append(','.join(y))
                        else:
                            nullRows += 1
                        
                    if nullRows and output:
                        while nullRows > 0:
                            # Only pack 255 at a time.
                            pack = min(255, nullRows)
                            output.append(doubleNull + chr(pack))
                            nullRows -= pack
   
                    if output:
                        # Apply skipping if necessary
                        # A walk in the park to remove the aditional 0 stuff here
                        count = 0
                        for code in output[::-1]:
                            if code[:2] == "\x00\x00": count += 1
                            else: break
      
                        if count:
                            output = output[:len(output)-count]
                            
                            if not output:
                                return "\x00\x00\x00|"
                            
                        data = ';'.join(output) 

                        return data + "|"
                    else:
                        return "\x00\x00\x00|"
                    
                # Level 2, X compare
                def xComp(zCom, z):
                    output = []
                    for row in range(areas[0]):
                        t = yComp(zCom[row] if row in zCom else {}, z, row)
                        if t:
                            output.append(t)

                    if not output:
                        return None
                    else:
                        # A walk in the park to remove the aditional 0 stuff here
                        count = 0
                        for code in output[::-1]:
                            if code[0:2] == "\x00\x00" and code[3] == '|': count += 1
                            else: break
                                
                        if count:
                            output = output[:len(output)-count]
                            
                        # BROKEN?
                        # A second awalk to optimize (\x00\x00\x00|\x00\x00\x00| -> \x00\x00\0x02|)
                        """_output = []
                        count = 0
                        for code in output:
                            if code[0:2] == "\x00\x00" and code[3] == '|': count += 1
                            else:
                                if count > 1:
                                    _output.append("\x00\x00" + chr(count) + '|')
                                elif count == 1:
                                    _output.append("\x00\x00\x00|")
                                count = 0
                                _output.append(code)
                        if count == 1:
                            _output.append("\x00\x00\x00|")
                        elif count > 1:
                            _output.append("\x00\x00" + chr(count) + '|')
                        output = _output"""
                        if not output:
                            return None
                            
                        output[-1] = output[-1][:len(output[-1])-1] + "!" # Change ;/| -> !
                        
                    #if not noRows >= areas[0]:
                    return ''.join(output)

                if not sector:
                    #print("--Skipped %d.%d.sec\n" % (xA, yA))
                    continue
                
                output = []
                for zPos in sector:
                    data = xComp(sector[zPos], zPos)
                    if data:
                        if zPos in nothingness:
                            nothingness.remove(zPos)
                        output.append("%s%s" % (chr(zPos), data))

                if extras:
                    output.append(''.join(extras))
                if output:
                    output = ''.join(output)
                    with io.open('%d.%d.sec' % (xA, yA), 'wb') as f:
                        f.write(output)
                    print("--Wrote %d.%d.sec\n" % (xA, yA))
                    
                else: # A very big load of nothing
                    #print("--Skipped %d.%d.sec\n" % (xA, yA))
                    continue

                    
                        
                
                    
                    
        output = ""
        output += "width = %d\n" % self.size[0]
        output += "height = %d\n" % self.size[1]
        output += "author = '%s'\n" % self._author
        output += 'description = """%s"""\n' % self._description
        output += "sectorSize = (%d, %d)\n" % (areas[0], areas[1])
        output += "towns = %s\n" % str(self.towns)
        output += "waypoints = %s\n" % str(self.waypoints)
        low = 15
        num = 0
        for level in self.area:
            if level in nothingness:
                continue
            if level < low:
                low = level
        num += 1
        print("Northingness on: %s" % (nothingness))
        output += "levels = (%d, %d)" % (num, low)
        with open('info.py', "w") as f:
            f.write(output)
        print("---Wrote info.py")

### Areas
class Area(object):
    __slots__ = ('level', 'area')
    def __init__(self, xA, yA, ground=100, level=7):
        self.level = level
        self.area = []
        for x in range(0, xA+1):
            self.area.append([])
            for y in range(0, yA+1):
                if isinstance(ground, int):
                    self.area[x].append({level: [Item(ground)]})
                else:
                    self.area[x].append({level: [ground]})

    def add(self, x,y,thing):
        self.area[x][y][self.level].append(thing)
        
    def merge(self, obj, offsetX, offsetY):
        for x in obj.area:
            for y in obj.area[x]:
                for z in obj.area[x][y]:
                    self.area[x+offsetX][y+offsetY][self.level] = obj.area[x][y][z] 

    def border(self, offset=0, north=None,south=None,east=None,west=None,northeast=None,northwest=None,southeast=None,southwest=None,behavior=iReplacer):
        # Run East
        if east:
            for sideY in self.area[offset][offset:(offset*-1)-1]:
                sideY[self.level] = behavior(sideY[self.level], east if isinstance(east, tuple) else [east])
        
        # Run West
        if west:
            for sideY in self.area[(offset*-1)-1][offset:(offset*-1)-1]:
                sideY[self.level] = behavior(sideY[self.level], west if isinstance(west, tuple) else [west])
                
        # Run North
        if north:
            for sideX in self.area[offset:(offset*-1)-1]:
                sideX[offset][self.level] = behavior(sideX[offset][self.level], north if isinstance(east, tuple) else [north])
        
        # Run South
        if south:
            for sideX in self.area[offset:(offset*-1)-1]:
                sideX[(offset*-1)-1][self.level] = behavior(sideX[(offset*-1)-1][self.level], south if isinstance(south, tuple) else [south])
                
        # Run northeast
        if northeast:
            self.area[(offset*-1)-1][offset][self.level] = behavior(self.area[(offset*-1)-1][offset][self.level], northeast if isinstance(northeast, tuple) else [northeast])
            
        # Run southeast
        if southeast:
            self.area[(offset*-1)-1][(offset*-1)-1][self.level] = behavior(self.area[(offset*-1)-1][(offset*-1)-1][self.level], southeast if isinstance(southeast, tuple) else [southeast])
            
        # Run northwest
        if northwest:
            self.area[offset][offset][self.level] = behavior(self.area[offset][offset][self.level], northwest if isinstance(northwest, tuple) else [northwest])
            
        # Run southwest
        if southwest:
            self.area[offset][(offset*-1)-1][self.level] = behavior(self.area[offset][(offset*-1)-1][self.level], southewst if isinstance(southwest, tuple) else [southwest])     

class Tile(object):
    __slots__ = ('area', 'pos')
    def __init__(self, x,y, ground=100, level=7):
        self.pos = (x,y,level)
        
        if isinstance(ground, int):
            self.area = [Item(ground)]
        elif ground:
            self.area = [ground]
        else:
            self.area = []
        
    def add(self, thing):
        self.area.append(thing)
        
    def get(self): # Unique for tiles i presume
        return self.area

                
### Things
class Item(object):
    __slots__ = ('id', 'attributes', 'actions')
    attributeIds = ('actions', 'count', 'solid','blockprojectile','blockpath','usable','pickable','movable','stackable','ontop','hangable','rotatable','animation', 'doorId', 'depotId', 'text', 'written', 'writtenBy', 'description', 'teledest')
    def __init__(self, id):
        self.id = id
        self.attributes = {}
        self.actions = []
        
    def attribute(self, key, value):
        attrId = self.attributeIds.index(key)
        
        self.attributes[attrId] = value
    
    def action(self, id):
        self.actions.append(id)

    # Attribute writer function. Needs to be a function so it can call itself in case of a list.
    def writeAttribute(self, name, value):
        # Only toplevel attributes got a name, since we're called from a list too, we need to verify this one.
        if name != None:
            string = chr(name)
        else:
            string = ''
        
        # Is the value a bool?
        if isinstance(value, bool):
            string += "T" if value else "F"

        # A number?
        elif isinstance(value, int):
            string += "i" + struct.pack("<i", value)
            
        # A string?
        elif isinstance(value, str):
            string += "s" + struct.pack("<i", len(value)) + value
            
            
        # Or a list (actions etc)
        elif isinstance(value, list) or isinstance(value, tuple):
            string += "l" + chr(len(value))
            for attr in value:
                string += self.writeAttribute(None, attr)
                
        return string
    
    def gen(self, x,y,z,rx,ry,extras):
        if isinstance(self.id, str):
            return self.id, extras

        code = struct.pack("<H", self.id)

        if self.actions:
            self.attributes[0] = self.actions
        
        if self.id in movable:
            print ("Notice: Movable item (ID: %d) on (%d,%d,%d) have been unmovabilized" % (self.id, x,y,z))
            self.attributes[7] = False
        
        
        if self.attributes:
            eta = []
            for key in self.attributes:
                eta.append(self.writeAttribute(key, self.attributes[key]))
            code += chr(len(eta))
            code += ''.join(eta)
        else:
            code += "\x00"
        self.id = code
        return code, extras


class RSItem(object):
    __slots__ = ('ids')
    def __init__(self, *argc):
        self.ids = argc
    def gen(self, x,y,z,rx,ry,extras):
        import random
        return ('I(%d)' % random.choice(self.ids), extras) 

class Spawn(object):
    __slots__ = ('radius', 'cret', 'center')
    def __init__(self, radius, centerPoint):
        self.radius = radius
        self.cret = []
        self.center = centerPoint
    def monster(self, name,x,y,z, spawntime):
        self.cret.append(chr(61) + chr(len(name)) + name + struct.pack("<bbI", x, y, spawntime))
        
    def npc(self, name,x,y,z, spawntime):
        self.cret.append(chr(62) + chr(len(name)) + name + struct.pack("<bbI", x, y, spawntime))
        
    def gen(self, x,y,z,rx,ry, extras):
        if self.cret:
            #extras.append( "%s.%s" % ("S(%d,%d%s%s)" % (self.center[0], self.center[1], ',%d'%z if z != 7 or self.radius != 5 else '', ",%d"%self.radius if self.radius != 5 else ''), '.'.join(self.cret)) )
            code = struct.pack("<BHHBBB", 60, self.center[0], self.center[1], z, self.radius, len(self.cret)) # opCode + positionX + positionY + positionZ + amount of creatures + radius
            extras.append(code + ''.join(self.cret))
            return (None, extras)
        return (None, extras)
        
       
