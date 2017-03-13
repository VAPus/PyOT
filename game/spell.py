import game.scriptsystem # We use the talkactions from here
import game.item
import game.map
import game.const
import random
import game.creature
import collections

spells = {}
fieldRunes = {}
targetRunes = {}

def calculateAreaDirection(position, direction, area):
    positions = []
    if area[0] == TARGET_DIRECTION:
        # We begin on row 1, right in front of us
        yp = 1
        blocking = [] # We keep the blocking tiles from this row because we are using them in the next
        prevBlocking = []
        count = 0 # Count of fields in previous row, so we can calculate fields required
        minEntry = maxEntry = 0
        prevMinEntry = prevMaxEntry = 0
        for yo in area[1:]: # As you might know, area[0] is used to determin the type. yo == y list
                
            for xp in yo: # xp == x position from y list
                # First agenda is to determin whatever a previous field blocked us
                if count and prevBlocking:
                    if prevBlocking[0] == prevMinEntry and prevBlocking[0] >= xp: # Are we extending the so called minEntry border?
                        blocking.append(prevBlocking[0])
                        minEntry = prevMinEntry
                        continue
                    elif prevBlocking[-1] == prevMaxEntry and prevBlocking[-1] <= xp: # Are we extending the so called maxEntry border?
                        blocking.append(prevBlocking[-1])
                        maxEntry = prevMaxEntry
                        continue
                    elif xp in prevBlocking:
                        continue

                if direction == 0: # North:
                    pos = game.position.Position(position.x - xp, position.y - yp, position.z) # Our new position
                    
                elif direction == 1: # East
                    pos = game.position.Position(position.x + yp, position.y + xp, position.z) # Our new position
                    
                elif direction == 2: # South
                    pos = game.position.Position(position.x + xp, position.y + yp, position.z) # Our new position
                    
                elif direction == 3: # West
                    pos = game.position.Position(position.x - yp, position.y - xp, position.z) # Our new position
                    
                if xp > maxEntry: # Determin this as our new min/max
                    maxEntry = xp
                elif xp < minEntry:
                    minEntry = xp
                    
                tile = game.map.getTile(pos)
                if not tile:
                    blocking.append(xp)
                    continue
                    
                ret = 0
                for item in tile.getItems():
                    if item.blockprojectile:
                        blocking.append(xp)
                        ret = 1
                        break
                    
                if not ret:
                    positions.append(pos)


            count = len(yo)
            
            if count and count == len(blocking): # 100% blocking, it basicly means we're done
                return positions
                
            prevBlocking = blocking[:]
            blocking = [] # New blocking, from this level
            prevMaxEntry = maxEntry
            prevMinEntry = minEntry
            yp += 1
                    
    elif area[0] == TARGET_CASTER_AREA:
        for a in area[1:]:
            x = position.x - a[0]
            y = position.y - a[1]
            pos = Position(x, y, position.z)  
            if pos.getTile():         
                positions.append(pos)
                  

    return positions
    
def typeToEffect(type):
    if type == "fire":
        return (EFFECT_HITBYFIRE, ANIMATION_FIRE)
    elif type == "poison":
        return (EFFECT_HITBYPOISON, ANIMATION_POISON)
  

def clear():
    fieldRunes.clear()
    targetRunes.clear()
    spells.clear()
    
    
    
### The new way ###

def damage(mlvlMin, mlvlMax, constantMin, constantMax, type=game.const.MELEE, lvlMin=5, lvlMax=5):
    def damageCallback(caster, target, strength=None):
        if not target: return
        
        if strength:
            dmg = -random.randint(strength[0], strength[1])
        else:
            maxDmg = (round((caster.data["level"]/lvlMax)+(caster.data["maglevel"]*mlvlMax)+constantMax))
            minDmg = (round((caster.data["level"]/lvlMin)+(caster.data["maglevel"]*mlvlMin)+constantMin))
            dmg = -random.randint(minDmg, maxDmg)
        
        target.onHit(caster, dmg, type)
        
    return damageCallback

def damageExtra(constant, type=game.const.MELEE):
    def damageCallback(caster, target, strength=None):
        if not target: return
        target.onHit(caster, len(caster.spellTargets) * constant, type, False)

    return damageCallback

