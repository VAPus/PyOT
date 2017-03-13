conjure = spell.Spell("Destroy Field", "adito grav", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=120, level=17, maglevel=0, soul=2, learned=0, vocations=(1, 2, 3, 5, 6, 7))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2261, 3))

# Incomplete! Self target rune?
rune = spell.Rune(2261, icon=30, count=3, target=TARGET_TARGET, group=SUPPORT_GROUP)
rune.cooldowns(0, 3)
rune.require(mana=0, level=17, maglevel=0)
rune.targetEffect() # TODO
rune.effects() # TODO