instant = spell.Spell("Magic Rope", "exani tera", icon=76, target=TARGET_SELF, group=SUPPORT_GROUP)
instant.onPos() #make sure that if we are not standing on a rope spot dont waste mana casting it
instant.require(mana=20, level=9, maglevel=0, learned=0, vocations=(1, 2, 3, 4, 5, 6, 7, 8))
instant.cooldowns(2, 3)
instant.targetEffect(callback=spell.magicRope())    
