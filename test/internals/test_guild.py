from test.framework import FrameworkTestGame
import unittest
import config

class TestGuild(FrameworkTestGame):
    def init(self):
        # Turn off protection zones.
        self.overrideConfig("protectedZones", False)
    
    def _setup(self):
        # The guilds exist in database we assume
        self.player.data["guild_id"] = 1
        
        # Virtual guild rank.
        genguild = game.guild.make_guild("__TEST_GUILD__")
        guild = self.player.guild()
        self.assertEqual(genguild, guild)
        guild.ranks[1] = game.guild.GuildRank(1, 1, "Test", 0xFFFFFFFF)
        self.player.data["guild_rank"] = 1
        
        self.addCleanup(self.cleanGuild, guild)
        
    def cleanGuild(self, guild):
        guild.ranks = {}
        
    def test_same_guild(self):
        self._setup()
        member = self.setupPlayer()
        member.data["guild_id"] = 1
        member.data["guild_rank"] = 1
        
        self.assertIs(self.player.guild(), member.guild())
        
    def test_same_rank(self):
        self._setup()
        
        member = self.setupPlayer()
        member.data["guild_id"] = 1
        member.data["guild_rank"] = 1
        
        self.assertIs(self.player.guildRank(), member.guildRank())

@unittest.skipIf(not config.enableWarSystem, "Require the war system")
class TestGuildWar(TestGuild):
    def test_friendly_emblem(self):
        self._setup()
        
        member = self.setupPlayer()
        member.data["guild_id"] = 1
        member.data["guild_rank"] = 1
        
        self.assertEqual(self.player.getEmblem(member), member.getEmblem(self.player))
        self.assertEqual(self.player.getEmblem(member), EMBLEM_GREEN)
        
    def test_netural_emblem(self):
        self._setup()
        
        member = self.setupPlayer()
        member.data["guild_id"] = 2
        member.data["guild_rank"] = 1
        
        # Hack
        # Hypotetical enemy
        import data.scripts.other.war_system
        data.scripts.other.war_system.wars[1] = [[10], [], []]
        data.scripts.other.war_system.wars[2] = [[11], [], []]
        
        self.assertEqual(self.player.getEmblem(member), member.getEmblem(self.player))
        self.assertEqual(self.player.getEmblem(member), EMBLEM_BLUE)
        
        # Clear
        data.scripts.other.war_system.wars = {}
        
    def test_enemy_emblem(self):
        self._setup()
        
        member = self.setupPlayer()
        member.data["guild_id"] = 2
        member.data["guild_rank"] = 1
        
        # Hack
        import data.scripts.other.war_system
        data.scripts.other.war_system.wars[1] = [[2], [], []]
        data.scripts.other.war_system.wars[2] = [[1], [], []]
        
        self.assertEqual(self.player.getEmblem(member), member.getEmblem(self.player))
        self.assertEqual(self.player.getEmblem(member), EMBLEM_RED)
        
    def test_no_emblem(self):
        # Neither are at war.
        self._setup()
        
        member = self.setupPlayer()
        member.data["guild_id"] = 2
        member.data["guild_rank"] = 1
        
        self.assertEqual(self.player.getEmblem(member), member.getEmblem(self.player))
        self.assertEqual(self.player.getEmblem(member), EMBLEM_NONE)
        