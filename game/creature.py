
from game.map import placeCreature, removeCreature, getTile
import game.const
import config
import time
import copy
import game.scriptsystem
import game.functions
import inspect
import game.errors
import math
import collections

# Build class.
from game.creature_talking import CreatureTalking
from game.creature_movement import CreatureMovement
from game.creature_attacks import CreatureAttacks

# Unique ids.
def __uid():
    idsTaken = 1
    while True:
        idsTaken += 1
        yield idsTaken

uniqueId = __uid().__next__

allCreatures = {}
allCreaturesObject = allCreatures.values()

class Creature(CreatureTalking, CreatureMovement, CreatureAttacks):
    itemId = 99
    def __init__(self, data, position, cid=None):
        self.data = data
        self.creatureType = 0
        self.direction = SOUTH
        self.position = position
        self.speed = 100.0
        self.scripts = { "onNextStep":[]}
        self.cid = cid if cid else self.generateClientID()
        self.outfit = [self.data["looktype"], self.data["lookhead"], self.data["lookbody"], self.data["looklegs"], self.data["lookfeet"]]
        self.mount = 0
        self.mounted = 0
        self.addon = self.data["lookaddons"]
        self.action = None
        self.lastAction = 0
        self.lastStep = 0
        self.target = None # target for follow/attacks
        self.targetMode = 0 # 0 = no particular reason, 1 = attack, 2 = follow
        self.vars = {}
        self.cooldowns = {} # This is a int32, icon are the first 8, then group is the next 7
        self.regenerate = None
        self.alive = True
        self.lastDamagers = deque(maxlen=config.trackHits)
        self.lastSupporters = deque(maxlen=config.trackHits)
        self.solid = not config.creatureWalkthrough
        self.emblem = 0
        self.shield = 0
        self.skull = 0
        self.knownBy = set()
        self.conditions = {}
        self.walkPattern = None
        self.activeSummons = []
        self.doHideHealth = False
        self.lastPassedDamage = 0
        
        # Skulls
        self.trackSkulls = {}
        self._checkSkulls = None

        # Light stuff
        self.lightLevel = 0
        self.lightColor = 0
        
        # Options
        self.canMove = True
        self.attackable = True

        # We are trackable
        allCreatures[self.cid] = self

        # Speaktypes
        self.defaultSpeakType = MSG_SPEAK_SAY
        self.defaultYellType = MSG_SPEAK_YELL
        
        # Combat
        self.ignoreBlock = False
        self.doBlock = True
        
        # Messages
        self.raiseMessages = False

        # Spells.
        self.spellTargets = [] # A temp value. Used by spells.

    def actionLock(self, *argc, **kwargs):
        _time = time.time()
        if self.lastAction > _time:
            if "stopIfLock" in kwargs and kwargs["stopIfLock"]:
                return False
            else:
                call_later(self.lastAction - _time, *argc, **kwargs)
            return False
        else:
            self.lastAction = _time
            return True
            
    def __repr__(self):
        return "<Creature (%s, %d, %s) at %s>" % (self.data["name"], self.clientId(), self.position, hex(id(self)))

    @staticmethod
    def actionDecor(f):
        """ Decorator used by external actions """
        def new_f(creature, *argc, **kwargs):
            if not creature.alive or not creature.actionLock(new_f, creature, *argc, **kwargs):
                return
            else:
                _time = time.time()
                creature.lastAction = _time
                f(creature, *argc, **kwargs)

        return new_f

    def register(self, event, func, **kwargs):
        game.scriptsystem.register(event, self, func, **kwargs)

    def registerAll(self, event, func, **kwargs):
        game.scriptsystem.register(event, self.thingId(), func, **kwargs)

    @staticmethod
    def isPlayer():
        return False

    @staticmethod
    def isNPC():
        return False

    @staticmethod
    def isMonster():
        return False

    @staticmethod
    def isItem():
        return False

    @staticmethod
    def isCreature():
        return True

    def isPushable(self, by):
        return False

    def isAttackable(self, by):
        if self.position.getTile().getFlags() & TILEFLAGS_PROTECTIONZONE:
            return False
        return self.attackable

    def isSummon(self):
        return False

    def isSummonFor(self, creature):
        return False

    def name(self):
        return self.data["name"]

    def description(self):
        return "You see a creature."

    def clientId(self):
        return self.cid

    def thingId(self):
        return self.creatureType # Used to indentify my "thing"

    def actionIds(self):
        """ Pure creature identifier, mostly overridden. """
        return ('creature',) # Static actionID

    def generateClientID(self):
        raise NotImplementedError("This function must be overrided by a secondary level class!")

    def notPossible(self):
        # Needs to be overrided in player
        # Here we can inform a script if a illigal event
        if self.raiseMessages:
            raise MsgNotPossible
        return

    def refreshStatus(self, streamX=None): pass
    def refreshSkills(self, streamX=None): pass
    def refreshConditions(self, streamX=None): pass

    def refresh(self):
        stackpos = game.map.getTile(self.position).findStackpos(self)
        for player in self.knownBy:
            stream = player.packet()
            stream.removeTileItem(self.position, stackpos)
            stream.addTileCreature(self.position, stackpos, self, player, True)

            stream.send(player.client)

    def despawn(self):
        self.alive = False
        try:
            tile = game.map.getTile(self.position)
            stackpos = tile.findStackpos(self)
            tile.removeCreature(self)

            for spectator in getSpectators(self.position):
                stream = spectator.packet()
                stream.removeTileItem(self.position, stackpos)
                stream.send(spectator)
        except:
            pass
        try:
            if self.respawn:
                if self.spawnTime:
                    call_later(self.spawnTime, self.base.spawn, self.spawnPosition)
                elif self.spawnTime == 0:
                    return

                else:
                    call_later(self.base.spawnTime, self.base.spawn, self.spawnPosition)
        except:
            pass

    def magicEffect(self, type, pos=None):
        if not type: return

        if not pos or pos[0] == 0xFFFF:
            pos = self.position
        for spectator in getSpectators(pos):
            stream = spectator.packet()
            stream.magicEffect(pos, type)
            stream.send(spectator)

    def shoot(self, fromPos, toPos, type):
        if not type: return

        if fromPos == toPos:
            self.magicEffect(type, fromPos)
        else:
            for spectator in getSpectators(fromPos) | getSpectators(toPos):
                stream = spectator.packet()
                stream.shoot(fromPos, toPos, type)
                stream.send(spectator)

    def refreshOutfit(self):
        for spectator in getSpectators(self.position):
            stream = spectator.packet(0x8E)
            stream.uint32(self.clientId())
            stream.outfit(self.outfit, self.addon, self.mount if self.mounted else 0x00)
            stream.send(spectator)

    def changeMountStatus(self, mounted):
        if self.mounted == mounted:
            return

        mount = game.resource.getMount(self.mount)
        if mount:
            self.mounted = mounted

            if mount.speed:
                self.setSpeed((self.speed + mount.speed) if mounted else (self.speed - mount.speed))
            self.refreshOutfit()

    def setOutfit(self, looktype, lookhead=0, lookbody=0, looklegs=0, lookfeet=0, addon=0):
        self.outfit = [looktype, lookhead, lookbody, looklegs, lookfeet]
        self.addon = addon
        self.refreshOutfit()

    def setSpeed(self, speed):
        if speed != self.speed:
            if speed > 1500:
                speed = 1500.0
            self.speed = float(speed)
            for spectator in getSpectators(self.position):
                stream = spectator.packet(0x8F)
                stream.uint32(self.clientId())
                stream.speed(int(self.speed))
                stream.send(spectator)

    def onDeath(self):
        #del allCreatures[self.clientId()]
        pass # To be overrided in monster and player

    def remove(self, entriesToo=True):
        """ Remove this creature from the map, stop the brain and so on """

        # All remove creatures are dead. No matter if they actually are alive.
        self.alive = False

        tile = self.position.getTile()
        try:
            tile.removeCreature(self)
        except:
            pass

        if self.isPlayer():
            ignore = (self,)
        else:
            ignore = ()

        for spectator in getSpectators(self.position, ignore=ignore):
            stream = spectator.packet(0x69)
            stream.position(self.position)
            stream.tileDescription(tile, spectator.player)
            stream.uint8(0x00)
            stream.uint8(0xFF)
            stream.send(spectator)

        # Don't call this on a player
        if entriesToo:
            if self.isPlayer():
                raise Exception("Creature.remove(True) (entriesToo = True) has been called on a player. This is (unfortunatly), not supported (yet?)")

            try:
                del allCreatures[self.clientId()]
            except:
                pass

    def rename(self, name):
        self.data["name"] = name

        self.refresh()

    def privRename(self, player, name):
        if player in self.knownBy:
            stackpos = game.map.getTile(self.position).findStackpos(self)
            stream = player.packet()
            stream.removeTileItem(self.position, stackpos)
            originalName = self.data["name"]

            self.data["name"] = name
            stream.addTileCreature(self.position, stackpos, self, player, True)
            self.data["name"] = originalName
            stream.send(player.client)

    def onSpawn(self):
        pass # To be overrided

    def setHealth(self, health):
        if self.data["health"] == 0 and health:
            self.alive = True

        self.data["health"] = int(max(0, health))

        if not self.getHideHealth():
            for spectator in getSpectators(self.position):
                stream = spectator.packet(0x8C)
                stream.uint32(self.clientId())
                stream.uint8(int(self.data["health"] * 100 / self.data["healthmax"]))
                stream.send(spectator)

        self.refreshStatus()

        if self.data["health"] == 0:
            self.alive = False
            self.onDeath()
            return False

        return True


    def modifyHealth(self, health, spawn=False):
        return self.setHealth(min(self.data["health"] + health, self.data["healthmax"]))

    def stopAction(self):
        ret = False
        try:
            self.action.cancel()
            ret = True
        except:
            pass
        self.action = None
        return ret

    def cancelWalk(self, d=None):
        return # Is only executed on players

    def canSee(self, position, radius=(8,6)):
        # We are on ground level and we can't see underground
        # We're on a diffrent instanceLevel
        # Or We are undergorund and we may only see 2 floors
        if position.x == 0xFFFF:
            return True # Assume True
        if (self.position.instanceId != position.instanceId) or (self.position.z <= 7 and position.z > 7) or (self.position.z >= 8 and abs(self.position.z-position.z) > 2):
            return False

        offsetz = self.position.z-position.z
        return position.x >= (self.position.x - radius[0] + offsetz) and position.x <= (self.position.x + radius[0] + offsetz + 1) and position.y >= (self.position.y - radius[1] + offsetz) and position.y <= (self.position.y + radius[1] + offsetz + 1)
    
    def canTarget(self, position, radius=(8,6), allowGroundChange=False):
        if self.position.instanceId != position.instanceId:
            return False

        if not allowGroundChange and self.position.z != position.z: # We are on ground level and we can't see underground
            return False

        # Can't target protected zone
        if position.getTile().getFlags() & TILEFLAGS_PROTECTIONZONE:
            return False

        return (position.x >= self.position.x - radius[0]) and (position.x <= self.position.x + radius[0]) and (position.y >= self.position.y - radius[1]) and (position.y <= self.position.y + radius[1])

    def distanceStepsTo(self, position):
        xSteps = abs(self.position.x-position.x)
        ySteps = abs(self.position.y-position.y)
        # Case one, diagonal right next to = 1. Fix diagonal attacks
        if xSteps == 1 and ySteps == 1:
            return 1
        
        return xSteps+ySteps

    def inRange(self, position, x, y, z=0):
        if position.x == 0xFFFF:
            return True
        return ( position.instanceId == self.position.instanceId and abs(self.position.x-position.x) <= x and abs(self.position.y-position.y) <= y and abs(self.position.z-position.z) <= z )

    def positionInDirection(self, direction):
        position = self.position.copy()
        if direction == 0:
            position.y -= 1
        elif direction == 1:
            position.x += 1
        elif direction == 2:
            position.y += 1
        elif direction == 3:
            position.x -= 1
        elif direction == 4:
            position.y += 1
            position.x -= 1
        elif direction == 5:
            position.y += 1
            position.x += 1
        elif direction == 6:
            position.y -= 1
            position.x -= 1
        elif direction == 7:
            position.y -= 1
            position.x += 1
        return position

    # Personal vars
    def setVar(self, name, value=None):
        try:
            if value == None:
                del self.vars[inspect.stack()[0][1] + name]
            else:
                self.vars[inspect.stack()[0][1] + name] = value
        except:
            return None

    def getVar(self, name):
        try:
            return self.vars[inspect.stack()[0][1] + name]
        except:
            return None

    # Global storage
    def setGlobal(self, field, value):
        try:
            game.functions.globalStorage['storage'][field] = value
            game.functions.saveGlobalStorage = True
        except:
            return False

    def getGlobal(self, field, default=None):
        try:
            return game.functions.globalStorage['storage'][field]
        except:
            return default

    def removeGlobal(self, field):
        try:
            del game.functions.globalStorage['storage'][field]
            game.functions.saveGlobalStorage = True
        except:
            pass

    # Global object storage
    def setGlobalObject(self, field, value):
        try:
            game.functions.globalStorage['objectStorage'][field] = value
            game.functions.saveGlobalStorage = True
        except:
            return False

    def getGlobalObject(self, field, default=None):
        try:
            return game.functions.globalStorage['objectStorage'][field]
        except:
            return default

    def removeGlobalObject(self, field):
        try:
            del game.functions.globalStorage['objectStorage'][field]
            game.functions.saveGlobalStorage = True
        except:
            pass

    def __followCallback(self, who):
        if self.target == who:
            self.walk_to(self.target.position, -1, True)
            self.target.scripts["onNextStep"].append(self.__followCallback)

    def follow(self, target):
        """if self.targetMode == 2 and self.target == target:
            self.targetMode = 0
            self.target = None
            return"""

        self.target = target
        self.targetMode = 2
        self.walk_to(self.target.position, -1, True)
        self.target.scripts["onNextStep"].append(self.__followCallback)

    def cancelTarget(self):
        self.target = None
        self.targetMode = 0
        
    # Change passability
    def setSolid(self, solid):
        if self.solid == solid:
            return

        self.solid = solid

        for client in getSpectators(self.position):
            stream = client.packet(0x92)
            stream.uint32(self.cid)
            stream.uint8(self.solid)
            stream.send(client)

    def setSolidFor(self, player, solid):
        stream = player.packet(0x92)
        stream.uint32(self.cid)
        stream.uint8(solid)
        stream.send(player.client)

    # Shields
    def setPartyShield(self, shield):
        if self.shield == shield:
            return

        self.shield = shield

        for player in getPlayers(self.position):
            stream = player.packet(0x90)
            stream.uint32(self.cid)
            stream.uint8(self.getPartShield(player))
            stream.send(player.client)

    def getPartyShield(self, creature):
        return self.shield # TODO

    # Emblem
    def setEmblem(self, emblem):
        if self.emblem == emblem:
            return

        self.emblem = emblem

        for player in getPlayers(self.position):
            stream = player.packet()
            stream.addTileCreature(self.position, game.map.getTile(self.position).findStackpos(self), self, player)
            stream.send(player.client)

    def getEmblem(self, craeture):
        return self.emblem
    
    # Skulls
    def verifySkulls(self):
        _time = time.time()
        if config.resetSkulls:
            """# TODO, something for red and black too.
            if self.getSkull() == SKULL_WHITE and self.lastDmgPlayer < _time - config.whiteSkull:
                print "nullify"
                self.setSkull(SKULL_NONE)"""
                
        if _time > self.skullTimeout:
            self.setSkull(SKULL_NONE)
            
        for creature in self.trackSkulls.copy():
            if self.trackSkulls[creature][1] < _time:
                stream = creature.packet()
                stream.skull(self.cid, self.skull)
                stream.send(creature.client)
                del self.trackSkulls[creature]
                
            elif self.trackSkulls[creature][0] == SKULL_GREEN: # We have to resend SKULL_GREEN every ~5sec.
                stream = creature.packet()
                stream.skull(self.cid, SKULL_GREEN)
                stream.send(creature.client)
                
        if self.trackSkulls:
            self._checkSkulls = call_later(5, self.verifySkulls)
        elif self.skull:
            self._checkSkulls = call_later(self.skullTimeout - _time, self.verifySkulls)
        else:
            self._checkSkulls = None
            
    def setSkull(self, skull, creature=None, _time=0):
        if self.getSkull(creature) == skull:
            return

        if not creature:
            assert skull in (SKULL_NONE, SKULL_RED, SKULL_BLACK, SKULL_WHITE)
            self.skull = skull
            if skull == SKULL_WHITE:
                if _time:
                    self.skullTimeout = time.time() + _time
                else:
                    self.skullTimeout = time.time() + config.whiteSkull
            elif skull == SKULL_RED:
                self.skullTimeout = time.time() + config.redSkull
            elif skull == SKULL_BLACK:
                self.skullTimeout = time.time() + config.blackSkull
            else:
                self.skullTimeout = 0
                
            for player in getPlayers(self.position):
                stream = player.packet()
                stream.skull(self.cid, self.getSkull(player))
                stream.send(player.client)
                
        else:
            if creature in self.trackSkulls and self.trackSkulls[creature][0] == skull:
                self.trackSkulls[creature][1] = time.time() + _time
            else:
                self.trackSkulls[creature] = [skull, time.time() + _time]
            
            stream = creature.packet()
            stream.skull(self.cid, skull)
            stream.send(creature.client)
            
        if not self._checkSkulls:
            self._checkSkulls = call_later(0, self.verifySkulls)
            
    def getSkull(self, creature=None):
        return self.skull # TODO

    def square(self, creature, color=27):
        pass

    # Conditions
    def condition(self, condition, stackbehavior=game.const.CONDITION_LATER, maxLength=0):
        try:
            oldCondition = self.conditions[condition.type]
            if not oldCondition.length:
                raise

            if stackbehavior == CONDITION_IGNORE:
                return False
            elif stackbehavior == CONDITION_LATER:
                return call_later(oldCondition.length * oldCondition.every, self.condition, condition, stackbehavior)
            elif stackbehavior == CONDITION_ADD:
                if maxLength:
                    oldCondition.length = min(condition.length + oldCondition.length, maxLength)
                else:
                    oldCondition.length += condition.length

            elif stackbehavior == CONDITION_MODIFY:
                if maxLength:
                    condition.length = min(condition.length + oldCondition.length, maxLength)
                else:
                    condition.length += oldCondition.length

                self.conditions[condition.type] = condition
            elif stackbehavior == CONDITION_REPLACE:
                oldCondition.stop()
                condition.start(self)
                self.conditions[condition.type] = condition

        except:
            condition.start(self)
            self.conditions[condition.type] = condition


        self.refreshConditions()

    def multiCondition(self, *argc, **kwargs):
        try:
            stackbehavior = kwargs["stackbehavior"]
        except:
            stackbehavior = CONDITION_LATER

        currCon = argc[0]
        for con in argc[1:]:
            currCon.callback = lambda: self.condition(con, stackbehavior)
            currCon = con

        self.condition(argc[0], stackbehavior)

    def hasCondition(self, conditionType, subtype=""):
        if subtype and isinstance(conditionType, str):
            conditionType = "%s_%s" % (conditionType, subtype)
        try:
            if self.conditions[conditionType].length > 0:
                return True
            else:
                self.loseCondition(conditionType)
        except:
            pass
        return False

    def getCondition(self, conditionType, subtype=""):
        if subtype and isinstance(conditionType, str):
            conditionType = "%s_%s" % (conditionType, subtype)
        try:
            return self.conditions[conditionType]
        except:
            return False

    def loseCondition(self, conditionType, subtype=""):
        if subtype and isinstance(conditionType, str):
            conditionType = "%s_%s" % (conditionType, subtype)
        try:
            self.condions[conditionType].stop()
            return True
        except:
            return False

    def loseAllConditions(self):
        if not self.conditions:
            return False

        for condition in self.conditions.copy():
            self.conditions[condition].stop()

        return True

    ##############
    ### Spells ###
    ##############
    def castSpell(self, spell, strength=None, target=None):
        game.spell.spells[spell][0](self, strength, target)

    #############
    ### House ###
    #############
    def kickFromHouse(self):
        tile = game.map.getTile(self.position)
        try:
            # Find door pos
            doorPos = game.map.houseDoors[tile.houseId]



            # Try north
            found = True
            doorPos[1] -= 1
            testTile = game.map.getTile(doorPos)
            for i in testTile.getItems():
                if i.solid:
                    found = False
                    break

            if found:
                self.teleport(doorPos, True)
                return True

            # Try south
            found = True
            doorPos[1] += 2 # Two to counter north change
            testTile = game.map.getTile(doorPos)
            for i in testTile.getItems():
                if i.solid:
                    found = False
                    break

            if found:
                self.teleport(doorPos, True)
                return True

            # Try east
            found = True
            doorPos[1] -= 1 # counter south change
            doorPos[0] -= 1
            testTile = game.map.getTile(doorPos)
            for i in testTile.getItems():
                if i.solid:
                    found = False
                    break

            if found:
                self.teleport(doorPos, True)
                return True

            # Try west
            found = True
            doorPos[0] += 2 # counter east change
            testTile = game.map.getTile(doorPos)
            for i in testTile.getItems():
                if i.solid:
                    found = False
                    break

            if found:
                self.teleport(doorPos, True)
                return True

            print("Wtf?")
            return False # Not found

        except:
            return False # Not in a house

    #####################
    ### Compatibility ###
    #####################
    def cooldownSpell(self, icon, group, cooldown, groupCooldown=None):
        if groupCooldown == None: groupCooldown = cooldown
        t = time.time()  + cooldown
        self.cooldowns[icon] = t
        self.cooldowns[group << 8] = t

    def cooldownIcon(self, icon, cooldown):
        self.cooldowns[icon] = time.time() + cooldown

    def cooldownGroup(self, group, cooldown):
        self.cooldowns[group << 8] = time.time() + cooldown

    def party(self):
        " Returns a dummy party for creatures (aga None). "
        return None

    ################
    ### Instance ###
    ################

    def setInstance(self, instanceId=None):
        # Teleport to the same position within instance
        newPosition = self.position.copy()
        newPosition.instanceId = instanceId
        self.teleport(newPosition)

    ###################
    ### Walkability ###
    ###################
    def walkable(self, state=True):
        self.canWalk = state

    def toggleWalkable(self):
        self.canWalk = not self.canWalk

    ####################
    ### Internal Use ###
    ####################
    def use(self, thing, index=None):
        return game.scriptsystem.get('use').run(thing=thing, creature=self, position=thing.position, index=index)

    #####################
    ### Hidden health ###
    #####################
    def hideHealth(self, do = True):
        self.doHideHealth = do

    def getHideHealth(self):
        return self.doHideHealth

    def toggleHideHealth(self):
        self.doHideHealth = not self.doHideHealth

    ######## Language placeholders #########
    def l(self, message):
        return message
    
    def lp(self, singular, plural, n):
        return singular if n != 1 else plural
        
    def lc(self, context, message):
        return message
        
    def lcp(self, context, singular, plural, n):
        return singular if n != 1 else plural
        
    ###################
    ### Light stuff ###
    ###################
    def setLight(self, level=0, color=0):
        self.lightColor = color
        self.lightLevel = level
        
        self.refreshLight()
        
    def refreshLight(self):
        for spectator in getSpectators(self.position):
            with spectator.packet() as stream:
                stream.creaturelight(self.cid, self.lightLevel, self.lightColor)
                
    ###################
    ### Summon & convince stuff
    ###################
    
    def summon(self, monsterName, position):
        if self.getSkull() == SKULL_BLACK and config.blackSkullDisableSummons:
            return None
            
        mon = game.monster.getMonster(monsterName).spawn(position, spawnDelay=0)
        mon.setMaster(self)
        mon.setRespawn(False)
        self.activeSummons.append(mon)    
        return mon
        
    def toggleRaiseMessages(self):
        self.raiseMessages = not self.raiseMessages
        
    ###################
    ### Party sheilds
    ###################
    def setShield(self, shield):
        if self.shield == shield:
            return

        self.shield = shield
        
        for player in getPlayers(self.position):
            with player.packet() as stream:
                stream.shield(self.cid, shield)

    def getShield(self, craeture):
        return self.shield
