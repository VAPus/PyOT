from test.framework import FrameworkTestGame
import game.functions as gfunctions
import collections
class _TestDocumentation(FrameworkTestGame):
    def _test_module(self, module):
        ignore = ["StringIO"]
        for name in dir(module):
            # Skip _ functions.
            if name[0] == "_" or name in ignore:
                continue

            # Is it a function. We don't care for variable documentation, really.
            func = getattr(module, name)
            if isinstance(func, collections.Callable):
                if not func.__doc__:
                    self.fail("%s.%s - Missing documentation" % (module.__name__, name))
                else:
                    self.assertGreater(len(func.__doc__), 10)

class TestModules(_TestDocumentation):
    def test_functions(self):
        self._test_module(gfunctions)

class TestClasses(_TestDocumentation):
    def test_player(self):
        self._test_module(game.player.Player)

    def test_creature(self):
        self._test_module(game.creature.Creature)

    def test_monster(self):
        self._test_module(game.monster.Monster)

    def test_monsterBase(self):
        self._test_module(game.monster.MonsterBase)

    def test_npc(self):
        self._test_module(game.npc.NPC)

    def test_npcBase(self):
        self._test_module(game.npc.NPCBase)

    def test_quest(self):
        self._test_module(game.resource.Quest)

    def test_item(self):
        self._test_module(Item)

    def test_tile(self):
        self._test_module(game.map.Tile)

    def test_position(self):
        self._test_module(Position)

    def test_stackposition(self):
        self._test_module(StackPosition)

    def test_party(self):
        self._test_module(game.party.Party)

    def test_guild(self):
        self._test_module(game.guild.Guild)

    def test_guildRank(self):
        self._test_module(game.guild.GuildRank)

    def test_vocation(self):
        self._test_module(game.vocation.Vocation)

    def test_deathEntry(self):
        self._test_module(game.deathlist.DeathEntry)

    def test_spell(self):
        self._test_module(game.spell.Spell)

    def test_rune(self):
        self._test_module(game.spell.Rune)

    def test_condition(self):
        self._test_module(Condition)

    def test_boost(self):
        self._test_module(Boost)
