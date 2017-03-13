conjure = spell.Spell("Enchant Spear", "exeta con", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=350, level=45, maglevel=0, soul=3, learned=0, vocations=(3, 7))
conjure.use(2389)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(7367, 1))
#requires a spear