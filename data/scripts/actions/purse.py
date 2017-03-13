ALLOWED_ITEMS = ()

@register("dropOnto", 'purse')
def dragOnPurse(creature, thing, onThing, onPosition, **k):
    if thing not in ALLOWED_ITEMS:
        creature.lmessage("You can't place this item in a purse")
        return False
