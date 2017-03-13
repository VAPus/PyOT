Parrot = genMonster("Parrot", 217, 6056)
Parrot.targetChance(0)
Parrot.type("blood")
Parrot.health(25)
Parrot.experience(0)
Parrot.speed(320) #corect
Parrot.walkAround(1,1,1) # energy, fire, poison
Parrot.behavior(summonable=250, hostile=False, illusionable=True, convinceable=250, pushable=False, pushItems=False, pushCreatures=False, targetDistance=0, runOnHealth=25)
Parrot.voices("You advanshed, you advanshed!", "Neeewbiiieee!", "Screeech!", "Hunterrr ish PK!", "BR? PL? SWE?", "Hope you die and loooosh it!", "You powerrrrrrabuserrrrr!", "You are corrrrupt! Corrrrupt!", "Tarrrrp?", "Blesshhh my stake! Screeech!", "Leeave orrr hunted!!", "Shhtop whining! Rraaah!", "I'm heeerrre! Screeeech!")
Parrot.immunity(0,0,0) # paralyze, invisible, lifedrain
Parrot.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Parrot.melee(5)#summons only? probably incorrect information