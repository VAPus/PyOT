import config
from struct import pack, unpack
import codecs
import sys

ffi = None
lib = None
try:
    # Attempt to use CFFI for decrypt/encrypt XTEA.
    import cffi
    ffi = cffi.FFI()
    ffi.cdef("""uint64_t xtea_decrypt(uint64_t v, uint32_t const key[64]);
    uint64_t xtea_encrypt(uint64_t v, uint32_t const key[64]);""")
    lib = ffi.verify("""uint64_t xtea_decrypt(uint64_t v, uint32_t const key[64]) {
    unsigned int i;
    uint32_t v1 = v >> 32, v0 = v & 0xffffffff;
    for (i=0; i < 32; i++) {
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ key[63 - i];
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ key[31 - i];
    }
    return (uint64_t)(v1) << 32 | v0;
    }
    uint64_t xtea_encrypt(uint64_t v, uint32_t const key[64]) {
    unsigned int i;
    uint32_t v1 = v >> 32, v0 = v & 0xffffffff; 
    for (i=0; i < 32; i++) {
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ key[i];
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ key[32 + i];
    }
    return (uint64_t)(v1) << 32 | v0;
    }
    """, extra_compile_args=["-Ofast", "-march=native"])
except:
    print("No CFFI")

if ffi and not lib:
    ffi = None

D = int(config.RSAKeys["d"])
N = int(config.RSAKeys["n"])

def bytes( long_int ):
    bytes = bytearray()
    while long_int != 0:
        b = long_int & 255
        bytes.append( b )
        long_int >>= 8
    bytes.append( 0 )
    bytes.reverse()
    return bytes

def decryptRSA(stream):
    return bytes(pow(int.from_bytes(stream, 'big'), D, N))

if ffi:
    def decryptXTEA(stream, k):
        length = len(stream) >> 3
        bstr = "<%dQ" % length
        packs = unpack(bstr, stream)
        repacks = []

        for v in packs:
            repacks.append(lib.xtea_decrypt(v, k))

        return pack(bstr, *repacks)

    def encryptXTEA(stream, k, length):
        pad = 8 - (length & 7)
        if pad:
            stream.append(b"\x33" * pad)
        length += pad
        length >>= 3
        stream = b''.join(stream)
        bstr = "<%dQ" % length
        packs = unpack(bstr, stream)
        repacks = []

        for v in packs:
            repacks.append(lib.xtea_encrypt(v, k))


        return pack(bstr, *repacks)

else:
    def decryptXTEA(stream, k):
        length = len(stream) >> 2
        bstr = "<%dL" % length
        packs = list(unpack(bstr, stream))

        for pos in range(0, length, 2):
            v0 = packs[pos]
            v1 = packs[pos+1]
            for i in range(32):
                v1 = (v1 - (((v0<<4 ^ v0>>5) + v0) ^ k[63-i])) & 0xffffffff
                v0 = (v0 - (((v1<<4 ^ v1>>5) + v1) ^ k[31-i])) & 0xffffffff
            packs[pos] = v0
            packs[pos+1] = v1

        return pack(bstr, *packs)

    def encryptXTEA(stream, k, length):
        pad = 8 - (length & 7)
        if pad:
            stream.append(b"\x33" * pad)
        length += pad
        length >>= 2
        stream = b''.join(stream)
        bstr = "<%dL" % length

        packs = list(unpack(bstr, stream))

        for pos in range(0, length, 2):
            v0 = packs[pos]
            v1 = packs[pos+1]
            for i in range(32):
                v0 = (v0 + (((v1<<4 ^ v1>>5) + v1) ^ k[i])) & 0xffffffff
                v1 = (v1 + (((v0<<4 ^ v0>>5) + v0) ^ k[32 + i])) & 0xffffffff
            packs[pos] = v0
            packs[pos+1] = v1


        return pack(bstr, *packs)
