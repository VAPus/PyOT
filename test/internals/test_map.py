from test.framework import FrameworkTestGame

class TestMap(FrameworkTestGame):
    def test_settile(self):
        tile = game.map.Tile([Item(100)])
        pos = Position(1001, 1000, 7)
        orgTile = pos.getTile()

        pos.setTile(tile)

        self.assertNotEqual(pos.getTile(), orgTile)
        self.assertEqual(pos.getTile(), tile)

        # Cleanup
        pos.setTile(orgTile)

    def test_copytile(self):
        pos = Position(1001, 1000, 7)
        orgTile = pos.getTile()
        copy = orgTile.copy()

        self.assertNotEqual(orgTile, copy)

        self.assertEqual(orgTile.flags, copy.flags)
        self.assertEqual(orgTile[0].itemId, copy[0].itemId)

    def test_load(self):
        sectorSum = (0, 4, 1)
        game.map.load(4, 1, 0, sectorSum)
        self.assertIn(sectorSum, game.map.sectors)
        
    def test_unload(self):
        sectorSum = (0, 4, 1)
        game.map.unload(4, 1, 0)
        self.assertNotIn(sectorSum, game.map.sectors)
