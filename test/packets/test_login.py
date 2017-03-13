from test.framework import FrameworkTest, async_test

class TestLogin(FrameworkTest):
    def test_login(self):
        packet = self.client.sendPacket("bhhbsss", 0xFF, 0x00, 963, 0, "111", "Test", "111", ret=True)
        yield self.server.onFirstPacket(packet)
        self.assertEqual(self.tr._packets[0].uint8(), 0x1F)
