from test.framework import FrameworkTestGame, async_test

class TestAttackSkulls(FrameworkTestGame):
    def init(self):
        # Turn off protection zones.
        self.overrideConfig("protectedZones", False)
        
    def test_yellowskull(self):
        # Create player to attack.
        target = self.setupPlayer()
        
        # Set target
        # Avoid auto attacks.
        self.player.target = target
        self.player.targetMode = 1
        
        # Give him a white skull.
        target.setSkull(SKULL_WHITE)

        # He is white right?
        self.assertEqual(target.getSkull(self.player), SKULL_WHITE)
        
        # Ignore blocking.
        self.player.ignoreBlock = True
        
        # We're suppose to have no skull to begin with.
        self.assertFalse(self.player.getSkull(target))
        
        # Damage him
        self.player.attackTarget(-10)
        self.assertEqual(self.player.getSkull(target), SKULL_YELLOW)
        
    def test_whiteskull(self):
        # Create player to attack.
        target = self.setupPlayer()
        
        # Set target
        # Avoid auto attacks.
        self.player.target = target
        self.player.targetMode = 1
        
        # Ignore blocking.
        self.player.ignoreBlock = True
        
        # Damage him
        self.player.attackTarget(-10)
        
        self.assertEqual(self.player.getSkull(target), SKULL_WHITE)
           
    def test_orangeskull(self):
        # Create player to attack.
        target = self.setupPlayer()
        
        # Set target
        # Avoid auto attacks.
        self.player.target = target
        self.player.targetMode = 1

        # Ignore blocking.
        self.player.ignoreBlock = True
        
        # Kill him.
        self.player.attackTarget(-1000)
        self.assertFalse(target.alive)
        
        self.assertEqual(self.player.getSkull(None), SKULL_WHITE)
        
        # Remove white skull.
        self.player.setSkull(SKULL_NONE)
        
        # Respawn.
        target.onSpawn()

        
        # 
        self.assertTrue(self.player.data["id"] in deathlist.byKiller)
        self.assertEqual(self.player.getSkull(target), SKULL_ORANGE)
        
    def test_redskull(self):
        # Create player to attack.
        target = self.setupPlayer()
        
        # Ignore blocking.
        self.player.ignoreBlock = True
        
        # Kill him enough times.
        for n in range(list(config.redSkullUnmarked.values())[0]+1):
            # Set target
            # Avoid auto attacks.
            self.player.target = target
            self.player.targetMode = 1


            
            # Kill him.
            self.player.attackTarget(-1000)
            self.assertFalse(target.alive)
            
            
            # Respawn.
            target.onSpawn()

        
        # 
        self.assertEqual(deathlist.getSkull(self.player.data["id"])[0], SKULL_RED)
        self.assertTrue(self.player.data["id"] in deathlist.byKiller)
        #self.assertEqual(self.player.getSkull(None), SKULL_RED)
        
        # Force refreshment test.
        self.player.skull = 0
        self.assertEqual(self.player.getSkull(None), SKULL_RED)
        
    def test_blackskull(self):
        
        # Ignore blocking.
        self.player.ignoreBlock = True
        
        # Kill him enough times.
        for n in range(list(config.blackSkullUnmarked.values())[0]+1):
            # Create player to attack.
            target = self.setupPlayer()
            
            # Set target
            # Avoid auto attacks.
            self.player.target = target
            self.player.targetMode = 1


            
            # Kill him.
            self.player.attackTarget(-1000)
            self.assertFalse(target.alive)
            
            # Respawn.
            target.onSpawn()

        # 
        self.assertEqual(deathlist.getSkull(self.player.data["id"])[0], SKULL_BLACK)
        self.assertTrue(self.player.data["id"] in deathlist.byKiller)
        #self.assertEqual(self.player.getSkull(None), SKULL_BLACK)
        
        # Force refreshment test.
        self.player.skull = 0
        self.assertEqual(self.player.getSkull(None), SKULL_BLACK)
        
    def test_greenskull(self):
        # Ignore blocking.
        self.player.ignoreBlock = True
        
        # Make party
        party = self.player.newParty()
        
        # Target
        target = self.setupPlayer()
        
        party.addMember(target)
        
        # We're green?
        self.assertEqual(self.player.getSkull(target), SKULL_GREEN)
        self.assertEqual(target.getSkull(self.player), SKULL_GREEN)
        
        # Attack
        # Set target
        # Avoid auto attacks.
        self.player.target = target
        self.player.targetMode = 1
        self.player.attackTarget(-10)
        
        # We're still green?
        self.assertEqual(self.player.getSkull(target), SKULL_GREEN)
        self.assertEqual(target.getSkull(self.player), SKULL_GREEN)
        
        
