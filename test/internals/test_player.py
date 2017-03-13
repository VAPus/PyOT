from test.framework import FrameworkTestGame, async_test

class TestPlayer(FrameworkTestGame):
    def test_class(self):
        self.assertIsInstance(self.player, Player)
        self.assertIsInstance(self.player, Creature)

    def test_talking(self):
        # These are NOT globals.
        from game.creature_talking import PlayerTalking, CreatureTalking
        
        self.assertIsInstance(self.player, PlayerTalking)
        self.assertIsInstance(self.player, CreatureTalking)
        self.player.say("Hello world!")
        
    def test_move(self):
        # These are NOT globals.
        from game.creature_movement import CreatureMovement

        self.assertIsInstance(self.player, CreatureMovement)
        newPosition = self.player.positionInDirection(SOUTH)

        self.player.move(SOUTH)
        
        self.assertEqual(newPosition, self.player.position)
        
    def test_teleport(self):
        newPosition = self.player.positionInDirection(SOUTH)
        self.player.teleport(newPosition)
        
        self.assertEqual(newPosition, self.player.position)
        
    def test_attackinheritence(self):
        """ A bug reported here: http://vapus.net/forum/pyot-opentibia-server-287/debug-serious-bugs-thread-2925-100/#post31523 """
        # This should NOT raise.
        self.player.cancelTarget(None)

    def test_losetarget(self):
        """ A test for this bug (#75): http://vapus.net/forum/project.php?issueid=75 """
        target = self.setupPlayer()

        self.assertTrue(target)

        self.player.target = target
        self.player.targetMode = 2

        pos = Position(1015, 1000, 7)
        self.player.teleport(pos, force=True)

        self.assertEqual(self.player.position, pos)
        self.assertEqual(self.player.target, None)
        self.assertEqual(self.player.targetMode, 0)

    def test_summon(self):
        """ A test for bug #87 """
        position = self.player.positionInDirection(NORTH)
        summon = self.player.summon("Wolf", position)

        self.assertTrue(summon)
        self.assertIn(summon, self.player.activeSummons)
        self.assertIn(summon, position.getTile().creatures())
        self.assertEqual(summon.master, self.player)
