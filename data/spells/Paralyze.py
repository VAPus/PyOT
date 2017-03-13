conjure = spell.Spell("Paralyze", "adana ani", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=1400, level=54, maglevel=0, soul=3, learned=0, vocations=(2, 6))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2278, 1))

# Incomplete! Target rune.
rune = spell.Rune(2278, icon=54, count=1, target=TARGET_TARGET, group=SUPPORT_GROUP)
rune.cooldowns(0, 2)
rune.require(mana=1400, level=54, maglevel=0)
rune.targetEffect() # TODO
rune.effects(target=EFFECT_MAGIC_RED)