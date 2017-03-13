instant = spell.Spell("Holy Flash", "utori san", icon=143, group=ATTACK_GROUP)
instant.require(mana=50, level=70, maglevel=0, learned=0, vocations=(3, 7))
instant.cooldowns(45, 2)
instant.targetEffect() # TODO
instant.effects() # TODO