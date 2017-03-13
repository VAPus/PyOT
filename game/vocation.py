vocations = {}
vocationsId = {}
class Vocation(object):
    def __init__(self, id, cid, name, description, health, mana, soulticks):
        self.id = id
        self.clientId = cid
        self.name = name
        self._description = description
        self.health = health
        self.mana = mana
        self.soulticks = soulticks
        self.calcMaxHP = lambda x: x*5 + 145
        self.calcMaxMana = lambda x: x*5 - 5
        self.calcMaxCapacity = lambda x: x*10 + 390
        self.soul = 100
        self.mlevel = 3
        self.meleeSkill = 2
        
        
    def maxHP(self, level):
        """ Return the maximum health for level `level`. """
        return self.calcMaxHP(level)
        
    def hpFormula(self, formula):
        """ Set the maximum health formula to `formula` """
        self.calcMaxHP = formula
        
    def maxMana(self, level):
        """ Return the maximum mana for level `level`. """
        return self.calcMaxMana(level)
        
    def manaFormula(self, formula):
        """ Set the maximum mana formula to `formula`. """
        self.calcMaxMana = formula   
        
    def maxCapacity(self, level):
        """ Return the maximum capasity for level `level` """
        return self.calcMaxCapacity(level)
        
    def capacityFormula(self, formula):
        """ Set the capasity formula to `formula` """
        self.calcMaxCapacity = formula   

    def maxSoul(self, soul):
        """ Set max soul value to `soul` """
        self.soul = soul
        
    def meleeSkillConstant(self, constant):
        """ Set the melee constant, used in melee damage formulas. """
        self.meleeSkill = constant
        
    def mlevelConstant(self, constant):
        """ Set the magic level constant. """
        self.mlevel = constant
    
    def description(self):
        """ Return the description (name) of the vocation """
        return "a %s" % self.name
        
def regVocation(id, cid, name, description, health, mana, soulticks):
    """ Register a new vocation, and return the Vocation object """
    vocation = Vocation(id, cid, name, description, health, mana, soulticks)
    vocations[name] = vocation
    vocationsId[id] = vocations[name]
    return vocation

def getVocation(name):
    """ Get the vocation by name """
    try:
        return vocations[name]
    except:
        return

def getVocationById(id):
    """ Get the vocation by id """
    try:
        return vocationsId[id]
    except:
        return
