# This is a shadow of 9.7
#from . import base
from struct import pack

base = sys.modules["game.protocols.970"]

provide = [981]

def verify(): return True


class Packet(base.Packet):
    maxOutfits = 34
    maxMounts = 32

    def speed(self, speed):
        self.uint16((speed - 49) // 2)

    def money(self, money):
        self.uint64(min(0xFFFFFFFFFFFFFFFE, money))
      
class Protocol(base.Protocol):
    Packet = Packet
