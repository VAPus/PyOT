from test.framework import FrameworkTestGame

class TestBan(FrameworkTestGame):
    def init(self):
        # Turn off protection zones.
        # XXX: Tests fail if we don't do it here :/. Looks like tests got to have a init function.
        self.overrideConfig("protectedZones", False)
        
    def clearBans(self):
        game.ban.banIps = {}
        game.ban.banPlayers = {}
        game.ban.banAccounts = {}
        
    def test_addban_ip(self):
        bans = len(game.ban.banIps)
        
        ip = '123.123.123.123'
        
        # 10 sec ban
        addBan(self.player, BAN_IP, ip, "test", 10)
        
        # Tests
        self.assertEqual(len(game.ban.banIps), bans + 1)
        self.assertTrue(ipIsBanned(ip))
        
        # Clear
        self.clearBans()
        
    def test_addban_player(self):
        victim = self.setupPlayer()
        bans = len(game.ban.banPlayers)
        
        # 10 sec ban
        addBan(self.player, BAN_PLAYER, victim.data["id"], "test", 10)
        
        # Tests
        self.assertEqual(len(game.ban.banPlayers), bans + 1)
        self.assertTrue(playerIsBanned(victim))
        self.assertTrue(playerIsBanned(victim.data["id"]))
        
        # Clear
        self.clearBans()
        
    def test_addban_account(self):
        victim = self.setupPlayer()
        bans = len(game.ban.banAccounts)
        
        # 10 sec ban
        addBan(self.player, BAN_ACCOUNT, victim.data["account_id"], "test", 10)
        
        # Tests
        self.assertEqual(len(game.ban.banAccounts), bans + 1)
        self.assertTrue(accountIsBanned(victim))
        self.assertTrue(accountIsBanned(victim.data["account_id"]))
        
        # Clear
        self.clearBans()