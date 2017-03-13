# A file where we store all error excetions, work a bit like otserv's return values


class BaseError(Exception):
    def __init__(self, value=""):
        self.value = value
    def __str__(self):
        if self.value:
            return repr(self.value)
        else:
            return ""

class ImpossibleMove(BaseError): pass
class Cheat(BaseError): pass
class SolidTile(BaseError): pass

# Spells
class SpellDefinition(BaseError): pass
class SpellDoesNotExist(BaseError):
    def __str__(self):
        return "'%s' is not registered!" % self.value
        
class RuneDoesNotExist(SpellDoesNotExist): pass

# Position
class PositionOutOfRange(BaseError): pass
class PositionNegative(BaseError): pass

# Messages
class MsgNotPossible(BaseError): pass
class MsgCancel(BaseError): pass
class MsgUnmarkedPlayer(BaseError): pass
class MsgCantUseObjectThatFast(BaseError): pass
