import sql
king = game.npc.genNPC("The King", (332, 20, 39, 45, 7, 0, 0))
king.setWalkable(False)
accept = ('Yes', 'Ok', 'Sure')
king.greet("Greetings %(playerName)s. I can {promote} you.")
 
class Promotion(game.npc.ClassAction):
    def action(self):
        self.on.onSaid('promote', self.promotion)
    def promotion(self, npc, player):
        npc.sayTo(player, "Do you want me to promote you?")
        word = yield
        word =word.title()
        if word in accept:
            if player.data["vocation"] < 4 and player.data["level"] > 20:
                if player.removeMoney(20000):
                    sql.runOperation("UPDATE `players` SET `vocation` = %s WHERE `id` = %s", (player.data["vocation"] + 4, player.data["id"]))
                    player.data["vocation"] += 4
                    npc.sayTo(player, "Congratulations! You are now promoted.")
                else:
                    npc.sayTo(player, "You do not have enough money!")
            elif player.data["level"] < 20:
                npc.sayTo(player, "I am sorry, but I can only promote you once you have reached level")
            else:
                npc.sayTo(player, "You are already promoted!")
 
king.module(Promotion)