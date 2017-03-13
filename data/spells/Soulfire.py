conjure = spell.Spell("Soulfire", "adevo res flam", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=600, level=27, maglevel=0, soul=3, learned=0, vocations=(1, 2, 5, 6))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2308, 3))

# Incomplete! Target rune.
rune = spell.Rune(2308, icon=50, count=3, target=TARGET_TARGET, group=ATTACK_GROUP)
rune.cooldowns(0, 2)
rune.require(mana=0, level=27, maglevel=0)
rune.targetEffect() # TODO
rune.effects(area=EFFECT_HITBYFIRE, shoot=ANIMATION_FIRE)