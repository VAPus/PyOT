# This is a shared resource maanger that we will use for quests, mounts and outfits

### Outfits ###
outfits = []
reverseOutfits = {}
class Outfit(object):
    def __init__(self, name="", premium=False):
        self.premium = premium
        self.name = name
        self.gender = None
        self.looks = {} # gender=>(looktype ---)

    def look(self, looktype, lookhead=0, lookbody=0, looklegs=0, lookfeet=0, gender=0):
        " Set a look based on gender. "
        self.looks[gender] = [looktype, lookhead, lookbody, looklegs, lookfeet]
        
    def getLook(self, gender=0):
        " Get the look based on the gender. "
        return self.looks[gender]
        

def regOutfit(outfit):
    """ Register a outfit for use """
    outfits.append(outfit)
    reverseOutfits[outfit.name] = len(outfits)-1

def getOutfit(name):
    """ Get outfit by name """
    return outfits[reverseOutfits[name]]
# Helper call
def genOutfit(name, premium=False):
    """ Append a outfit and return the object """
    if name == "<Placeholder>":
        outfits.append(None)
        return
        
    outfit = Outfit(name, premium)
    regOutfit(outfit)
    return outfit
    
    
    
### Mounts ###
mounts = []
reverseMounts = {} # id and name

class Mount(object):
    def __init__(self, name, cid, speed=0, premium=False):
        self.premium = premium
        self.name = name
        self.cid = cid
        self.speed = speed
        

def regMount(mount):
    """ Register a mount object for use. """
    mounts.append(mount)
    reverseMounts[mount.name] = len(mounts)-1
    reverseMounts[mount.cid] = len(mounts)-1 

def getMount(name):
    """ Get mount by name """
    return mounts[reverseMounts[name]]
    
# Helper call
def genMount(name, cid, speed=0, premium=False):
    """ Generate a mount object, register it and return it for use """
    if name == "<Placeholder>":
        mounts.append(None)
        return
        
    mount = Mount(name, cid, speed, premium)
    regMount(mount)
    return mount
    
### Quest ###
quests = []
reverseQuests = {}
class Quest(object):
    def __init__(self, name):
        self.name = name
        self.steps = 0
        self.descriptions = []
        self.missions = []
        
    def mission(self, name):
        " Append a mission to this quest. "
        self.missions.append([name, len(self.descriptions), 0])
        
    def description(self, description):
        " Append a description for this quest, with the last appended mission as it's parent. "
        self.descriptions.append(description)
        self.missions[-1][2] += 1
        self.steps += 1
        
def genQuest(name):
    """ Generate a quest object, register it and return it for use. """
    quest = Quest(name)
    if name == "<Placeholder>":
        quests.append(None)
        return
    quests.append(quest)
    reverseQuests[name] = len(quests)-1
    return quest
    
def getQuest(name):
    """ Get a quest, either by 'id' or name. """
    try:
        return quests[name]
    except:
        return quests[reverseQuests[name]]
