@register("talkactionFirstWord", "/a")
@register("talkaction", "/a")
@access("TELEPORT")
def teleportTiles(creature, text): #/a value,force *force is opitional
    number = 0
    force_teleport = False
    force = ''
    try:
        value,force = text.split(',')
    except:
        value = text
    if not value or text == "/a": # "/a" and "/a "
        value = 1
    if force.lower().strip() in {'y', 'yes', 'true', '1'}:
        force_teleport = True
    try:
        number = int(value)
    except:
        creature.message("Invalid parameter")
        return False
    if number > 0:
        teleporta = creature.position.copy()
        if creature.direction == WEST:
            teleporta.x -= number
        if creature.direction == EAST:
            teleporta.x += number
        if creature.direction == NORTH:
            teleporta.y -= number
        if creature.direction == SOUTH:
            teleporta.y += number
        try:
            creature.teleport(teleporta, force_teleport)
        except SolidTile: # May rise SolidTile etc
            creature.notPossible()
        else:
            creature.magicEffect(EFFECT_TELEPORT)    
    return False
