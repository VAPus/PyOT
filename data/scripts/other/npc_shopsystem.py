"to be fixed onbuyerwalks and turnagainst"
from game.npc import ClassAction, regClassAction
greetings = ('hi', 'hey', 'hello', 'hail')
farwells = ('bye', 'farewell', 'cya')
offers = ('offer', 'trade')

# Have to apply on all prestores
@register("playerSayTo", b'npc')
def saidTo(creature, creature2, said, channelType, channelId, **k):
    if not creature2.isNPC():
        return # We got nothing todo
        
    
    if creature.position.z != creature2.position.z or creature2.distanceStepsTo(creature.position) >= 5:
        return # Too far away to care.

    said = said.lower()
    _sayParams = {"playerName":creature.name()}
    ok = True
    if channelType == 1 and not creature in creature2.focus:
        ok = False
        for greeting in greetings:
            if greeting == said:
                ok = True
                break
        if ok:
            if not creature2._onBuyerWalks in creature.scripts["onNextStep"]:
                creature.scripts["onNextStep"].insert(0, creature2._onBuyerWalks)
            creature2.focus.add(creature)
            # Allow functions to be greatings.
            if hasattr(creature2.base.speakGreet, '__call__'):
                creature2.base.speakGreet(npc=creature2, player=creature)
            else:
                creature2.sayTo(creature, creature2.base.speakGreet % _sayParams)
                
            creature2.turnAgainst(creature.position)
            return
        
    elif channelType == 11 and not creature in creature2.focus:
        ok = False
        for greeting in greetings:
            if greeting == said:
               ok = True
               break
        if ok:
            if not creature2._onBuyerWalks in creature.scripts["onNextStep"]:
                creature.scripts["onNextStep"].insert(0, creature2._onBuyerWalks)
            creature2.focus.add(creature)
            # Allow functions to be greatings.
            if hasattr(creature2.base.speakGreet, '__call__'):
                creature2.base.speakGreet(npc=creature2, player=creature)
            else:
                creature2.sayTo(creature, creature2.base.speakGreet % _sayParams)
                    
            creature2.turnAgainst(creature.position)
            return
    if ok:
        # Check for goodbyes
        if channelType == 11 and said in farwells:
            creature2.farewell(creature)
        
        elif creature2.activeModule:
            try:
                creature2.activeModule.send(said)
            except StopIteration:
                creature2.activeModule = None
        else:
            creature2.handleSpeak(creature, said)
            


# The offers action
class Shop(ClassAction):
    def action(self):
        self.on.offers = []
        self.on.shopBuy = "Do you want to buy %(itemCount)d %(itemName)s for %(totalcost)d gold coins?"
        self.on.shopOnBuy = "It was a pleasure doing business with you."
        self.on.shopDecline = "Not good enough, is it... ?"
        self.on.shopClose = "Thank you, come back when you want something more."
        self.on.shopWalkAway = "How rude!"
        self.on.shopEmpty = "Sorry, I'm not offering anything."
        self.on.shopTrade = "Here's my offer, %(playerName)s. Don't you like it?"

        self.on.onSaid(offers, self.handleOffers, self.handleClose)
        
    def offer(self, name, sellPrice=0, buyPrice=0, subtype=0):
        if type(name) == str:
            temp = game.item.idByName(name)
            if temp:
                name = temp

        # verify.
        if name not in game.item.items:
            print("[WARNING] %s is not a valid shop item." % name)
            return
            
        self.on.offers.append( (name, sellPrice, buyPrice, subtype) )

    def offerContainer(self, name, contains, count, buyPrice=0):
        pass # TODO
    
    def handleOffers(self, npc, player):
        if player.position.z != npc.position.z: return

        if not player in npc.focus: npc.focus.add(player) # Hack...

        _sayParams = {"playerName":player.name()}
        
        if self.on.offers and player.position.z == npc.position.z and player in npc.focus:
            npc.sayTo(player, self.on.shopTrade % _sayParams)
            npc.sendTradeOffers(player)
            player.setTrade(npc)
        else:
            npc.sayTo(player, self.on.shopEmpty % _sayParams)

    def handleClose(self, npc, player):
        player.closeTrade()
        
    def decline(self, decline):
        self.on.shopDecline = decline
        
regClassAction('shop', Shop)

