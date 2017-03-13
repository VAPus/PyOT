#!/usr/bin/python2

import re
import argparse
from xml.dom.minidom import parse

# Helpers
functions = {}
def functionName(type):
    global functions
    if not type in functions:
        functions[type] = 0
        return type
    name = type + str(functions[type])
    functions[type] += 1
    return name
    

parser = argparse.ArgumentParser(description='Process a script')
parser.add_argument('script', metavar='<script>', type=str, help='A script')
USE_UNIQUE_ID = False                   
args = parser.parse_args()
if args.script:
    fileName = args.script
else:
    fileName = raw_input("File: ")
file = open(fileName).read()

dom = parse("actions.xml")
list = []
for element in dom.getElementsByTagName("action"):
        if element.getAttribute("script").split("/")[-1] == fileName or element.getAttribute("value").split("/")[-1] == fileName:
            uniqueid = element.getAttribute("uniqueid")
            if uniqueid:
                list.append(str(uniqueid))
                USE_UNIQUE_ID = True
                continue
            try:
                list.append(int(element.getAttribute("itemid")))
            except:
                for i in range(int(element.getAttribute("fromid")), int(element.getAttribute("toid"))+1):
                    list.append(i)

file = file.replace("math.random(1, #", "math.random(0, #")
lenRe = re.compile(r"#(?P<a>[^) ]*)")
file = lenRe.sub(r"len(\g<a>)-1", file)

# Replace all true with True and false with False
trueRe = re.compile(r" (?i)true")
falseRe = re.compile(r" (?i)false")
file = trueRe.sub(r" True", file)
file = falseRe.sub(r" True", file)

file = file.replace("local ", "").replace(" then", ":").replace(" .. ", " + ").replace("--- ", "# ").replace("-- ", "# ").replace("elseif", "elif").replace("else", "else:").replace("itemEx", "item2").replace("fromPosition", "frompos").replace("toPosition", "topos")
newcode = ""
level = 0
data = []
for line in file.split("\n"):
    if "onUse" in line:
        if line.count("item2") >= 2 or line.count("topos") >= 2:
            NAME = functionName("onUseWith")
            line = line.replace("onUse(cid, item, frompos, item2, topos)", "%s(creature, thing, position, stackpos, onThing, onPosition, onStackpos, **k)" % NAME)
            
            try:
                data.append('@register("useWith", %s)' % tuple(list))
            except:
                data.append('@register("useWith", %s)' % repr(tuple(list)))
        else:
            NAME = functionName("onUse")
            line = line.replace("onUse(cid, item, frompos, item2, topos)", "%s(creature, thing, position, stackpos, **k)" % NAME)
            try:
                data.append('@register("use", %s)' % tuple(list))
            except:
                data.append('@register("use", %s)' % repr(tuple(list)))

    elif "onEquip" in line:
        NAME = functionName("onEquip")
        line = line.replace("onEquip(cid, item, slot)", "%s(creature, thing, slot, **k)" % NAME)
        try:
            data.append('@register("equip", %s)' % tuple(list))
        except:
            data.append('@register("equip", %s' % repr(tuple(list)))
                
    elif "onDeEquip" in line:
        NAME = functionName("unEquip")
        line = line.replace("onDeEquip(cid, item, slot)", "%s(creature, thing, slot, **k)" % NAME)
        try:
            data.append('@register("unEquip", %s)' % tuple(list))
        except:
            data.append('@register("unEquip", %s)' % repr(tuple(list)))
                
    elif "onStepIn" in line:
        NAME = functionName("walkOn")
        line = line.replace("onStepIn(cid, item, position, fromPosition)", "%s(creature, thing, position, fromPosition, **k)" % NAME)
        try:
            data.append('@register("walkOn", %s)' % tuple(list))
        except:
            data.append('@register("walkOn", %s)' % repr(tuple(list)))

    elif "onStepOut" in line:
        NAME = functionName("WalkOff")
        line = line.replace("onStepOut(cid, item, position, fromPosition)", "%s(creature, thing, position, fromPosition, **k)" % NAME)
        try:
            data.append('@register("walkOff", %s)' % tuple(list))
        except:
            data.append('@register("walkOff", %s)' % repr(tuple(list)))

    data.append(line)
file = "\n".join(data)

