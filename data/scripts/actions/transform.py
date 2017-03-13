transformOnUse = {}
transformEquipTo = {}
transformDeEquipTo = {}

_items = game.item.items
for itemId in _items:
    _attr = _items[itemId]
    if "transformOnUse" in _attr:
        transformOnUse[itemId] = _attr["transformOnUse"]
    if "transformEquipTo" in _attr:
        transformEquipTo[itemId] = _attr["transformEquipTo"]
    if "transformDeEquipTo" in _attr:
        transformDeEquipTo[itemId] = _attr["transformDeEquipTo"]

@register("use", transformOnUse.keys())
def onUse(thing, **k):
    thing.transform(transformOnUse[thing.itemId])

@register("equip", transformEquipTo.keys())
def onEquip(thing, **k):
    thing.transform(transformEquipTo[thing.itemId])

@register("unequip", transformDeEquipTo.keys())
def onDeEquip(thing, **k):
    thing.transform(transformDeEquipTo[thing.itemId])