# Runes
class RuneShop(Shop):
    def action(self):
        Shop.action(self)
        # Include shop actions
        self.on.actions.append('shop')
        self.offer('intense healing rune', 95, -1, 1)
        self.offer('ultimate healing rune', 175, -1, 1)
        self.offer('magic wall rune', 2293, -1, 3)
        self.offer('destroy field rune', 45, -1, 3)
        self.offer('light magic missile rune', 40, -1, 10)
        self.offer('heavy magic missile rune', 120, -1, 10)
        self.offer('great fireball rune', 180, -1, 4)
        self.offer('explosion rune', 250, -1, 6)
        self.offer('sudden death rune', 350, -1, 3)
        #self.offer('death arrow rune', 300, -1, 3)
        self.offer('paralyze rune', 700, -1, 1)
        self.offer('animate dead rune', 375, -1, 1)
        self.offer('convince creature rune', 80, -1, 1)
        self.offer('chameleon rune', 210, -1, 1)
        self.offer('desintegrate rune', 80, -1, 3)

        self.offer('wand of vortex', 500, 250)
        self.offer('wand of dragonbreath', 1000, 500)
        self.offer('wand of decay', 5000, 2500)
        self.offer('wand of draconia', 7500, 3750)
        self.offer('wand of cosmic energy', 10000, 5000)
        self.offer('wand of inferno', 15000, 7500)
        self.offer('wand of starstorm', 18000, 9000)
        self.offer('wand of voodoo', 22000, 11000)

        self.offer('snakebite rod', 500, 250)
        self.offer('moonlight rod', 1000, 500)
        self.offer('necrotic rod', 5000, 2500)
        self.offer('northwind rod', 7500, 3750)
        self.offer('terra rod', 10000, 5000)
        self.offer('hailstorm rod', 15000, 7500)
        self.offer('springsprout rod', 18000, 9000)
        self.offer('underworld rod', 22000, 11000)

        self.offer('spellbook', 150)
        self.offer('magic lightwand', 400)

        self.offer('small health potion', 20, -1, 1)
        self.offer('health potion', 45, -1, 1)
        self.offer('mana potion', 50, -1, 1)
        self.offer('strong health potion', 100, -1, 1)
        self.offer('strong mana potion', 80, -1, 1)
        self.offer('great health potion', 190, -1, 1)
        self.offer('great mana potion', 120, -1, 1)
        self.offer('great spirit potion', 190, -1, 1)
        self.offer('ultimate health potion', 310, -1, 1)
        self.offer('antidote potion', 50, -1, 1)
        
regClassAction('runeshop', RuneShop)

# Furniture
class Furniture(Shop):
    def action(self):
        Shop.action(self)
        # Include shop actions
        self.on.actions.append('shop')
        self.offer(7906, 80)
        self.offer(7905, 80)
        self.offer(7904, 80)
        self.offer(7907, 80)
        self.offer(3903, 40)
        self.offer(3904, 40)
        self.offer(3901, 15)
        self.offer(3928, 25)
        self.offer(3902, 55)
        self.offer(6115, 50)
        self.offer(3916, 12)
        self.offer(3938, 70)
        self.offer(5086, 10)
        self.offer(3925, 10)
        self.offer(3930, 10)
        self.offer(3921, 18)
        self.offer(3932, 25)
        self.offer(3934, 30)
        self.offer(3935, 7)
        self.offer(3918, 50)
        self.offer(8692, 200)
        self.offer(3908, 25)
        self.offer(3927, 50)
        self.offer(7700, 50)
        self.offer(3937, 35)
        self.offer(7962, 70)
        self.offer(2099, 40)
        self.offer(2102, 6)
        self.offer(2100, 5)
        self.offer(2103, 5)
        self.offer(3929, 8)
        self.offer(2104, 5)
        self.offer(3917, 50)
        self.offer(3926, 200)
        self.offer(1681, 25)
        self.offer(1679, 25)
        self.offer(1685, 30)
        self.offer(1680, 25)
        self.offer(1686, 25)
        self.offer(1692, 25)
        self.offer(1687, 25)
        self.offer(1693, 25)
        self.offer(1684, 20)
        self.offer(1688, 25)
        self.offer(1689, 25)
        self.offer(3916, 12)
        self.offer(1690, 25)
        self.offer(1691, 25)
        self.offer(1692, 25)
        self.offer(1683, 20)
        self.offer(1872, 25)
        self.offer(1860, 25)
        self.offer(1866, 25)
        self.offer(1857, 25)
        self.offer(1869, 25)
        self.offer(1880, 25)
        self.offer(1863, 25)
        self.offer(3909, 30)
        self.offer(3911, 25)
        self.offer(3912, 20)
        self.offer(3910, 25)
        self.offer(7936, 50)
        self.offer(1851, 40)
        self.offer(1848, 40)
        self.offer(1845, 40)
        self.offer(1852, 50)
        self.offer(1854, 50)
        self.offer(1853, 50)
        
regClassAction('furniture', Furniture)

# Equipment
class Equipment(Shop):
    def action(self):
        Shop.action(self)
        # Include shop actions
        self.offer('blessed wooden stake', 10000) 
        self.offer('obsidian knife', 10000)
        self.offer('shovel', 50)
        self.offer('backpack', 20)
        self.offer(6538, 30)
        self.offer('plate', 6)
        self.offer('present', 10)
        self.offer('watch', 20)
        self.offer('worm', 1)
        self.offer('flask of rust remover', 100)
        self.offer('crowbar', 1000)
        self.offer(10516, 10000)
        self.offer(10511, 10000)
        self.offer(10513, 10000)
        self.offer(1955, 15)
        self.offer(1950, 15)
        self.offer(1958, 15)
        self.offer('fishing rod', 150)
        self.offer('machete', 40)
        self.offer('bag', 5)
        self.offer('orange backpack', 20)
        self.offer('orange bag', 5)
        self.offer('pick', 50)
        self.offer('scythe', 50)
        self.offer('document', 12)
        self.offer('parchment', 8)
        self.offer('scroll', 5)
        self.offer('bottle', 3)
        self.offer(2120, 50)
        self.offer(2050, 2)
regClassAction('equipment', Equipment)
