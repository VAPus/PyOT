from test.framework import FrameworkTestGame

class TestRaiseMessages(FrameworkTestGame):
    def init(self):
        # Turn off protection zones.
        self.overrideConfig("protectedZones", False)
        self.player.raiseMessages = True
        
    def cleanup(self):
        self.player.raiseMessages = False
        
    def test_raise(self):
        self.assertRaises(MsgNotPossible, self.player.notPossible)

    def test_unmarked(self):
        # Make target
        target = self.setupPlayer()

        # Make sure we got unmarked warnings on.
        self.player.modes[2] = True
        
        self.assertTrue(self.player.raiseMessages)
        
        # Run setAttackTarget.
        future = self.player.setAttackTarget(target.cid)
        yield future
        
        # Should raise MsgUnmarkedPlayer
        self.assertEqual(MsgUnmarkedPlayer, future)

    def test_toggleraisemessages(self):
        self.player.raiseMessages = False
        self.player.toggleRaiseMessages()
        self.assertEqual(self.player.raiseMessages, True)

        self.assertRaises(MsgNotPossible, self.player.notPossible)

        self.player.toggleRaiseMessages()
        self.assertEqual(self.player.raiseMessages, False)
        
        # Cleanup.
        self.player.raiseMessages = True