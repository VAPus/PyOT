import datetime
from tornado import gen

# XXX: Kill these globals, move into BanEntry.
banAccounts = {}
banPlayers = {}
banIps = {}

class BanEntry(object):
    __slots__ = 'id', 'by', 'time', 'reason'
    
    def __init__(self, id, by, time, reason):
        self.id = id
        self.by = by
        self.time = time
        self.reason = reason
    
    def message(self):
        return "Reason: %s. It will expire: %s" % (self.reason, datetime.datetime.fromtimestamp(self.time).strftime(config.banTimeFormat))
    
    def remove(self):
        global banAccounts
        global banPlayers
        global banIps
        
        # We can't remove until we got our id.
        assert self.id
        
        # Walk over all and remove us. This is ineffective. But not so common.
        found = False
        for entry in banAccounts:
            if banAccounts[entry] is self:
                del banAccounts[entry]
                found = True
                break
                
        if not found:
            found = False
            for entry in banPlayers:
                if banPlayers[entry] is self:
                    del banPlayers[entry]
                    found = True
                    break
                    
        if not found:
            found = False
            for entry in banPlayers:
                if banPlayers[entry] is self:
                    del banPlayers[entry]
                    found = True
                    break
                    
        if not found:
            raise Exception("Ban was not found. Can't remove.")
        
        sql.runOperation("DELETE FROM bans WHERE ban_id = %s", self.id)
        
            
@gen.coroutine    
def refresh():
    global banAccounts, banPlayers, banIps
    _banAccounts = {}
    _banPlayers = {}
    _banIps = {}
    
    _time = time.time()
    
    for entry in (yield sql.runQuery("SELECT ban_id, ban_type, ban_by, ban_data, ban_reason, ban_expire FROM bans WHERE ban_expire > %s", _time)):
        banEntry = BanEntry(entry[0], entry[3], entry[5], entry[4])
        
        if entry[1] == BAN_ACCOUNT:
            accountId = int(entry[3])
            _banAccounts[accountId] = banEntry
            
            # Check if any player use this account.
            for player in game.player.allPlayersObject:
                if player.data["account_id"] == accountId:
                    player.exit("Your account have been banned! \n%s" % banEntry.message())
        elif entry[1] == BAN_PLAYER:
            playerId = int(entry[3])
            _banPlayers[playerId] = banEntry
            
            # Check if player is online.
            for player in game.player.allPlayersObject:
                if player.data["id"] == playerId:
                    player.exit("Your player have been banned! \n%s" % banEntry.message())
                    break
                    
        elif entry[1] == BAN_IP:
            _banIps[entry[3]] = banEntry
            
            # Check if player is online.
            for player in game.player.allPlayersObject:
                if player.getIP() == entry[2]:
                    player.exit("Your ip have been banned! \n%s" % banEntry.message())
                    break
    

    if config.refreshBans:
        call_later(config.refreshBans, refresh)
        
    banAccounts = _banAccounts
    banPlayers = _banPlayers
    banIps = _banIps
    
def ipIsBanned(ip):
    if isinstance(ip, game.player.Player):
        ip = ip.getIP()
        
    try:
        entry = banIps[ip]
        if entry.time > time.time():
            return True
    except:
        return False
        
    return False

def playerIsBanned(player):
    if isinstance(player, game.player.Player):
        player = player.data["id"]
    return player in banPlayers

    try:
        entry = banPlayers[player]
        if entry.time > time.time():
            return True
    except:
        return False
        
    return False

def accountIsBanned(account):
    if isinstance(account, game.player.Player):
        account = account.data["account_id"]

    try:
        entry = banAccounts[account]
        if entry.time > time.time():
            return True
    except:
        return False
        
    return False

@gen.coroutine
def addBan(by, type, data, reason, expire):
    global banAccounts, banPlayers, banIps
    
    if isinstance(by, game.player.Player):
        by = by.data["id"]
        
    expire = time.time() + expire
    banEntry = BanEntry(0, by, expire, reason)
    if type == BAN_ACCOUNT:
        banAccounts[data] = banEntry
        
        for player in game.player.allPlayersObject:
            if player.data["account_id"] == data:
                player.exit("Your account have been banned! \n%s" % banEntry.message())
    elif type == BAN_PLAYER:
        banPlayers[data] = banEntry
        
        for player in game.player.allPlayersObject:
            if player.data["id"] == data:
                player.exit("Your player have been banned! \n%s" % banEntry.message())
                
    elif type == BAN_IP:
        banIps[data] = banEntry
        for player in game.player.allPlayersObject:
            if player.getIP() == data:
                player.exit("Your ip have been banned! \n%s" % banEntry.message())
                
    banEntry.id = yield sql.runOperationLastId("INSERT INTO bans (ban_type, ban_by, ban_data, ban_reason, ban_expire) VALUES(%s, %s, %s, %s, %s)", type, by, data, reason, expire)
        
