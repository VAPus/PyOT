from test.framework import FrameworkTestGame

class TestMailBox(FrameworkTestGame):
    def test_letter(self):
        target = self.setupPlayer()
        result = mail(target, None, "Hello World", 1)
        self.assertTrue(result)
        depot = target.getDepot(1)
        self.assertEqual(len(depot), 1)
        self.assertEqual(depot[0].itemId, ITEM_LETTER_STAMPED)
        self.assertTrue(depot[0].text)

    def test_letter_by_name(self):
        target = self.setupPlayer()
        result = mail(target.name(), None, "Hello World", 1)
        self.assertTrue(result)
        depot = target.getDepot(1)
        self.assertEqual(len(depot), 1)
        self.assertEqual(depot[0].itemId, ITEM_LETTER_STAMPED)
        self.assertTrue(depot[0].text)    

    def test_parcel_by_list(self):
        target = self.setupPlayer()
        result = mail(target, [Item(1234), Item(2345)], "", 1)
        self.assertTrue(result)
        depot = target.getDepot(1)
        self.assertEqual(len(depot), 1)
        self.assertEqual(depot[0].itemId, ITEM_PARCEL_STAMPED)
        self.assertEqual(len(depot[0].container), 3)

    def test_parcel_without_label(self):
        item = Item(ITEM_PARCEL)
        target = self.setupPlayer()
        result = mail(target, item, "", 1)
        self.assertFalse(result)
        self.assertEqual(item.itemId, ITEM_PARCEL)
