instant = spell.Spell("Strong Haste", "utani gran hur", icon=39, target=TARGET_SELF, group=SUPPORT_GROUP)
instant.require(mana=100, level=20, maglevel=0, learned=0, vocations=(1, 2, 5, 6))
instant.cooldowns(2, 3)

def newspeed(creature, attribute, make):
    baseSpeed = min(220.0 + (2 * creature.data["level"]-1), 1500.0)
    if make:
        return (baseSpeed * 1.7) - 56
    else:
        return baseSpeed
        
instant.casterCondition(Boost("speed", newspeed, 22))

instant.effects(caster=EFFECT_MAGIC_GREEN)