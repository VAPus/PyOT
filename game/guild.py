guilds = {}
guild_names = {}

def getGuildById(id):
    " Get guild by guild id."
    try:
        return guilds[id]
    except:
        return None
        
def getGuildByName(name):
    " Get guild based on guild name."
    try:
        return guild_names[name]
    except:
        return None
        
def guildExists(id):
    " Does a guild with this id exist. Basically a bool version of :func:`getGuildById` "
    if getGuildById(id) is not None:
        return True
    else:
        return False
        
class Guild(object):
    def __init__(self, id, name, motd, balance):
        self.id = id
        self.name = name
        self.ranks = {} # rankId -> GuildRank
        self.motd = motd
        self.balance = balance
        self.chatChannel = game.chat.openInstanceChannel(name, CHANNEL_GUILD)
        
    # Creature alike money interface.
    def setMoney(self, amount):
        " Set the guild balance to `amount` "
        self.balance = amount
        sql.runOperation("UPDATE guilds SET balance = %sd WHERE guild_id = %s", amount, self.id)
        
    def getMoney(self):
        " Return the guild balance. "
        return self.balance
    
    def removeMoney(self, amount):
        " Remove `amount` from the guild balance. "
        self.balance -= amount
        sql.runOperation("UPDATE guilds SET balance = %s WHERE guild_id = %s", self.balance, self.id)
        
    def addMoney(self, amount):
        " Add `amount` to the guild balance. "
        self.balance += amount
        sql.runOperation("UPDATE guilds SET balance = %s WHERE guild_id = %s", self.balance, self.id)
        
    def setMotd(self, motd):
        " Set the guild motd. "
        self.motd = motd
        sql.runOperation("UPDATE guilds SET motd = %s WHERE guild_id = %s", motd, self.id)
        
    def setName(self, name):
        " Set guild name. "
        self.name = name
        sql.runOperation("UPDATE guilds SET name = %s WHERE guild_id = %s", name, self.id)
        
    def rank(self, rankId):
        " Return guild rank based on id. "
        return self.ranks[rankId]
    
    
class GuildRank(object):
    def __init__(self, guild_id, rank_id, title, permissions):
        self.guild_id = guild_id
        self.rank_id = rank_id
        self.title = title
        self.permissions = permissions
        
    def isMember(self):
        " Is this guildrank a member of the guild. "
        return self.permissions & GUILD_MEMBER
    
    def isLeader(self):
        " Is this guildrank a leader of the guild. "
        return self.permissions & GUILD_LEADER
    
    def isSubLeader(self):
        " Is this guildrank a subleader of the guild. "
        return self.permissions & GUILD_SUBLEADER
        
    def permission(self, permission):
        " Check other guild permissions (like permission setting, promotion etc) using a `permission` constant. "
        return self.permissions & permission
    
    def guild(self):
        " Return the guild object for this rank. "
        return guilds[self.guild_id]
        
def make_guild(name, motd='', balance=0, _id=1):
    # TODO: SQL Query!
    guild = Guild(_id, name, motd, balance)
    guilds[_id] = guild
    guild_names[name] = guild
    
    return guild
    
@gen.coroutine
def load():
    " Initial load of the guilds. Shouldn't be used after loading. "
    # Guilds
    for entry in (yield sql.runQuery("SELECT guild_id, name, motd, balance FROM `guilds` WHERE world_id = %s", config.worldId)):
        guild = Guild(int(entry['guild_id']), entry['name'], entry['motd'], int(entry['balance']))
        guilds[int(entry['guild_id'])] = guild
        guild_names[entry['name']] = guild
        
    # Ranks
    if guilds:
        for entry in (yield sql.runQuery("SELECT guild_id, rank_id, title, permissions FROM `guild_ranks` WHERE guild_id IN %s" % repr(tuple(guilds.keys())))):
            guilds[int(entry['guild_id'])].ranks[entry['rank_id']] = GuildRank(int(entry['guild_id']), entry['rank_id'], entry['title'], entry['permissions'])
