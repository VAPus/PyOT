instant = spell.Spell("Haste", "utani hur", icon=6, target=TARGET_SELF, group=SUPPORT_GROUP)
instant.require(mana=60, level=14, maglevel=0, learned=0, vocations=(1, 2, 3, 4, 5, 6, 7, 8))
instant.cooldowns(2, 3)

def newspeed(creature, attribute, make):
    baseSpeed = min(220.0 + (2 * creature.data["level"]-1), 1500.0)
    if make:
        return (baseSpeed * 1.3) - 24
    else:
        return baseSpeed
        
instant.casterCondition(Boost("speed", newspeed, 31)) #31 or 33?

instant.effects(caster=EFFECT_MAGIC_GREEN)