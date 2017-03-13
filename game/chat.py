import weakref

channels = {}
GLOBAL_MESSAGES = []

class Channel(object):
    def __init__(self, name, id, public=False):
        self.id = id
        self.members = []
        self.messages = []
        self.invites = []
        self.name = name
        self.public = public

    def addMember(self, player):
        self.members.append(weakref.proxy(player))

    def addInvite(self, player):
        self.invites.append(weakref.proxy(player))
        
    def removeMember(self, player):
        try:
            self.members.remove(player)
            return True
        except:
            return False

    def removeInvites(self, player):
        try:
            self.invites.remove(player)
            return True
        except:
            return False
            
    def isMember(self, player):
        if player in self.members:
            return True
        return False
        
    def canJoin(self, player):
        # TODO: Admin/moderator features
        if self.public:
            return True
        elif player in self.invites:
            return True
        else:
            return False
            
    def addMessage(self, player, text, type):
        id = len(GLOBAL_MESSAGES) # First get the next ID.
        self.messages.append((weakref.proxy(player), text, type)) # Then we append the tuple.
        GLOBAL_MESSAGES.append((weakref.proxy(player), self, text, type)) # Then we append the tuple.
        return id
        
    def getLocalMessage(self, messageId):
        try:
            return self.messages[messageId]
        except:
            assert messageId < len(self.messages)
            return None
            
    def getMessage(self, messageId):
        try:
            return GLOBAL_MESSAGES[messageId]
        except:
            assert messageId < len(GLOBAL_MESSAGES)
            return None        
            
def openChannel(channelName, id = None, public=True):
    channelId = id or (len(channels) + CHANNEL_OFFSET)
    channel = Channel(channelName, channelId, public)
    channels[channelId] = channel
    return channel

def openInstanceChannel(channelName, id):
    channelId = id
    channel = Channel(channelName, channelId, False)
    return channel

def delChannel(channelId):
    try:
        del channels[channelId]
    except:
        pass

def getChannelsWithPlayer(player):
    channelList = []
    for channelId in channels:
        channel = channels[channelId]
        if player in channel.members:
            channelList.append(channel)

    return channelList

def getChannels(player):
    channelList = {}
    for channelId in channels:
        channel = channels[channelId]
        if channel.canJoin(player):
            channelList[channelId] = channel

    return channelList
    
def getChannel(id):
    try:
        return channels[id]
    except:
        return
        
def getMessage(self, messageId):
    try:
        return GLOBAL_MESSAGES[messageId]
    except:
        assert messageId < len(GLOBAL_MESSAGES)
        return None   