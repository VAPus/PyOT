# This is a shadow of the main branch, 9.1
import sys

provide = []

def verify(): return True

class Packet(sys.modules["game.protocols.861"].Packet):
    maxKnownCreatures = 1300
    

class Protocol(sys.modules["game.protocols.861"].Protocol):
    Packet = Packet