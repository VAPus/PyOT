conjure = spell.Spell("Animate Dead", "adana mort", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=600, level=27, maglevel=0, soul=5, learned=0, vocations=(1, 2, 5, 6))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2316, 1))

# Incomplete! Field rune.
rune = spell.Rune(2316, icon=83, count=1, target=TARGET_AREA, group=SUPPORT_GROUP)
rune.cooldowns(0, 3)
rune.require(mana=0, level=27, maglevel=0)
rune.targetEffect() # TODO
rune.effects() # TODO