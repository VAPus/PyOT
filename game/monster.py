from .creature import Creature, uniqueId, allCreatures
from . import map, scriptsystem
from .packet import TibiaPacket
import copy, random, time
import game.const
from . import errors
from . import item
import config
import game.errors
from tornado import gen
monsters = {}
brainFeatures = {}

def chance(procent):
    if procent == 100: return (lambda creature: True)
    elif procent == 0: return (lambda creature: False)

    def gen(creature):
        if random.randint(0, 99) < procent:
            return True
        else:
            return False
    return gen

class Monster(Creature):
    @staticmethod
    def generateClientID():
        return 0x40000000 + uniqueId()

    @staticmethod
    def isMonster():
        return True

    def __init__(self, base, position, cid=None):
        Creature.__init__(self, base.data.copy(), position, cid)
        self.base = base
        self.creatureType = 1
        self.spawnPosition = position.copy()
        self.lastStep = 0
        self.speed = float(base._speed)
        self.lastMelee = 0
        self.lastDistance = 0
        self.walkPer = base._walkPer
        self.brainEvent = None
        self.spawnTime = None
        self.radius = 5
        self.master = None
        self.respawn = True
        self.skull = base._skull # We make a copy of the int so we might set a skull in scripts later.
        self.canWalk = base._walkable
        self.intervals = {}
        self.defaultSpeakType = MSG_SPEAK_MONSTER_SAY
        self.defaultYellType = MSG_SPEAK_MONSTER_YELL
        self.lastRetarget = 0

    def actionIds(self):
        """ Monster, creature and monster name, action bindable ids """
        return ('creature', 'monster', self.data["name"]) # Static actionIDs

    def setMaster(self, creature):
        self.master = creature
        self.respawn = False

        # Reset target.
        self.target = None
        self.targetMode = 0

    def setRespawn(self, state):
        self.respawn = state

    def isSummon(self):
        if self.master:
            return True
        else:
            return False

    def isSummonFor(self, creature):
        return self.master == creature

    def __repr__(self):
        return "<Monster (%s, %d, %s) at %s>" % (self.data["name"], self.clientId(), self.position, hex(id(self)))

    def damageToBlock(self, dmg, type):
        if type == MELEE:
            return dmg - self.base._armor
        elif type == PHYSICAL:
            return dmg * self.base._physical
        elif type == FIRE:
            return dmg * self.base._fire
        elif type == EARTH:
            return dmg * self.base._earth
        elif type == ENERGY:
            return dmg * self.base._energy
        elif type == ICE:
            return dmg * self.base._ice
        elif type == HOLY:
            return dmg * self.base._holy
        elif type == DEATH:
            return dmg * self.base._death
        elif type == DROWN:
            return dmg * self.base._drown
        elif type == LIFEDRAIN:
            return dmg * self.base._lifedrain
        elif type == MANADRAIN:
            return dmg * self.base._manadrain

        # What, no match?
        return dmg

    def defaultSpeed(self):
        self.speed = float(self.base._speed)

    def turnOffBrain(self):
        try:
            self.brainEvent.cancel()
        except:
            pass

        self.brainEvent = None
    def onDeath(self):
        # Remove master summons
        isSummon = self.isSummon()

        if self.master:
            self.master.activeSummons.remove(self)

        self.turnOffBrain()

        # Remove summons
        if self.activeSummons:
            for summon in self.activeSummons:
                summon.magicEffect(EFFECT_POFF)
                summon.despawn()
                summon.turnOffBrain()

        # Lose all conditions.
        self.loseAllConditions()

        # Transform
        tile = map.getTile(self.position)
        lootMsg = []
        if self.base.data["corpse"]:
            corpse = game.item.Item(self.base.data["corpse"], actions=self.base._corpseAction)

            corpse.movable = False
            def _move_corpse():
                corpse.movable = True

            call_later(config.moveCorpseAfter, _move_corpse)

            # Set owner.
            if self.lastDamagers:
                if self.getLastDamager().isPlayer():
                    corpse.owners = [self.getLastDamager()]

                    def _clear_private_loot():
                        del corpse.owners

                    # Callback to remove owner after config.privateLootFor seconds
                    call_later(config.privateLootFor, _clear_private_loot)
            if not isSummon and not self.lastDamagers or self.getLastDamager() != self.master:
                try:
                    maxSize = game.item.items[self.base.data["corpse"]]["containerSize"]
                except:
                    # Monsters with loot MUST have a container with some size in it.
                    if self.base.lootTable:
                        print("[WARNING] Monster %s got a bad corpse" % self.name())
                    maxSize = 0
                drops = []
                if maxSize:
                    for loot in self.base.lootTable:
                        if config.lootDropRate*loot[1]*100 > random.randint(0, 10000): # [7363, 28.5, 4]
                            if len(drops)+1 == maxSize:
                                if config.stockLootInBagsIfNeeded:
                                    drops.insert(0, (config.stockLootBagId, None))
                                    maxSize += item.items[config.stockLootBagId]["containerSize"]
                                else:
                                    drops.append(loot)
                                break
                            else:
                                drops.append(loot)

                        elif len(loot) == 4:
                            drops.append((loot[0], None, loot[4]))

                ret = scriptsystem.get("loot").run(creature2=self, creature=(self.getLastDamager() if self.lastDamagers else None), loot=drops, maxSize=maxSize)
                if type(ret) == list:
                    drops = ret

                for loot in drops:
                    lenLoot = len(loot)
                    ret = 0
                    if lenLoot == 2:
                        ritem = game.item.Item(random.choice(loot[0]) if isinstance(loot[0], list) else loot[0], 1)
                        lootMsg.append(ritem.name)
                        ret = corpse.placeItemRecursive(ritem)

                    elif lenLoot == 3:
                        count = random.randint(1, loot[2]) * config.lootMaxRate
                        if count > 100:
                            while count:
                                depCount = min(count, 100)
                                ritem = game.item.Item(random.choice(loot[0]) if isinstance(loot[0], list) else loot[0], depCount)
                                lootMsg.append(ritem.name)
                                ret = corpse.placeItemRecursive(ritem)
                                count -= depCount
                        else:
                            ritem = game.item.Item(random.choice(loot[0]) if isinstance(loot[0], list) else loot[0], count)
                            lootMsg.append(ritem.name)
                            ret = corpse.placeItemRecursive(ritem)

                    elif lenLoot == 4:
                        count = random.randint(loot[4], loot[2]) * config.lootMaxRate
                        if count > 100:
                            while count:
                                depCount = min(count, 100)
                                ritem = game.item.Item(random.choice(loot[0]) if isinstance(loot[0], list) else loot[0], depCount)
                                lootMsg.append(ritem.name)
                                ret = corpse.placeItemRecursive(ritem)
                                count -= depCount

                        else:
                            ritem = game.item.Item(random.choice(loot[0]) if isinstance(loot[0], list) else loot[0], count)
                            lootMsg.append(ritem.name)
                            ret = corpse.placeItemRecursive(ritem)


                    if ret == None:
                        print("Warning: Monster '%s' extends all possible loot space" % self.data['name'])
                        break

        else:
            corpse = None

        scriptsystem.get("death").run(creature2=self, creature=(self.getLastDamager() if self.lastDamagers else None), corpse=corpse)
        if self.alive or self.data["health"] > 0:
            print("[May bug] Death events brought us back to life?")
            return

        # Remove both small and full splashes on the tile.
        for item in tile.getItems():
            if item.itemId in SMALLSPLASHES or item.itemId in FULLSPLASHES:
                tile.removeItem(item)

        # Add full splash
        splash = Item(FULLSPLASH)
        splash.fluidSource = self.base._blood

        if corpse:
            res = corpse.place(self.position) 
            assert res
        res = splash.place(self.position)
        assert res

        # Start decay
        if corpse:
            corpse.decay()
        splash.decay()

        # Remove me. This also refresh the tile.
        self.remove()

        if not isSummon and self.lastDamagers and self.getLastDamager().isPlayer() and self.getLastDamager() != self.master:
            if lootMsg:
                self.getLastDamager().message(_l(self.getLastDamager(), "loot of %(who)s: %(loot)s") % {"who": self.data["name"].lower(), "loot": ', '.join(lootMsg)}, MSG_LOOT)
            else:
                self.getLastDamager().message(_l(self.getLastDamager(), "loot of %s: nothing") % (self.data["name"]), MSG_LOOT)

            # Experience split.
            attackerParty = self.getLastDamager().party()
            if attackerParty and attackerParty.shareExperience and attackerParty.checkShareExperience():
                for member in attackerParty.members:
                    if member.data["stamina"] or config.noStaminaNoExp == False:
                        exp = (self.base._experience / len(attackerParty.members)) * config.partyExperienceFactor
                        member.modifyExperience(exp * member.getExperienceRate())

                        if exp >= member.data["level"]:
                            member.soulGain()
            else:
                if self.getLastDamager().data["stamina"] or config.noStaminaNoExp == False:
                    self.getLastDamager().modifyExperience(self.base._experience *self.getLastDamager().getExperienceRate())

                    if self.base._experience >= self.getLastDamager().data["level"]:
                        self.getLastDamager().soulGain()

        # Begin respawn
        if self.respawn:
            self.position = self.spawnPosition
            self.target = None
            self.targetMode = 0
            if self.spawnTime != 0:
                if self.spawnTime:
                    call_later(self.spawnTime, self.base.spawn, self.spawnPosition, spawnTime = self.spawnTime, spawnDelay=0, check=False)
                else:
                    return
            else:
                call_later(self.base.spawnTime, self.base.spawn, self.spawnPosition, spawnDelay=0, check=False)

    def description(self):
        return "You see %s" % self.base.data["description"]

    def isPushable(self, by):
        return self.base._pushable

    def isAttackable(self, by):
        return self.base._attackable

    def targetCheck(self, targets=None):
        _time = time.time()
        if self.lastRetarget > _time - 7:
            return
        self.lastRetarget = _time

        if not self.target:
            # Null walkpatterns.
            self.walkPattern = None

        _target = self.target
        if not targets:
            targets = getPlayers(self.position) # Get all creaturse in range
            if not targets:
                self.target = None
                self.targetMode = 0
                return

        target = None

        bestDist = 127
        for player in targets:
            # Can we target him, same floor
            if player.isAttackable(self) and self.canTarget(player.position):
                # Walk steps ignore targets 1 step from us.
                distance = self.distanceStepsTo(player.position)
                if distance == 1:
                    bestDist = 1
                    target = player
                    break

                path = calculateWalkPattern(self, self.position, player.position, -1, True)

                if not path: continue
                # Calc x+y distance, diagonal is honored too.
                dist = len(path)
                if dist < bestDist:
                    # If it's smaller then the previous value
                    bestDist = dist
                    target = player

        if _target == target:
            return # We already have this target
        elif target:
            ret = game.scriptsystem.get('target').run(creature2=self, creature=target, attack=True)

            if ret == False:
                return
            elif ret != None:
                self.target = ret
            else:
                self.target = target
            self.targetMode = 1
        else:
            self.walkPattern = None
            self.stopAction()
            self.target = None
            self.targetMode = 0
            return

        # When we reach our destination, can we target check
        def __walkComplete(x):
            if not x:
                # Walk not possible. Loose target
                self.target = None
                self.targetMode = 0
                return
            # Are we OK?
            if self.distanceStepsTo(self.target.position) <= self.base._targetDistance:
                self.turnAgainst(self.target.position)
            else:
                # Apperently not. Try walking again.
                if self.canTarget(self.target.position) and not self.walkPattern:
                    self.walk_to(self.target.position, -self.base._targetDistance, __walkComplete)

        # XXX: Bug?
        if isinstance(self.target, list):
            try:
                self.target = self.target.pop()
            except:
                self.target = None
                return False
        # Begin autowalking
        if bestDist > 1:
            self.walk_to(self.target.position, -self.base._targetDistance, __walkComplete)

        # If the target moves, we need to recalculate, if he moves out of sight it will be caught in next brainThink
        def __followCallback(who):
            if self.target == who:
                if self.canTarget(self.target.position):
                    self.walk_to(self.target.position, -self.base._targetDistance, __walkComplete)
                else:
                    self.target = None
                    self.targetMode = 0

                if self.target:
                    # We shall be called again later
                    self.target.scripts["onNextStep"].append(__followCallback)

        if self.target:
            self.target.scripts["onNextStep"].append(__followCallback)
        return True


    def verifyMove(self, tile):
        """ This function verify if the tile is walkable in a regular state (pathfinder etc)
            This function handle things like PZ.
        """

        # Protected zone?
        if tile.getFlags() & TILEFLAGS_PROTECTIONZONE:
            return False

        for thing in tile:
            if isinstance(thing, Item):
                field = thing.field
                if self.base._ignoreFire and field == 'fire':
                    continue
                elif self.base._ignorePoison and field == 'poison':
                    continue
                elif self.base._ignoreEnergy and field == 'energy':
                    continue
                elif field:
                    return False
                elif thing.blockpath:
                    return False
                elif thing.teleport:
                    return False

            elif isinstance(thing, Creature):
                ok = not thing.solid
                if not ok and self.base._pushCreatures and isinstance(thing, Monster) and thing.base._pushable:
                    return 30
                if not ok:
                    return False

        return True

