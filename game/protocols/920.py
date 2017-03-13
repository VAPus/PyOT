# This is a shadow of the main branch, 9.2
from . import base

provide = []

def verify(): return True

class Packet(base.BasePacket): pass
class Protocol(base.BaseProtocol): pass
