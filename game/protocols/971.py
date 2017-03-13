# This is a shadow of the main branch, 9.51
#from . import base
from struct import pack

base = sys.modules["game.protocols.970"]

provide = []

def verify(): return True


class Packet(base.Packet):
    pass  
        
class Protocol(base.Protocol):
    Packet = Packet
