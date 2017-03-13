from test.framework import FrameworkTestGame

class TestItem(FrameworkTestGame):
    def test_transformitem(self):
        """ This report: http://vapus.net/forum/pyot-opentibia-server-287/debug-serious-bugs-thread-2925-100/#post31523 """
        position = Position(1000,1000,7)
        
        item = Item(3031)
         
        item.place(position)
        
        transformItem(item, 3035)
        
        self.assertEqual(item.itemId, 3035)
        
        # Transform back, and to 0. These should work too.
        item.transform(3031)
        item.transform(0)

    def test_move(self):
        item = Item(7449)
        
        self.player.itemToInventory(item, SLOT_RIGHT)
        
        self.assertEqual(self.player.inventory[SLOT_RIGHT], item)
        
        self.assertTrue(moveItem(self.player, Position(0xFFFF, SLOT_RIGHT+1, 0), self.player.position))
        
        self.assertEqual(self.player.inventory[SLOT_RIGHT], None)
