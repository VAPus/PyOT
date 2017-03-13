instant = spell.Spell("Practise Healing", "exura dis", icon=1, target=TARGET_SELF, group=HEALING_GROUP)
instant.require(mana=5, level=1, maglevel=0, learned=0, vocations=(1, 2, 3, 4, 5, 6, 7, 8))
instant.cooldowns(1, 1)
instant.effects(caster=EFFECT_MAGIC_BLUE)
instant.targetEffect()#TODO