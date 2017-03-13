@register("talkactionRegex", r"/ban (?P<player>\w+) (?P<length>\d+) ?(?P<reason>.*)")
@access("BAN")
def banPlayer(creature, player, length, reason, **k):
    player = getPlayer(player)
    
    if not player:
        creature.message("Player %s cannot be found" % player.name())
        return False
    
    if playerIsBanned(player):
        creature.message("Player %s is already banned" % player.name())
        return False
        
    addBan(creature, BAN_PLAYER, player.data["id"], reason, int(length))
    
    creature.message("Player %s has been banned." % player.name())
    return False
    
@register("talkactionRegex", r"/ipban (?P<playerIp>[.\w]+) (?P<length>\d+) ?(?P<reason>.*)")
@access("BAN")
def banIp(creature, playerIp, length, reason, **k):
    
    player = getPlayer(playerIp)
    ip = playerIp
    
    if player:
        ip = player.getIP()
        
    if ipIsBanned(ip):
        creature.message("Ip %s is already banned!" % ip)
        return False
    
    # Assume ipv4.
    if len(ip.split(".")) != 4:
        creature.message("Invalid IP")
        return
        
    try:
        for part in ip.split("."):
            if int(part) > 255 or int(part) < 0:
                creature.message("Invalid IP")
                return
    except:
        creature.message("Invalid IP")
        return
        
        
    addBan(creature, BAN_IP, ip, reason, int(length))
    
    creature.message("Ip %s has been banned." % ip)
    return False
    
@register("talkactionRegex", r"/accban (?P<account>\w+) (?P<length>\d+) ?(?P<reason>.*?)")
@access("BAN")
def banAccount(creature, account, length, reason, **k):
    if accountIsBanned(account):
        creature.message("account %s is already banned" % account)
        return False
        
    # XXX No vertification.
    addBan(creature, BAN_ACCOUNT, account, reason, int(length))
    
    creature.message("Account %s has been banned." % account)
    return False