import game.player
import re
try:
    import pickle as pickle
except:
    import pickle
    
houseData = {}
def getHouseById(id):
    try:
        return houseData[id]
    except:
        return None
        
class House(object):
    def __init__(self, id, owner, guild, paid, name, town, size, rent, data):
        self.id = id
        self.owner = owner
        self.guild = guild
        self.paid = paid
        self.name = name
        self.town = town
        self.rent = rent
        self.size = size
        self.save = False
        if data:
            try:
                self.data = pickle.loads(data)
            except:
                print("[WARNING] Broken house data. House ID %d" % self.id)
                self.data = {"items":{}, "subowners": [], "guests": [], "doors":{}}
                self.save = True
                
        else:
            self.data = {"items":{}, "subowners": [], "guests": [], "doors":{}}

        

    # Doors
    def getDoorAccess(self, doorId):
        try:
            return self.data["doors"][doorId]
        except:
            self.data["doors"][doorId] = []
            return self.data["doors"][doorId]
            
    def addDoorAccess(self, doorId, name):
        self.save = True
        
        try:
            self.data["doors"][doorId].append(name)
        except:
            self.data["doors"][doorId] = [name]
            
    def removeDoorAccess(self, doorId, name):
        self.save = True
        try:
            self.data["doors"][doorId].remove(name)
        except:
            pass
    def haveDoorAccess(self, doorId, nameOrPlayer):
        # TODO: guild!
        
        try:
            if isinstance(nameOrPlayer, game.player.Player):
                check = nameOrPlayer.name()
                 
            else:
                check = nameOrPlayer
            
            for e in self.data["doors"][doorId]:
                try:
                    isnot = False
                    if e[0] == "!":
                        isnot = True
                    if "@" in e:
                        # No guild support yet
                        continue
                    if "#" in e:
                        continue # Comment
                        
                    if re.match(e, nameOrPlayer, re.I):
                        if isnot: continue
                        else: return True
                    else:
                        if isnot: return True
                        else: continue
                except:
                    continue
        except:
            pass
        return False
            
    # Guests
    def addGuest(self, name):
        self.save = True
        try:
            self.data["guests"].append(name)
        except:
            self.data["guests"] = [name]
    def removeGuest(self, name):
        self.save = True
        try:
            self.data["guests"].remove(name)
        except:
            pass
    def isGuest(self, nameOrPlayer):
        # TODO: guild!
        
        try:
            if isinstance(nameOrPlayer, game.player.Player):
                check = nameOrPlayer.name()
                 
            else:
                check = nameOrPlayer
            
            for e in self.data["guests"]:
                try:
                    isnot = False
                    if e[0] == "!":
                        isnot = True
                    if "@" in e:
                        # No guild support yet
                        continue
                    if "#" in e:
                        continue # Comment
                        
                    if re.match(e, nameOrPlayer, re.I):
                        if isnot: continue
                        else: return True
                    else:
                        if isnot: return True
                        else: continue
                except: # Malformed regex, such as name**
                    continue
        except:
            pass
        return False
            
    # Subowners
    def addSubOwner(self, name):
        self.save = True
        try:
            self.data["subowners"].append(name)
        except:
            self.data["subowners"] = [name]
    def removeSubOwner(self, name):
        self.save = True
        try:
            self.data["subowners"].remove(name)
        except:
            pass
    def isSubOwner(self, nameOrPlayer):
        # TODO: guild!
        
        try:
            if isinstance(nameOrPlayer, game.player.Player):
                check = nameOrPlayer.name()
                 
            else:
                check = nameOrPlayer
            
            for e in self.data["subowners"]:
                try:
                    isnot = False
                    if e[0] == "!":
                        isnot = True
                    if "@" in e:
                        # No guild support yet
                        continue
                    if "#" in e:
                        continue # Comment
                        
                    if re.match(e, nameOrPlayer, re.I):
                        if isnot: continue
                        else: return True
                    else:
                        if isnot: return True
                        else: continue
                except:
                    continue
        except:
            pass
        
        return False

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name != "save":
            object.__setattr__(self, "save", True)