class MonsterBase(object):
    def __init__(self, data, brain):
        self.data = data
        self.voiceslist = []
        self.brain = brain
        self.scripts = {"onFollow":[], "onTargetLost":[]}
        self.summons = []
        self.maxSummon = 1

        self.spawnTime = 60

        self._speed = 100
        self._experience = 0

        self._attackable = True

        self.behavior()
        self.immunity()
        self.walkAround()
        self.type()
        self.targetChance()
        self.defense()

        self.meleeAttacks = []
        self.distanceAttacks = []
        self.spellAttacks = []
        self.defenceSpells = []

        self._intervals = {}
        self.lootTable = []

        self._walkable = True
        self._walkPer = config.monsterWalkPer

        self.brainFeatures = "default"
        self._skull = 0

        self._corpseAction = []
        self.prepared = False
        self._loot = None


    def spawn(self, position, place=True, spawnTime=None, spawnDelay=0.1, radius=5, radiusTo=None, monster=None, check=False):
        if spawnDelay:
            return call_later(spawnDelay, self.spawn, position, place, spawnTime, 0, radius, radiusTo, monster, check)
        else:
            if place:
                tile = position.getTile()
                if not tile:
                    print("Spawning of creature('%s') on %s failed. Tile does not exist!" % (self.data["name"], str(position)))
                    return

            if not monster:
                monster = Monster(self, position, None)
                if not self.prepared:
                    self.prepare()

            if not monster.alive:
                monster.data = monster.base.data.copy()
                monster.alive = True

            if not monster.clientId() in allCreatures:
                allCreatures[monster.clientId()] = monster

            monster.lastDamagers.clear()

            if place:
                # Vertify that there are no spectators if check = True
                if check and hasSpectators(position):
                    # If so, try again in 10s
                    call_later(10, self.spawn, position, place, spawnTime, 0, radius, radiusTo, monster, check)
                    return

                elif tile.hasCreatures() and config.tryToSpawnCreaturesNextToEachother:
                    ok = False
                    for testx in (-1,0,1):
                        position[0] += testx
                        tile = position.getTile()
                        if not tile:
                            continue
                        elif tile.hasCreatures():
                            for testy in (-1,0,1):
                                position[0] += testy
                                tile = position.getTile()
                                if not tile:
                                    continue

                                if not tile.hasCreatures():
                                    try:
                                        stackpos = map.getTile(position).placeCreature(monster)
                                        ok = True
                                    except:
                                        pass
                                    break
                        else:

                            try:
                                stackpos = map.getTile(position).placeCreature(monster)
                                ok = True
                            except:
                                pass
                        if ok:
                            break
                    if not ok:
                        print("Spawning of creature('%s') on %s failed" % (self.data["name"], str(position)))
                        return
                elif not tile.hasCreatures() or config.tryToSpawnCreatureRegardlessOfCreatures:
                    try:
                        stackpos = tile.placeCreature(monster)
                    except:
                        print("Spawning of creature('%s') on %s failed" % (self.data["name"], str(position)))
                        return
                else:
                    print("Spawning of creature('%s') on %s failed" % (self.data["name"], str(position)))
                    return

            monster.spawnTime = spawnTime
            monster.radius = radius

            if radius <= 1:
                self.walkable = False
            if radiusTo:
                monster.radiusTo = radiusTo
            else:
                monster.radiusTo = (position[0], position[1])

            if place and stackpos and stackpos < 10:
                for player in getPlayers(position):
                    stream = player.packet()
                    stream.addTileCreature(position, stackpos, monster, player)
                    stream.send(player.client)

            self.brain.beginThink(monster) # begin the heavy thought process!

            return monster

    def health(self, health, healthmax=None):
        if not healthmax:
            healthmax = health
        self.data["health"] = health
        self.data["healthmax"] = healthmax

        return self

    def defaultSpawnTime(self, spawnTime):
        self._spawnTime = spawnTime

    def type(self, color="blood"):
        self._blood = getattr(const, 'FLUID_'+color.upper())

    def outfit(self, lookhead, lookbody, looklegs, lookfeet):
        self.data["lookhead"] = lookhead
        self.data["lookbody"] = lookbody
        self.data["looklegs"] = looklegs
        self.data["lookfeet"] = lookfeet

    def addons(self, addon):
        self.data["lookaddons"] = addon

    def defense(self, armor=0, fire=1, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=1, lifedrain=1, manadrain=1):
        self._armor = armor
        self._fire = fire
        self._earth = earth
        self._energy = energy
        self._ice = ice
        self._holy = holy
        self._death = death
        self._drown = drown
        self._physical = physical
        self._lifedrain = lifedrain
        self._manadrain = manadrain
        if armor == -1:
            self._attackable = False

    def targetChance(self, chance=10):
        self._targetChance = chance

    def maxSummons(self, max):
        self.maxSummon = max

    def summon(self, monster=None, chance=10):
        self.summons.append((monster, chance))

    def experience(self, experience):
        self._experience = experience

    def speed(self, speed):
        self._speed = speed

    def corpseAction(self, action):
        self._corpseAction.append(action)

    def behavior(self, summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0, targetChange=1):
        self._summonable = summonable
        self._hostile = hostile
        self._illusionable = illusionable
        self._convinceable = convinceable
        self._pushable = pushable
        self._pushItems = pushItems
        self._pushCreatures = pushCreatures
        self._targetDistance = targetDistance
        self._runOnHealth = runOnHealth
        self._targetChange = targetChange

    def walkAround(self, energy=0, fire=0, poison=0):
        self._ignoreEnergy = energy
        self._ignoreFire = fire
        self._ignorePoison = poison

    def immunity(self, paralyze=1, invisible=1, drunk=1, lifedrain=1):
        self._paralyze = paralyze
        self._invisible = invisible
        self._drunk = drunk
        self._lifedrain = lifedrain # XXX: Kill, since this is part of immunity.

    def walkable(self, state):
        self._walkable = state

    def randomWalkInterval(self, per):
        self._walkPer = per

    def brainFeatures(self, *argc):
        self._brainFeatures = argc

    def voices(self, *argc):
        self.voiceslist = tuple(argc)

    def skull(self, skull):
        self._skull = skull

    def melee(self, maxDamage, check=lambda x: True, interval=config.meleeAttackSpeed, condition=None, conditionChance=0, conditionType=game.const.CONDITION_ADD):
        self.meleeAttacks.append([interval, check, maxDamage, condition, conditionChance, conditionType])

    def distance(self, maxDamage, shooteffect, check=chance(10), interval=config.meleeAttackSpeed):
        self.distanceAttacks.append([interval, maxDamage, shooteffect, check])

    def targetSpell(self, spellName, min, max, interval=2, check=chance(10), range=7, length=None):
        if isinstance(spellName, spell.Spell) or isinstance(spellName, spell.Rune):
            obj = spellName
        elif isinstance(spellName, str):
            try:
                obj = spell.spells[spellName][0]
            except:
                raise game.errors.SpellDoesNotExist(spellName)

        elif isinstance(spellName, int):
            try:
                obj = spell.targetRunes[spellName]
            except:
                raise game.errors.RuneDoesNotExist(spellName)

        if length:
            self.spellAttacks.append([interval, obj, check, range, (min, max, length)])
        else:
            self.spellAttacks.append([interval, obj, check, range, (min, max)])

    def selfSpell(self, spellName, min, max, interval=2, check=chance(10), length=None):
        if isinstance(spellName, spell.Spell) or isinstance(spellName, spell.Rune):
            obj = spellName.func
        elif isinstance(spellName, str):
            obj = spell.spells[spellName][0]
        elif isinstance(spellName, int):
            obj = spell.targetRunes[spellName]

        if length:
            self.defenceSpells.append([interval, obj, check, (min, max, length)])
        else:
            self.defenceSpells.append([interval, obj, check, (min, max)])

    def loot(self, *argc):
        self._loot = argc
    def prepare(self):
        self.prepared = True
        if not self._loot:
            return

        argc = self._loot

        # Convert name to Id here
        if config.lootInAlphabeticalOrder:
            cache = []
            for loot in argc:
                # Id to name
                if type(loot[0]) == int:
                    loot = list(loot)
                    try:
                        loot[0] = item.items[loot[0]]["name"]
                    except:
                        print("ItemId %d not found in loot. Ignoring!" % loot[0])
                        continue
                cache.append(loot)

            cache.reverse()

            for loot in cache[:]:
                if type(loot[0]) == tuple:
                    loot = list(loot)
                    loots = loot[0][:]
                    loot[0] = []
                    for ritem in loots:
                        sid = item.idByName(ritem)
                        if sid:
                            loot[0].append(sid)
                        else:
                            print("Monster loot, no item with the name '%s' exists (in %s)" % (ritem, self.data["name"]))

                else:
                    loot = list(loot)
                    sid = item.idByName(loot[0])
                    if sid:
                        loot[0] = sid
                    else:
                        print("Monster loot, no item with the name '%s' exists (in %s)" % (loot[0], self.data["name"]))

                self.lootTable.append(loot)

        else:
            for loot in argc:
                if type(loot[0]) == tuple:
                    loot = list(loot)
                    loots = loot[0][:]
                    loot[0] = []
                    for ritem in loots:
                        loot[0].append(item.idByName(ritem))

                elif type(loot[0]) == str:
                    loot = list(loot)
                    loot[0] = item.idByName(loot[0])

                self.lootTable.append(loot)
        del self._loot
