from tornado.gen import Return
# Is the war system enabled?
if config.enableWarSystem:
    # Guild war constants.
    GUILD_WAR_INVITE = 0
    GUILD_WAR_REJECT = 1
    GUILD_WAR_PENDING_PAYMENT = 2
    GUILD_WAR_CANCEL = 3
    GUILD_WAR_ACTIVE = 4
    GUILD_WAR_OVER = 5
    
    class WarEntry(object):
        def __init__(self, warId, guild1, guild2, started, duration, frags, stakes):
            self.warId = warId
            self.guild1 = guild1
            self.guild2 = guild2
            self.started = started
            self.duration = duration
            self.frags = frags
            self.stakes = stakes
            self.status = -1
            
            def _(res):
                self.guild1_frags, self.guild2_frags = res
                
            warFrags(warId, guild1, guild2).addCallback(_)
            
                
        def start(self):
            # When to cancel war.
            length = (self.started + self.duration) - time.time()
            if length > 0:
                call_later(length, cancelWar, self)
            else:
                # War might be over already.
                cancelWar(self)
            
        def setStatus(self, status):
            global wars, warObjects, warInvites
            oldStatus = self.status
            
            self.status = status
            
            
            
            if not self.guild1 in wars:
                wars[self.guild1] = [], [], []
                
            if not self.guild2 in wars:
                wars[self.guild2] = [], [], []
                
                
            if status == GUILD_WAR_PENDING_PAYMENT:
                if not checkPayment(self):
                    pendingPayments.append(self)
                else:
                    status = GUILD_WAR_ACTIVE
                    
            if status == GUILD_WAR_ACTIVE:
                if not self.started:
                    self.started = time.time()
                if oldStatus != -1 and status != oldStatus:
                    sql.runOperation("UPDATE guild_wars SET started = %s WHERE war_id = %s", (self.started, warId))
                    
                wars[self.guild1][0].append(self.guild2)
                wars[self.guild1][1].append(self)

                wars[self.guild2][0].append(self.guild1)
                wars[self.guild2][1].append(self)
                
                self.start()
                    
            elif status == GUILD_WAR_INVITE:
                wars[self.guild1][2].append(self)

                wars[self.guild2][2].append(self)
                    
            elif status == GUILD_WAR_OVER:
                cancelWar(self)
                
            if status in (GUILD_WAR_REJECT, GUILD_WAR_CANCEL) or (oldStatus == GUILD_WAR_INVITE and status == GUILD_WAR_PENDING_PAYMENT):
                try:
                    # Ow well.
                    wars[self.guild1][2].remove(self)
                except:
                    pass
                
                try:
                    # Ow well.
                    wars[self.guild2][2].remove(self)
                except:
                    pass
            
            if self.status != status:
                sql.runOperation("UPDATE guild_wars SET status = %s WHERE war_id = %s", (status, warId))
        
        @gen.coroutine
        def insert(self):
            self.warId = yield sql.runOperationLastId("INSERT INTO guild_wars(guild_id, guild_id2, started, duration, frags, stakes, `status`) VALUES(%s, %s, %s, %s, %s, %s, %s)", (self.guild1, self.guild2, self.started, self.duration, self.frags, self.stakes, self.status))
            
    wars = {} # GUILDID -> [guildIds at war], [warObjects at war], [warObjects on invite]
    pendingPayments = []
    
    _oldGetEmblem = game.player.Player.getEmblem
    # New emblem function.
    def getEmblem(self, creature):
        guildId = self.data["guild_id"]
        if guildId:
            if guildId == creature.data["guild_id"]:
                # Same guild.
                return EMBLEM_GREEN
            if guildId in wars:
                if creature.data["guild_id"] in wars[guildId][0]:
                    # We are at war with this guild.
                    return EMBLEM_RED
                    
                # We are at war, but not with him.
                return EMBLEM_BLUE
        
        # Call default function.
        return _oldGetEmblem(self, creature)

    @gen.coroutine
    def warFrags(warId, guild1, guild2):
        entry = yield sql.runQuery("SELECT COUNT((SELECT 1 FROM pvp_deaths d WHERE d.war_id = %s AND (SELECT 1 FROM players p WHERE d.victim_id = p.id AND p.id IN (SELECT player_id FROM player_guild WHERE guild_id = %s)))), COUNT((SELECT 1 FROM pvp_deaths d WHERE d.war_id = %s AND (SELECT 1 FROM players p WHERE d.victim_id = p.id AND p.id IN (SELECT player_id FROM player_guild WHERE guild_id = %s))))", (warId, guild2, warId, guild1))
        raise Return(entry[0].values())
    
    @gen.coroutine
    def decideWinner(entry):
        guild1_frags, guild2_frags = yield warFrags(entry.warId, entry.guild1, entry.guild2)
        guild1 = getGuildById(entry.guild1)
        guild2 = getGuildById(entry.guild2)
        
        if guild1_frags == guild2_frags:
            # It's a draw.
            guild1.addMoney(entry.stakes)
            guild2.addMoney(entry.stakes)
            
        elif guild1_frags > guild2_frags:
            # Guild1 won
            guild1.addMoney(entry.stakes * 2)
            
        else:
            # Guild2 won.
            guild2.addMoney(entry.stakes * 2)
            
    # Cleanup callback.
    def cancelWar(warEntry):
        global wars, warObjects
        wars[warEntry.guild1][0].remove(warEntry.guild2)
        wars[warEntry.guild2][0].remove(warEntry.guild1)
        
        wars[warEntry.guild1][1].remove(warEntry)
        wars[warEntry.guild2][1].remove(warEntry)
        
        # Now, time to figure out who won. Async.
        decideWinner(warEntry)
    
    def checkPayment(entry):
        guild1 = getGuildById(entry.guild1)
        guild2 = getGuildById(entry.guild2)
        
        if guild1.getMoney() >= entry.stakes and guild2.getMoney() >= entry.stakes:
            # We can pay.
            guild1.removeMoney(entry.stakes)
            guild2.removeMoney(entry.stakes)
            return True
            
        return False
    def checkPayments():
        global pendingPayments
        for entry in pendingPayments[:]:
            if checkPayment(entry):
                pendingPayments.remove(entry)
                entry.setStatus(GUILD_WAR_ACTIVE)
                
            
        call_later(3600, checkPayments) # Try once per hour to check for payments.
    
    def findInvite(creature, guild):
        try:
            for entry in wars[creature.data["guild_id"]][2]:
                if entry.guild2 == creature.data["guild_id"] and entry.guild1 == guild.id:
                    return entry
        except:
            pass
        
    def findIssuedInvite(creature, guild):
        try:
            for entry in wars[creature.data["guild_id"]][2]:
                if entry.guild1 == creature.data["guild_id"] and entry.guild2 == guild.id:
                    return entry
        except:
            pass
        
    # Loader.
    @gen.coroutine
    def loadGuildWars():
        for entry in (yield sql.runQuery("SELECT w.war_id, w.guild_id, w.guild_id2, w.started, w.duration, w.frags, w.stakes, w.status FROM guild_wars w WHERE (SELECT 1 FROM guilds g WHERE g.world_id = %s AND g.guild_id = w.guild_id) AND w.status IN (0, 2, 4)", config.worldId)):
            warEntry = WarEntry(entry['war_id'], entry['guild_id'], entry['guild_id2'], entry['started'], entry['duration'], entry['frags'], entry['stakes'])
            warEntry.setStatus(entry['status'])
            
        checkPayments()
            
                    
    @register("startup")
    def init():
        # Replace the getEmblem for players.
        game.player.Player.getEmblem = getEmblem
        
        # Load using async sql.
        loadGuildWars()
        
    @register("talkactionRegex", "/war (?P<status>(accept|reject|cancel)) (?P<guildname>\w+)")
    def war_management(creature, status, guildname, **k):
        rank = creature.guildRank()
        if not rank or not rank.permission(GUILD_MANAGE_WARS):
            creature.lmessage("You are not allowed to manage wars for this guild.")
            return False
            
        # Find invite entry.
        guild = getGuildByName(guildname)
        if not guild:
            creature.lmessage("Guild not found. Did you spell it right?")
            return False
            
        if status == "cancel":
            entry = findIssuedInvite(creature, guild)
        else:
            entry = findInvite(creature, guild)
                
        if not entry:
            creature.lmessage("Invite not found.")
            
        if status == "cancel":
            entry.setStatus(GUILD_WAR_CANCEL)
        elif status == "reject":
            entry.setStatus(GUILD_WAR_REJECT)
        else:
            entry.setStatus(GUILD_WAR_PENDING_PAYMENT)
            
        creature.message(_l(creature, "War invitation with %(guildname)s have been %(status)s") % {"guildname":guildname, "status":status})
        return False
        
    @register("talkactionRegex", r"/war invite (?P<guildname>\w+) (?P<stakes>\d+) (?P<duration>\d+) (?P<frags>\d+)")
    def war_invitation(creature, guildname, stakes, duration, frags, **k):
        rank = creature.guildRank()
        if not rank or not rank.permission(GUILD_MANAGE_WARS):
            creature.lmessage("You can't invite a guild to war.")
            return False
            
        myGuild = creature.guild()
        
        enemyGuild = getGuildByName(guildname)
        if not enemyGuild:
            creature.lmessage("Guild not found.")
            return False
            
        try:
            stakes = int(stakes)
            duration = int(duration)
            frags = int(frags)
        except:
            creature.lmessage("Invalid parameters")
            return False
            
        if stakes < config.minWarLosePenalty or stakes > config.maxWarLosePenalty:
            creature.message(_l(creature, "stakes has to be between %(min)d and %(max)d") % {"min":config.minWarLosePenalty, "max":config.maxWarLosePenalty})
            return False
            
        if duration < config.minWarDuration or duration > config.maxWarDuration:
            creature.message(_l(creature, "duration has to be between %(min)d and %(max)d") % {"min":config.minWarDuration, "max":config.maxWarDuration})
            return False
            
        if frags < config.minWarFrags or frags > config.maxWarFrags:
            creature.message(_l(creature, "frags has to be between %(min)d and %(max)d") % {"min":config.minWarFrags, "max":config.maxWarFrags})
            return False
            
            
        warEntry = warEntry(0, myGuild.id, enemyGuild.id, 0, duration, frags, stakes, GUILD_WAR_INVITE)
        warEntry.setStatus(GUILD_WAR_INVITE)
        warEntry.insert()
        
        return False
        
    @register("talkactionRegex", r"/balance (?P<command>(pick|donate)) ?(?P<amount>\d+)")
    def balance_management(creature, command, amount, **k):
        # TODO: This is suppose to happen in the bank balance, not the inventory, but it's harder to debug it then, right?.
        
        try:
            amount = int(amount.trim())
            command = command.trim()
        except:
            creature.lmessage("Invalid parameters.")
            return False
            
        guild = creature.guild()
        if not guild:
            creature.lmessage("You are not member of a guild.")
            return False
            
        if not amount:
            creature.lmessage("You have to specify an amount")
            return False
        if command == "donate":
            money = creature.getMoney()
            if money < amount:
                creature.lmessage("You don't have that much money.")
                return False
                
            creature.removeMoney(amount)
            guild.addMoney(amount)
            
            creature.message(_l(creature, "You donated %(amount)d to your guild!") % {"amount": amount})
            
        elif command == "pick":
            if not creature.guildRank().permission(GUILD_WITHDRAW_MONEY):
                creature.lmessage("You can't withdraw funds from your guild account.")
                return False
            
            money = guild.getMoney()
            if money < amount:
                creature.lmessage("Your guild don't have that much money.")
                return False
            
            guild.removeMoney(amount)
            creature.addMoney(amount)
            
            creature.message(_l(creature, "You picked %(amount)d from your guild!") % {"amount": amount})
        
            
        return False
        
    @register("talkaction", "/balance")
    def balance(creature, text, **k):
        guild = creature.guild()
        if not guild:
            creature.lmessage("You are not member of a guild.")
            return False
            
        if not text:
            creature.lmessage("Guild balance is %d." % guild.getMoney())
        
    @register("death", b'player')
    def fragCounter(creature, creature2, deathData, **k):
        # If creature is in war with creature2.
        if creature.isPlayer() and creature2.isPlayer():
            guildId = creature.data["guild_id"]
            guildId2 = creature2.data["guild_id"]
            if guildId and guildId2 and guildId in wars:
                if guildId2 in wars[guildId][0]:
                    # We are at war with this guild.
                    entry = None
                    for entry in wars[guildId][1]:
                        if entry.guild1 == guildId and entry.guild2 == guildId2:
                            entry.guild1_frags += 1
                            break
                        elif entry.guild2 == guildId and entry.guild1 == guildId2:
                            entry.guild2_frags += 1
                            break
                            
                    # Is the fight over?
                    if entry.guild1_frags >= entry.frags or entry.guild2_frags >= entry.frags:
                        cancelWar(entry)
                        
                    # Mark as a just kill regardless. regardless.
                    deathData["unjust"] = False
                    
