conjure = spell.Spell("Cure Poison Rune", "adana pox", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=200, level=15, maglevel=0, soul=1, learned=0, vocations=(2, 6))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2266, 1))

# Incomplete! Target rune.
rune = spell.Rune(2266, icon=31, count=1, target=TARGET_TARGET, group=HEALING_GROUP)
rune.cooldowns(0, 1)
rune.require(mana=0, level=15, maglevel=0)
rune.targetEffect() # TODO
rune.effects() # TODO