def meleeBased(aConst, bConst, constantMin, constantMax, type=game.const.MELEE, lvlMin=5, lvlMax=5):
    def meleeBasedCallback(caster, target, strength=None):
        if not target: return
        
        if strength:
            dmg = -random.randint(strength[0], strength[1])
        else:
            b = 0
            weapon = caster.inventory[SLOT_RIGHT]
            if weapon:
                skillType = weapon.weaponSkillType
                b = weapon.attack
            else:
                skillType = SKILL_FIST
            a = caster.getActiveSkill(skillType)
            c = caster.data["level"]
            maxDmg = (round((a*aConst+b*bConst)*constantMax+(c/lvlMax)))
            minDmg = (round((a*aConst+b*bConst)*constantMin+(c/lvlMin)))
            dmg = -random.randint(minDmg, maxDmg)
        
        target.onHit(caster, dmg, type)
        
    return meleeBasedCallback

def element(type):
    # This is for Creature spells ONLY!
    def elementDamageCallback(caster, target, strength):
        # Target required!
        if not target: return
 
        # Only rely on strength, this will raise a console error if a player attampts to cast this spell.
        dmg = random.randint(strength[0], strength[1])
 
        target.onHit(caster, dmg, type)

    return elementDamageCallback
    
def heal(mlvlMin, mlvlMax, constantMin, constantMax, lvlMin=5, lvlMax=5, cure=game.const.CONDITION_PARALYZE):
    def healCallback(caster, target, strength=None):
        if not target: return
        
        if strength:
            minDmg, maxDmg = strength
        else:
            maxDmg = round((caster.data["level"]/lvlMax)+(caster.data["maglevel"]*mlvlMax)+constantMax)
            minDmg = round((caster.data["level"]/lvlMin)+(caster.data["maglevel"]*mlvlMin)+constantMin)

        target.onHeal(caster, random.randint(minDmg, maxDmg))
        
        # Cure paralyzation if configurated to do so.
        if cure:
            target.loseCondition(cure)

        target.addSupporter(caster)
        
    return healCallback

def cure(condition):
    def cureCallback(caster, target, strength=None):
        target.addSupporter(caster)
        target.loseCondition(condition)
    return cureCallback

def mana(mlvlMin, mlvlMax, constantMin, constantMax, lvlMin=5, lvlMax=5):
    def manaCallback(caster, target, strength=None):
        if not target: return
        
        if strength:
            minDmg, maxDmg = strength
        else:
            maxDmg = round((caster.data["level"]/lvlMax)+(caster.data["maglevel"]*mlvlMax)+constantMax)
            minDmg = round((caster.data["level"]/lvlMin)+(caster.data["maglevel"]*mlvlMin)+constantMin)
        
        mana = -random.randint(minDmg, maxDmg)

        if mana < 0:
            target.addDamager(caster)
        elif mana > 0:
            target.addSupporter(caster)

        target.modifyMana(mana)
        
    return manaCallback
    
def conjure(make, count=1, **kwargs):
    def conjureCallback(caster, target, strength=None):
        if target.isPlayer():
            item = game.item.Item(make, count, **kwargs)

            ret = target.itemToUse(item)
            if not ret:
                return target.notEnoughRoom()
                
            target.message("Made %dx%s" % (count, item.rawName()))
            
    return conjureCallback

def field(fieldId):
    def makeFieldCallback(position, **k):
        item = Item(fieldId)
        
        item.place(position)
                            
    return makeFieldCallback

def magicRope():
    def magicRopeCallback(caster, target=None, strength=None):
        ropeSpots = 384, 418, 8278, 8592
        Pos = caster.position
        newPos = Pos.copy()
        item = getTile(Pos).getThing(0)
        if item.itemId in ropeSpots:
            newPos.y += 1
            newPos.z -= 1
            caster.teleport(newPos)

    return magicRopeCallback

