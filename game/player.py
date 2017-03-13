
from game.map import placeCreature, removeCreature, getTile
import config
from collections import deque
import game.scriptsystem
from game.item import Item
from game.creature import Creature, uniqueId, allCreatures
import time
import game.party
import game.resource
import game.chat
import game.protocol
from . import sql
import game.vocation
import random
import math
from . import otjson
import datetime
import game.language
import copy
from tornado import gen

# Build class.
from game.creature_talking import PlayerTalking
from game.creature_attacks import PlayerAttacks

try:
    import pickle as pickle
except:
    import pickle

allPlayers = {}
allPlayersObject = allPlayers.values() # Quick speedup

if config.enableExtensionProtocol:
    from .service.extserver import IPS as MEDIA_IPS

class Player(PlayerTalking, PlayerAttacks, Creature): # Creature last.
    def __init__(self, client, data):
        # XXX: Hack.
        # TODO: Rewrite this to save memory. And to simplefy lookups later on.
        data["skills"] = {SKILL_FIST: data['fist'], SKILL_SWORD: data['sword'], SKILL_CLUB: data['club'], SKILL_AXE: data['axe'], SKILL_DISTANCE: data['distance'], SKILL_SHIELD: data['shield'], SKILL_FISH: data['fishing']}
        data["skill_tries"] =  {SKILL_FIST: data['fist_tries'], SKILL_SWORD: data['sword_tries'], SKILL_CLUB: data['club_tries'], SKILL_AXE: data['axe_tries'], SKILL_DISTANCE: data['distance_tries'], SKILL_SHIELD: data['shield_tries'], SKILL_FISH: data['fishing_tries']}

        # Explicit. Decimal to int (XXX: Restructure database?)
        data["experience"] = int(data["experience"])
        data["balance"] = int(data["balance"])
        data["manaspent"] = int(data["manaspent"])
        data["balance"] = int(data["balance"])
        data["health"] = int(data["health"])
        data["mana"] = int(data["mana"])

        if not data['instanceId']:
            data['instanceId'] = 0
        Creature.__init__(self, data, Position(int(data['posx']),
                                               int(data['posy']),
                                               int(data['posz']),
                                               data['instanceId']
                         ))
        self.client = client
        self.modes = [0,0,0]
        self.gender = 0
        self.knownCreatures = set()
        self.openContainers = {}
        self.lastOpenContainerId = 0
        self.doingSoulGain = False

        # OT milisec to pyot seconds
        self.data["stamina"] = self.data["stamina"] / 1000

        self.lastDmgPlayer = 0

        self.targetChecker = None
        self._openChannels = {}
        self.idMap = []
        self.openTrade = None
        self.isTradingWith = None
        self.tradeItems = []
        self.startedTrade = False
        self.tradeAccepted = False
        self.removeMe = False

        self.windowTextId = 0
        self.windowHandlers = {}
        self.partyObj = None
        self.solid = not config.playerWalkthrough

        self.blessings = 0
        self.deathPenalityFactor = 1

        self.lastStairHop = 0

        self.lastUsedObject = 0

        self.market = None
        self.depotMarketCache = {}
        self.marketDepotId = 0
        self.lastClientMove = None
        """# Light stuff
        self.lightLevel = 0x7F
        self.lightColor = 27"""

        # Cache a protocol packet instance
        try:
            self._packet = self.client.protocol.Packet()
        except:
            self._packet = game.protocol.getProtocol(game.protocol.protocolsAvailable[-1]).Packet()

        assert self.client is not None
        self._packet.stream = self.client

        # Extra icons
        self.extraIcons = 0

        # Send premium code
        self.sendPremium = config.sendPremium

        # Rates
        # 0 => Experience rate, 1 => Stamina loose rate, 2 => drop rate,
        # 3 => drop rate (max items), 4 => regain rate
        self.rates = [config.experienceRate, 60, config.lootDropRate,
                      config.lootMaxRate, 1]
        self.inventoryWeight = 0

        # Direction
        self.direction = SOUTH
        #del self.data["direction"]

        # Inventory
        self.inventoryCache = {}
        if self.data['inventory']:
            self.unpickleInventory(self.data['inventory'])

            # Call on equip
            for x in range(0, len(self.inventory)):
                item = self.inventory[x]
                if item:
                    game.scriptsystem.get("equip").run(creature=self, thing=item,
                                                           slot = x+1)

        else:
            purse = Item(1987)
            purse.name = "Purse"
            purse.addAction('purse')
            self.inventory = [None, None, None, None, None, None, None, None, None, None, purse] # Last item XXX is purse.

        #del self.data['inventory']

        # Depot, (yes, we load it here)
        if self.data['depot']:
            self.depot = pickle.loads(self.data['depot'])
        else:
            self.depot = {} # {depotId : inventoryList}

        #del self.data['depot']

        # Calculate level from experience
        vocation = self.getVocation()
        level = int(config.levelFromExpFormula(self.data["experience"]))

        # Calculate magic level from manaspent
        self.data["maglevel"] = int(config.magicLevelFromManaFormula(self.data["manaspent"],
                                                                     vocation.mlevel))

        self.setLevel(level, False)
        self.defaultSpeed()

        # Skills = active skills!
        self.skills = self.data["skills"].copy()

        # Skill goals
        self.skillGoals = {}
        for x in self.skills:
            if not self.skills[x]: # New player usually.
                self.skills[x] = config.defaultSkillLevel
                self.data["skills"][x] = config.defaultSkillLevel
                if self.data["skill_tries"][x] == None:
                    self.data["skill_tries"][x] = 0


            self.skillGoals[x] = config.skillFormula(self.skills[x],
                                                     self.getVocation().meleeSkill)

        if self.data["storage"]:
            self.storage = otjson.loads(self.data["storage"].decode('utf-8'))

        else:
            self.storage = {}

        #del self.data["storage"]

        if self.data["conditions"]:
            try:
                self.conditions = pickle.loads(self.data["conditions"])
                for x in self.conditions.copy():
                    self.conditions[x].start(self)
            except ImportError:
                pass # pypy and cpython pickle might be cross compatible.
                
        # Storage states
        self.saveStorage = False
        self.saveInventory = False
        self.saveDepot = False
        self.saveSkills = False
        self.saveData = False
        self.saveCondition = False
        self.doSave = True

        if self.data["language"] != "en_EN":
            self.setLanguage(self.data["language"])

    def generateClientID(self):
        return 0x10000000 + uniqueId()

    def isPlayer(self):
        return True

    def isPushable(self, by):
        return config.playerIsPushable

    def actionIds(self):
        """ Creature and player action identifier for players, static """
        return ('creature', 'player') # Static actionID

    def __repr__(self):
        return "<Player (%s, %d, %s) at %s>" % (self.data["name"], self.clientId(), self.position, hex(id(self)))

    def sexPrefix(self):
        # TODO: Can be dropped now that we are going for context stuff
        if self.data["sex"] == 1:
            return _("He")
        else:
            return _("She")

    def sexAdjective(self):
        # TODO: Can be dropped now that we are going for context stuff
        if self.data["sex"] == 1:
            return _("his")
        else:
            return _("heres")

    def description(self, isSelf=False):
        if isSelf:
            output = _l(self, "You see yourself. You are %s.") % _lc(self, 'look_at', self.getVocation().description())
        else:
            ### TODO: We can drop sex prefixes now that we need to hardcode them anyway!
            if self.data["sex"] == 1:
                output = _lc(self, 'look_at_male', "You see %(name)s (Level %(level)d). %(prefix)s is %(description)s.") % {"name": self.name(),
                                                "level": self.data["level"],
                                                "prefix": _l(self, self.sexPrefix()),
                                                "description": _l(self, self.getVocation().description())}
            else:
                output = _lc(self, 'look_at_female', "You see %(name)s (Level %(level)d). %(prefix)s is %(description)s.") % {"name": self.name(),
                                                "level": self.data["level"],
                                                "prefix": _l(self, self.sexPrefix()),
                                                "description": _l(self, self.getVocation().description())}
        return output

    def packet(self, type=None):
        self._packet.clear()
        if type:
            self._packet.uint8(type)
        return self._packet

    def getIP(self):
        if self.client:
            return self.client.address

    def refreshViewWindow(self, stream=None):
        if stream:
            stream.uint8(0x64)
            stream.position(self.position)
            stream.mapDescription(Position(self.position.x - 8,
                                           self.position.y - 6, self.position.z),
                                  18, 14, self)
        else:
            with self.packet(0x64) as stream: # Map description
                stream.position(self.position)
                stream.mapDescription(Position(self.position.x - 8,
                                            self.position.y - 6, self.position.z),
                                    18, 14, self)

    def defaultSpeed(self):
        # Low:
        lowLevel = max(self.data['level'], config.playerSpeedLowCut)
        speed = config.playerBaseSpeed + (config.playerSpeedLowIncrease * lowLevel)

        # High
        highLevel = self.data['level'] - lowLevel
        speed += config.playerSpeedHighIncrease * highLevel

        self.speed = min(speed, 1500.0)

    def sendFirstPacket(self):
        if not self.data["health"]:
            self.onSpawn()

        # If we relogin we might be in remove mode,
        # make sure we're not tagget for it!
        self.removeMe = False
        self.client.ready = True
        self.alive = True

        # We might login using a different client version. Fix it.
        try:
            self._packet = self.client.protocol.Packet()
        except:
            self._packet = game.protocol.getProtocol(game.protocol.protocolsAvailable[-1]).Packet()

        self._packet.stream = self.client

        if self.client.version >= 980:

            with self.packet(0x0A) as stream:
                stream.uint8(0x17)
                stream.uint32(self.clientId()) # Cid
                stream.uint16(0x32) # Drawing delay.

                # New speed formula thingy.
                stream.double(857.36)
                stream.double(261.29)
                stream.double(-4795.01)

                stream.uint8(1) # Rule violations?

        with self.packet() as stream:
            if self.client.version < 980:
                stream.uint8(0x0A)
                stream.uint32(self.clientId()) # Cid
                stream.uint16(0x32) # Drawing delay.
                stream.uint8(1) # Rule violations?
                #stream.violation(0)
            else:
                stream.uint8(0x0F) # Ping back

            stream.uint8(0x64) # Map description
            stream.position(self.position)
            stream.mapDescription(Position(self.position.x - 8, self.position.y - 6,
                                        self.position.z),
                                18, 14, self)

            self.refreshInventory(stream)
            self.refreshStatus(stream)
            self.refreshSkills(stream)

            stream.playerInfo(self)
            stream.worldlight(getLightLevel(), LIGHTCOLOR_DEFAULT)
            stream.creaturelight(self.cid, self.lightLevel, self.lightColor)

            if self.position.getTile().getFlags() & TILEFLAGS_PROTECTIONZONE:
                self.setIcon(CONDITION_PROTECTIONZONE)
            self.refreshConditions(stream)

            stream.magicEffect(self.position, 0x03)

        #self.sendVipList()

        # Stamina loose
        if self.data["stamina"]:
            def loseStamina():
                if self.client:
                    self.data["stamina"] -= 60
                    if self.data["stamina"] < 0:
                        self.data["stamina"] = 0
                    else:
                        call_later(self.rates[1], loseStamina)

                    if self.data["stamina"] < (42*3600):
                        self.refreshStatus()

            call_later(self.rates[1], loseStamina)

    def refreshInventory(self, streamX = None):
        if self.client:
            if not streamX:
                stream = self.packet()
            else:
                stream = streamX

            for slot in range(SLOT_CLIENT_FIRST,SLOT_CLIENT_FIRST+SLOT_CLIENT_SLOTS):
                if self.inventory[slot-1]:
                    stream.uint8(0x78)
                    stream.uint8(slot)

                    stream.item(self.inventory[slot-1])
                else:
                    stream.uint8(0x79)
                    stream.uint8(slot)

            if not streamX:
                stream.send(self.client)
    def refreshStatus(self, stream=None):
        if self.client:
            if stream:
                stream.status(self)
            else:
                with self.packet() as stream:
                    stream.status(self)

    def refreshConditions(self, stream=None):
        if self.client:
            send = self.extraIcons
            for conId in self.conditions:
                try:
                    if self.conditions[conId].length > 0:
                        conId = int(conId)
                        send += conId
                except:
                    pass

            if stream:
                stream.icons(send)
            else:
                with self.packet() as stream:
                    stream.icons(send)

    def refreshShield(self):
        for player in getPlayers(self.position):
            with player.packet() as stream:
                stream.shield(self.cid, self.getShield(player))

    def setIcon(self, icon):
        if not self.hasIcon(icon):
            self.extraIcons += icon

    def removeIcon(self, icon):
        if self.hasIcon(icon):
            self.extraIcons -= icon

    def hasIcon(self, icon):
        return self.extraIcons & icon

    def refreshSkills(self, stream=None):
        if self.client:
            if stream:
                stream.skills(self)

            else:
                with self.packet() as stream:
                    stream.skills(self)

    def refreshSkull(self, stream=None):
        for player in getPlayers(self.position):
            stream = player.packet(0x90)
            stream.uint32(self.cid)
            stream.uint8(self.getSkull(player))
            stream.send(player.client)

    def pong(self):
        self.packet(0x1E).send(self.client)

    def getVocation(self):
        return game.vocation.getVocationById(self.data["vocation"])

    def getVocationId(self):
        return self.data["vocation"]

    def freeCapacity(self):
        return max(self.data["capacity"] - self.inventoryWeight, 0)

    def findItem(self, position, sid=None):
        # Option 1, from the map:
        if position:
            if position.x != 0xFFFF:
                if hasattr(position, "stackpos"):
                    thing = position.getThing()
                    if sid and thing and thing.itemId != sid:
                        raise Exception("Got request for a item at %s, but spritId mismatches (should be: %d, is: %s)" % (position, sid, thing.itemId))
                    return thing
                else:
                    raise AttributeError("Position is not a subclass of StackPosition, but points to a map position.")

            # Option 2, the inventory
            elif position.y < 64:
                return self.inventory[position.y-1]

            # Option 3, the bags, if there is one ofcource
            else:
                try:
                    bag = self.openContainers[position.y - 64]
                except:
                    return

                item = bag.getThing(position.z)
                return item or bag

        # Option 4, find any item the player might posess
        if sid:
            # Inventory
            try:
                return self.inventoryCache[sid][-1]
            except:
                return None

    def findItemWithPlacement(self, position, sid=None):
        # Option 1, from the map:
        if position:
            if position.x != 0xFFFF:
                if hasattr(position, "stackpos"):
                    thing = position.getThing()
                    if isinstance(thing, game.item.Item):
                        return (0, thing, position.getTile())
                    else:
                        return None
                else:
                    raise AttributeError("Position is not a subclass of StackPosition, but points to a map position.")

            # Option 2, the inventory
            elif position.y < 64:
                return (1, self.inventory[position.y-1]) if self.inventory[position.y-1] else None

            # Option 3, the bags, if there is one ofcource
            else:
                try:
                    bag = self.openContainers[position.y - 64]
                except:
                    return
                item = bag.getThing(position.z)
                return (2, item, bag)

        # Option 4, find any item the player might posess
        if sid:
            # Inventory
            try:
                itemFound = self.inventoryCache[sid][-1]
                if item.container:
                    return (3, itemFound, itemFound)
            except:
                return None

    def findItemById(self, itemId, count=0, remove=True, clientId = False):
        items = []
        foundCount = 0
        stream = self.packet()
        # From inventory?
        for item in self.inventory:
            if item and ((not clientId and item.itemId == itemId) or (clientId and item.cid == itemId)):
                items.append((1, item, self.inventory.index(item)))
                if count:
                    foundCount += item.count

                    if foundCount >= count: break
                else:
                    break


        if (not len(items) or foundCount < count) and self.inventory[SLOT_BACKPACK]:
            bags = [self.inventory[SLOT_BACKPACK]]
            for bag in bags:
                index = 0
                for item in bag.container:
                    if ((not clientId and item.itemId == itemId) or (clientId and item.cid == itemId)):
                        items.append((2, item, bag, index))
                        if count:
                            foundCount += item.count

                            if foundCount >= count: break
                        else:
                            break
                    elif item.containerSize:
                        bags.append(item)
                    index += 1

        if (count and foundCount < count) or not items:
            return None

        elif not remove:
            return items[0][1]

        elif not count:
            if items[0][0] == 1:
                self.inventory[items[0][3]] = None
                stream.removeInventoryItem(items[0][2]+1)

            elif items[0][0] == 2:
                items[0][2].removeItem(items[0][1])
                if items[0][2].openIndex != None:
                    stream.removeContainerItem(items[0][2].openIndex, items[0][3])

            # Update cached data
            if self.removeCache(items[0][1]):
                self.refreshStatus(stream)

            stream.send(self.client)
            return items[0][1]
        else:
            newItem = Item(itemId, count)
            sendUpdate = False
            for item in items:
                if not count:
                    break
                precount = item[1].count
                item[1].reduceCount(min(item[1].count, count))
                count = precount - item[1].count
                if item[1].count:
                    if item[0] == 1:
                        stream.addInventoryItem(item[2]+1, item[1])
                    elif item[0] == 2 and item[2].openIndex != None:
                        stream.updateContainerItem(item[2].openIndex, item[3], item[1])

                    # Update cached data
                    if self.modifyCache(item[1], -count if count > 0 else -1) and not sendUpdate:
                        sendUpdate = True

                else:
                    if item[0] == 1:
                        self.inventory[item[2]+1-1] = None
                        stream.removeInventoryItem(item[2]+1)
                    elif item[0] == 2 and item[2].openIndex != None:
                        item[2].removeItem(item[1])
                        stream.removeContainerItem(item[2].openIndex, item[3])

                    # Update cached data
                    if self.modifyCache(item[1], -count if count > 0 else -1) and not sendUpdate:
                        sendUpdate = True

            if sendUpdate:
                self.refreshStatus(stream)
            stream.send(self.client)
            return newItem

    def removeItem(self, thing):
        return thing.remove()

    def getContainer(self, openId):
        try:
            return self.openContainers[openId]
        except:
            return

    def removeCache(self, item):
        print("removeCache")
        # Update cached data
        try:
            try:
                del item.inContainer
            except:
                pass
            try:
                del item.creature
            except:
                pass

            print("Modifying weight, removecache")
            self.inventoryCache[item.itemId].remove(item)
            self.inventoryCache[item.itemId][0] -= item.count or 1
            weight = item.weight

            # Save
            self.saveInventory = True

            if weight:
                self.inventoryWeight -= weight * (item.count or 1)
                return True
        except:
            pass

    def addCache(self, item, container=None):
        weight = item.weight
        if weight:
            self.inventoryWeight += weight * (item.count or 1)
            if self.inventoryWeight < 0:
                self.inventoryWeight -= weight * (item.count or 1)
                return False
        try:
            self.inventoryCache[item.itemId].append(item)
            self.inventoryCache[item.itemId][0] += item.count or 1
        except:
            self.inventoryCache[item.itemId] = [item.count or 1, item]

        if container:
            item.inContainer = container
        item.creature = self

        # Save
        self.saveInventory = True

        if weight:
            return True

    def modifyCache(self, item, count):
        if not count: return

        try:
            self.inventoryCache[item.itemId][0] += count
            weight = item.weight

            # Save
            self.saveInventory = True

            if weight:
                self.inventoryWeight += weight * (count)
                return True

        except:
            pass

    def itemCount(self, item):
        try:
            return self.inventoryCache[item.itemId][0]
        except:
            return 0

    # Experience & level
    def setLevel(self, level, send=True):
        vocation = self.getVocation()
        try:
            oldLevel = self.data["level"]
        except:
            oldLevel = 0
        if oldLevel != level:
            res = game.scriptsystem.get("level").run(creature=self, fromLevel=oldLevel, toLevel=level)
            if res == False:
                return False
            self.saveData = True
            self.data["level"] = level

            self.data["healthmax"] = vocation.maxHP(level)
            self.data["manamax"] = vocation.maxMana(level)
            self.data["capacity"] = vocation.maxCapacity(level) * 100

            if self.data["manamax"] < config.minMana:
                self.data["manamax"] = config.minMana
                print("[WARNING] Player %s (ID:%d) is likely promoted to a higher vocation then his level allows, manamax < config.minMana!" % (self.name(), self.data["id"]))

            if self.data["healthmax"] < config.minHealth:
                self.data["healthmax"] = config.minHealth

            if self.data["health"] > self.data["healthmax"]:
                self.data["health"] = self.data["healthmax"]

            if self.data["mana"] > self.data["manamax"]:
                self.data["mana"] = self.data["manamax"]

            if send:
                if level > oldLevel:
                    self.message("You advanced from level %d to Level %d." % (oldLevel, level), MSG_EVENT_ADVANCE)
                elif level < oldLevel:
                    self.message("You were downgraded from level %d to Level %d." % (oldLevel, level), MSG_EVENT_ADVANCE)
                self.refreshStatus()

    def modifyLevel(self, mod):
        self.setLevel(self.data["level"] + mod)

    def modifyMagicLevel(self, mod):
        if not mod:
            return


        res = game.scriptsystem.get("skill").run(creature=self, skill=MAGIC_LEVEL, fromLevel=self.data["maglevel"], toLevel=self.data["maglevel"] + mod)

        if res != False:
            self.data["maglevel"] += mod
            if self.data["maglevel"] < 0:
                self.data["maglevel"] = 0
            self.refreshStatus()
    def modifyExperience(self, exp):
        exp = int(exp)

        up = True
        if exp < 0:
            up = False

        self.data["experience"] += exp

        self.saveData = True

        if up:
            level = 0
            self.message(_lp(self, "You gained %d experience point.", "You gained %d experience points.", exp) % exp, MSG_EXPERIENCE, color=config.experienceMessageColor, value=exp, pos=self.position)
            while True:
                if config.totalExpFormula(self.data["level"]+level) > self.data["experience"]:
                    break
                level += 1
            if level:
                self.setLevel(self.data["level"]+level)
        else:
            level = 0
            self.message(_lp(self, "You lost %d experience point.", "You lost %d experience points.", exp) % exp, MSG_EXPERIENCE, color=config.experienceMessageColor, value=-exp)
            while True:
                if config.totalExpFormula(self.data["level"]-level) > self.data["experience"]:
                    break
                level += 1
            if level:
                self.setLevel(self.data["level"]-level)
        if not level:
            self.refreshStatus()

    # Mana & soul
    def setMana(self, mana):
        if self.data["health"] > 0:
            self.saveData = True
            self.data["mana"] = mana
            self.refreshStatus()
            return True
        return False

    def modifyMana(self, mana):
        return self.setMana(min(self.data["mana"] + mana, self.data["manamax"]))

    def modifySpentMana(self, mana, refresh=False):
        self.data["manaspent"] += mana

        if self.data["manaspent"] < 0:
            self.data["manspent"] = 0

        self.saveData = True
        modify = 0
        maglevel = self.data["maglevel"]
        if mana > 0:
            while self.data["manaspent"] > int(config.magicLevelFormula(maglevel, self.getVocation().mlevel)):
                modify += 1
                maglevel += 1


        else:
            while self.data["manaspent"] < int(config.magicLevelFormula(maglevel, self.getVocation().mlevel)):
                modify -= 1
                maglevel -= 1

        self.modifyMagicLevel(modify)
        if refresh:
            self.refreshStatus()


    def setSoul(self, soul):
        if self.data["health"] > 0:
            self.saveData = True
            self.data["soul"] = soul
            self.refreshStatus()
            return True
        return False

    def modifySoul(self, soul):
        return self.setSoul(self.data["soul"] + soul)

    # Skills
    def addSkillLevel(self, skill, levels):
        res = game.scriptsystem.get("skill").run(creature=self, skill=skill, fromLevel=self.skills[skill], toLevel=self.skills[skill] + levels)
        if res == False: return

        # Saved data
        self.data["skills"][skill] += levels

        # Active data
        self.skills[skill] += levels

        # Update goals
        goal = config.skillFormula(self.skills[skill], self.getVocation().meleeSkill)
        self.setStorage('__skill%d' % skill, 0)
        self.data["skill_tries"][skill] = 0
        self.skillGoals[skill] = goal

        self.refreshSkills()
        self.saveSkills = True

    def tempAddSkillLevel(self, skill, level):
        self.skills[skill] = self.skills[skill] + level
        self.refreshSkills()
        self.saveSkills = True

    def tempRemoveSkillLevel(self, skill):
        self.skills[skill] = self.skills[skill]
        self.refreshSkills()
        self.saveSkills = True

    def getActiveSkill(self, skill):
        return self.skills[skill]

    def skillAttempt(self, skillType, amount = 1):
        try:
            self.data["skill_tries"][skillType] += amount

        except:
            # Happends on new members using new weapons
            self.data["skill_tries"][skillType] = amount

        skill = self.data["skill_tries"][skillType]
        skillGoal = self.skillGoals[skillType]
        if skill >= skillGoal:
            self.addSkillLevel(skillType, 1)
            attempts = skillGoal - skill
            if attempts:
                self.skillAttempt(skillType, attempts)
                return # No refresh yet

        self.refreshSkills()

    def getSkillAttempts(self, skill):
        return self.data["skill_tries"][skill]

    # Soul
    def soulGain(self):
        def doSoulGain(gainOverX):
            self.modifySoul(1)
            if self.doingSoulGain - gainOverX >= time.time():
                call_later(gainOverX, doSoulGain, gainOverX)
            else:
                self.doingSoulGain = False

        if self.doingSoulGain > time.time():
            self.doingSoulGain += (config.soulGain)
        else:
            self.doingSoulGain = time.time() + (config.soulGain)
            gainTime = self.getVocation().soulticks * self.getRegainRate()
            call_later(gainTime, doSoulGain, gainTime)
    # Spells
    def cooldownSpell(self, icon, group, cooldown, groupCooldown=None):
        if groupCooldown == None: groupCooldown = cooldown

        stream = self.packet()
        if cooldown > 0:
            stream.cooldownIcon(icon, cooldown)
        if groupCooldown > 0:
            stream.cooldownGroup(group, groupCooldown)

        stream.send(self.client)
        t = time.time()
        self.cooldowns[icon] = t + cooldown
        self.cooldowns[group << 8] = t + groupCooldown

    def cooldownIcon(self, icon, cooldown):
        self.cooldowns[icon] = time.time() + cooldown
        stream = self.packet()
        stream.cooldownIcon(icon, cooldown)
        stream.send(self.client)

    def cooldownGroup(self, group, cooldown):
        self.cooldowns[group << 8] = time.time() + cooldown
        stream = self.packet()
        stream.cooldownGroup(group, cooldown)
        stream.send(self.client)

    def canDoSpell(self, icon, group):
        t = time.time()
        group = group << 8
        if not group in self.cooldowns or self.cooldowns[group] < t:
            if not icon in self.cooldowns or self.cooldowns[icon] < t:
                return True
        return False

    def setModes(self, attack, chase, secure):
        res = game.scriptsystem.get('modeChange').run(creature=self, attack=attack, chase=chase, secure=secure)

        if res == False: return
        self.modes[0] = attack

        if self.target and self.targetMode == 1 and self.modes[1] != 1 and chase == 1:
            self.walk_to(self.target.position, -1, True)
            self.target.scripts["onNextStep"].append(self.followCallback)

        self.modes[1] = chase
        self.modes[2] = secure

    def setTarget(self, target):
        stream = self.packet(0xA3)
        stream.uint32(target.cid)
        stream.send(self.client)
        if not self.target:
            self.target = target

    def cancelWalk(self, direction=None):
        direction = direction if direction is not None else self.direction

        if self.lastClientMove == direction:
            self.lastClientMove = None
            stream = self.packet(0xB5)
            stream.uint8(direction if direction is not None else self.direction)
            stream.send(self.client)

    def tutorial(self, tutorialId):
        stream = self.packet(0xDC)
        stream.uint8(tutorialId)
        stream.send(self.client)

    def mapMarker(self, position, typeId, desc=""):
        stream = self.packet(0xDD)
        stream.position(position)
        stream.uint8(typeId)
        stream.string(desc)
        stream.send(self.client)

    def outfitWindow(self):
        stream = self.packet(0xC8)

        # First the current outfit
        stream.outfit(self.outfit, self.addon, self.mount)
        looks = []
        for outfit in game.resource.outfits:
            if len(looks) == stream.maxOutfits:
                break
            if outfit and self.canWearOutfit(outfit.name):
                looks.append(outfit)

        if looks:
            stream.uint8(len(looks))
            for outfit in looks:
                look = outfit.getLook(self.gender)
                stream.uint16(look[0])
                stream.string(outfit.name)
                stream.uint8(self.getAddonsForOutfit(outfit.name))
        else:
            # Send the current outfit only
            stream.uint8(1)
            stream.uint16(self.outfit[0])
            stream.string("Current outfit")
            stream.uint8(self.addon)

        if self.client.version >= 870:
            if config.allowMounts:
                mounts = []
                for mount in game.resource.mounts:
                    if len(mounts) == stream.maxMounts:
                        break
                    if mount and self.canUseMount(mount.name):
                        mounts.append(mount)

                stream.uint8(len(mounts))
                for mount in mounts:
                    stream.uint16(mount.cid)
                    stream.string(mount.name)
            else:
                stream.uint8(0)

        stream.send(self.client)

    def setWindowHandler(self, windowId, callback):
        self.windowHandlers[windowId] = callback

    def textWindow(self, item, canWrite=False, maxLen=0xFF, text="", writtenBy="", timestamp=0):
        stream = self.packet(0x96)

        self.windowTextId += 1
        item._windowTextId = self.windowTextId

        stream.uint32(self.windowTextId)

        stream.uint16(item.cid)
        if canWrite:
            stream.uint16(maxLen)
            stream.string(text)
        else:
            stream.uint16(len(text))
            stream.string(text)

        stream.string(writtenBy)
        if timestamp:
            timestamp = datetime.datetime.fromtimestamp(timestamp)

            stream.string("%d/%d/%d - %d:%d" % (timestamp.day, timestamp.month, timestamp.year, timestamp.hour, timestamp.minute))
        else:
            stream.string("")

        stream.send(self.client)
        return self.windowTextId

    def dialog(self, title, message, buttons=["Ok", "Exit"], defaultEnter=0, defaultExit=1):
        stream = self.packet()

        self.windowTextId += 1
        stream.dialog(self, self.windowTextId, title, message, buttons, defaultEnter, defaultExit)
        stream.send(self.client)
        return self.windowTextId

    def houseWindow(self, text):
        stream = self.packet(0x97)
        self.windowTextId += 1

        stream.uint8(0) # Unused in PyOT
        stream.uint32(self.windowTextId)
        stream.string(text)
        stream.send(self.client)

        return self.windowTextId

    def stopAutoWalk(self):
        self.stopAction()

        self.cancelWalk(self.direction)

    def updateContainer(self, container, parent=False, update=True):
        if parent and update:
            # Replace it in structure
            for i in list(self.openContainers.items()):
                if i[1] == container:
                    self.openContainers[i[0]] = container
                    break

        self.openContainer(container, parent, update)

    def updateAllContainers(self):
        if self.openContainers:
            stream = self.packet(0x6E)
            for i in list(self.openContainers.items()):
                parent = False
                try:
                    parent = bool(i[1].parent)
                except:
                    pass
                stream.uint8(i[0])

                stream.uint16(i[1].cid)
                stream.string(i[1].rawName())

                stream.uint8(i[1].containerSize)
                stream.uint8(parent)
                stream.uint8(len(i[1].container))

                for item in i[1].container:
                    stream.item(item)
        else:
            stream = self.packet()

        for slot in range(SLOT_CLIENT_FIRST,SLOT_CLIENT_FIRST+SLOT_CLIENT_SLOTS):
            if self.inventory[slot-1]:
                stream.uint8(0x78)
                stream.uint8(slot)

                stream.item(self.inventory[slot-1])
            else:
                stream.uint8(0x79)
                stream.uint8(slot)
        stream.send(self.client)

    def openContainer(self, container, parent=False, update=False):
        containerId = None

        if update or not container in list(self.openContainers.values()):
            stream = self.packet(0x6E)

            if not update:
                containerId = self.lastOpenContainerId
                self.lastOpenContainerId += 1
                container.openIndex = containerId
                self.openContainers[containerId] = container
            else:
                for i in list(self.openContainers.items()):
                    if i[1] == container:
                        containerId = i[0]
                        break
                if containerId == None:
                    print("problem!")
                    return False

            stream.uint8(containerId)

            stream.uint16(container.cid)
            stream.string(container.rawName())

            stream.uint8(container.containerSize)
            stream.uint8(parent)
            stream.uint8(len(container.container))

            for item in container.container:
                stream.item(item)

            stream.send(self.client)

            return True

    def closeContainer(self, container):
        if container.openCreatures:
            container.openCreatures.remove(self)
            if not container.openCreatures:
                del container.openCreatures

        if container.openIndex == None:
            return False

        #def callOpen(): game.scriptsystem.get('use').run(container, self, end, position=StackPosition(0xFFFF, 0, 0, 0), index=index)

        res = game.scriptsystem.get('close').run(thing=container, creature=self, index=container.openIndex)
        if res == False:
            return False

        stream = self.packet(0x6F)
        stream.uint8(container.openIndex)
        del self.openContainers[container.openIndex]
        if container.openIndex == self.lastOpenContainerId-1:
            self.lastOpenContainerId -= 1
            if self.lastOpenContainerId:
                for i in range(self.lastOpenContainerId-2, -1, -1):
                    try:
                        self.openContainers[i]
                        break
                    except:
                        self.lastOpenContainerId -= 1

        del container.openIndex
        stream.send(self.client)

    def closeContainerId(self, openId):
        try:
            container = self.openContainers[openId]

            res = game.scriptsystem.get('close').run(creature=self, thing=container, index=openId)
            if res == False:
                return False

            stream = self.packet(0x6F)
            stream.uint8(openId)
            del self.openContainers[openId]
            if openId == self.lastOpenContainerId-1:
                self.lastOpenContainerId -= 1
                if self.lastOpenContainerId:
                    for i in range(self.lastOpenContainerId-2, -1, -1):
                        try:
                            self.openContainers[i]
                            break
                        except:
                            self.lastOpenContainerId -= 1
            del container.openIndex
            stream.send(self.client)
            return True

        except:
            return False

    def arrowUpContainer(self, openId):
        bagFound = self.openContainers[openId]

        if bagFound.parent:
            bagFound.parent.openIndex = openId
            del bagFound.openIndex
            self.openContainers[openId] = bagFound.parent

            game.scriptsystem.get('close').run(thing=bagFound, creature=self, index=openId)
            if res == False:
                return False

            self.updateContainer(self.openContainers[openId], True if self.openContainers[openId].parent else False)

    # Item to container
    def addItem(self, item, placeOnGround=True):
        ret = False
        if self.inventory[2]:
            try:
                ret = self.itemToContainer(self.inventory[2], item)
            except:
                pass

        if ret == False and not self.inventory[9]:
            if self.addCache(item) != False:
                self.inventory[9] = item
                item.setPosition(Position(0xFFFF, 10, 0), self)
                stream = self.packet()
                stream.addInventoryItem(10, self.inventory[9])
                self.refreshStatus(stream)
                stream.send(self.client)
                item.decay()
                return True
        if ret == False and placeOnGround:
            return item.place(self.position)

        elif ret == False:
            return False

        return True

    def itemToContainer(self, container, item, count=None, recursive=True, stack=True, placeOnGround=True, streamX=None):
        stream = streamX
        update = False

        if not streamX:
            stream = self.packet()

        if not count:
            count = 1 if item.count == None or item.count <= 0 else item.count

        try:
            self.inventoryCache[container.itemId].index(container)
            update = True
        except:
            pass

        # Find item to stack with
        if stack and item.stackable and count < 100:
            slot = 0
            bags = [container]
            for bag in bags:
                for itemX in container.container:
                    if itemX.itemId == item.itemId and itemX.count < 100:
                        _newItem = game.scriptsystem.get("stack").run(thing=item, creature=self, position=item.position, onThing=itemX, onPosition=itemX.position, count=count, end=False)
                        if _newItem == False:
                            ret = self.itemToContainer(container, item, stack=False, recursive=recursive, streamX=streamX)
                            return ret
                        elif isinstance(_newItem, Item):
                            self.itemToContainer(container, _newItem)
                            continue

                        total = itemX.count + count
                        Tcount = min(total, 100)
                        count = total - Tcount
                        if update:
                            ret = self.modifyCache(itemX, itemX.count - Tcount)
                            if ret == False:
                                item.place(self.position)
                                self.tooHeavy()
                                return

                        itemX.count = Tcount


                        # Is it a open container, if so, send item update
                        if bag.openIndex != None:
                            stream.updateContainerItem(bag.openIndex, slot, itemX)



                        if not count:
                            break

                    elif recursive and itemX.containerSize and itemX != bag:
                        bags.append(itemX) # Found a container for recursive

                    slot += 1

                if not count:
                    break

                slot = 0

        print(item.count, count)
        if count != item.count:
            item.count = count

        if count:
            # Add item
            if update and (self.freeCapacity() - ((item.weight or 0) * (item.count or 1)) < 0):
                self.tooHeavy()
                return False

            if recursive:
                info = container.placeItemRecursive(item)
            else:
                info = container.placeItem(item)

            if info == None:
                return False # Not possible

            if container.position.x == 0xFFFF and update:
                item.setPosition(Position(0xFFFF, DYNAMIC_CONTAINER, info), self)
            else:
                item.setPosition(Position(0xFFFF, DYNAMIC_CONTAINER, info))

            item.inContainer = container if isinstance(info, int) else info

            if recursive and info and info.openIndex != None:
                stream.addContainerItem(info.openIndex, item)

            elif container.openIndex != None:
                stream.addContainerItem(container.openIndex, item)

            if update:
                self.addCache(item, container)



        if not streamX:
            if update:
                self.refreshStatus(stream)
            stream.send(self.client)

        # HACK!!!
        self.updateContainer(container)

        return True

    def itemToUse(self, item):
        # Means, right hand, left hand, ammo or bag. Stackable only
        if not self.inventory[4]:
            self.inventory[4] = item
            item.setPosition(Position(0xFFFF, 5, 0), self)
            stream = self.packet()
            stream.addInventoryItem(5, self.inventory[4])
            stream.send(self.client)
            return True
        elif self.inventory[4].itemId == item.itemId and self.inventory[4].count < 100:
            prevCount = self.inventory[4].count
            self.inventory[4].count = min(100, prevCount + item.count)
            item.count = (prevCount + item.count) - self.inventory[4].count
            stream = self.packet()
            stream.addInventoryItem(5, self.inventory[4])
            stream.send(self.client)
        if item.count:
            if not self.inventory[5]:
                self.inventory[5] = item
                item.setPosition(Position(0xFFFF, 6, 0), self)
                stream = self.packet()
                stream.addInventoryItem(6, self.inventory[5])
                stream.send(self.client)
                return True
            elif self.inventory[5].itemId == item.itemId and self.inventory[5].count < 100:
                prevCount = self.inventory[5].count
                self.inventory[5].count = min(100, prevCount + item.count)
                item.count = (prevCount + item.count) - self.inventory[5].count
                stream = self.packet()
                stream.addInventoryItem(6, self.inventory[5])
                stream.send(self.client)

        if item.count:
            if not self.inventory[9]:
                self.inventory[9] = item
                item.setPosition(Position(0xFFFF, 10, 0), self)
                stream = self.packet()
                stream.addInventoryItem(10, self.inventory[0])
                stream.send(self.client)
                return True
            elif self.inventory[9].itemId == item.itemId and self.inventory[9].count < 100:
                prevCount = self.inventory[5].count
                self.inventory[9].count = min(100, prevCount + item.count)
                item.count = (prevCount + item.count) - self.inventory[9].count
                stream = self.packet()
                stream.addInventoryItem(10, self.inventory[9])
                stream.send(self.client)

        if item.count and self.inventory[2]:
            return self.itemToContainer(self.inventory[2], item)
        elif item.count:
            return False
        return True
    # Item To inventory slot
    def itemToInventory(self, item, slot=None, stack=True):
        if slot == None:
            slot = item.slots()
            if not slot:
                return False
            slot = slot[0]

        if self.inventory[slot] and stack and item.stackable and item.itemId == self.inventory[slot].itemId and self.inventory[slot].count+item.count <= 100:
            self.inventory[slot].count += item.count
            self.modifyCache(self.inventory[slot], item.count)
        else:
            if self.inventory[slot]:
                self.removeCache(self.inventory[slot])
            self.inventory[slot] = item
            self.addCache(item)
        item.setPosition(Position(0xFFFF, slot+1, 0), self)
        stream = self.packet()
        stream.addInventoryItem(slot+1, self.inventory[slot])
        stream.send(self.client)

        return True

    def updateInventory(self, slot):
        stream = self.packet()
        if not self.inventory[slot] or (self.inventory[slot].stackable and not self.inventory[slot].count):
            stream.removeInventoryItem(slot+1)
        else:
            stream.addInventoryItem(slot+1, self.inventory[slot])
        stream.send(self.client)

    # Death stuff
    def sendReloginWindow(self, percent=0):
        stream = self.packet(0x28)
        if self.client.version > 870: # XXX, when was this introduced?
            stream.uint8(percent)
        stream.send(self.client)

        # And kill the readyness
        # self.client.ready = False

    def losePrecent(self, withBlessings=True):
        if not config.loseCutoff:
            return 0

        elif self.data["level"] < config.loseCutoff:
            lose = config.loseConstant
        else:
            lose = config.loseFormula(self.data["level"]) / self.data["experience"]

        if withBlessings and self.blessings:
            lose *= 0.92 ** self.blessings

        return int(lose * self.deathPenalityFactor)

    def itemLosePrecent(self):
        if self.getSkull() in (SKULL_BLACK, SKULL_RED) and config.redSkullLoseRate:
            return (config.redSkullLoseRate, config.redSkullLoseRate)

        # This is constants it would seem.
        container = 100
        if self.blessings == 1:
            container = 70
        elif self.blessings == 2:
            container = 45
        elif self.blessings == 3:
            container = 25
        elif self.blessings == 4:
            container = 10

        return (container, container / 10.0)

    def onDeath(self):
        try:
            lastAttacker = self.getLastDamager()
            lastDmgIsPlayer = lastAttacker.isPlayer()
        except:
            lastAttacker = self
            lastDmgIsPlayer = False
        deathData = {}
        loseRate = self.losePrecent()
        itemLoseRate = self.itemLosePrecent()

        if self.getSkull() in (SKULL_RED, SKULL_BLACK):
            itemLoseRate = config.redSkullLoseRate, config.redSkullLoseRate

        deathData["loseRate"] = loseRate
        deathData["itemLoseRate"] = itemLoseRate
        deathData["unjust"] = False
        corpse = Item(HUMAN_CORPSE)

        lastDamagerSkull = self.getSkull(lastAttacker)
        if lastDmgIsPlayer:
            # Just or unjust?
            unjust = True
            if self.getSkull() or lastDamagerSkull in (SKULL_ORANGE, SKULL_YELLOW, SKULL_GREEN):
                unjust = False

            deathData["unjust"] = unjust

        if (game.scriptsystem.get("death").run(creature=self, creature2=lastAttacker, corpse=corpse, deathData=deathData)) == False:
            return

        # Lose all conditions.
        self.loseAllConditions()

        unjust = deathData["unjust"]
        loseRate = deathData["loseRate"]
        itemLoseRate = deathData["itemLoseRate"]

        print("TODO: Unfair fight.")
        if self.client:
            self.sendReloginWindow(100)

        # Reduce experience, manaspent and total skill tries (ow my)
        if loseRate:
            self.modifyExperience(-int(self.data["experience"] * (loseRate/100.0)))
            self.modifySpentMana(-int(self.data["manaspent"] * (loseRate/100.0)))

            for skill in range(SKILL_FIRST, SKILL_LAST):
                # First, get total skill tries.
                tries = config.totalSkillFormula(self.data["skills"][skill], self.getVocation().meleeSkill) + self.getSkillAttempts(skill)

                # Reduce them.
                tries /= 1 + (loseRate/100.0)
                tries = int(tries)

                # Skill tries to level.
                level = int(config.skillTriesToLevel(self.getVocation().meleeSkill, tries))

                # Previous level skill tries.
                prevTries = int(config.totalSkillFormula(level-1, self.getVocation().meleeSkill))

                # Get the level goals.
                goal = tries-prevTries

                # Set new level.
                self.addSkillLevel(skill, level - self.data["skills"][skill])
                self.skillAttempt(skill, goal)

        # PvP experience and death entries.
        if lastDmgIsPlayer:
            # Was this revenge?
            if lastDamagerSkull == SKULL_ORANGE:
                revengeEntry = death.findUnrevengeKill(lastAttacker.data["id"], self.data["id"])
                if not revengeEntry:
                    print("BUG: This was a revenge, but we can't find the revenge death entry...")
                elif revengeEntry.revenged == True:
                    print("BUG: revenging a revenged kill.")
                else:
                    revengeEntry.revenge()
            entry = deathlist.DeathEntry(lastAttacker.data["id"], self.data["id"], unjust)
            deathlist.addEntry(entry)

            # Resend attackers skull.
            # Trick to destroy cache:
            lastAttacker.skull = 0
            lastAttacker.refreshSkull()

            # PvP Experience.
            lastAttacker.modifyExperience(config.pvpExpFormula(lastAttacker.data["level"], self.data["level"], self.data["experience"]))

        #if temp skull remove it on death
        if self.getSkull() in (SKULL_WHITE, SKULL_YELLOW, SKULL_GREEN):
            self.setSkull(SKULL_NONE)

        # Remove summons
        if self.activeSummons:
            for summon in self.activeSummons:
                summon.magicEffect(EFFECT_POFF)
                summon.despawn()
                summon.noBrain = True

        tile = game.map.getTile(self.position)

        self.despawn()

        # Set position
        self.position = Position(*game.map.mapInfo.towns[self.data["town_id"]][1])
        self.data["health"] = self.data["healthmax"]
        self.data["mana"] = self.data["manamax"]

        # Are we suppose to lose the container?
        itemLoseRate = self.itemLosePrecent()
        if self.inventory[2] and random.randint(1, 100) < itemLoseRate[0]:
            corpse.placeItem(self.inventory[2])
            self.inventory[2] = None

        # Loop over each item in the inventory to see if we lose em.
        for index in range(SLOT_FIRST-1, SLOT_CLIENT_SLOTS):
            if self.inventory[index] and random.randint(1, 1000) < (itemLoseRate[1] * 10):
                corpse.placeItem(self.inventory[index])
                self.inventory[index] = None

        if not self.alive and self.data["health"] < 1:

            splash = Item(FULLSPLASH)
            splash.fluidSource = FLUID_BLOOD

            corpse.place(self.position)
            splash.place(self.position)

            splash.decay()
            corpse.decay()

            try:
                tile.removeCreature(self)
            except:
                pass
            for spectator in getSpectators(self.position, ignore=[self]):
                stream = spectator.packet(0x69)
                stream.position(pos)
                stream.tileDescription(tile)
                stream.uint8(0x00)
                stream.uint8(0xFF)
                stream.send(spectator)

    def onSpawn(self):
        if self.clientId() not in allCreatures:
            allCreatures[self.clientId()] = self

        if self.data["health"] <= 0 or not self.alive:
            if self.getSkull() == SKULL_BLACK:
                self.data["health"] = config.blackSkullRecoverHealth if config.blackSkullRecoverHealth != -1 else self.data["healthmax"]
                self.data["mana"] =  config.blackSkullRecoverMana if config.blackSkullRecoverMana != -1 else self.data["manamax"]
            else:
                self.data["health"] = self.data["healthmax"]
                self.data["mana"] = self.data["manamax"]
            self.alive = True
            game.scriptsystem.get("respawn").run(creature=self)
            self.teleport(Position(*game.map.mapInfo.towns[self.data['town_id']][1]))

    # Loading:
    def __buildInventoryCache(self, container):
        for item in container.container:
            weight = item.weight

            item.inContainer = container
            item.creature = self
            item.position = Position(0xFFFF, DYNAMIC_CONTAINER, 0)
            if weight:
                self.inventoryWeight += weight * (item.count or 1)
            try:
                self.inventoryCache[item.itemId].append(item)
                self.inventoryCache[item.itemId][0] += item.count or 1
            except:
                self.inventoryCache[item.itemId] = [item.count or 1, item]

            if item.container:
                try:
                    item.container.remove(item)
                except:
                    pass
                self.__buildInventoryCache(item)

    def unpickleInventory(self, inventoryData):
        try:
            self.inventory = pickle.loads(inventoryData)
        except:
            print("Broken inventory (blame MySQL, it usually means you killed the connection in the middle of a save)")
            purse = Item(1987)
            purse.name = "Purse"
            purse.addAction('purse')
            purse.position = Position(0xFFFF, 11, 0)
            purse.creature = self
            self.inventory = [None, None, None, None, None, None, None, None, None, None, purse] # Last item XXX is purse.

        # Generate the inventory cache
        for item in self.inventory:
            if isinstance(item, game.item.Item):
                weight = item.weight
                item.creature = self
                item.position = Position(0xFFFF, self.inventory.index(item)+1, 0)
                if weight:
                    self.inventoryWeight += weight * (item.count or 1)
                try:
                    self.inventoryCache[item.itemId].append(item)
                    self.inventoryCache[item.itemId][0] += item.count or 1
                except:
                    self.inventoryCache[item.itemId] = [item.count or 1, item]

                if item.container:
                    try:
                        item.container.remove(item)
                    except:
                        pass
                    self.__buildInventoryCache(item)

    # Saving
    def pickleInventory(self):
        return fastPickler(self.inventory)

    def pickleDepot(self):
        return fastPickler(self.depot)

    def _saveQuery(self, force=False):
        extraQuery = ""
        extras = []

        # To this little check here
        if self.removeMe:
            del allPlayers[self.name()]
            del game.creature.allCreatures[self.clientId()]

            # Reset online status
            extraQuery = ", p.`online` = 0"


        if not self.doSave:
            return



        tables = "`players` AS `p`"
        if self.saveDepot or force:
            extras.append(self.pickleDepot())
            extraQuery += ", p.`depot` = %s"
            self.saveDepot = False

        if self.saveStorage or force:
            extras.append(otjson.dumps(self.storage))
            extraQuery += ", p.`storage` = %s"
            self.saveStorage = False

        if self.saveSkills or force:
            tables += ", `player_skills` as `s`"
            # TODO: Custom skills.
            extraQuery += ", s.`fist` = %d, s.`fist_tries` = %d, s.`sword` = %d, s.`sword_tries` = %d, s.`club` = %d, s.`club_tries` = %d, s.`axe` = %d, s.`axe_tries` = %d, s.`distance` = %d, s.`distance_tries` = %d, s.`shield` = %d, s.`shield_tries` = %d, s.`fishing` = %d, s.`fishing_tries` = %d" % (self.data["skills"][SKILL_FIST], self.data["skill_tries"][SKILL_FIST], self.data["skills"][SKILL_SWORD], self.data["skill_tries"][SKILL_SWORD], self.data["skills"][SKILL_CLUB], self.data["skill_tries"][SKILL_CLUB], self.data["skills"][SKILL_AXE], self.data["skill_tries"][SKILL_AXE], self.data["skills"][SKILL_DISTANCE], self.data["skill_tries"][SKILL_DISTANCE], self.data["skills"][SKILL_SHIELD], self.data["skill_tries"][SKILL_SHIELD], self.data["skills"][SKILL_FISH], self.data["skill_tries"][SKILL_FISH])
            self.saveSkills = False

        if self.saveInventory or force:
            extras.append(self.pickleInventory())
            extraQuery += ", p.`inventory` = %s"
            self.saveInventory = False

        if self.saveCondition or force:
            for conId in self.conditions.copy():
                if not self.conditions[conId].length > 0:
                    del self.conditions[conId]

            extras.append(fastPickler(self.conditions))
            extraQuery += ", p.`conditions` = %s"
            self.saveCondition = False

        # XXX hack
        extras.append(self.data["id"])

        if self.saveData or extraQuery or force: # Don't save if we 1. Change position, or 2. Just have stamina countdown
            return ["UPDATE "+tables+" SET p.`experience` = %s, p.`manaspent` = %s, p.`mana`= %s, p.`health` = %s, p.`soul` = %s, p.`stamina` = %s, p.`posx` = %s, p.`posy` = %s, p.`posz` = %s, p.`instanceId` = %s, p.`balance` = %s"+extraQuery+" WHERE p.`id` = %s", self.data["experience"], self.data["manaspent"], self.data["mana"], self.data["health"], self.data["soul"], self.data["stamina"] * 1000, self.position.x, self.position.y, self.position.z, self.position.instanceId, self.data["balance"]]+extras

    def save(self, force=False):
        if self.doSave:
            argc = self._saveQuery(force)
            if argc:
                sql.runOperation(*argc)



    def saveSkills(self):
        sql.runOperation("UPDATE `players` SET `skills`= %s WHERE `id` = %d", otjson.dumps(self.skills), self.data["id"])


    def saveExperience(self):
        sql.runOperation("UPDATE `players` SET `experience`= %d, `manaspent` = %d WHERE `id` = %d", self.data["experience"], self.data["manaspent"], self.data["id"])


    def saveStorage(self):
        sql.runOperation("UPDATE `players` SET `storage`= %s WHERE `id` = %d", otjson.dumps(self.storage), self.data["id"])

    # Shopping
    def setTrade(self, npc):
        if not self.openTrade:
            self.openTrade = npc


    def closeTrade(self):
        if self.openTrade:
            stream = self.packet(0x7C)
            stream.send(self.client)
            self.openTrade = None
        else:
            stream = self.packet(0x7F)
            stream.send(self.client)

    def getMoney(self):
        if not self.inventory[2]:
            return 0

        money = 0
        for item in self.inventory[2].getRecursive():
            currency = item.worth
            if currency:
                money += currency * item.count

        return money

    def removeMoney(self, amount):
        moneyItems = []
        money = 0
        for item, bag, pos in self.inventory[2].getRecursiveWithBag():
            currency = item.worth
            if currency:
                money += currency * item.count
                moneyItems.append((item, bag, pos))
                if money >= amount:
                    break

        if money >= amount:
            removedMoney = 0
            for i in moneyItems[:-1]:
                removedMoney += i[0].worth * i[0].count
                i[1].removeItem(i[0])

            last = moneyItems[-1]
            count = 0
            currency = last[0].worth
            for i in range(last[0].count):
                removedMoney += currency
                count += 1
                if removedMoney >= amount:
                    last[0].count -= count
                    if last[0].count <= 0:
                        last[1].removeItem(last[0])
                    break

            addBack = removedMoney - amount
            if addBack: # Add some money back
                for x in MONEY_MAP:
                    if addBack >= x[1]:
                        coins = int(addBack / x[1])
                        addBack = addBack % x[1]
                        while coins:
                            count = min(100, coins)
                            self.itemToContainer(self.inventory[2], game.item.Item(x[0], count))
                            coins -= count

                    if not addBack:
                        break
            self.updateAllContainers()
            return amount

        else:
            return 0

    def addMoney(self, amount):
        for x in MONEY_MAP:
            if amount >= x[1]:
                coins = int(amount / x[1])
                amount = amount % x[1]
                while coins:
                    count = min(100, coins)
                    self.itemToContainer(self.inventory[2], game.item.Item(x[0], count))
                    coins -= count
                if not amount:
                    break
        return True

    # Storage
    def setStorage(self, field, value):
        self.storage[field] = value
        self.saveStorage = True

    def getStorage(self, field, default=None):
        try:
            return self.storage[field]
        except:
            return default

    def modifyStorage(self, field, change):
        self.storage[field] += change
        self.saveStorage = True

    def removeStorage(self, field):
        try:
            del self.storage[field]
            self.saveStorage = True
        except:
            pass

    # Depot stuff
    def getDepot(self, depotId):
        if depotId in self.depot:
            return self.depot[depotId]
        else:
            return []

    def setDepot(self, depotId, storage):
        self.depot[depotId] = storage
        self.saveDepot = True

    def _getDepotItemCount(self, items):
        count = 0
        for x in items:
            count += 1
            if x.containerSize:
                count += self._getDepotItemCount(x.container)
        return count

    def getDepotItemCount(self, depotId):
        depot = self.getDepot(depotId)
        if depot:
            return self._getDepotItemCount(depot)
        else:
            return 0

    def _depotMarketCache(self, cache, items):
        for item in items:
            if item.duration or (item.charges and item.charges != game.item.items[item.itemId]["charges"]):
                continue

            if item.containerSize:
                self._depotMarketCache(cache, item.container)
            else:
                try:
                    cache[item.itemId] += item.count or 1
                except:
                    cache[item.itemId] = item.count or 1

    def getDepotMarketCache(self, depotId):
        depot = self.getDepot(depotId)
        if not depot:
            return {}
        else:
            depotCache = {}
            self._depotMarketCache(depotCache, depot)
            return depotCache

    def _removeFromDepot(self, items, itemId, count):
        _count = 0
        for item in copy.copy(items):
            if item.itemId == itemId:
                oldCount = item.count or 1
                item.count = max(0, oldCount - count)
                _count += oldCount - item.count
                if not item.count:
                    items.remove(item)
                if _count == count:
                    return _count
            if item.container:
                _count += self._removeFromDepot(item.container, itemId, count - _count)
                if _count == count:
                    return _count

        return _count

    def removeFromDepot(self, depotId, itemId, count=1):
        depot = self.getDepot(depotId)
        if not depot:
            return 0

        return self._removeFromDepot(depot, itemId, count)

    # Stuff from protocol:
    def followCallback(self, who):
        if self.target == who and self.targetMode > 0:
            self.walk_to(self.target.position, -1, True)
            self.target.scripts["onNextStep"].append(self.followCallback)

    def setFollowTarget(self, cid):
        if not cid: # or self.targetMode == 2
            #self.cancelWalk()
            self.cancelTarget()

            self.target = None
            self.targetMode = 0
            self.message(_l(self, "Target lost.")) # Required :p
            return

        if cid in allCreatures:
            target = allCreatures[cid]
            ret = game.scriptsystem.get('target').run(creature=self, creature2=target, attack=True)
            if ret == False:
                return
            elif ret != None:
                self.target = ret
            else:
                self.target = target

            self.targetMode = 2
            self.walk_to(self.target.position, -1, True)
            self.target.scripts["onNextStep"].append(self.followCallback)
        else:
            self.notPossible()

    # Skull and emblems and such
    def square(self, creature, color=27):
        stream = self.packet(0x86)
        stream.uint32(creature.cid)
        stream.uint8(color)
        stream.send(self.client)

    # Quest system
    def beginQuest(self, questIdentifier):
        if isinstance(questIdentifier, game.resource.Quest):
            questIdentifier = questIdentifier.name

        quests = self.getStorage('__quests')
        if not quests:
            quests = {}

        quests[questIdentifier] = [1, 0, False, time.time(), False] # Mission, completed steps, startTime, endTime

        self.setStorage('__quests', quests)

        if config.sendTutorialSignalUponQuestLogUpdate:
            self.tutorial(3)

    def progressQuest(self, questIdentifier):
        if isinstance(questIdentifier, game.resource.Quest):
            questIdentifier = questIdentifier.name

        quests = self.getStorage('__quests')
        quests[questIdentifier][1] += 1
        self.setStorage('__quests', quests)

        if config.sendTutorialSignalUponQuestLogUpdate:
            self.tutorial(3)

    def progressQuestMission(self, questIdentifier):
        if isinstance(questIdentifier, game.resource.Quest):
            questIdentifier = questIdentifier.name

        quests = self.getStorage('__quests')
        quests[questIdentifier][0] += 1
        self.setStorage('__quests', quests)

        if config.sendTutorialSignalUponQuestLogUpdate:
            self.tutorial(3)

    def finishQuest(self, questIdentifier):
        if isinstance(questIdentifier, game.resource.Quest):
            questIdentifier = questIdentifier.name

        quests = self.getStorage('__quests')
        quests[questIdentifier][1] += 1 # Finish the last step
        quests[questIdentifier][2] = True
        quests[questIdentifier][4] = time.time()
        self.setStorage('__quests', quests)

        if config.sendTutorialSignalUponQuestLogUpdate:
            self.tutorial(3)

    def questLog(self):
        quests = self.getStorage('__quests')
        if not quests:
            quests = {}

        game.scriptsystem.get("questLog").run(creature=self, questLog=quests)

        # Vertify the quests
        for quest in quests.copy():
            try:
                game.resource.getQuest(quest)
            except:
                print("Debug, ending quest %s" % quest)
                del quests[quest]
                self.setStorage('__quests', quests)

        stream = self.packet(0xF0)
        stream.uint16(len(quests))
        for quest in quests:
            questObj = game.resource.getQuest(quest)
            if not questObj.missions:
                stream.uint16(0)
            stream.uint16(game.resource.reverseQuests[quest]+1)
            stream.string(questObj.name)
            stream.uint8(quests[quest][2])

        stream.send(self.client)

    def questLine(self, questIdentifier):
        if isinstance(questIdentifier, game.resource.Quest):
            questIdentifier = questIdentifier.name

        quests = self.getStorage('__quests')
        questObj = game.resource.getQuest(questIdentifier)
        stream = self.packet(0xF1)
        stream.uint16(game.resource.reverseQuests[questIdentifier]+1)

        stream.uint8(questObj.missions[quests[questIdentifier][0]-1][1] + questObj.missions[quests[questIdentifier][0]-1][2])
        for i in range(quests[questIdentifier][0]):
            for x in range(questObj.missions[i][1], questObj.missions[i][1]+questObj.missions[i][2]):
                stream.string(questObj.missions[i][0] + (' (completed)' if quests[questIdentifier][1] > x else ''))
                stream.string(questObj.descriptions[x])

        stream.send(self.client)

    def questProgress(self, questIdentifier):
        if isinstance(questIdentifier, game.resource.Quest):
            questIdentifier = questIdentifier.name

        quests = self.getStorage('__quests')
        try:
            return quests[questIdentifier][1]
        except:
            return 0

    def questStarted(self, questIdentifier):
        if isinstance(questIdentifier, game.resource.Quest):
            questIdentifier = questIdentifier.name

        quests = self.getStorage('__quests')
        try:
            quests[questIdentifier]
            return True
        except:
            return False

    def questCompleted(self, questIdentifier):
        if isinstance(questIdentifier, game.resource.Quest):
            questIdentifier = questIdentifier.name

        quests = self.getStorage('__quests')
        try:
            return quests[questIdentifier][2]
        except:
            return False

    # VIP system
    def getVips(self):
        vips = self.getStorage('__vips')
        if not vips:
            return []
        return vips

    @gen.coroutine
    def sendVipList(self):
        vips = self.getStorage('__vips')
        if not vips:
            return

        result = yield sql.runQuery("SELECT `id`, `name` FROM players WHERE `id` IN (%s)" % (tuple(vips)))
        if result:
            stream = self.packet()
            for player in result:
                online = bool(player['name'] in allPlayers and allPlayers[player['name']].client)
                stream.vip(player['id'], player['name'], online)
                if online:
                    pkg = allPlayers[player['name']].packet()
                    pkg.vipLogin(self.data["id"])
                    pkg.send(allPlayers[player['name']].client)
            stream.send(self.client)

    def addVip(self, playerId):
        vips = self.getStorage('__vips')
        if not vips:
            vips = [playerId]
        else:
            try:
                vips.index(playerId)
                return
            except:
                vips.append(playerId)

        self.setStorage('__vips', vips)
        self.sendVipList()

    @gen.coroutine
    def addVipByName(self, name):
        result = yield getPlayerIDByName(name)
        if result:
            self.addVip(result)

    def removeVip(self, playerId):
        vips = self.getStorage('__vips')
        if not vips:
            return
        else:
            try:
                vips.remove(playerId)
            except:
                return

        self.setStorage('__vips', vips)
        #self.sendVipList()

    @gen.coroutine
    def removeVipByName(self, name):
        result = yield getPlayerIDByName(name)
        if result:
            self.removeVip(result)

    def isVip(self, playerId):
        vips = self.getStorage('__vips')
        if not vips:
            return False
        else:
            try:
                vips.index(playerId)
                return True
            except:
                return False
    # Exit
    def exit(self, message):
        self.prepareLogout(True)

        stream = self.packet()
        stream.exit(message)
        stream.send(self.client)

    def prepareLogout(self, force=False):
        if not force and self.hasCondition(CONDITION_INFIGHT):
            self.lmessage("You can't logout yet.")
            return False

        # Remove summons
        if self.activeSummons:
            for summon in self.activeSummons:
                summon.magicEffect(EFFECT_POFF)
                summon.despawn()
                summon.noBrain = True

        self.removeMe = True

        # Clear party.
        if self.party():
            self.leaveParty()

        #self.remove(False)

        return True

    # Cleanup the knownCreatures
    def removeKnown(self, creature):
        cid = 0
        try:
            self.knownCreatures.remove(creature)
            creature.knownBy(self)
            cid = creature.cid
        except:
            pass
        return cid

    def checkRemoveKnown(self):
        dead = []
        for creature in self.knownCreatures:
            if not self.canSee(creature.position, radius=(16,16)):
                return self.removeKnown(creature)
            elif creature.data["health"] < 1:
                dead.append(creature)
        try:
            return self.removeKnown(dead.pop())
        except:
            return None

    # Outfit and mount
    def canWearOutfit(self, name):
        return self.getStorage('__outfit%s' % game.resource.reverseOutfits[name])

    def addOutfit(self, name):
        self.setStorage('__outfit%s' % game.resource.reverseOutfits[name], True)

    def removeOutfit(self, name):
        self.removeStorage('__outfit%s' % game.resource.reverseOutfits[name])

    def getAddonsForOutfit(self, name):
        return self.getStorage('__outfitAddons%s' % game.resource.reverseOutfits[name]) or 0

    def addOutfitAddon(self, name, addon):
        addons = self.getAddonsForOutfit(name)
        if addons & addon == addon:
            return
        else:
            addons += addon
            self.setStorage('__outfitAddons%s' % game.resource.reverseOutfits[name], addons)

    def removeOutfitAddon(self, name, addon):
        addons = self.getAddonsForOutfit(name)
        if addons & addon == addon:
            addons -= addon
            self.setStorage('__outfitAddons%s' % game.resource.reverseOutfits[name], addons)
        else:
            return

    def canUseMount(self, name):
        return self.getStorage('__mount%s' % game.resource.reverseMounts[name])

    def addMount(self, name):
        self.setStorage('__mount%s' % game.resource.reverseMounts[name], True)

    def removeMount(self, name):
        self.removeStorage('__mount%s' % game.resource.reverseMounts[name])


    # Rates
    def getExperienceRate(self):
        return self.rates[0]
    def setExperienceRate(self, rate):
        self.rates[0] = rate
    def getRegainRate(self):
        return self.rates[4]
    def setRegainRate(self, rate):
        self.rates[4] = rate

    # Guild & party
    def guild(self):
        try:
            return game.guild.guilds[self.data["guild_id"]]
        except:
            return None

    def guildRank(self):
        guild = self.guild()
        if guild:
            return guild.rank(self.data["guild_rank"])

    def party(self):
        # We use party() here because we might need to check for things. this is a TODO or to-be-refactored.
        return self.partyObj

    def newParty(self):
        self.partyObj = game.party.Party(self)
        return self.partyObj

    def leaveParty(self):
        if self.partyObj:
            self.partyObj.removeMember(self)

    def setParty(self, partyObj):
        if self.partyObj:
            raise Exception("You got to leave the party before you can join another one")

        self.partyObj = partyObj
    # Trade
    def tradeItemRequest(self, between, items, confirm=False):
        if confirm:
            stream = self.packet(0x7D)
        else:
            stream = self.packet(0x7E)

        stream.string(between.name())
        _items = []
        itemCount = 0
        for item in items:
            _items.append(item)
            itemCount += 1
            if itemCount != 255 and item.containerSize:
                for i in item.container:
                    stream.item(i)
                    itemCount += 1
                    if itemCount == 255:
                        break
            elif itemCount == 255:
                break

        stream.uint8(itemCount)
        for i in _items:
            stream.item(i)

        stream.send(self.client)

    # Spell learning
    def canUseSpell(self, name):
        return self.getStorage("__ls%s" % name)

    def learnSpell(self, name):
        return self.setStorage("__ls%s" % name, True)

    def unlearnSpell(self, name):
        return self.setStorage("__ls%s" % name, False)

    def getSpells(self):
        # Return all spells this user can do.
        spells = []
        for spell in game.spell.spells:
            if self.canUseSpell(spell):
                spells.append(spell)

        return spells

    # Market
    def openMarket(self, marketId=0):
        if not config.enableMarket or self.client.version < 944:
            return

        market = getMarket(marketId)
        self.market = market

        stream = self.packet(0xF6)

        stream.money(self.getBalance())
        # XXX: Some older than 9.7 version needed this.
        # stream.uint8(self.getVocation().clientId)
        stream.uint8(len(market.saleOffers(self))) # Active offers

        if not self.marketDepotId in self.depotMarketCache:
            self.depotMarketCache[self.marketDepotId] = self.getDepotMarketCache(self.marketDepotId)

        stream.uint16(len(self.depotMarketCache[self.marketDepotId]))
        for entry in self.depotMarketCache[self.marketDepotId]:
            stream.uint16(cid(entry))
            stream.uint16(self.depotMarketCache[self.marketDepotId][entry])

        """stream.uint16(market.size())
        for entry in market.getItems():
            stream.uint16(game.item.cid(entry[0]))
            stream.uint16(entry[1])"""
        stream.send(self.client)

        self.marketOpen = True

        #self.marketDetails()
        #self.marketOffers() # Doesn't work

    def closeMarket(self):
        # TODO: Script events.
        self.marketOpen = False

    def marketOffers(self, itemId):
        if not config.enableMarket or self.client.version < 944:
            return

        stream = self.packet()
        stream.uint8(0xF9)
        print("itemId - marketOffers - ", itemId)
        stream.uint16(cid(itemId))

        buyOffers = self.market.getBuyOffers(itemId, self.data["id"])
        stream.uint32(len(buyOffers))
        for entry in buyOffers:
            stream.uint32(entry.expire)
            stream.uint16(entry.counter)
            stream.uint16(entry.amount)
            stream.uint32(entry.price)
            stream.string(entry.playerName)

        saleOffers = self.market.getSaleOffers(itemId, self.data["id"])

        stream.uint32(len(saleOffers))
        for entry in saleOffers:
            stream.uint32(entry.expire)
            stream.uint16(entry.counter)
            stream.uint16(entry.amount)
            stream.uint32(entry.price)
            stream.string(entry.playerName)

        stream.send(self.client)

        self.marketDetails(itemId)

    def marketDetails(self, itemId):
        # Lazy.
        item = Item(itemId)

        with self.packet(0xF8) as stream:
            stream.uint16(item.cid)
            stream.string(str(item.armor or ""))
            stream.string(str(item.attack or ""))
            stream.string(str(item.containerSize or ""))
            stream.string(str(item.defence or ""))
            desc = ""
            if "description" in game.item.items[itemId]:
                desc =  game.item.items[itemId]["description"]

            stream.string(desc)
            stream.string(str(item.duration or ""))
            stream.string("") # XXX: Absorbe Abilities.
            stream.string("") # XXX: Min required level.
            stream.string("") # XXX: Min required magic level.
            stream.string("") # XXX: Vocation
            stream.string(str(item.runeSpellName or ""))
            stream.string("") # XXX: Bonus.
            stream.string(str(item.charges or ""))
            stream.string(item.weaponType or "")
            stream.string(str(item.weight or ""))

            if itemId in self.market.buyStatistics:
                stream.uint8(1)
                stream.uint32(self.market.buyStatistics[itemId][0])
                stream.uint32(self.market.buyStatistics[itemId][1] / self.market.buyStatistics[itemId][0])
                stream.uint32(self.market.buyStatistics[itemId][3])
                stream.uint32(self.market.buyStatistics[itemId][2])
            else:
                stream.uint8(0)

            if itemId in self.market.saleStatistics:
                stream.uint8(1)
                stream.uint32(self.market.saleStatistics[itemId][0])
                stream.uint32(self.market.saleStatistics[itemId][1] / self.market.saleStatistics[itemId][0])
                stream.uint32(self.market.saleStatistics[itemId][3])
                stream.uint32(self.market.saleStatistics[itemId][2])
            else:
                stream.uint8(0)

    def createMarketOffer(self, type, itemId, amount, price, anonymous=0):
        fee = max(20, min(1000, (amount*price) / 100))

        if type == 1 and (not itemId in self.depotMarketCache[self.marketDepotId] or amount > self.depotMarketCache[self.marketDepotId][itemId] or self.getBalance() < fee):
            return self.notPossible()
        elif type == 0 and self.getBalance() < (amount*price)+fee:
            print("XXX: Can't afford it.")
            return self.notPossible()


        offer = game.market.Offer(self.data["id"], itemId, price, int(time.time() + config.marketOfferExpire), amount, type=MARKET_OFFER_BUY if type == 0 else MARKET_OFFER_SALE)
        if anonymous:
            offer.playerName = "Anonymous"
        else:
            offer.playerName = self.name()

        if type == 0:
            self.market.addBuyOffer(offer)
        else:
            self.market.addSaleOffer(offer)

        offer.save()
        if type == 1:
            self.removeFromDepot(self.marketDepotId, itemId, amount)
            self.depotMarketCache[self.marketDepotId] = self.getDepotMarketCache(self.marketDepotId)
        elif type == 0:
            self.modifyBalance(-(amount * price))

        # Fees.
        self.modifyBalance(-fee)

        if self.marketOpen:
            self.marketOffers(itemId)
            self.openMarket(self.market.id)

    def marketOwnOffers(self):
        with self.packet(0xF9) as stream:
            stream.uint16(0xFFFE)

            buyOffers = self.market.buyOffers(self)
            saleOffers = self.market.saleOffers(self)

            stream.uint32(len(buyOffers))
            for entry in buyOffers:
                stream.uint32(entry.expire)
                stream.uint16(entry.counter)
                stream.uint16(cid(entry.itemId))
                stream.uint16(entry.amount)
                stream.uint32(entry.price)

            stream.uint32(len(saleOffers))
            for entry in saleOffers:
                stream.uint32(entry.expire)
                stream.uint16(entry.counter)
                stream.uint16(cid(entry.itemId))
                stream.uint16(entry.amount)
                stream.uint32(entry.price)

    @gen.coroutine
    def marketHistory(self):
        counter = 0
        buyHistory = yield sql.runQuery("SELECT h.`time`, o.`item_id`, h.`amount`, o.`price` FROM `market_history` h, `market_offers` o WHERE h.`offer_id` = o.`id` AND h.`player_id` = %s AND o.`market_id` = %s", self.data["id"], self.market.id)
        saleHistory = yield sql.runQuery("SELECT h.`time`, o.`item_id`, h.`amount`, o.`price` FROM `market_history` h, `market_offers` o WHERE h.`offer_id` = o.`id` AND o.`player_id` = %s AND o.`market_id` = %s", self.data["id"], self.market.id)
        with self.packet(0xF9) as stream:
            stream.uint16(0xFFFF)

            stream.uint32(len(buyHistory))
            for entry in buyHistory:
                stream.uint32(entry["time"])
                stream.uint16(counter) # Relevant to something?
                stream.uint16(cid(entry["item_id"]))
                stream.uint16(entry["amount"])
                stream.uint32(entry["price"])
                stream.uint8(1) # XXX?
                counter = (counter + 1) & 0xFFFF
            counter = 0
            stream.uint32(len(saleHistory))
            for entry in saleHistory:
                stream.uint32(entry["time"])
                stream.uint16(counter) # Relevant to something?
                stream.uint16(cid(entry["item_id"]))
                stream.uint16(entry["amount"])
                stream.uint32(entry["price"])
                stream.uint8(1) # XXX?
                counter = (counter + 1) & 0xFFFF

    def setLanguage(self, lang):
        if lang != 'en_EN':
            C = "%s\x04%s"
            try:
                self.l = game.language.LANGUAGES[lang].gettext
                self.lp = game.language.LANGUAGES[lang].ngettext
                self.lc = lambda context, message: self.l(C % (context, message))
                self.lcp = lambda context, message: self.lcp(C % (context, singular), C % (context, plural), n)
            except:
                print("WARNING: Language %s not loaded, falling back to defaults" % lang)
        else:
            self.l = lambda message: message
            self.lp = lambda s,p,n: s if n != 1 else p
            self.lc = lambda c, m: m
            self.lcp = lambda c, s, p, n: s if n != 1 else p

        self.data["language"] = lang

    ###### Group stuff
    def getGroupFlags(self, default={}):
        try:
            return game.functions.groups[self.data["group_id"]][1]
        except:
            print("Warning: GroupID %d doesnt exist!" % self.data["group_id"])
            return default

    def hasGroupFlag(self, flag):
        try:
            return flag in game.functions.groups[self.data["group_id"]][1]
        except:
            print("Warning: GroupID %d doesnt exist!" % self.data["group_id"])
            return False

    def hasGroupFlags(self, *flags):
        g = self.getGroupFlags()

        for flag in flags:
            if not flag in g:
                return False

        return True

    # "Premium" stuff
    def togglePremium(self):
        self.sendPremium = not self.sendPremium
        with self.packet() as stream:
            stream.playerInfo(self)

    def delayWalk(self, delay):
        with self.packet() as stream:
            stream.delayWalk(delay)

    # Skull stuff
    def getSkull(self, creature=None):
        if creature and creature.isPlayer():
            # Green skull to members of the same party.
            myParty = self.party()
            if myParty and creature.party() == myParty:
                return SKULL_GREEN

            elif creature in self.trackSkulls:
                if self.trackSkulls[creature][1] >= time.time():
                    return self.trackSkulls[creature][0]
                del self.trackSkulls[creature]

            skull = deathlist.getSkull(self.data["id"], creature.data["id"])

            if skull[0]:
                self.trackSkulls[creature] = skull
                return skull[0]

        if self.skull == 0:
            self.skull, self.skullTimeout = deathlist.getSkull(self.data["id"])

            if self.skullTimeout and not self._checkSkulls:
                self._checkSkulls = call_later(self.skullTimeout - time.time(), self.verifySkulls)

        return self.skull

    # Shield
    def setShield(self, shield):
        raise Exception("NOT AVAILABLE ON PLAYERS.")

    def getShield(self, creature):
        myParty = self.party()
        reqParty = creature.party()

        if myParty:
            return myParty.getShield(self, creature)
        elif reqParty:
            return reqParty.getShield(self, creature)
        else:
            return SHIELD_NONE

    # Balance stuff
    def getBalance(self):
        return self.data["balance"]

    def setBalance(self, balance):
        self.data["balance"] = balance

    def modifyBalance(self, modBalance):
        self.data["balance"] += modBalance

    def media(self):
        if not config.enableExtensionProtocol:
            raise Exception("ExtensionPorotocol is not enabled")

        ip = self.getIP()
        if ip in MEDIA_IPS:
            return MEDIA_IPS[ip]
        else:
            return None

    # Extended opcode
    def getOSType(self):
        return self.client.OSType

    def sendExtendedOpcode(self, opcode, buffer):
        if self.client and self.getOSType() >= 0x0A:
            stream = self.packet(0x32)
            stream.uint8(opcode)
            stream.string(str(buffer))
            stream.send(self.client)

        # Else, just ignore.