file = file.replace("math.random", "random.randint").replace("doPlayerSendTextMessage(cid, MESSAGE_INFO_DESCR, ", "creature.message(")
file = file.replace("doDecayItem(item2.uid)", "onThing.decay(onPosition)")
file = file.replace("doDecayItem(item.uid)", "thing.decay(position)").replace("doSendMagicEffect(", "magicEffect(").replace("getThingPos(item2.uid)", "onPosition").replace("getThingPos(item.uid)", "position")
file = file.replace("doSendMagicEffect(getThingPos(item.uid)", "magicEffect(position").replace(".itemid", ".itemId").replace("CONST_ME", "EFFECT").replace("doRemoveItem(item2.uid)", "creature.removeItem(onPosition, onStackpos)")
file = file.replace("doRemoveItem(item.uid)", "creature.removeItem(position, stackpos)").replace("getCreatureName(cid)", "creature.name()").replace("getCreatureName(item2.uid)", "onThing.name()").replace("getCreatureName(item.uid)", "thing.name()").replace(" ~= ", " != ").replace("doSendMagicEffect(frompos, ", "creature.magicEffect(")
file = file.replace("TALKTYPE_ORANGE_1", "'MSG_SPEAK_MONSTER_SAY'").replace("TALKTYPE_MONSTER", "'MSG_SPEAK_MONSTER_SAY'").replace("doPlayerSay(cid, ", "creature.say(").replace("doCreatureSay(cid, ", "creature.say(").replace("doCreatureSay(item2.uid, ", "onThing.say(").replace("doPlayerSendCancel(cid, ", "creature.cancelMessage(").replace("doPlayerSendCancel(cid,", "creature.cancelMessage(").replace("doPlayerAddHealth(cid, ", "creature.modifyHealth(")
file = file.replace("doRemoveItem(item.uid, ", "creature.modifyItem(thing, position, stackpos, -").replace("doRemoveItem(item2.uid, ", "creature.modifyItem(onThing, onPosition, onStackpos, -").replace("doPlayerRemoveItem(item.uid, ", "creature.modifyItem(thing, position, stackpos, -").replace("doPlayerRemoveItem(item2.uid, ", "creature.modifyItem(onThing, onPosition, onStackpos, -")
file = file.replace("hasProperty(item2.uid, CONST_PROP_BLOCKSOLID)", "onThing.solid").replace("hasProperty(item.uid, CONST_PROP_BLOCKSOLID)", "thing.solid")
file = file.replace("isCreature(item2.uid)", "onThing.isCreature()").replace("isPlayer(item2.uid)", "onThing.isPlayer()").replace("isMonster(item2.uid)", "onThing.isMonster()").replace("isItem(item2.uid)", "onThing.isItem()")
file = file.replace("getThingPos(cid)", "creature.position").replace("CONTAINER_POSITION", "0xFFFF")
file = file.replace("item2.uid == cid", "onThing == creature").replace("doPlayerSendDefaultCancel(cid, RETURNVALUE_YOUAREEXHAUSTED)", "creature.exhausted()").replace("== true", "")
file = file.replace("getPlayerLevel(cid)", 'creature.data["level"]').replace("hasCondition(cid, ", "creature.hasCondition(").replace("getPlayerPosition(cid)", "creature.position").replace("getPlayerHealth(cid)", 'creature.data["health"]').replace("getPlayerMaxHealth(cid)", 'creature.data["healthmax"]')
file = file.replace("getPlayerName(cid)", "creature.name()").replace("getCreaturePos(pos)", "creature.position").replace("getPlayerMoney(cid)", "creature.getMoney()")
file = file.replace("doPlayerAddLevel(cid, ", "creature.modifyLevel(").replace("doPlayerRemoveLevel(cid, ", "creature.modifyLevel(-").replace("doPlayerSendCancel(cid, ", "creature.cancelMessage(").replace("ITEM_GOLD_COIN", "2148").replace("ITEM_PLATINUM_COIN", "2152")
file = file.replace("doPlayerSendDefaultCancel(cid, RETURNVALUE_NOTENOUGHLEVEL)", "creature.notEnough('level')").replace("doPlayerSendDefaultCancel(cid, RETURNVALUE_NOTENOUGHMANA)", "creature.notEnough('mana')").replace("doPlayerSendDefaultCancel(cid, RETURNVALUE_NOTENOUGHSOUL)", "creature.notEnough('soul')")
file = file.replace("getPlayerSoul(cid)", 'creature.data["soul"]').replace("getPlayerMana(cid)", 'creature.data["mana"]').replace("isPremium(cid)", "creature.isPremium()").replace("doPlayerSendDefaultCancel(cid, RETURNVALUE_YOUNEEDPREMIUMACCOUNT)", "creature.needPremium()")
file = file.replace("doPlayerAddMana(cid, ", "creature.modifyMana(").replace("doPlayerAddSoul(cid, ", "creature.modifySoul(").replace(" <> ", " != ").replace("doSendMagicEffect(topos, ", "magicEffect(onPosition, ")
file = file.replace("getCreaturePosition(cid)", "creature.position").replace("return False", "return").replace("getPlayerVocation(cid)", "creature.getVocationId()")
file = file.replace("for _,", "for").replace("for i,", "for") # TFS specific, properly fixed down below
file = file.replace("CONST_", "") # TFS constants
file = file.replace('"no",', "False,").replace('"yes",', "True,").replace("getPlayerFreeCap(cid)", "creature.freeCapacity()").replace("getHouseFromPos(", "getHouseId(")
file = file.replace("doPlayerSendDefaultCancel(cid, RETURNVALUE_NOTPOSSIBLE)", "creature.notPossible()").replace("getCreatureSkullType(cid)", "creature.skull")
file = file.replace("isNpc(item.uid)", "thing.isNPC()").replace("isNpc(item2.uid)", "onThing.isNPC()").replace("doPlayerSendTextMessage(cid, MESSAGE_STATUS_CONSOLE_ORANGE, ", "creature.orangeStatusMessage(")
file = file.replace("isSummon(item.uid)", "thing.isSummon()").replace("isSummon(item2.uid)", "onThing.isSummon()").replace("doPlayerSetExperienceRate(cid, ", "creature.setExperienceRate(").replace("getPlayerTown(cid)", 'creature.data["town_id"]')
file = file.replace("0xFFFF", "INVENTORY_POSITION")

