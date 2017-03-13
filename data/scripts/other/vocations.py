# regVocation() # ID, ClientId, name, description, (health, per sec), (mana, per sec), soulseconds)
vocation = regVocation(0, 1, "rookie", "a rookie", (1, 12), (2, 6), 120)

vocation = regVocation(1, 8, "sorcerer", "a sorcerer", (1, 12), (2, 3), 120)
vocation.manaFormula(lambda x: x*30 - 205)
vocation.mlevelConstant(1.1)

vocation = regVocation(2, 16, "druid", "a druid", (1, 12), (2, 3), 120)
vocation.manaFormula(lambda x: x*30 - 205)
vocation.mlevelConstant(1.1)
vocation.meleeSkillConstant(1.8)

vocation = regVocation(3, 4, "paladin", "a paladin", (1, 8), (2, 4), 120)
vocation.hpFormula(lambda x: x*10+105)
vocation.manaFormula(lambda x: x*15-85)
vocation.capacityFormula(lambda x: x*20+310)
vocation.mlevelConstant(1.4)
vocation.meleeSkillConstant(1.2)

vocation = regVocation(4, 2, "knight", "a knight", (1, 6), (2, 6), 120)
vocation.hpFormula(lambda x: x*15+65)
vocation.capacityFormula(lambda x: x*25+270)
vocation.meleeSkillConstant(1.1)


vocation = regVocation(5, 8, "master sorcerer", "a master sorcerer", (1, 12), (2, 2), 15)
vocation.manaFormula(lambda x: x*30 - 205)
vocation.mlevelConstant(1.1)
vocation.maxSoul(200)

vocation = regVocation(6, 16, "elder druid", "an elder druid", (1, 12), (2, 2), 15)
vocation.manaFormula(lambda x: x*30 - 205)
vocation.mlevelConstant(1.1)
vocation.meleeSkillConstant(1.8)
vocation.maxSoul(200)

vocation = regVocation(7, 4, "royal paladin", "a royal paladin", (1, 6), (2, 3), 15)
vocation.hpFormula(lambda x: x*10+105)
vocation.manaFormula(lambda x: x*15-85)
vocation.capacityFormula(lambda x: x*20+310)
vocation.mlevelConstant(1.4)
vocation.meleeSkillConstant(1.2)
vocation.maxSoul(200)

vocation = regVocation(8, 2, "elite knight", "an elite knight", (1, 4), (2, 6), 15)
vocation.hpFormula(lambda x: x*15+65)
vocation.capacityFormula(lambda x: x*25+270)
vocation.meleeSkillConstant(1.1)
vocation.maxSoul(200)

# TODO:
"""
set those:
        
    def hpFormula(self, formula):
        
        
    def manaFormula(self, formula): 
        
        
    def capacityFormula(self, formula):

        
    def meleeSkillConstant(self, constant):
        
    def mlevelConstant(self, constant):
    
    TODO: Shielding etc

"""
