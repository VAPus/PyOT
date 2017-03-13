JUNGLE_GRASS_TRANSFORM = {2782, 3985}
JUNGLE_GRASS_REMOVE = {1499}
SPIDER_WEB = {7538, 7539}

@register("useWith", (2420, 2442))
def onUseWith(onThing, onPosition, **k):
    if onThing.itemId in JUNGLE_GRASS_REMOVE:
        onThing.transform(0)
    elif onThing.itemId in JUNGLE_GRASS_TRANSFORM:
        onThing.transform(onThing.itemId - 1)
        onThing.decay()
    elif onThing.itemId in SPIDER_WEB:
        onThing.transform(onThing.itemId + 6)
        onThing.decay()