# House stuff
file = file.replace("House.getHouseByPos", "getHouseByPos")

# Ugly spelling in script?
file = file.replace(" not(", " not (") # All in all, we hope the stripper does the rest of the job here.

# getPosByDir
file = file.replace("getPosByDir", "positionInDirection")

# LUA_NULL
file = file.replace("LUA_NULL", "None")

lists = re.compile(r"{(?P<params>[^={}]+)}")
file = lists.sub("[\g<params>]", file)

possibleKeys = []

badKeys = attributes = ('solid','blockprojectile','blockpath','usable','pickable','movable','stackable','ontop','hangable','rotatable','animation', 'itemId', 'actions')
# This is my dict builder
def dictBuilder(m):
    text = m.group("params").replace("\t", " ")
    # Resursive:
    text = re.sub(r"{(?P<params>.+)}", dictBuilder, text)
    parts = re.split(r"""(\w+ = \[[^]]*\])|(\w+ = \"[^"]*\")|, """, text)
    toInsert = []
    try:
        for part in parts:
            if part:
                key, value = part.split(" = ")
                try:
                    key = "%d" % int(key) # number
                except:
                    if not key.isupper() and "[" not in key: # Don't do constants or lists
                        if not key in possibleKeys:
                            possibleKeys.append(key)
                        key = '"%s"' % key # string
                        
                toInsert.append("%s: %s" % (key, value))
        return "{%s}" % ', '.join(toInsert)
    except:
        # Buggy, it's a list instead
        for part in parts:
            if part:
                toInsert.append(part)
        return "[%s]" % ", ".join(toInsert)
    
file = re.sub(r"{(?P<params>.+)}", dictBuilder, file, re.M|re.DOTALL)

for key in possibleKeys[:]:
    if key in badKeys:
        possibleKeys.remove(key)

# Clear away "== false" first
inArrayRe = re.compile(r"isInArray\((?P<a>.*), (?P<b>.*)\) == False", re.I)
file = inArrayRe.sub(r"\g<b> not in \g<a>", file)

inArrayRe = re.compile(r"isInArray\((?P<a>.*), (?P<b>.*)\)", re.I)
file = inArrayRe.sub(r"\g<b> in \g<a>", file)

inArrayRe2 = re.compile(r"(?P<a>\w+)\[(?P<b>[a-zA-Z0-9_().]*)\] == nil")
file = inArrayRe2.sub(r"\g<b> not in \g<a>", file)

inArrayRe3 = re.compile(r"(?P<a>\w+)\[(?P<b>[a-zA-Z0-9_().]*)\] != nil")
file = inArrayRe3.sub("\g<b> in \g<a>", file)

