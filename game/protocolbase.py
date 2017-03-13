from tornado.tcpserver import *
from packet import TibiaPacketReader
import config
from struct import unpack
import socket

if config.checkAdler32:
    from zlib import adler32

class TibiaProtocol:
    #__slots__ = 'gotFirst', 'xtea', 'buffer', 'nextPacketLength', 'bufferLength'
    enableTcpNoDelay = False
    webSocket = False
    def __init__(self, stream, address, server):
        self.transport = stream
        self.address = address
        self.server = server
        self.gotFirst = False
        self.xtea = None
        self.onInit()
        self.player = None
        
        # Register disconnect callback.
        self.transport.set_close_callback(self.connectionLost)

        self.connectionMade()

        # Start Handle reading. First one uint16_t for length of the packet.
        self.transport.read_bytes(2, self.handlePacketLength)

    def connectionMade(self):
        print("Connection made from {0}".format(self.address))

        # Enable TCP_NO_DELAY and keepalive.
        try:
            self.transport.socket.setsockopt(socket.IPPROTO_TCP, socket.SO_KEEPALIVE, 1)
        except:
            pass # This might fail on windows.
            
        try:
            self.transport.set_nodelay(True)
        except:
            pass # This might fail on some systems too. Kernel params etc.
            
        # Inform the Protocol that we had a connection
        self.onConnect()

    def connectionLost(self, reason=None):
        print("Connection lost from {0}".format(self.address))

        # Inform the Protocol that we lost a connection
        self.onConnectionLost()

    def handlePacketLength(self, packetData):
        length = unpack("<H", packetData)[0]

        # Read this packet upto length.
        self.transport.read_bytes(length, self.handlePacketData)

    def handlePacketData(self, packetData):
        packet = TibiaPacketReader(packetData)
        # Adler32:
        if config.checkAdler32:
            adler = packet.uint32()
            calcAdler = adler32(packet.getData())
            if adler != calcAdler:
                print("Adler32 missmatch, it's %s, should be: %s" % (calcAdler, adler))
                self.transport.close()
                return
        else:
            packet.pos += 4


        if self.gotFirst:
            self.onPacket(packet)
        else:
            self.gotFirst = True
            self.onFirstPacket(packet)

        # Start Handle reading for the next packet.
        self.transport.read_bytes(2, self.handlePacketLength)

    #### Protocol spesific, to be overwritten ####
    def onConnect(self):
        pass

    def onConnectionLost(self):
        pass

    def onFirstPacket(self, packet):
        self.onPacket(packet)

    def onPacket(self, packet):
        pass

    def onInit(self):
        pass

    #### Some simplefiers ####
    def loseConnection(self):
        self.onConnectionLost()
        call_later(1, self.transport.close) # We add a 1sec delay to the lose to prevent unfinished writtings from happending

class TibiaFactory(TCPServer):
    #__slots__ = 'clientCount'
    protocol = None # This HAVE to be overrided!

    def handle_stream(self, stream, address):
        """Called when new IOStream object is ready for usage"""
        self.protocol(stream, address, self)