import config
from tornado import gen

class CreatureAttacks(object):
    def hitEffects(self):
        if self.isPlayer() or self.base._blood == FLUID_BLOOD:
            return COLOR_RED, EFFECT_DRAWBLOOD
        elif self.base._blood == FLUID_SLIME:
            return COLOR_LIGHTGREEN, EFFECT_HITBYPOISON
        elif self.base._blood == FLUID_ENERGY:
            return COLOR_PURPLE, EFFECT_PURPLEENERGY
        elif self.base._blood == FLUID_UNDEAD:
            return COLOR_GREY, EFFECT_HITAREA
        elif self.base._blood == FLUID_FIRE:
            return COLOR_ORANGE, EFFECT_DRAWBLOOD

    def damageToBlock(self, dmg, type):
        # Overrided to creatures.
        return dmg

    def onHit(self, by, dmg, type, effect=None):

        if not type == DISTANCE:
            if by and not by.ignoreBlock and self.doBlock:
                dmg = min(self.damageToBlock(dmg, type), 0) # Armor calculations(shielding+armor)

        if type == ICE:
            textColor = COLOR_TEAL
            magicEffect = EFFECT_ICEATTACK

        elif type == FIRE:
            textColor = COLOR_ORANGE
            magicEffect = EFFECT_HITBYFIRE

        elif type == EARTH:
            textColor = COLOR_LIGHTGREEN
            magicEffect = EFFECT_HITBYPOISON

        elif type == ENERGY:
            textColor = COLOR_PURPLE
            magicEffect = EFFECT_ENERGYHIT

        elif type == HOLY:
            textColor = COLOR_YELLOW
            magicEffect = EFFECT_HOLYDAMAGE

        elif type == DEATH:
            textColor = COLOR_DARKRED
            magicEffect = EFFECT_SMALLCLOUDS

        elif type == DROWN:
            textColor = COLOR_LIGHTBLUE
            magicEffect = EFFECT_ICEATTACK

        elif type == DISTANCE:
            textColor, magicEffect = COLOR_RED, None
            if by and not by.ignoreBlock and self.doBlock:
                dmg = min(self.damageToBlock(dmg, type), 0) # Armor calculations(armor only. for now its the same function)
        elif type == LIFEDRAIN:
            textColor = COLOR_TEAL
            magicEffect = EFFECT_ICEATTACK

        else: ### type == MELEE:
            textColor, magicEffect = self.hitEffects()
        if effect != None:
            magicEffect = effect

        # pvpDamageFactor.
        if self.isPlayer() and (by and by.isPlayer()) and (not config.blackSkullFullDamage or by.getSkull() != SKULL_BLACK):
            dmg = int(dmg * config.pvpDamageFactor)
            
        process = game.scriptsystem.get("hit").run(creature2=self, creature=by, damage=dmg, type=type, textColor=textColor, magicEffect=magicEffect)
        if process == False:
            return

        dmg = max(-self.data["health"], dmg)
        
        if dmg:
            if by:
                self.addDamager(by)
                by.lastPassedDamage = time.time()
            
            if magicEffect:
                self.magicEffect(magicEffect)
            tile = game.map.getTile(self.position)
            for item in tile.getItems():
                if item.itemId in SMALLSPLASHES or item.itemId in FULLSPLASHES:
                    tile.removeItem(item)

            splash = Item(SMALLSPLASH)

            if self.isPlayer():
                splash.fluidSource = FLUID_BLOOD
            else:
                splash.fluidSource = self.base._blood
            if splash.fluidSource in (FLUID_BLOOD, FLUID_SLIME):
                splash.place(self.position)

                # Start decay
                splash.decay()

            updateTile(self.position, tile)

            if by and by.isPlayer():
                by.condition(Condition(CONDITION_INFIGHT, length=config.loginBlock), CONDITION_REPLACE)
                by.message(_lp(by, "%(who)s loses %(amount)d hitpoint due to your attack.", "%(who)s loses %(amount)d hitpoints due to your attack.", -dmg) % {"who": self.name().capitalize(), "amount": -dmg}, MSG_DAMAGE_DEALT, value = -1 * dmg, color = textColor, pos=self.position)
                
            if self.isPlayer():
                self.condition(Condition(CONDITION_INFIGHT, length=config.loginBlock), CONDITION_REPLACE)
                if by:
                    self.message(_lp(self, "You lose %(amount)d hitpoint due to an attack by %(who)s.", "You lose %(amount)d hitpoints due to an attack by %(who)s.", -dmg) % {"amount": -dmg, "who": by.name().capitalize()}, MSG_DAMAGE_RECEIVED, value = -1 * dmg, color = textColor, pos=self.position)
                else:
                    self.message(_lp(self, "You lose %(amount)d hitpoint.", "You lose %(amount)d hitpoints.", -dmg) % {"amount": -dmg}, MSG_DAMAGE_RECEIVED, value = -1 * dmg, color = textColor, pos=self.position)

            elif by and not self.target and self.data["health"] < 1:
                self.follow(by) # If I'm a creature, set my target

            self.modifyHealth(dmg)

            if by and self.data["health"] < 1:
                by.target = None
                by.targetMode = 0
                if by.isPlayer():
                    by.cancelTarget()

            return True
        else:
            return False

    def onHeal(self, by, amount):
        if self.data["healthmax"] != self.data["health"]:
            if by and by.isPlayer() and by != self:
                by.message(_lp(by, "%(who)s gain %(amount)d hitpoint.", "%(who)s gain %(amount)d hitpoints.", amount) % {"who": self.name().capitalize(), "amount": amount}, MSG_HEALED, value = amount, color = COLOR_GREEN, pos=self.position)

            if self.isPlayer():
                if by is self:
                    self.message(_lp(self, "You healed yourself for %(amount)d hitpoint.", "You healed yourself for %(amount)d hitpoints.", amount)  % {"amount": amount}, MSG_HEALED, value = amount, color = COLOR_GREEN, pos=self.position)
                elif by is not None:
                    self.message(_lp(self, "You gain %(amount)d hitpoint due to healing by %(who)s.", "You gain %(amount)d hitpoints due to healing by %(who)s.", amount)  % {"amount": amount, "who": by.name().capitalize()}, MSG_HEALED, value = amount, color = COLOR_GREEN, pos=self.position)
                else:
                    self.message(_lp(self, "You gain %d hitpoint.", "You gain %d hitpoints.", amount) % amount, MSG_HEALED, value = amount, color = COLOR_GREEN, pos=self.position)
             
                self.modifyHealth(amount)
        else:
            return False
            
    def addDamager(self, creature):
        self.lastDamagers.appendleft((creature, time.time()))
    def addSupporter(self, creature):
        self.lastSupporters.appendleft((creature, time.time()))
    def getLastDamager(self):
        return self.lastDamagers[0][0]
    def getLastSupporter(self):
        return self.lastDamagers[0][0]
            
