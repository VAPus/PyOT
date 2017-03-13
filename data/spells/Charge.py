instant = spell.Spell("Charge", "utani tempo hur", icon=131, target=TARGET_SELF, group=SUPPORT_GROUP)
instant.require(mana=100, level=25, maglevel=0, learned=0, vocations=(4, 8))
instant.cooldowns(2, 3)

def newspeed(creature, attribute, make):
    baseSpeed = min(220.0 + (2 * creature.data["level"]-1), 1500.0)
    if make:
        return baseSpeed + round((creature.data["level"] * 1.8 + 123.3)/2, 1) * 2
    else:
        return baseSpeed
        
instant.casterCondition(Boost("speed", newspeed, 5))

instant.effects(caster=EFFECT_MAGIC_GREEN)