class Spell(object):
    def __init__(self, name=None, words=None, icon=0, target=game.const.TARGET_TARGET, group=game.const.ATTACK_GROUP):
        self.name = name
        self.words = words
        self.targetType = target
        
        self.vocations = None
        
        self.castEffect = None
        self._targetEffect = None
        self.shootEffect = None
        self.areaEffect = None
        
        self.targetRange = 7
        
        self.targetArea = None
        
        self.effectOnCaster = []
        self.effectOnTarget = []
        self.conditionOnCaster = []
        self.conditionOnTarget = []
        
        self.icon = icon
        self.group = group
        
        self.learned = False
        
        self._requireGreater = []
        self._requireLess = []
        self._requireCallback = []
        
        self.cooldown = 2
        self.groupCooldown = 2

        self.func = self.doEffect()
        def l():
            try:
                mana = self._requireGreater["mana"]
            except:
                mana = 0
                
            try:
                level = self._requireGreater["level"]
            except:
                level = 0
                
            spells[name] = (self.func, words, level, mana)
        
        # Delay the input a little.
        call_later(0.1, l)
        spells[name] = (self.func,)
        if words:
            game.scriptsystem.get("talkaction").register(words, self.func)
            
    def effects(self, caster=None, shoot=None, target=None, area=None):
        self.castEffect = caster
        self.shootEffect = shoot
        self._targetEffect = target
        self.areaEffect = area
        
        return self
        
    def area(self, area):
        self.targetArea = area
        
        return self
    
    def range(self, distance):
        self.targetRange = distance
        
        return self
        
    def casterEffect(self, mana=0, health=0, soul=0, callback=None):
        if mana or health:
            def _effect(caster, target, **k):
                # Target = caster
                if health:
                    target.modifyHealth(health)
                if mana:
                    target.modifyMana(mana)
                if soul:
                    target.modifySoul(soul)
                    
            self.effectOnCaster.append(_effect)
            
        if callback:
            self.effectOnCaster.append(callback)
            
        return self
            
    def targetEffect(self, mana=0, health=0, soul=0, callback=None):
        if mana or health:
            def _effect(target, caster, **k):
                # Target = actual target
                added = False
                if health:
                    if health < 0:
                        target.addDamager(caster)
                        added = True
                    elif not added:
                        target.addSupporter(caster)
                    target.modifyHealth(health)
                if mana:
                    if not added and mana < 0:
                       target.addDamager(caster)
                       added = True
                    elif not added:
                       target.addSupporter(caster)

                    target.modifyMana(mana)
                    
                if soul:
                    target.modifySoul(soul)
                    
            self.effectOnTarget.append(_effect)
            
        if callback:
            self.effectOnTarget.append(callback)
        
        return self
        
    def casterCondition(self, *argc, **kwargs):
        try:
            stack = kwargs['stackbehavior']
        except:
            stack = CONDITION_LATER
            
        for con in argc:
            self.conditionOnCaster.append((con, stack))

        return self
        
    def targetCondition(self, *argc, **kwargs):
        try:
            stack = kwargs['stackbehavior']
        except:
            stack = CONDITION_LATER
            
        for con in argc:
            self.conditionOnTarget.append((con, stack))
   
        return self
        
    def require(self, learned=False, vocations=None, **kwargs):
        self._requireGreater = kwargs
        self.vocations = vocations
        self.learned = learned
        
        return self
   
    def requireLess(self, **kwargs):
        self._requireLess = kwargs
        
        return self

    def requireCallback(self, *args):
        self._requireCallback.extend(args)
        
        return self

    def element(self, type):
        self.effectOnTarget.append(element(type))
        
        return self
        
    def use(self, itemId=2260, count=1):
        def check(caster):
            useItem = caster.findItemById(itemId, count)
                
            if not useItem:
                caster.needMagicItem()
                caster.magicEffect(EFFECT_POFF)
                return False
                
            return True
            
        self._requireCallback.append(check)
        
        return self

    def onPos(self):
        def verify(caster, **k):
            found = False
            item = getTile(caster.position).getThing(0)
            ropeSpots = 384, 418, 8278, 8592
            if item.itemId in (ropeSpots):
                found = True
            else:
                caster.notPossible()
            return found
        self._requireCallback.append(verify)

        return self
    
    def cooldowns(self, cooldown=0, groupCooldown=None):
        if cooldown and groupCooldown == None:
            groupCooldown = cooldown
           
        self.cooldown = cooldown
        self.groupCooldown = groupCooldown
        
        return self
       
    def doEffect(self):
        # Stupid weakrefs can't deal with me directly since i can't be a strong ref. Yeye, I'll just cheat and wrap myself!
        def spellCallback(creature, strength=None, **k):
            target = creature
            if self.targetType == TARGET_TARGET or self.targetType == TARGET_TARGETSELF or self.targetType == TARGET_TARGETONLY:
                if creature.target:
                    target = creature.target
                    if self.targetType == TARGET_TARGETONLY:
                        self.targetType = TARGET_TARGET
                elif self.targetType == TARGET_TARGET and self.targetArea: #if no target but area still cast the spell (dont need not creature.target)
                    self.targetType = TARGET_AREA #if not and the spell is cast as an area spell do the area being defined.
                elif self.targetType == TARGET_TARGET and not self.targetArea:
                    return False
                elif self.targetType == TARGET_TARGETONLY:
                    return creature.cancelMessage(_l(creature, "You need a target to cast this spell."))
 
            if creature.isPlayer():
                if not target.inRange(creature.position, self.targetRange, self.targetRange):
                    creature.cancelMessage(_l(creature, "Target is too far away"))

                    return False
                    
                if not creature.canDoSpell(self.icon, self.group):
                    creature.exhausted()

                    return False
                    
                if creature.getSkull() == SKULL_BLACK and config.blackSkullDisableAreaSpells and self.targetType == TARGET_AREA:
                    return creature.cancelMessage(_l(creature, "You have a black skull and can't cast area spells."))
                
                if self.learned and not creature.canUseSpell(self.name):
                    return creature.cancelMessage(_l(creature, "You need to learn this spell first."))
                    
                if self.vocations and creature.getVocationId() not in self.vocations:
                    return creature.cancelMessage(_l(creature, "Your vocation cannot use this spell."))
                    
                if self._requireGreater:
                    for var in self._requireGreater:
                        if creature.data[var] < self._requireGreater[var]:
                            creature.notEnough(var)

                            return False
                            
                if self._requireLess:
                    for var in self._requireLess:
                        if creature.data[var] > self._requireLess[var]:
                            creature.message(_l(creature, "Your %s is too high!") % var)

                            return False
                
                if self._requireCallback:
                    for call in self._requireCallback:
                        if not call(caster=creature):

                            return
                        
                # Integrate mana seeker
                try:
                    creature.modifyMana(-self._requireGreater["mana"])
                    creature.modifySpentMana(self._requireGreater["mana"])
                except:
                    pass

                # Integrate soul seeker
                try:
                    creature.modifySoul(-self._requireGreater["soul"])
                except:
                    pass
                
                creature.cooldownSpell(self.icon, self.group, self.cooldown, self.groupCooldown)
            creature.spellTargets = []
                    
            if self.castEffect:
                creature.magicEffect(self.castEffect)

            for call in self.effectOnCaster:
                call(caster=creature, target=creature, strength=strength)
            
            for array in self.conditionOnCaster:
                creature.condition(array[0].copy(), array[1])
                
            if self.targetType in (TARGET_TARGET, TARGET_TARGETSELF) and target and target != creature and self.shootEffect:
                creature.shoot(creature.position, target.position, self.shootEffect)
                
            if not self.targetType == TARGET_AREA:
                creature.spellTargets.append(target)
                for call in self.effectOnTarget:
                    call(target=target, caster=creature, strength=strength)
                
                if self._targetEffect:
                    target.magicEffect(self._targetEffect)
                    
                for array in self.conditionOnTarget:
                    target.condition(array[0].copy(), array[1])

            if self.targetType == TARGET_AREA:
                area = self.targetArea(caster=creature) if isinstance(self.targetArea, collections.Callable) else self.targetArea
                positions = calculateAreaDirection(creature.position, creature.direction, area)
                targetGenerators = []
                for pos in positions:
                    if self.areaEffect:
                        creature.magicEffect(self.areaEffect, pos)
                        
                    creatures = game.map.getTile(pos).creatures()
                    if creatures:
                        targetGenerators.append(creatures)
                        
                for generator in targetGenerators:
                    for targ in generator:
                        if creature.isMonster() and not config.monsterAoEAffectMonsters and targ.isMonster():
                            continue

                        creature.spellTargets.append(targ)

                        if self._targetEffect:
                            targ.magicEffect(self._targetEffect)
                        
                        for call in self.effectOnTarget:
                            call(target=targ, caster=creature, strength=strength)
                        
        return spellCallback
        
       
