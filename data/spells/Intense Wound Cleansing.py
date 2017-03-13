instant = spell.Spell("Intense Wound Cleansing", "exura gran ico", icon=158, target=TARGET_SELF, group=HEALING_GROUP)
instant.require(mana=200, level=80, maglevel=0, learned=0, vocations=(4, 8))
instant.cooldowns(180, 1)
instant.effects(caster=EFFECT_MAGIC_BLUE)
instant.targetEffect(callback=spell.heal(10, 20, 8, 11)) #incorrect