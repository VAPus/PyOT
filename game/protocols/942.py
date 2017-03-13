# This is a shadow of the main branch, 9.42
from . import base

provide = []

def verify(): return True


class Packet(base.BasePacket):
    maxOutfits = 31
    maxMounts = 27
	
class Protocol(base.BaseProtocol):
    Packet = Packet