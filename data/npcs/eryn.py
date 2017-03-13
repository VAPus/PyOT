Eryn = genNPC("Eryn", (130, 39, 122, 125, 37, 0, 2212), "Eryn, the rune vendor")
Eryn.setWalkable(False)

Eryn.greet("Hello %(playerName)s. I sell runes, potions, wands and rods.")

class Test(game.npc.ClassAction):
    def action(self): self.on.onSaid('test', self.test)
    def test(self, npc, player):
        npc.sayTo(player, "I can multiply any number by two! Please tell me one!")
        number = (yield)
        try:
            npc.sayTo(player, "It'll be %d" % (int(number)*2))
        except:
            npc.sayTo(player, "Ehm, %s is not a number!" % number)
Eryn.module(Test)

shop = Eryn.module('runeshop')
shop.decline("Is %(totalcost)d gold coins too much for you? Get out of here!")

