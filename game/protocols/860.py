# This is a shadow of the main branch, 9.1.
import sys

provide = []

def verify():
    return True

# Use 8.54 as base, optional.
try:
    module = sys.modules["game.protocols.854"]
except:
    module = getattr( __import__('game.protocols.854', globals(), locals()).protocols, '854')

class Packet( module.Packet ):

    def cancelTarget( self ):
        self.uint8( 0xA3 )
        self.uint32( 0 )
        
        
class Protocol( module.Protocol ):
    Packet = Packet