inArrayRe4 = re.compile(r"(!(=))(?P<a>\w+)\[(?P<b>[a-zA-Z0-9_().]*)\]")
file = inArrayRe4.sub("\g<a> in \g<b> and \g<b>[\g<a>]", file)



getItemName = re.compile(r"getItemName\((?P<arg>\w+)\)", re.I)
file = getItemName.sub("\g<arg>.rawName()", file)

transformItem = re.compile(r"doTransformItem\((?P<item>\w+)\.uid, (?P<to>[^,()]*)\)")
file = transformItem.sub(r"\g<item>.transform(\g<to>, position)", file)

transformItem = re.compile(r"doTransformItem\((?P<item>\w+)\.uid, (?P<to>[^,()]*), (?P<count>\w+)\)")
file = transformItem.sub(r"\n\g<item>.count = \g<count>\n\g<item>.transform(\g<to>, position)", file)

arrays = re.compile(r"\[(?P<a>\w+)\]([ \t]*)=([ \t]*)")
file = arrays.sub("\g<a>: ", file)

"""
arrays = re.compile(r"\{(?P<a>[0-9, ]+)\},", re.M)
file = arrays.sub(r"(\g<a>),\\", file)

arrays = re.compile(r"\{(?P<a>[0-9, ]+)\}", re.M)
file = arrays.sub(r"(\g<a>)\\", file)
"""

doChangeTypeItem = re.compile(r"doChangeTypeItem\((?P<item>\w+)\.uid, (?P<type>[^)]+)\)")
file = doChangeTypeItem.sub("\g<item>.type = \g<type>", file)

doSetItemSpecialDescription = re.compile(r"doSetItemSpecialDescription\((?P<item>\w+)\.uid, (?P<type>[^)]+)\)")
file = doSetItemSpecialDescription.sub("\g<item>.description = \g<type>", file)

doSetItemActionId = re.compile(r"doSetItemActionId\((?P<item>\w+)\.uid, (?P<type>[^)]+)\)")
file = doSetItemActionId.sub("\g<item>.addAction('\g<type>')", file)

doPlayerAddItem = re.compile(r"doPlayerAddItem\(cid, (?P<item>[^,]+), (?P<count>\w+)\)")
file = doPlayerAddItem.sub("creature.addItem(Item(\g<item>, \g<count>))", file)

doPlayerAddItem = re.compile(r"doPlayerAddItem\(cid, (?P<item>[^,]+)\)")
file = doPlayerAddItem.sub("creature.addItem(Item(\g<item>))", file)

doCreateItem = re.compile(r"doCreateItem\((?P<item>[^,]+), (?P<count>[^,]+), (?P<pos>\w+)\)")
file = doCreateItem.sub("placeItem(Item(\g<item>, \g<count>), \g<pos>)", file)

getContainerSize = re.compile(r"getContainerSize\((?P<item>\w+).uid\)")
file = getContainerSize.sub("\g<item>.container.size()", file)

getContainerCap = re.compile(r"getContainerCap\((?P<item>\w+).uid\)")
file = getContainerCap.sub("\g<item>.containerSize", file)

getPlayerSlotItem = re.compile(r"getPlayerSlotItem\(cid,([ ]*)(?P<slot>\w+)\)")
file = getPlayerSlotItem.sub("creature.inventory[\g<slot>]", file)

doAddContainerItem = re.compile(r"doAddContainerItem\((?P<container>[^,]+).uid, (?P<item>[^,]+)\)")
file = doAddContainerItem.sub("creature.itemToContainer(\g<container>, Item(\g<item>)", file)

doAddContainerItem = re.compile(r"doAddContainerItem\((?P<container>[^,]+).uid, (?P<item>[^,]+), (?P<count>[^,]+)\)")
file = doAddContainerItem.sub("creature.itemToContainer(\g<container>, Item(\g<item>, \g<count>)", file)

ipairs = re.compile(r"ipairs\((?P<param>.*?)\)")
file = ipairs.sub("\g<param>", file)

forLoop = re.compile(r"for([ \t]+)(?P<val>\w+)([ \t]+)=([ \t]+)(\w+),([ \t]+)(?P<in>(.*?))")
file = forLoop.sub("for \g<val> in \g<in>", file)

