# This is a shadow of the main branch, 9.51
from . import base
from struct import pack

provide = []

def verify(): return True


class Packet(base.BasePacket):
    maxOutfits = 33
    maxMounts = 31

    # Magic Effect
    def magicEffect(self, pos, type):
        self.raw(pack("<BHHBB", 0x83, pos.x, pos.y, pos.z, type))
        self.length += 7

class Protocol(base.BaseProtocol):
    Packet = Packet
