@register("talkactionFirstWord", '/t')
@access("TELEPORT")
def teleportToTemple(creature, text):
    online = {}
    for name in game.player.allPlayers:
        player = game.player.allPlayers[name]
        if player.alive and player.client.ready:
            import data.map.info
            online[player.name().lower()] = data.map.info.towns[player.data["town_id"]][1]
    if not text:
        return False
    try:
        x,y,z = online[text.lower()]
        player2 = game.player.allPlayers[text.title()]
        player2.teleport(Position(x,y,z))
    except:
        creature.lmessage(text+" is not an online player.")
    else:
        player2.magicEffect(EFFECT_TELEPORT)
    return False
@register("talkaction", '/t')
@access("TELEPORT")
def teleportToTemple2(creature, text):
    import data.map.info
    x,y,z = data.map.info.towns[creature.data["town_id"]][1]
    try:
        creature.teleport(Position(x,y,z))
    except:
        creature.lmessage("You can't go there!")
    else:
        creature.magicEffect(EFFECT_TELEPORT)
    return False