item = {
9808: ((2464, "Chain Armor", 33), (2483, "Scale Armor", 25), (2465, "Brass Armor", 10), (2463, "Plate Armor", 2)),

9809: ((2464, "Chain Armor", 16), (2465, "Brass Armor", 14), (2483, "Scale Armor", 13), (2463, "Plate Armor", 10),
(2476, "Knight Armor", 6), (8891, "Paladin Armor", 3), (2487, "Crown Armor", 1)),

9810: ((2464, "Chain Armor", 20), (2465, "Brass Armor", 17), (2483, "Scale Armor", 15), (2463, "Plate Armor", 12),
(2476, "Knight Armor", 10), (8891, "Paladin Armor", 5), (2487, "Crown Armor", 4), (2466, "Golden Armor", 2), (2472, "Magic Plate Armor", 1)),

9811: ((2468, "Studded Legs", 33), (2648, "Chain Legs", 25), (2478, "Brass Legs", 10), (2647, "Plate Legs", 2)),

9812: ((2468, "Studded Legs", 16), (2648, "Chain Legs", 14), (2478, "Brass Legs", 13), (2647, "Plate Legs", 10),
(2477, "Knight Legs", 6), (2488, "Crown Legs", 1)),

9813: ((2478, "Brass Legs", 17), (2647, "Plate Legs", 12), (2477, "Knight Legs", 10), (2488, "Crown Legs", 4), (2470, "Golden Legs", 2))
}

effect_broke = 3
effect_renew = 28

@register("useWith", 9930)
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    developed = None
    const = onThing.itemId
    
    if const in item:
        random_item = random.randint(1, 100)
        
        for i in item[const]:
            if random_item <= i[2]:
                developed = i
        
        if developed:
            magicEffect(onPosition, effect_renew)
            onThing.transform(developed[0])
            creature.lmessage("You have renewed the %s !" % (developed[1]))
            thing.modify(-1)
            
        else:
            magicEffect(onPosition, effect_broke)
            onThing.modify(-1)
            thing.modify(-1)
            creature.lmessage("Your Rusty Remover has broken.")
            return
            
    else:
        creature.lmessage("Use it on Rusty Items (Common, Semi-Rare or Rare: Armors or Legs).")
        return
