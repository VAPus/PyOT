classes = {'red':MSG_STATUS_CONSOLE_RED, 'white':MSG_EVENT_ADVANCE, 'green':MSG_INFO_DESCR, 'warning':MSG_STATUS_WARNING}

# /b msg;color
# /ba is the same, except it doesn't show your nickname.

@register("talkactionFirstWord", "/ba")
@access("TALK_RED")

def broadcastMessageAnonymously(creature, text):
    msgclass = MSG_STATUS_WARNING
    msgcolor = 'warning'
    if not text or text.count(';') > 1:
        return False
		
    split = text.split(";")

    if len(split) == 2:
        msg, msgcolor = split
    else:
        msg = text

    try:
        msgclass = classes[msgcolor.lower().strip()]
    except:
        pass
        
    for name in game.player.allPlayers:
        player = game.player.allPlayers[name]
        if player.alive and player.client.ready:
            player.message(msg, msgclass)
    return False

@register("talkactionFirstWord", "/b")
@access("TALK_RED")

def broadcastMessage(creature, text):
	return broadcastMessageAnonymously(creature, creature.name() + ": " + text)