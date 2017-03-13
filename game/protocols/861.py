# This is a shadow of the main branch, 9.1
import sys

provide = []

def verify(): return True

class Packet(sys.modules["game.protocols.860"].Packet):
    protocolEnums = sys.modules["game.protocols.860"].Packet.protocolEnums
    protocolEnums["MSG_SPEAK_MONSTER_SAY"] = 0x0D
    protocolEnums["MSG_SPEAK_MONSTER_YELL"] = 0x0E
    
    protocolEnums["MSG_STATUS_CONSOLE_ORANGE"] = 0x0D
    protocolEnums["MSG_EVENT_ORANGE"] = 0x0E
    protocolEnums["MSG_STATUS_WARNING"] = 0x0F
    protocolEnums["MSG_EVENT_ADVANCE"] = 0x10
    protocolEnums["MSG_EVENT_DEFAULT"] = 0x11
    protocolEnums["MSG_STATUS_DEFAULT"] = 0x12
    protocolEnums["MSG_INFO_DESCR"] = 0x13
    protocolEnums["MSG_STATUS_SMALL"] = 0x14
    protocolEnums["MSG_STATUS_CONSOLE_BLUE"] = 0x15
    protocolEnums["MSG_STATUS_CONSOLE_RED"] = 0x16
    

class Protocol(sys.modules["game.protocols.860"].Protocol):
    Packet = Packet
