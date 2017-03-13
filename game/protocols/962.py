# This is a shadow of the main branch, 9.51
from . import base

provide = [950]

def verify(): return True


class Packet(base.BasePacket):
    maxOutfits = 33
    maxMounts = 31
	
class Protocol(base.BaseProtocol):
    Packet = Packet