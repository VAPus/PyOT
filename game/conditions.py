import copy
import math

class Condition(object):
    def __init__(self, type, subtype="", length=1, every=2, check=None, *argc, **kwargs):
        self.length = length
        self.every = every
        self.creature = None
        self.tickEvent = None
        self.check = check

        if subtype and isinstance(type, str):
            self.type = "%s_%s" % (type, subtype)
        else:
            self.type = type
        self.effectArgs = argc
        self.effectKwargs = kwargs

        try:
            self.effect
        except:
            if type == CONDITION_FIRE:
                self.effect = self.effectFire
            elif type == CONDITION_POISON:
                self.effect = self.effectPoison
            elif type == CONDITION_ENERGY:
                self.effect = self.effectEnergy
            elif type == CONDITION_REGENERATEHEALTH:
                self.effect = self.effectRegenerateHealth
            elif type == CONDITION_REGENERATEMANA:
                self.effect = self.effectRegenerateMana
            elif type == CONDITION_DRUNK:
                self.effect = self.effectDrunk
            else:
                self.effect = self.effectNone

    def start(self, creature):
        """ Start the condition.
        :param creature: The creature object that this condition should affect.
        """
        self.creature = creature
        if self.type == CONDITION_HASTE:
            raise Exception("CONDITION_HASTE is a boost, not a condition.")
        if self.creature.isPlayer():
            self.saveCondition = True
            if self.type == CONDITION_PARALYZE and self.creature.hasCondition(CONDITION_HASTE):
                self.creature.removeCondition(CONDITION_HASTE)
            
        elif self.creature.isMonster():
            if self.type == CONDITION_DRUNK and self.creature.base._drunk:
                self.stop()
            elif self.type == CONDITION_PARALYZE and self.creature.base._paralyze:
                self.stop()
            elif self.type == CONDITION_INVISIBLE and self.creature.base._invisible:
                self.stop()

        if self.type == CONDITION_PARALYZE:
            creature.setSpeed(100)

        self.init()
        
        self.tickEvent = call_later(self.every, self.tick)

    def stop(self):
        """ Stops the condition."""
        try:
            ioloop_ins.remove_timeout(self.tickEvent)
        except:
            pass

        self.finish()

    def init(self):
        """ (For subclassing) Used to create your own custom initializer when subclassing Conditions."""
        pass

    def callback(self):
        """ (For subclassing) Called when the Condition finishes when used in a subclassed Condition."""
        pass

    def finish(self):
        """ Called when the condition finishes. Etc, when :func:`conditions.Condition.stop` is called. Or we're out of ticks. """
        self.tickEvent = None
        try:
            del self.creature.conditions[self.type]
        except:
            pass # May already have happend. Etc one tick conditions.

        if self.type == CONDITION_PARALYZE:
            self.defaultSpeed()
        if self.creature.isPlayer():
            self.saveCondition = True
        self.creature.refreshConditions()
        self.callback()

    def effectPoison(self, damage=0, minDamage=0, maxDamage=0, display=True):
        """ The default effect handler when the condition is a poison type """
        self.creature.magicEffect(EFFECT_GREEN_RINGS)
        if not damage:
            damage = random.randint(minDamage, maxDamage)
        if display:
            self.creature.onHit(None, -damage, DEATH, False)
        else:
            self.creature.modifyHealth(-damage)

    def effectFire(self, damage=0, minDamage=0, maxDamage=0, display=True):
        """ The default effect handler when the condition is a fire type """
        self.creature.magicEffect(EFFECT_HITBYFIRE)
        if not damage:
            damage = random.randint(minDamage, maxDamage)

        if display:
            self.creature.onHit(None, -damage, FIRE, False)
        else:
            self.creature.modifyHealth(-damage)
        
    def effectEnergy(self, damage=0, minDamage=0, maxDamage=0, display=True):
        """ The default effect handler when the condition is a energy type """
        self.creature.magicEffect(EFFECT_ENERGYHIT)
        if not damage:
            damage = random.randint(minDamage, maxDamage)

        if display:
            self.creature.onHit(None, -damage, ENERGY, False)
        else:
            self.creature.modifyHealth(-damage)

    def effectRegenerateHealth(self, gainhp=None, display=True):
        """ The default effect handler when the condition is a health regen type """
        if not gainhp:
            gainhp = self.creature.getVocation().health[0]
            self.creature.onHeal(None, gainhp[0])

        if display:
            self.creature.onHeal(None, gainhp)
        else:
            self.creature.modifyHealth(gainhp)

    def effectRegenerateMana(self, gainmana=None):
        """ The default effect hander when the condition is a mana regen type """
        if not gainmana:
            gainmana = self.creature.getVocation().mana
            self.creature.modifyMana(gainmana[0])

        else:
            self.creature.modifyMana(gainmana)

    def effectDrunk(self):
        " Drunk effect "
        # Does drunkenness have any effect? Dunno.
        # XXX: Drarwenring supression.
        self.creature.magicEffect(EFFECT_BUBBLES)

    def effectNone(self):
        """ Dummy function when no effect is used. """
        pass
    
    def tick(self):
        """ Handles the ticks. Calls the effect, schedule the next tick or finishes if there are no next tick """
        if not self.creature:
            return

        self.effect(*self.effectArgs, **self.effectKwargs)
        self.length -= self.every # This "can" become negative!

        if self.check: # This is what we do if we got a check function, independantly of the length
            if self.check(self.creature):
                self.tickEvent = call_later(self.every, self.tick)
            else:
                self.finish()

        elif self.length > 0:
            self.tickEvent = call_later(self.every, self.tick)
        else:
            self.finish()

    def process(self):
        """ Mostly useful in tests. This repeats the tick process of this Condition until the Condition is finished without waiting. """
        if self.tickEvent:
            while self.tickEvent:
                ioloop_ins.remove_timeout(self.tickEvent)
                self.tick()

    def copy(self):
        """ Returns a copy of this Condition. """
        return copy.deepcopy(self)

    def __getstate__(self):
        """ Returns a saveable version of the Condition, without the creature and tick event set. """
        d = self.__dict__.copy()
        d["creature"] = None
        del d["tickEvent"]
        return d