class MonsterBrain(object):
    def beginThink(self, monster, check=False):
        if not monster.brainEvent:
            monster.brainEvent = call_later(0, self.handleThink, monster, check)
        else:
            raise Exception("Attempting to start a brain of a active monster!")

    def handleThink(self, monster, check=True):
        # Are we alive? And placed on a live position
        if not monster.alive: #or not monster.position.exists():
            monster.turnOffBrain()
            return # Stop looper

        if monster.base.voiceslist and random.randint(0, 99) < 10: # 10%
            # Find a random text
            text = random.choice(monster.base.voiceslist)

            # If text is uppercase, then yell it.
            if text.isupper():
                monster.yell(text)
            else:
                monster.say(text)

        if monster.target or (check and hasZLevelSpectators(monster.position, (9,7))) or not check:
            try:
                ret = brainFeatures[monster.base.brainFeatures](monster)
            except:
                ret = False
                scriptsystem.handle_script_exception()

            if ret == False:
                monster.turnOffBrain()
                return
            elif ret == True:
                monster.brainEvent = call_later(1, self.handleThink, monster)
                return
        else:
            # Are anyone watching?
            monster.turnOffBrain()
            return
        if not monster.walkPattern and monster.canWalk and not monster.action and time.time() - monster.lastStep > monster.walkPer: # If no other action is available
            self.walkRandomStep(monster) # Walk a random step

        monster.brainEvent = call_later(1, self.handleThink, monster)

    def walkRandomStep(self, monster, badDir=None, steps=[0,1,2,3]):
        if not badDir:
            badDir = set()
        random.shuffle(steps)

        for step in steps:
            # Prevent checks in "bad" directions
            if step in badDir:
                continue

            # Prevent us from autowalking futher then radius steps from our spawn point
            if step == 0 and monster.radiusTo[1]-(monster.position.y-1) > monster.radius:
                continue

            elif step == 1 and (monster.position.x+1)-monster.radiusTo[0] > monster.radius:
                continue

            elif step == 2 and (monster.position.y+1)-monster.radiusTo[1] > monster.radius:
                continue

            elif step == 3 and monster.radiusTo[0]-(monster.position.x-1) > monster.radius:
                continue

            badDir.add(step)

            # First verify the move.
            pos = monster.positionInDirection(step)
            tile = pos.getTile()
            if not tile or not monster.verifyMove(tile):
                continue

            if config.monsterNeverSkipWalks:
                def _():
                    if len(badDir) < 4:
                        self.walkRandomStep(monster, badDir)
                monster.move(step, failback=_, stopIfLock=True, push=False)
            else:
                monster.move(step, stopIfLock=True, push=False)

            break

        monster.lastStep = time.time()

brain = MonsterBrain()
def genMonster(name, looktype, corpse=0, lookhead=0, lookfeet=0, lookbody=0, looklegs=0, lookaddons=0, description=""):
    # baseMonsters
    if not corpse:
        corpse = idByName('dead %s' % name)
        if not corpse:
            corpse = idByName('slain %s' % name)
   
    baseMonster = MonsterBase({"lookhead":lookhead, "lookfeet":lookfeet, "lookbody":lookbody, "looklegs":looklegs, "lookaddons":lookaddons, "looktype":looktype, "corpse":corpse, "name":name, "description":description or inflect.a(name)}, brain)
    """try:
        baseMonster.regCorpseAction(look[2])
    except:
        pass"""
    monsters[name] = baseMonster

    return baseMonster

def getMonster(name):
    return monsters.get(name)

def regBrainFeature(name, function):
    if not name in brainFeatures:
        brainFeatures[name] = function
    else:
        print("Warning, brain feature %s exists!" % name)
