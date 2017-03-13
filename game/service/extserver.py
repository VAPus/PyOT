import protocolbase
from packet import TibiaPacket, TibiaPacketReader
import sql
import otcrypto
import config
import socket
from struct import pack

class SimplePacket(TibiaPacket):
    def send(self, stream):
        if not stream or not self.data: return
        stream.transport.write(self.data)

IPS = {}

# Format:
# Operations from server.
# 0x00, loading to play cache.
#    string resource
# 0x01 = Play once,
#    string resource
# 0x02 = Play loop
#    string resource
# 0x02 = Stop one
#    string resource
# 0x03 = Stop all
# 0x04 = Drop resource (useful if you do things like dynamically made sounds).
# 0x05 = Resource data.
#    string resource
#    int32 length
#    string length
# 0x06 = Seek
#    string resource
#    uint16 at
# 0x07 = Volume
#    string resource
#    uint8 volume

# Operations from client.
# 0x00, loading ok.
# 0x01, request resource.
#   string resource

# Some ideas:
# Load custom client or custom item data.

# TODO:
# * Support in vapus custom client generator.
# * Authorization.

class extProtocol(protocolbase.TibiaProtocol):
    files = {}
    def onInit(self):
        self.gotFirst = True
        self.lastResource = ""
        self.player = None
        self.ip = ""
        self.loading = True
    def dataReceived(self, data):
        packet = TibiaPacketReader(data)
        self.onPacket(packet)

    def onConnect(self):
        self.ip = self.transport.getPeer().host
        IPS[self.ip] = self

    def onPacket(self, packet):
        type = packet.uint8()

        if type == 0x00:
            self.loading = False
        if type == 0x01:
            resource = packet.string()

            if not resource in self.files:
                # Requesting unknown resource.
                print(("Unknown resource.", resource))
                return

            p = SimplePacket(0x05)
            data = self.files[resource].read()
            p.string(resource)
            p.uint32(len(data))
            p.raw(data)
            p.send(self)

    def _load(self, res):
        self.loading = True
        if not res in self.files:
            if res[:4] == "data":
                self.files[res] = open(res)
        self.lastResource = res
        p = SimplePacket()
        p.uint8(0x00)
        p.string(res)
        p.send(self)

    def play(self, res, loop=False):
        if not res in self.files:
            if res[:4] == "data":
                self.files[res] = open(res)

        p = SimplePacket(0x02 if loop else 0x01)
        p.string(res)
        p.send(self)

    def stop(self, res=None):
        if not res:
            p = SimplePacket(0x03)
        else:
            # Assume resource IS loaded.
            p = SimplePacket(0x02)
            p.string(res)

        p.send(self)

    def destroy(self):
        p = SimplePacket(0x04)
        p.send(self)

    def seek(self, res, seek):
        p = SimplePacket(0x06)
        p.string(res)
        p.uint16(seek)
        p.send(self)

    def volume(self, res, volume):
        p = SimplePacket(0x07)
        p.string(res)
        p.uint8(volume)
        p.send(self)

    def onConnectionLost(self):
        if self.player:
            pass

        del IPS[self.ip]

    def resource(self, res, data):
        self.files[res] = data

class ExtFactory(protocolbase.TibiaFactory):
    __slots__ = ()
    protocol = extProtocol

    def __repr__(self):
        return "<Ext Server Factory>"
