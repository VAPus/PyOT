# This is a shadow of the main branch, 9.51
from . import base
from struct import pack

provide = []

def verify(): return True


class Packet(base.BasePacket):
    maxOutfits = 33
    maxMounts = 33

    # Magic Effect
    def magicEffect(self, pos, type):
        self.raw(pack("<BHHBB", 0x83, pos.x, pos.y, pos.z, type))
        self.length += 7
   
    def vip(self, playerId, playerName, online=False):
        self.uint8(0xD2)
        self.uint32(playerId)
        self.string(playerName)
        self.string("") # TODO, description
        self.uint32(0) # TODO, icon
        self.uint8(1) # TODO notify
        self.uint8(online)
        
class Protocol(base.BaseProtocol):
    Packet = Packet