forOverNumberic = re.compile(r"for (?P<var>\w+) in (?P<what>[^ ()\[\]]+) ")
file = forOverNumberic.sub("for \g<var> in range(\g<what>) ", file)

ifNone = re.compile(r"(?P<item>\w+).uid([ ]+)==([ ]+)")
file = ifNone.sub("not \g<item>", file)

doCreatureAddHealth = re.compile(r"do(Creature|Player)AddHealth\((?P<creature>[^,]+).uid, (?P<param>(.*))\)")
file = doCreatureAddHealth.sub("\g<creature>.modifyHealth(\g<param>)", file)

doCreatureAddMana = re.compile(r"do(Creature|Player)AddMana\((?P<creature>[^,]+).uid, (?P<param>(.*))\)")
file = doCreatureAddMana.sub("\g<creature>.modifyMana(\g<param>)", file)

getItemParent = re.compile(r"getItemParent\((?P<item>[^,]+).uid\)")
file = getItemParent.sub("\g<item>.inContainer", file)

getSpectators = re.compile(r"getSpectators\((?P<position>[^,]+), (?P<x>[^,]+), (?P<y>[^()]+)\)")
file = getSpectators.sub("getPlayers(\g<position>, (\g<x>, \g<y>))", file)

getContainerItem = re.compile(r"getContainerItem\((?P<container>[^,]+).uid, (?P<stackpos>(.*))\)") # Unsafe!
file = getContainerItem.sub("\g<container>.container.getThing(\g<stackpos>)", file)

getItemInfo = re.compile(r"getItemInfo\((?P<itemId>[^,]+)\)\.(?P<attr>\w+)")
file = getItemInfo.sub('itemAttribute(\g<itemId>, "\g<attr>")', file)

getConfigInfo = re.compile(r"""getConfigInfo\(('|")(?P<opt>\w+)('|")\)""")
file = getConfigInfo.sub("config.\g<opt>", file)

getConfigInfo = re.compile(r"""getConfigInfo\((?P<opt>[^() ]+)\)""")
file = getConfigInfo.sub('getattr(config, "\g<opt>")', file)

doAddCondition = re.compile(r"doAddCondition\((?P<creature>[^,]+), (?P<condition>[^,()]+)\)")
file = doAddCondition.sub("""\g<creature>.condition(<Add a PyOT compatible condition replacement for "\g<condition>" here ! >)""", file)

addEvent = re.compile(r"addEvent\((?P<callback>\w+), (?P<time>[^,]+)(?P<param>(.*))\)")
file = addEvent.sub("call_later(\g<time>/1000.0, \g<callback>\g<param>)", file)

doRemoveCreature = re.compile(r"doRemoveCreature\((?P<creature>[^,]+).uid\)")
file = doRemoveCreature.sub("\g<creature>.despawn()", file)

doPlayerAddMount = re.compile(r"doPlayerAddMount\(cid, (?P<id>[^,()]+)\)")
file = doPlayerAddMount.sub("creature.addMount(<Insert name of mount here to replace <'\g<id>'> >)", file)

getPlayerMount = re.compile(r"getPlayerMount\(cid, (?P<id>[^,()]+)\)")
file = getPlayerMount.sub("creature.canMount(<Insert name of mount here to replace <'\g<id>'> >)", file)

getTownTemplePosition = re.compile(r"getTownTemplePosition\((?P<param>(.*))\)")
file = getTownTemplePosition.sub("townPosition(\g<param>)", file)

isStackable = re.compile(r"isStackable\((?P<item>[^,]+).uid\)")
file = isStackable.sub("\g<item>.stackable", file)

isMoveable = re.compile(r"isMoveable\((?P<item>[^,]+).uid\)")
file = isMoveable.sub("\g<item>.moveable", file)

isSolid = re.compile(r"isSolid\((?P<item>[^,]+).uid\)")
file = isMoveable.sub("\g<item>.solid", file)

isHangable = re.compile(r"isHangable\((?P<item>[^,]+).uid\)")
file = isMoveable.sub("\g<item>.hangable", file)

getThingFromPos = re.compile(r"getThingFromPos\((?P<param>(.*))\)")
file = getThingFromPos.sub("getTile(\g<param>).getThing(<INSERT the stackpos you like here!>)", file)

# I don't recall if it's the houseId or the house we're after.
getTileInfo = re.compile(r"getTileInfo\((?P<param>(.*))\).house")
file = getTileInfo.sub("getHouseByPos(\g<param>)", file)

