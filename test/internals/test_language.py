from test.framework import FrameworkTestGame

class TestLanguage(FrameworkTestGame):
    def init(self):
        self.overrideConfig("defaultLanguage", 'en_EN')
        self.overrideConfig("enableTranslations", True)
        
    def test_bug58(self):
        """ #58. Language not resetting to english. http://vapus.net/forum/project.php?issueid=58 """
        
        # Make sure we're default language already.
        self.assertTrue(self.player.data["language"], 'en_EN')

        # Set a different language, like polish.
        self.player.setLanguage('pl_PL')
        self.assertNotEqual(self.player.l, Creature.l)
        self.assertNotEqual(self.player.lp, Creature.lp)

        # Reset
        self.player.setLanguage('en_EN')
        
        self.assertEqual(self.player.l("Hello world"), "Hello world")
        