class PlayerAttacks(CreatureAttacks):
    # Damage calculation:
    def damageToBlock(self, dmg, type):
        if dmg > 0:
            return int(dmg)

        if type == MELEE or type == PHYSICAL:
            # Armor and defence
            armor = 0
            defence = 0
            extradef = 0

            for item in self.inventory:
                if item:
                    armor += item.armor or 0
                    extradef += item.extradef or 0
                    block = (item.absorbPercentPhysical or 0) + (item.absorbPercentAll or 0)
                    if block:
                        dmg += (-dmg * block / 100.0)

            if self.inventory[SLOT_LEFT]:
                defence = self.inventory[SLOT_LEFT].defence
            elif self.inventory[SLOT_RIGHT]:
                defence = self.inventory[SLOT_RIGHT].defence

            if not defence:
                defence = 0
                
            defence += extradef
            defRate = 1
            if self.modes[1] == OFFENSIVE:
                defRate = 0.5
            elif self.modes[1] == BALANCED:
                defRate = 0.75

            if random.randint(1, 100) <= defence * defRate:
                self.lmessage("You blocked an attack!")
                self.magicEffect(EFFECT_BLOCKHIT)
                return 0

            # Apply some shielding effects
            dmg  = int((dmg + random.uniform(armor*0.475, (armor*0.95)-1)) + ((-dmg * armor) / 100.0))
            if dmg > 0:
                return 0
            else:
                return dmg
        else:
            # Damage types other than physical
            attrs = { FIRE: 'absorbPercentFire', ICE: 'absorbPercentIce', ENERGY: 'absorbPercentEnergy', EARTH: 'absorbPercentEarth', HOLY: 'absorbPercentHoly', DEATH: 'absorbPercentDeath', DROWN: 'absorbPercentDrown' }
            absorb = 0
            if not type in attrs: return dmg # Not implanted, or something entierly custom?
            for item in self.inventory:
                if item:
                    absorb += (item.absorbPercentAll or 0) + (getattr(item, attrs[type]) or 0)
                    if item.charges and absorb > 0:
                        item.useCharge()

            dmg -= int(dmg * absorb/100.0)
        return dmg

    def attackTarget(self, dmg = None):
        if dmg:
            assert dmg < 0, "Damage must be negative"
          
        atkRange = 1
        weapon = self.inventory[SLOT_RIGHT]
        ammo = None
        ok = True

        if weapon and weapon.range:
            atkRange = weapon.range
            # This is probably a slot consuming weapon.
            ammo = self.inventory[SLOT_AMMO]
            if weapon.ammoType == "bolt" and (not ammo or ammo.ammoType != "bolt" or ammo.count <= 0):
                self.cancelMessage("You are out of bolts.")
                ok = False
            elif weapon.ammoType == "arrow" and (not ammo or ammo.ammoType != "arrow" or ammo.count <= 0):
                self.cancelMessage("You are out of arrows.")
                ok = False
        
        if ok and self.target and self.target.isAttackable(self) and self.inRange(self.target.position, atkRange, atkRange):
            if not self.target.data["health"]:
                self.target = None
            else:
                atkType = MELEE
                factor = 1
                if self.modes[1] == BALANCED:
                    factor = 0.75
                elif self.modes[1] == DEFENSIVE:
                    factor = 0.5

                if not self.inventory[5]:
                    skillType = SKILL_FIST
                    if dmg is None:
                        dmg = -random.randint(0, round(config.meleeDamage(1, self.getActiveSkill(skillType), self.data["level"], factor)))

                elif not dmg and atkRange > 1:
                    # First, hitChance.
                    defaultMax = 75
                    base = 1.25
                    baseRange = 4
                    if weapon.slotType == "two-handed":
                        defaultMax = 90
                        base = 1.25 * 1.2
                        baseRange = 6
                    
                    distance = baseRange - self.distanceStepsTo(self.target.position)
                    chance = 50 # XXX: chance for spears, to be corrected
                  
                    if not weapon.breakChance:
                        chance = min((ammo.maxHitChance or defaultMax), self.getActiveSkill(SKILL_DISTANCE) * (base ** distance) * (ammo.hitChance or 1))

                    animation = ANIMATION_ROYALSPEAR
                    # spears
                    if weapon.breakChance:
                        animation = weapon.shootType
                        if random.randint(1, 100) < weapon.breakChance:
                            weapon.modify(-1)
                    # ammo
                    else:
                        animation = ammo.shootType
                        ammo.modify(-1)
                    # shoot effect
                    self.shoot(self.position, self.target.position) # animation
                    
                    if chance < random.randint(1,100):
                        self.message("You missed!")
                        self.targetChecker = call_later(config.meleeAttackSpeed, self.attackTarget)
                        return
                    
                    minDmg = config.minDistanceDamage(self.data["level"])
                    maxDmg = config.distanceDamage((weapon.attack or 0) + (ammo.attack if ammo else 0), self.getActiveSkill(SKILL_DISTANCE), factor)
                    
                    dmg = -random.randint(round(minDmg), round(maxDmg))
                    
                    skillType = SKILL_DISTANCE
                    atkType = DISTANCE
                    
                    # Critical hit
                    if config.criticalHitRate > random.randint(1, 100):
                        dmg = dmg * config.criticalHitMultiplier
                        self.criticalHit()
                    # Charges.
                    if self.inventory[5].charges:
                        self.inventory[5].useCharge()

                else:
                    skillType = self.inventory[5].weaponSkillType

                    if dmg is None:
                        dmg = -random.randint(0, round(config.meleeDamage(self.inventory[5].attack, self.getActiveSkill(skillType), self.data["level"], factor)))

                        # Critical hit
                        if config.criticalHitRate > random.randint(1, 100):
                            dmg = dmg * config.criticalHitMultiplier
                            self.criticalHit()

                        # Use charge.
                        if self.inventory[5].charges:
                            self.inventory[5].useCharge()

                targetIsPlayer = self.target.isPlayer() # onHit might remove this.
                target = self.target

                if dmg:
                    """if self.target.isPlayer() and (self.target.data["level"] <= config.protectionLevel and self.data["level"] <= config.protectionLevel):
                            self.cancelTarget()
                            self.cancelMessage(_l(self, "In order to engage in combat you and your target must be at least level %s." % config.protectionLevel))
                    else:
                        self.target.onHit(self, dmg, MELEE)
                        self.skillAttempt(skillType)"""
                    
                    target.onHit(self, dmg, atkType)
                    
                    if skillType != SKILL_FIST:
                        # weapon elemental damage
                        # XXX: What about elemental arrows when skillType == SKILL_DISTANCE?
                        weapon = self.inventory[SLOT_RIGHT]
                        if skillType == SKILL_DISTANCE and not weapon.breakChance: # not a spear
                            weapon = self.inventory[SLOT_AMMO]

                        if weapon.elementFire:
                            target.onHit(self, -weapon.elementFire, FIRE)
                        if weapon.elementIce:
                            target.onHit(self, -weapon.elementIce, ICE)
                        if weapon.elementEarth:
                            target.onHit(self, -weapon.elementEarth, EARTH)                        
                        if weapon.elementEnergy:
                            target.onHit(self, -weapon.elementEnergy, ENERGY)
                        if weapon.elementHoly:
                            target.onHit(self, -weapon.elementHoly, HOLY)
                        if weapon.elementDeath:
                            target.onHit(self, -weapon.elementDeath, DEATH)
                        if weapon.elementDrown:
                            target.onHit(self, -weapon.elementDrown, DROWN)
                        if weapon.elementLifedrain:
                            target.onHit(self, -weapon.elementLifedrain, LIFEDRAIN)
                        
                    self.skillAttempt(skillType)
                else:
                    target.magicEffect(EFFECT_BLOCKHIT)
                    
                if targetIsPlayer:
                    self.lastDmgPlayer = time.time()
                    # If target do not have a green skull.
                    if target.getSkull(self) != SKULL_GREEN:
                        # If he is unmarked.
                        if config.whiteSkull and target.getSkull(self) not in (SKULL_ORANGE, SKULL_YELLOW) and target.getSkull(self) not in SKULL_JUSTIFIED:
                            self.setSkull(SKULL_WHITE)
                        elif config.yellowSkull and (target.getSkull(self) == SKULL_ORANGE or target.getSkull() in SKULL_JUSTIFIED):
                            # Allow him to fight back.
                            if self.getSkull(target) == SKULL_NONE:
                                self.setSkull(SKULL_YELLOW, target, config.loginBlock)
                if config.loginBlock:
                    # PZ block.
                    self.condition(Condition(CONDITION_INFIGHT, length=config.loginBlock), CONDITION_REPLACE)
                    if targetIsPlayer:
                        self.condition(Condition(CONDITION_PZBLOCK, length=config.loginBlock), CONDITION_REPLACE)

        if self.target:
            self.targetChecker = call_later(config.meleeAttackSpeed, self.attackTarget)

    def criticalHit(self):
        self.message(_l(self, "You strike a critical hit!"), MSG_STATUS_CONSOLE_RED)

    def cancelTarget(self, streamX=None):
        if not streamX:
            stream = self.packet()
        else:
            stream = streamX
        if self.target:
            self.target.scripts["onNextStep"] = [a for a in self.target.scripts["onNextStep"] if a != self.followCallback]
            """try:
                self.targetChecker.cancel()
            except:
                pass"""
            #self.walkPattern  =deque()
            
            stream.cancelTarget()
        
            if not streamX:
                stream.send(self.client)

    def setAttackTarget(self, cid):
        if self.targetMode == 1 and self.target:
            self.targetMode = 0
            self.target = None
            self.cancelTarget()
            return

        if time.time() - self.lastStairHop < config.stairHopDelay:
            self.cancelTarget()
            self.message("You can't attack so fast after changing level or teleporting.")
            return
        
        if cid in game.creature.allCreatures:
            if game.creature.allCreatures[cid].isAttackable(self):
                target = game.creature.allCreatures[cid]
                if target.isPlayer() and self.modes[2]:
                    self.cancelTarget()
                    self.unmarkedPlayer()
                    return
                ret = game.scriptsystem.get('target').run(creature=self, creature2=target, attack=True)
                if ret == False:
                   self.cancelTarget()
                   return
                elif ret != None:
                    self.target = ret
                else:
                    self.target = target

                self.targetMode = 1
                if not target.target and isinstance(target, game.monster.Monster):
                    target.target = self
                    target.targetMode = 1
            else:
                self.cancelTarget()
                return
        else:
            self.cancelTarget()
            self.notPossible()
            return
        if not self.target:
            self.cancelTarget()
            self.notPossible()
            return

        if self.modes[1] == CHASE:
            print("did")
            self.walk_to(self.target.position, -1, True)
            self.target.scripts["onNextStep"].append(self.followCallback)

        if not self.targetChecker or not self.targetChecker.active():
            self.attackTarget()
            
    def isAttackable(self, creature):
        if creature.isMonster() and not creature.base._invisible and self.hasCondition(CONDITION_INVISIBLE):
            return False
        return True