# string.lower
strLower = re.compile(r"string.lower\((?P<item>\w+)\)")
file = strLower.sub("\g<item>.lower()", file)

# Reverse .insert arguments
inserts = re.compile(r"table.insert\((?P<item>\w+), (?P<thing>\w+)\)")
file = inserts.sub("\g<item>.append(\g<thing>)", file)

# Do this last in case you convert some params before
dictKeyTransform = re.compile(r"(?P<name>(\w+))\.(?P<key>(%s))(?P<ending>(\)|\n|,| ))" % '|'.join(possibleKeys))
file = dictKeyTransform.sub("""\g<name>["\g<key>"]\g<ending>""", file)

file = file.replace("item.", "thing.").replace("item2", "onThing").replace("frompos", "position").replace("topos", "onPosition").replace("{\n", "{\\\n")
file = file.replace(" ~= nil", "").replace("nil", "None").replace("cid", "creature").replace(".uid", "")

# Our ugly position system isn't based on classes like lua is.
luaPosition = re.compile(r"\[x=(?P<x>[^,]+),([ \t]*)y=(?P<y>[^,]+),([ \t]*)z=(?P<z>[^,]+),([ \t]*)stackpos=([^]]+)\]")
file = luaPosition.sub("[\g<x>, \g<y>, \g<z>]", file)

# Fix the bugs that will araise.
file = file.replace("[onPosition.x, onPosition.y, onPosition.z]", "onPosition.copy()").replace("[position.x, position.y, position.z]", "position.copy()")

skipNext = 0
for line in file.split("\n"):
    if skipNext:
        skipNext -= 1
        continue
    
    line = line.strip()
    thislevel = level
    if line == "end":
        level -= 1
        continue
    elif line[:9] == "function ":
        newcode += "def %s:\n" % (line[9:])
        level += 1
        continue
    elif line == "if onThing.actionid != 0:" or line == "if thing.actionid != 0:" or line == "if onThing.actionid ~= 0:" or line == "if thing.actionid ~= 0:":
        skipNext = 2
        continue
    elif line[:2] == "if":
        level += 1
    elif line[:4] == "elif":
        thislevel -= 1
    elif line[:5] == "else:":
        thislevel -= 1
    elif line[:3] == "for":
        level += 1
        newcode += "%s%s:\n" % ("    "*thislevel, line[:-3])
        continue
    elif "= getBooleanFromString" in line:
        continue
    elif line[:2] == "--": # Ugly scripts
        line = "# %s" % line[2:]

    newcode += "%s%s\n" % ("    "*thislevel, line)

# Finalize by doing a bit of a cleanup
doSetItemActionId = re.compile(r"(?P<item>\w+)\.actionid == (?P<type>\w+)")
newcode = doSetItemActionId.sub("\g<item>.hasAction('\g<type>')", newcode)

doSetItemActionId = re.compile(r"(?P<item>\w+)\.actionid != (?P<type>\w+)")
newcode = doSetItemActionId.sub("not \g<item>.hasAction('\g<type>')", newcode)

ifs = re.compile(r"(?P<type>(if|elif))([ \t]*)not([ \t]*)\((?P<param>(.*?))\)([ \t]*):", re.M)
newcode = ifs.sub(r"\g<type> not \g<param>:", newcode)

ifs = re.compile(r"(?P<type>(if|elif))([ \t]*)\((?P<param>(.*?))\)([ \t]*):", re.M)
newcode = ifs.sub(r"\g<type> \g<param>:", newcode).replace(" :\n", ":\n").replace("'0' not in ", "not ")

# Crap code remover
crapCode = re.compile("if not ([^.]+).actions:\n([ ]*)([^.]+).actions.append('([^.]+).actionid')", re.M)
newcode = crapCode.sub("", newcode)

# Fix loops to use range.
loopFix = re.compile(r"for i in len\((?P<item>\w+)\)-1")
newcode = loopFix.sub("for i in xrange(len(\g<item>))", newcode)

rangeFix = re.compile(r"for (?P<val>\w+) = (?P<start>[^,]+), (?P<stop>[^:]+)")
newcode = rangeFix.sub("for \g<val> in xrange(\g<start>, \g<stop>+1)", newcode)

print "# Autoconverted script for PyOT"
print "# Untested. Please remove this message when the script is working properly!\n"

if USE_UNIQUE_ID:
    print "# WARNING: Replies on uniqueid!\n\n"

print newcode
raw_input()