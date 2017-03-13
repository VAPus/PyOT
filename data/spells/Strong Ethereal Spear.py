instant = spell.Spell("Strong Ethereal Spear", "exori gran con", icon=57, group=ATTACK_GROUP)
instant.require(mana=55, level=90, maglevel=0, learned=0, vocations=(3, 7))
instant.cooldowns(8, 2)
instant.targetEffect(callback=spell.damage(2, 4, 7, 13, HOLY)) #unknown distance based?
instant.effects(shoot=ANIMATION_ETHEREALSPEAR) #incorrent?