class Rune(Spell):
    def __init__(self, rune, icon=0, count=1, target=game.const.TARGET_TARGET, group=game.const.ATTACK_GROUP):
        self.rune = rune
        self.targetType = target
        self.count = count
        
        self.vocations = None
        
        self.castEffect = None
        self._targetEffect = None
        self.shootEffect = None
        self.areaEffect = None
        
        self.targetRange = 7
        
        self.targetArea = None
        
        self.effectOnCaster = []
        self.effectOnTarget = []
        self.conditionOnCaster = []
        self.conditionOnTarget = []
        
        self.icon = icon
        self.group = group
        
        self.learned = False
        
        self._requireGreater = []
        self._requireLess = []
        self._requireCallback = []
        
        self.cooldown = 2
        self.groupCooldown = 2

        self.func = self.doEffect()
        targetRunes[rune] = self.func # Just to prevent reset
        game.scriptsystem.get("useWith").register(rune, self.func)
        
    def doEffect(self):
        # Stupid weakrefs can't deal with me directly since i can't be a strong ref. Yeye, I'll just cheat and wrap myself!
        def runeCallback(thing, creature, position, onPosition, onThing, strength=None, **k):
            print("runeCallback")
            target = creature
            if self.targetType == TARGET_TARGET:
                target = onThing
                if not isinstance(target, Creature):
                    if not isinstance(target, Creature):
                        print(onThing, onThing.position, onThing.position.getTile().getCreatureCount())
                        try:
                            target = onThing.position.getTile().topCreature()
                            print(target)
                        except:
                            raise                    
                    if not target:
                        creature.onlyOnCreatures()
                        return False

            creature.spellTargets = [target]
                    
            if creature.isPlayer():
                if not target.inRange(creature.position, self.targetRange, self.targetRange):
                    creature.cancelMessage(_l(creature, "Target is too far away"))
                    return False
                    
                if not creature.canDoSpell(self.icon, self.group):
                    creature.exhausted()
                    return False

                if creature.getSkull() == SKULL_BLACK and config.blackSkullDisableAreaRunes and self.targetType == TARGET_AREA:
                    return creature.cancelMessage(_l(creature, "You have a black skull and can't cast area spells."))
                
                if self.learned and not creature.canUseSpell(self.name):
                    return creature.cancelMessage(_l(creature, "You need to learn this spell first."))
                    
                if self.vocations and creature.getVocationId() not in self.vocations:
                    return creature.cancelMessage(_l(creature, "Your vocation cannot use this spell."))
                    
                if self._requireGreater:
                    for var in self._requireGreater:
                        if creature.data[var] < self._requireGreater[var]:
                            creature.notEnough(var)
                            return False
                            
                if self._requireLess:
                    for var in self._requireLess:
                        if creature.data[var] > self._requireLess[var]:
                            creature.message(_l(creature, "Your %s is too high!") % var)
                            return False
                
                if self._requireCallback:
                    for call in self._requireCallback:
                        if not call(caster=creature): return

                if not thing.count:
                    creature.needMagicItem()
                    creature.magicEffect(EFFECT_POFF)
                        
                else:
                    thing.modify(-1)  
                    
                    # Integrate mana seeker
                    try:
                        creature.modifyMana(-self._requireGreater["mana"])
                        creature.modifySpentMana(self._requireGreater["mana"])
                    except:
                        pass

                    # Integrate soul seeker
                    try:
                        creature.modifySoul(-self._requireGreater["soul"])
                    except:
                        pass
                    
                    creature.cooldownSpell(self.icon, self.group, self.cooldown, self.groupCooldown)
                    
            if self.castEffect:
                creature.magicEffect(self.castEffect)
            
            for call in self.effectOnCaster:
                call(caster=creature, target=creature, strength=strength)
            
            for array in self.conditionOnCaster:
                creature.condition(array[0].copy(), array[1])
                
            if self.targetType == TARGET_TARGET and self.shootEffect:
                creature.shoot(creature.position, target.position, self.shootEffect)
                
            if not self.targetType == TARGET_AREA:
                for call in self.effectOnTarget:
                    call(target=target, caster=creature, strength=strength)
                
                if self._targetEffect:
                    target.magicEffect(self._targetEffect)
                    
                for array in self.conditionOnTarget:
                    target.condition(array[0].copy(), array[1])
        
            else:
                area = self.targetArea(caster=creature) if isinstance(self.targetArea, collections.Callable) else self.targetArea
                positions = calculateAreaDirection(creature.position, creature.direction, area)
                targetGenerators = []
                for pos in positions:
                    if self.areaEffect:
                        creature.magicEffect(self.areaEffect, pos)
                        
                    creatures = game.map.getTile(pos).creatures()
                    if creatures:
                        targetGenerators.append(creatures)
                        
                for generator in targetGenerators:
                    for targ in generator:
                        if creature.isMonster() and not config.monsterAoEAffectMonsters and targ.isMonster():
                            continue

                        creature.spellTargets.append(targ)

                        if self._targetEffect:
                            targ.magicEffect(self._targetEffect)
                        
                        for call in self.effectOnTarget:
                            call(target=targ, caster=creature, strength=strength)
                    
        if config.runeCastDelay:
            def castDelay(*a, **k):
                call_later(config.runeCastDelay, runeCallback, *a, **k)
                
            return castDelay
            
        return runeCallback
