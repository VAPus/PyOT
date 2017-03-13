from struct import unpack, pack, Struct
from otcrypto import encryptXTEA
from zlib import adler32
from position import StackPosition, Position
import config

uint8Prebuild = [b""] * 256
for n in range(256):
    uint8Prebuild[n] = pack("<B", n) 

pack_uint16 = Struct("<H").pack
pack_uint32 = Struct("<I").pack
pack_header = Struct("<HI").pack

class TibiaPacketReader(object):
    __slots__ = ('pos', 'data')
    def __init__(self, data):
        self.pos = 0
        self.data = data

    # 8bit - 1byte, C type: char
    def uint8(self):
        self.pos += 1
        return self.data[self.pos-1]
    def int8(self):
        self.pos += 1
        return unpack("<b", self.data[self.pos-1])[0]

    # 16bit - 2bytes, C type: short
    def uint16(self):
        self.pos += 2
        return unpack("<H", self.data[self.pos-2:self.pos])[0]
    def int16(self):
        self.pos += 2
        return unpack("<h", self.data[self.pos-2:self.pos])[0]

    # 32bit - 4bytes, C type: int
    def uint32(self):
        self.pos += 4
        return unpack("<I", self.data[self.pos-4:self.pos])[0]
    def int32(self):
        self.pos += 4
        return unpack("<i", self.data[self.pos-4:self.pos])[0]

    # 64bit - 8bytes, C type: long long
    def uint64(self):
        self.pos += 8
        return unpack("<Q", self.data[self.pos-8:self.pos])[0]
    def int64(self):
        self.pos += 8
        return unpack("<q", self.data[self.pos-8:self.pos])[0]

    # 32bit - 4bytes, C type: float
    def float(self):
        self.pos += 4
        return unpack("<f", self.data[self.pos-4:self.pos])[0]

    # 64bit - 8bytes, C type: double
    def double(self):
        self.pos += 8
        return unpack("<d", self.data[self.pos-8:self.pos])[0]

    def string(self):
        length = self.uint16()
        self.pos += length
        #return ''.join(map(str, unpack("%ds" % length, self.data[self.pos-length:self.pos])))
        return self.data[self.pos-length:self.pos].decode("utf8")

    def getX(self, size):
        self.pos += size
        #return ''.join(map(str, struct.unpack_from("B"*size, self.data, self.pos - size)))
        return self.data[self.pos-size:self.pos]

    def getData(self):
        return self.data[self.pos:]

    def position(self, instance=None):
        self.pos += 5
        x,y,z = unpack("<HHB", self.data[self.pos - 5:self.pos])
        return Position(x, y, z, instance)

    def stackPosition(self, instance=None):
        self.pos += 6
        x,y,z, stackPos = unpack("<HHBB", self.data[self.pos - 6:self.pos])
        return StackPosition(x, y, z, stackPos, instance)

class TibiaPacket:
    def __init__(self, header=None):
        self.data = [b""]
        self.raw = self.data.append
        self.length = 0
        self.stream = None
        if header:
            self.uint8(header)

    def clear(self):
        self.data = [b""]
        self.raw = self.data.append
        self.length = 0

    # 8bit - 1byte, C type: char
    def uint8(self, data, pack = uint8Prebuild):
        self.raw(pack[data])
        self.length += 1
        
    def int8(self, data, pack=pack):
        self.raw(pack("<b", data))
        self.length += 1

    # 16bit - 2bytes, C type: short
    def uint16(self, data, pack=pack_uint16):
        self.raw(pack(data))
        self.length += 2
        
    def int16(self, data, pack=pack):
        self.raw(pack("<h", data))
        self.length += 2

    # 32bit - 4bytes, C type: int
    def uint32(self, data, pack=pack_uint32):
        self.raw(pack(data))
        self.length += 4
        
    def int32(self, data):
        self.raw(pack("<i", data))
        self.length += 4
        
    # 64bit - 8bytes, C type: long long
    def uint64(self, data):
        self.raw(pack("<Q", data))
        self.length += 8
        
    def int64(self, data):
        data = int(data)
        self.raw(pack("<q", data))
        self.length += 8

    def double(self, data):
        self.uint8(3)
        self.uint32((round(data, 3) * 1000) + 0x7FFFFFFF)

    def string(self, string, pack=pack):
        length = len(string)
        self.uint16(length)
        self.raw(string.encode('iso8859-1'))
        self.length += length

    def put(self, string):
        string = str(string)
        self.length += len(string)
        self.raw(string)

    if config.lagPolicy == 1:
        def send(self, stream):
            call_later(config.lagTarget, self._send, stream, self.data, self.length)
    elif config.lagPolicy == 2:
        def send(self, stream):
            delay = config.lagTarget - stream.ping
            if delay <= 0.01: # Rounding error.
                self._send(stream, self.data, self.length)
            else:
                call_later(delay, self._send, stream, self.data, self.length)
    else:
        def send(self, stream):
            self._send(stream, self.data, self.length)

    # The send process.
    def _send(self, stream, data, length, pack_length=pack_uint16, pack_header = pack_header, adler32=adler32, encryptXTEA=encryptXTEA):
        if not stream:
            return
            
        if stream.webSocket is True:
            stream.write_message(b''.join(data), True)
        else:
            data[0] = pack_length(length)
            length += 2

            if stream.xtea:
                data = encryptXTEA(data, stream.xtea, length)
            else:
                data = b''.join(data)
            stream.transport.write(b''.join((pack_header(len(data)+4, adler32(data)), data)))

    # For use with with statement. Easier :)
    def __exit__(self, type, value, traceback):
        if not type:
            self.send(self.stream)

    def __enter__(self):
        return self
