#!/usr/bin/env python
# -*- coding: latin-1 -*-

import struct, sys, io

# UTF-8 hack
import codecs
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# The reader class:
class Reader(object):
    def __init__(self, data):
        self.length = len(data)
        self.pos = 0
        self.data = data

    # 8bit - 1byte, C type: char
    def uint8(self):
        self.pos += 1
        return ord(self.data[self.pos-1])
        
    def peekUint8(self):
        try:
            return ord(self.data[self.pos])
        except:
            return None
    def int8(self):
        self.pos += 1
        return struct.unpack("<b", self.data[self.pos-1:self.pos])[0]

    # 16bit - 2bytes, C type: short
    def uint16(self):
        self.pos += 2
        return struct.unpack("<H", self.data[self.pos-2:self.pos])[0]
    def int16(self):
        self.pos += 2
        return struct.unpack("<h", self.data[self.pos-2:self.pos])[0]

    # 32bit - 4bytes, C type: int
    def uint32(self):
        self.pos += 4
        return struct.unpack("<I", self.data[self.pos-4:self.pos])[0]
    def int32(self):
        self.pos += 4
        return struct.unpack("<i", self.data[self.pos-4:self.pos])[0]

    # 64bit - 8bytes, C type: long long
    def uint64(self):
        self.pos += 8
        return struct.unpack("<Q", self.data[self.pos-8:self.pos])[0]
    def int64(self):
        self.pos += 8
        return struct.unpack("<q", self.data[self.pos-8:self.pos])[0]

    # 32bit - 4bytes, C type: float
    def float(self):
        self.pos += 4
        return struct.unpack("<f", self.data[self.pos-4:self.pos])[0]

    # 64bit - 8bytes, C type: double
    def double(self):
        self.pos += 8
        return struct.unpack("<d", self.data[self.pos-8:self.pos])[0]

    def string(self):
        length = self.uint16()
        self.pos += length
        return ''.join(map(str, struct.unpack("%ds" % length, self.data[self.pos-length:self.pos])))

    def getX(self, size):
        self.pos += size
        return ''.join(map(str, struct.unpack_from("B"*size, self.data, self.pos - size)))

    def getXString(self, size):
        self.pos += size
        return ''.join(map(str, struct.unpack("%ds" % size, self.data[self.pos-size:self.pos])))
        
    def getData(self):
        return self.data[self.pos:]
    
class Item(object):
    def __init__(self):
        self.type = 0
        self.flags = {}
        self.attr = {}
        self.cid = 0
        self.sid = 0
        self.alsoKnownAs = []
        self.junk = False

class Node(object):
    def __init__(self, otb):
        global LEVEL
        self.data = b""
        self.nodes = []
        byte = otb.uint8()
        nextIsEscaped = False
        while byte != None:
            if byte == 0xFE and not nextIsEscaped:
                node = self.handleBlock(otb)

            elif byte == 0xFF and not nextIsEscaped:
                LEVEL -= 1
                if LEVEL < 0:
                    print "DEBUG!"
                break
                
            elif byte == 0xFD and not nextIsEscaped:
                nextIsEscaped = True
                
            else:
                nextIsEscaped = False 
                self.data += struct.pack("<B", byte)
                
            byte = otb.uint8()
        self.data = Reader(self.data)
    def handleBlock(self, otb):
        global LEVEL
        LEVEL += 1
        node = Node(otb)
        self.nodes.append(node)
        return node
        
    def next(self):
        if self.nodes:
            return self.nodes.pop(0)
        else:
            return None
            
otbFile = io.open("items.otb", 'rb')
otb = Reader(otbFile.read())

otb.pos += 5
LEVEL = 1
node = Node(otb) # We use 1 here since we skip the "root"

node.data.uint8() # 0x00
node.data.uint32() # 0x00
node.data.uint8() # 0x01
node.data.uint16() # Really unimportant
majorVersion = node.data.uint32()
minorVersion = node.data.uint32()
buildVersion = node.data.uint32()
stringVersion = node.data.getXString(128)

print "-- "
print "-- OTB version %d.%d (Client: %s, build: %d)" % (majorVersion, minorVersion, stringVersion[12:16], buildVersion)