class Boost(Condition):
    def __init__(self, type, mod, length, subtype="", percent=False, *argc, **kwargs):
        self.length = length
        self.every = 2 # Required for CONDITION_LATER
        self.creature = None
        self.tickEvent = None
        if subtype and isinstance(type, str):
            self.type = "%s_%s" % (type, subtype)
        elif isinstance(type, int):
            self.type = '_'+str(type)
        else:
            self.type = '_'.join(map(str, type))
        self.ptype = [type] if not isinstance(type, list) else type
        self.effectArgs = argc
        self.effectKwargs = kwargs
        self.mod = [mod] if not isinstance(mod, list) else mod
        self.percent = percent

    def add(self, type, mod):
        """ Adds yet another variaible to boost.
        :param type: The type (like speed, health, healthmax) to boost.
        :param mod: How much to modify the type.
        """
        self.ptype.append(type)
        self.mod.append(mod)
        return self

    def tick(self):
        """ Handles the tick. Boost usually doesn't have any ticks. """
        pass

    def init(self):
        """ Initialize the Boost, this function sets the boosting."""
        
        pid = 0
        for ptype in self.ptype:
            # Apply
            if isinstance(ptype, int):
                # Skill.
                pvalue = self.creature.getActiveSkill(ptype)
            else:
                try:
                    pvalue = getattr(self.creature, ptype)
                    inStruct = 0
                except:
                    pvalue = self.creature.data[ptype]
                    inStruct = 1

            if isinstance(self.mod[pid], int):
                if self.percent:
                    pvalue *= self.mod[pid]
                else:
                    pvalue += self.mod[pid]
            else:
                pvalue = self.mod[pid](self.creature, ptype, True)

            # Hack
            if ptype == "speed":
                self.type = CONDITION_HASTE
                self.creature.setSpeed(pvalue)
            elif isinstance(ptype, int):
                #  Skills.
                self.creature.tempAddSkillLevel(ptype, int(pvalue - self.creature.getActiveSkill(ptype)))
            else:
                if inStruct == 0:
                    setattr(self.creature, ptype, pvalue)
                else:
                    self.creature.data[ptype] = pvalue
            pid += 1

        self.tickEvent = call_later(self.length, self.finish)

        self.creature.refreshStatus()
    def callback(self):
        """ Called when the boost ends. Substracts the boosting. """
        pid = 0
        for ptype in self.ptype:
            # Apply
            if isinstance(ptype, int):
                # Skill.
                pvalue = self.creature.getActiveSkill(ptype)
            else:
                try:
                    pvalue = getattr(self.creature, ptype)
                    inStruct = 0
                except:
                    pvalue = self.creature.data[ptype]
                    inStruct = 1

            if isinstance(self.mod[pid], int):
                if self.percent:
                    pvalue /= self.mod[pid]
                else:
                    pvalue -= self.mod[pid]
            else:
                pvalue = self.mod[pid](self.creature, ptype, False)

            # Hack
            if ptype == "speed":
                self.creature.setSpeed(pvalue)
            elif isinstance(ptype, int):
                #  Skills.
                # pvalue is already negative.
                self.creature.tempAddSkillLevel(ptype, (int(pvalue - self.creature.getActiveSkill(ptype))))
            else:
                if inStruct == 0:
                    setattr(self.creature, ptype, pvalue)
                else:
                    self.creature.data[ptype] = pvalue

            pid += 1
        self.creature.refreshStatus()
        
