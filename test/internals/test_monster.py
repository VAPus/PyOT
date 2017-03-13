from test.framework import FrameworkTestGame

class TestMonster(FrameworkTestGame):
    def test_corpses(self):
        # For "special" monsters with no corpse or so.
        ignore = ("Northern Pike", "Rift Worm", "Insect Swarm", "Fish", "Slime", "Butterfly", "Son Of Verminor")

        printer = self.fail
        #printer = sys.__stdout__.write
        for monsterName in game.monster.monsters:
            if monsterName in ignore:
                continue

            monster = getMonster(monsterName)
            if not monster.data['corpse']:
                printer("[ERROR] Monster %s got no corpse!\n" % monsterName)
                continue
            corpse = monster.data['corpse']
            item = Item(corpse)
            if not item.name:
                printer("[WARNING] Monster %s (corpse: %d) doesn't have a name, likely invalid\n" % (monsterName, corpse))

            else:
                name = item.name.lower()
                if not "dead" in name and not "slain" in name and not "undead" in name and not "remains" in name and not "lifeless" in name:
                    printer("[WARNING] Monster %s (corpse: %d) doesn't have dead/slain/undead/remains/lifeless in it's name, likely invalid\n" % (monsterName, corpse))
                    continue

            if not item.corpseType:
                printer("[WARNING] Monster %s corpse (%d) don't have a corpseType\n" % (monsterName, corpse))
