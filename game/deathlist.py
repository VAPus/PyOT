from tornado import gen
byKiller = {}
byVictim = {}

loadedDeathIds = set()
        
class DeathEntry(object):
    def __init__(self, killerId, victimId, unjustified, revenged=0, _time=None, war_id=0, deathId=0):
        if not _time:
            _time = time.time()
        self.id = deathId
        self.killerId = killerId
        self.victimId = victimId
        self.time = _time
        self.unjustified = unjustified
        self.revenged = revenged
        self.warId = war_id
        
    def justify(self):
        " Mark this DeathEntry as a justified kill "
        sql.runOperation("UPDATE pvp_deaths SET unjust = 0 WHERE death_id = %s", self.id)
        self.revenged = 1 # Justified kills can't be revenged.
        self.unjustifed = 0
        
    def revenge(self):
        " Mark this DeathEntry as a revengable kill. "
        sql.runOperation("UPDATE pvp_deaths SET revenged = 1 WHERE death_id = %s", self.id)
        self.revenged = 1
    
    def saveQuery(self):
        " Make a save query (for saving). "
        return "(%s, %s, %s, %s, %s, %s)" % (self.killerId, self.victimId, self.unjustified, self.time, self.revenged, self.warId)

@gen.coroutine
def loadDeathList(playerId):
    " Loads the deathentries for this `playerId` from the database. "
    global byVictim, byKiller, loadedDeathIds
    query = yield sql.runQuery("SELECT death_id, killer_id, victim_id, unjust, `time`, revenged, war_id FROM pvp_deaths WHERE killer_id = %s OR victim_id = %s AND `time` >= %s", playerId, playerId, int(time.time() - (config.deathListCutoff * 3600 * 24)))
    
    if not query:
        return
    
    for entry in query:
        if entry[0] in loadedDeathIds: continue
        
        deathEntry = DeathEntry(entry[1], entry[2], entry[3], entry[5], entry[4], entry[6], entry[0])
        
        try:
            byVictim[entry[2]].append(deathEntry)
        except:
            byVictim[entry[2]] = [deathEntry]
            
        try:
            byKiller[entry[1]].append(deathEntry)
        except:
            byKiller[entry[1]] = [deathEntry]
            
        loadedDeathIds.add(entry[0])

def findUnrevengeKill(killerId, victimId):
    " Returns unrevenged deathentries based on killer and victim. "

    for kill in byVictim[killerId]:
        if kill.unjustified and not kill.revenged:
            return kill
def getSkull(playerId, targetId=None):
    " Returns the skull for playerId "

    if not playerId in byKiller: return SKULL_NONE, 0
    
    _time = time.time()
    
    if targetId:
        orangeTime = _time - config.orangeSkullLength
        for deathEntry in byKiller[playerId]:
            if deathEntry.revenged == 0 and deathEntry.victimId == targetId and deathEntry.time > orangeTime:
                return [SKULL_ORANGE, deathEntry.time + config.orangeSkullLength]
                
    whiteSkull = False
    redEntries = {}
    blackEntries = {}
    
    for i in list(config.redSkullUnmarked.keys()):
        redEntries[i] = 0
        
    for i in list(config.blackSkullUnmarked.keys()):
        blackEntries[i] = 0
        
    # Try to check for white skull and sort entries in red and black.
    
    whiteTime = _time - config.whiteSkull
    whiteTimeout = 0
    redTimeout = 0
    blackTimeout = 0

    for deathEntry in byKiller[playerId]:
        if deathEntry.time >= whiteTime and (deathEntry.time + config.whiteSkull) >= whiteTimeout:
            whiteSkull = True
            whiteTimeout = deathEntry.time + config.whiteSkull
            
        for t in redEntries:
            if deathEntry.time >= _time - (t * 3600):
                redEntries[t] += 1
                if (deathEntry.time + config.redSkull) > redTimeout:
                    redTimeout = deathEntry.time + config.redSkull
                
        for t in blackEntries:
            if deathEntry.time >= _time - (t * 3600):
                blackEntries[t] += 1
                if (deathEntry.time + config.blackSkull) > blackTimeout:
                    blackTimeout = deathEntry.time + config.blackSkull

    # Now, check what kind of skulls he qualified for, try black first.
    for t in blackEntries:
        if blackEntries[t] >= config.blackSkullUnmarked[t]:
            return SKULL_BLACK, blackTimeout
        
    # Now redEntries
    for t in redEntries:
        if redEntries[t] >= config.redSkullUnmarked[t]:
            return SKULL_RED, redTimeout
        
    # Now white
    if whiteSkull:
        return SKULL_WHITE, whiteTimeout
   
    # None
    return SKULL_NONE, 0


@gen.coroutine
def _addEntryToDatabase(deathEntry):
    deathEntry.id = yield sql.runOperationLastId("INSERT INTO pvp_deaths(`killer_id`, `victim_id`, `unjust`, `time`, `revenged`, `war_id`) VALUES %s;" % deathEntry.saveQuery())

    loadedDeathIds.add(deathEntry.id)
    
def addEntry(deathEntry):
    " Adds a deathentry to the database and to the cache. "
    try:
        byKiller[deathEntry.killerId].append(deathEntry)
    except KeyError:
        byKiller[deathEntry.killerId] = [deathEntry]
    try:
        byVictim[deathEntry.victimId].append(deathEntry)
    except KeyError:
        byVictim[deathEntry.victimId] = [deathEntry]
        
    _addEntryToDatabase(deathEntry)
