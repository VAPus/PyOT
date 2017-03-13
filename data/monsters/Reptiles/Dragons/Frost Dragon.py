frost_dragon = genMonster("Frost Dragon", 248, 7091)
frost_dragon.health(1800)
frost_dragon.type("undead")
frost_dragon.defense(armor=42, fire=0, earth=0, energy=1, ice=0, holy=1, death=0.9, physical=0.95, drown=1)
frost_dragon.experience(2100)
frost_dragon.speed(260)
frost_dragon.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=250)
frost_dragon.walkAround(energy=1, fire=0, poison=0)
frost_dragon.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
frost_dragon.voices("YOU WILL FREEZE!", "ZCHHHHH!", "I am so cool.", "Chill out!")
frost_dragon.loot( (2148, 100, 245), ("dragon ham", 77.5, 5), ("power bolt", 21.0, 6), ("golden mug", 3.0), ("energy ring", 5.0), ("small sapphire", 5.0), ("green mushroom", 12.0), ("ice cube", 4.0), ("book", 9.0), ("life crystal", 0.5), ("dragon scale mail", 0.0025), ("shard", 0.5), ("tower shield", 0.25), ("ice rapier", 0.25), ("strange helmet", 0.5), ("dragon slayer", 0.0025), ("royal helmet", 0.25) )

#Smoke Strike (0-200; does Physical Damage), Smoke Wave (0-380; does Life Drain), Ice Wave (very strong Paralyze), Avalanche (strong Paralyze), Ice Berserk (0-120), Smoke Berserk (strong Paralyze), Haste.
frost_dragon.melee(220)
frost_dragon.selfSpell("Light Healing", 180, 220, check=chance(18))
frost_dragon.targetSpell(2274, 0, 240, check=chance(20)) #avalache