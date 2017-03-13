# Itemid 8693, 7700 when used you temporarily converted into Dwarf Geomancer/Amazon

CONSTRUCTIONS = {\
3901: 1652, 3902: 1658, 3903: 1666, 3904: 1670, 3905: 3813, 3906: 3817, 3907: 3821, 3908: 1619, 3909: 1614, 3910: 1615,
3911: 1616, 3912: 2604, 3913: 3805, 3914: 3807, 3915: 1716, 3916: 1724, 3917: 1728, 3918: 1732, 3919: 3809, 3920: 3811,
3921: 2084, 3922: 2095, 3923: 2098, 3924: 2064, 3925: 1674, 3926: 2080, 3927: 1442, 3928: 1446, 3929: 2034, 3930: 1447,
3931: 2101, 3932: 1774, 3933: 2105, 3934: 2117, 3935: 2582, 3936: 3832, 3937: 1775, 3938: 1750, 5086: 5056, 5087: 5055,
5088: 5046, 6114: 6109, 6115: 6111, 6372: 6356, 6373: 6371, 8692: 8688, 9974: 9975, 7960: 10515, 7961: 10511, 7962: 10513,
7503: 1750, 11126: 11127, 11124: 11125, 11133: 1129
}

@register("use", CONSTRUCTIONS.keys())
def onUse(creature, thing, position, **k):
    if position.x == INVENTORY_POSITION:
        creature.cancelMessage("Put the construction kit on the floor first.")
    elif not getHouseByPos(position):
        creature.cancelMessage("You may construct this only inside a house.")
    elif thing.itemId in CONSTRUCTIONS:
        thing.transform(CONSTRUCTIONS[thing.itemId])
        magicEffect(position, EFFECT_POFF)
    else:
        return
    
    return True