items = {}
lastRealItem = None

child = node.next()
while child:
    item = Item()
    item.type = child.data.uint8()
    flags = child.data.uint32()
    
    if (flags & 1) == 1:
        item.flags["solid"] = 1
    if (flags & 2) == 2:
        item.flags["blockprojectile"] = 1
    if (flags & 4) == 4:
        item.flags["blockpath"] = 1
    if (flags & 8) == 8:
        item.flags["hasheight"] = 1
    if (flags & 16) == 16:
        item.flags["usable"] = 1
    if (flags & 32) == 32:
        item.flags["pickable"] = 1
    if (flags & 64) == 64:
        item.flags["movable"] = 1
    if (flags & 128) == 128:
        item.flags["stackable"] = 1
    if (flags & 8192) == 8192:
        item.flags["ontop"] = 1
    if (flags & 131072) == 131072:
        item.flags["vertical"] = 1
    if (flags & 262144) == 262144:
        item.flags["horizontal"] = 1
    if (flags & 65536) == 65536:
        item.flags["hangable"] = 1
    if (flags & 1048576) == 1048576:
        item.flags["distanceread"] = 1
    if (flags & 32768) == 32768:
        item.flags["rotatable"] = 1
    if (flags & 16384) == 16384:
        item.flags["readable"] = 1
    if (flags & 8388608) == 8388608:
        item.flags["lookthrough"] = 1
    if (flags & 16777216) == 16777216:
        item.flags["animation"] = 1
    if (flags & 33554432) == 33554432:
        item.flags["walkstack"] = 1
    """if (flags & 4194304) == 4194304:
        item.flags["charges"] = 1"""
    
    sub = child.next()
    while child.data.peekUint8():
        attr = child.data.uint8()
        datalen = child.data.uint16()
        if attr is 0x10:
            item.sid = child.data.uint16()
                    
        elif attr is 0x11:
            item.cid = child.data.uint16()
        elif attr == 0x12:
            item.attr["name"] = child.data.getXString(datalen)

        elif attr is 0x14:
            item.flags["speed"] = child.data.uint16()
            
        elif attr is 0x2B:
            item.flags["order"] = child.data.uint8()

        elif attr == 0x2C:
            item.flags["wareid"] = child.data.uint16()            
        else:
            child.data.pos += datalen        

    if item.cid:
        items[item.sid] = item
        lastRealItem = item
    else:
        lastRealItem.alsoKnownAs.append(item.sid)
    
    child = node.next()
print "-- Got a total of %d items!" % len(items)
print "-- "
print ""

import json, xml.dom.minidom as dom

data = {}
dom = dom.parse("items.xml")
for xItem in dom.getElementsByTagName("item"):
     xId = xItem.getAttribute("id")
     xFromId = xItem.getAttribute("fromid")
     xToId = xItem.getAttribute("toid")
     xName = xItem.getAttribute("name")
     xArticle = xItem.getAttribute("article")
     xPlural = xItem.getAttribute("plural")
     xAttributes = xItem.getElementsByTagName("attribute")

     prep = {"name":xName, "plural":xPlural, "article":xArticle}
     for attr in xAttributes:
         key = attr.getAttribute("key")
         
         if key == "defense":
             key = "defence"
             
         try:
            prep[key] = int(attr.getAttribute("value"))
         except:
            prep[key] = attr.getAttribute("value").replace("'", "\\'")
     if xId:
         data[int(xId)] = prep

     elif xFromId and xToId:
         for x in range(int(xFromId), int(xToId)+1):
             data[int(x)] = {"name": xName, "plural":xPlural, "article":xArticle}
             for attr in xAttributes:
                 key = attr.getAttribute("key")
                 
                 if key == "defense":
                     key = "defence"
                 try:
                    data[int(x)][key] = int(attr.getAttribute("value"))
                 except:
                    data[int(x)][key] = attr.getAttribute("value").replace("'", "\\'")
             
             
#print data
# Current suggested format:
# sid, cid, name, refids, flags, description, weight, worth, slot, duration, decayTo, floorchange
#id = raw_input("ID? ")

import copy

