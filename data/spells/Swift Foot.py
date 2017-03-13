instant = spell.Spell("Swift Foot", "utamo tempo san", icon=134, target=TARGET_SELF, group=SUPPORT_GROUP)
instant.require(mana=400, level=55, maglevel=0, learned=0, vocations=(3, 7))
instant.cooldowns(2, 10)

def newspeed(creature, attribute, make):
    baseSpeed = min(220.0 + (2 * creature.data["level"]-1), 1500.0)
    if make:
        return baseSpeed + round((creature.data["level"] * 1.6 + 110)/2, 1) * 2
    else:
        return baseSpeed
        
instant.casterCondition(Boost("speed", newspeed, 10))

instant.effects(caster=EFFECT_MAGIC_GREEN)