def MultiCondition(type, subtype="", *argc):
    """ Return one Condition where the callback have been set to call the next condition upon the finish of the first. """
    conditions = []
    for x in argc:
        conditions.append(Condition(type, subtype, **x))

    for index in len(conditions):
        if index != len(conditions)-1:
            conditions[index].callback = lambda self: self.creature.condition(conditions[index+1])

    return conditions[0]

class CountdownCondition(Condition):
    def __init__(self, type, startdmg, subtype=""):
        # This is constant. EVERY 2 sec, do recalculations
        # Finishes when dmg hits 1.
        self.creature = None
        self.tickEvent = None
        self.damage = startdmg
        # Cheat, this is a requirement.
        self.length = 2
        self.every = 2 # Required for CONDITION_LATER
        
        if subtype and isinstance(type, str):
            self.type = "%s_%s" % (type, subtype)
        else:
            self.type = type

        try:
            self.effect
        except:
            if type == CONDITION_FIRE:
                self.effect = self.effectFire
            elif type == CONDITION_POISON:
                self.effect = self.effectPoison
            elif type == CONDITION_REGENERATEHEALTH:
                self.effect = self.effectRegenerateHealth
            elif type == CONDITION_REGENERATEMANA:
                self.effect = self.effectRegenerateMana        

    def tick(self):
        if not self.creature:
            return

        self.effect(self.damage)
        
        # So, time for damage reduction.
        # If >18, it's 100% chance.
        # Otherwise, use a chance formula.
        if self.damage > 18:
            # Decrease by 2-3.
            self.damage -= random.randint(2, 3)
        elif random.randint(0, 99) < 60 - ((18-self.damage) * 2):
            self.damage -= 1
            
        # No damamge? Finish it!
        # Otherwise, scheduler next tick.
        if self.damage <= 0:
            self.length = 0
            self.finish()
        else:
            self.tickEvent = call_later(2, self.tick)
            
class PercentCondition(Condition): #under 100% it will decrase in percentages
    def __init__(self, type, startdmg, percent, rptcount=False, subtype=""):
        # This is constant. EVERY 2 sec, do recalculations
        # Finishes when dmg hits 1.
        self.creature = None
        self.tickEvent = None
        self.damage = startdmg
        self.percent = percent
        if not rptcount:
            self.count = 20
        else:
            self.count = rptcount

        self.length = self.count * 2
        self.every = 2 # Required for CONDITION_LATER
        
        if subtype and isinstance(type, str):
            self.type = "%s_%s" % (type, subtype)
        else:
            self.type = type

        try:
            self.effect
        except:
            if type == CONDITION_FIRE:
                self.effect = self.effectFire
            elif type == CONDITION_POISON:
                self.effect = self.effectPoison
            elif type == CONDITION_REGENERATEHEALTH:
                self.effect = self.effectRegenerateHealth
            elif type == CONDITION_REGENERATEMANA:
                self.effect = self.effectRegenerateMana        

    def tick(self):
        if not self.creature:
            return

        self.effect(math.ceil(self.damage))
        
        self.count -= 1
        self.length -= 2

        self.damage = round(self.damage * self.percent, 2)
        if self.count <= 0 or self.damage <= 0.27:
            self.finish()
        else:
            self.tickEvent = call_later(2, self.tick)
            

class RepeatCondition(Condition):
    def __init__(self, type, startdmg, rptcount=False, subtype=""):
        # This is constant. EVERY 2 sec, do recalculations
        # Finishes when dmg hits 1.
        self.creature = None
        self.tickEvent = None
        self.damage = startdmg

        if not rptcount:
            self.count = 10
        else:
            self.count = rptcount

        self.length = self.count * 2
        self.every = 2 # Required for CONDITION_LATER
        
        if subtype and isinstance(type, str):
            self.type = "%s_%s" % (type, subtype)
        else:
            self.type = type

        try:
            self.effect
        except:
            if type == CONDITION_FIRE:
                self.effect = self.effectFire
            elif type == CONDITION_POISON:
                self.effect = self.effectPoison
            elif type == CONDITION_REGENERATEHEALTH:
                self.effect = self.effectRegenerateHealth
            elif type == CONDITION_REGENERATEMANA:
                self.effect = self.effectRegenerateMana        

    def tick(self):
        if not self.creature:
            return

        self.effect(self.damage)
        
        self.count -= 1
        self.length -= 2

        if self.count <= 0:
            self.finish()
        else:
            self.tickEvent = call_later(2, self.tick)
