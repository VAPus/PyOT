"""import game.scriptsystem
import game.item

# Magicly transform closed doors to open doors!
def addMapItem(creature, thing, options):
    if game.item.items[thing.itemId+1]["name"] == "open door":
        item = game.item.Item(thing.itemId+1, **options)
    else:
        item = game.item.Item(1238, **options)
        
    return item # Must always do that

lockedDoors = 1219, 1221, 1209, 1212, 1231, 1234, 1249, 1252, 3535, 3544, 4913, 4916, 5098, 5107, 5116, 5125, 5134, 5137, 5140, 5143, 5278, 5281, 5732, 5735, 6192, 6195, 6249, 6252, 6891, 6900, 7033, 7042, 8541, 8544, 9165, 9168, 9267, 9270, 10268, 10271, 10468, 10477
game.scriptsystem.get("addMapItem").register(lockedDoors, addMapItem)"""