if __name__ == "__main__":

    print "CREATE TABLE `items` ( \n\
`id` SMALLINT UNSIGNED NOT NULL,\n\
`type` TINYINT UNSIGNED NOT NULL, \n\
`name` VARCHAR( 32 ) NOT NULL,\n\
`article` CHAR( 3 ) NOT NULL DEFAULT '',\n\
`plural` VARCHAR( 32 ) NOT NULL DEFAULT '',\n\
`speed` SMALLINT UNSIGNED NOT NULL, \n\
`order` TINYINT UNSIGNED NOT NULL, \n\
`wareid` SMALLINT UNSIGNED NOT NULL,\n\
`solid` BOOL NOT NULL DEFAULT 0,\n\
`blockprojectile` BOOL NOT NULL DEFAULT 0,\n\
`blockpath` BOOL NOT NULL DEFAULT 0,\n\
`hasheight` BOOL NOT NULL DEFAULT 0,\n\
`usable` BOOL NOT NULL DEFAULT 0,\n\
`pickable` BOOL NOT NULL DEFAULT 0,\n\
`movable` BOOL NOT NULL DEFAULT 0,\n\
`stackable` BOOL NOT NULL DEFAULT 0,\n\
`ontop` BOOL NOT NULL DEFAULT 0,\n\
`vertical` BOOL NOT NULL DEFAULT 0,\n\
`horizontal` BOOL NOT NULL DEFAULT 0,\n\
`hangable` BOOL NOT NULL DEFAULT 0,\n\
`distanceread` BOOL NOT NULL DEFAULT 0,\n\
`rotatable` BOOL NOT NULL DEFAULT 0,\n\
`readable` BOOL NOT NULL DEFAULT 0,\n\
`charges` BOOL NOT NULL DEFAULT 0,\n\
`animation` BOOL NOT NULL DEFAULT 0,\n\
`lookthrough` BOOL NOT NULL DEFAULT 0,\n\
`walkstack` BOOL NOT NULL DEFAULT 0,\n\
`custom` BOOL NOT NULL DEFAULT 0,\n\
PRIMARY KEY ( `id` )\n\
) ENGINE = MYISAM; \n\
CREATE TABLE `item_attributes` ( \n\
`id` SMALLINT UNSIGNED NOT NULL ,\n\
`key` VARCHAR( 32 ) NOT NULL ,\n\
`value` VARCHAR( 255 ) NOT NULL ,\n\
`custom` BOOL NOT NULL DEFAULT '0'\n\
) ENGINE = MYISAM ;"
    taken = set()
    for item in items.values():
        if item.sid in data and not item.cid in taken:
            if "solid" in item.flags and "speed" in item.flags:
                del item.flags["speed"]
            if "name" in item.attr:
                data[item.sid]["name"] = item.attr["name"]
        
            # Hack
            data[item.sid]["name"] = data[item.sid]["name"].decode("utf-8")
            print (u"INSERT INTO items (`id`, `type`, `name`%s%s%s) VALUES(%d, %d, '%s'%s%s%s);" % (', `article`' if data[item.sid]["article"] else '', ', `plural`' if data[item.sid]["plural"] else '', ', `'+"`, `".join(item.flags.keys())+'`' if item.flags else '', item.cid, item.type,data[item.sid]["name"].replace("'", "\\'"), ", '"+data[item.sid]["article"]+"'" if data[item.sid]["article"] else '', ", '"+data[item.sid]["plural"].replace("'", "\\'")+"'" if data[item.sid]["plural"] else '', ", '"+"', '".join(map(str, item.flags.values()))+"'" if item.flags else ''))

            del data[item.sid]["name"]
            del data[item.sid]["plural"]
            del data[item.sid]["article"]
            taken.add(item.cid)

            if data[item.sid]:
                output = u"INSERT INTO item_attributes (`id`, `key`, `value`) VALUES"
                for key in data[item.sid]:
                    output += "(%d, '%s', '%s'),\n" % (item.cid, key, data[item.sid][key])
                print (output[:-2]+";\n").encode('utf-8')

    #else:
    #    print("---WARNING, item with sid=%d not no data!" % item.sid)
    
