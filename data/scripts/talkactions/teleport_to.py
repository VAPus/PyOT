@register("talkactionFirstWord", '/goto')
@access("TELEPORT")
def teleportTo(creature, text):
    online = {}
    for id in game.creature.allCreatures:
        obj = game.creature.allCreatures[id]
        online[obj.name().lower()] = obj.position
    if not text:
        creature.lmessage("Command param required.")
        return False
    try:
        creature.teleport(online[text.lower()])
    except:
        try:
            x,y,z = text.split(',')
        except:
            creature.lmessage("Invalid parameter.")
        else:
            try:
                creature.teleport(Position(int(x),int(y),int(z)))
            except:
                creature.lmessage("Can't teleport to solid tiles!")
            else:  
                creature.magicEffect(EFFECT_TELEPORT)
        return False
    else:
        creature.magicEffect(EFFECT_TELEPORT)
        return False 