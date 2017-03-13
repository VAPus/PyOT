import game.const as enum
import config
from tornado import gen

# Interface.
class CreatureTalking(object):
    # Talking
    def say(self, message, messageType=None):
        if not messageType:
            messageType = self.defaultSpeakType

        for spectator in getSpectators(self.position, config.sayRange):
            stream = spectator.packet(0xAA)
            stream.uint32(0)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"] if "level" in self.data else 0)
            assert stream.const(messageType) > 0
            stream.uint8(stream.const(messageType))
            stream.position(self.position)
            stream.string(message)
            stream.send(spectator)

    def yell(self, message, messageType=None):
        if not messageType:
            messageType = self.defaultYellType

        for spectator in getSpectators(self.position, config.yellRange):
            stream = spectator.packet(0xAA)
            stream.uint32(0)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"] if "level" in self.data else 0)
            assert stream.const(messageType) > 0
            stream.uint8(stream.const(messageType))
            stream.position(self.position)
            stream.string(message.upper())
            stream.send(spectator)

    def whisper(self, message, messageType=enum.MSG_SPEAK_WHISPER):
        group = getSpectators(self.position, config.whisperRange)
        listeners = getSpectators(self.position, config.sayRange) - group

        for spectator in group:
            stream = spectator.packet(0xAA)
            stream.uint32(0)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"] if "level" in self.data else 0)
            assert stream.const(messageType) > 0
            stream.uint8(stream.const(messageType))
            stream.position(self.position)
            stream.string(message)
            stream.send(spectator)

        for spectator in listeners:
            stream = spectator.packet(0xAA)
            stream.uint32(0)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"] if "level" in self.data else 0)
            stream.uint8(stream.const(messageType))
            stream.position(self.position)
            stream.string(config.whisperNoise)
            stream.send(spectator)

    def broadcast(self, message, messageType=enum.MSG_GAMEMASTER_BROADCAST):
        import game.players
        for player in game.player.allPlayersObject:
            stream = player.packet(0xAA)
            stream.uint32(0)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"] if "level" in self.data else 0)
            stream.uint8(stream.const(messageType))
            stream.position(self.position)
            stream.string(message)
            stream.send(player.client)

    def sayPrivate(self, message, to, messageType=enum.MSG_PRIVATE_FROM):
        if not to.isPlayer(): return

        stream = to.packet(0xAA)
        stream.uint32(0)
        stream.string(self.data["name"])
        stream.uint16(self.data["level"] if "level" in self.data else 0)
        stream.uint8(stream.const(messageType))
        stream.position(self.position)
        stream.string(message)
        stream.send(to.client)
        
    # Messages
    def message(self, message, msgType=None, color=0, value=0, pos=None):
        pass

    def lmessage(self, message, msgType=None, color=0, value=0, pos=None):
        pass

    def lcmessage(self, context, message, msgType=None, color=0, value=0, pos=None):
        pass
    
    def lcpmessage(self, context, singular, plural, n, msgType=None, color=0, value=0, pos=None):
        pass
    
    def lpmessage(self, singular, plural, n, msgType=None, color=0, value=0, pos=None):
        pass
    
    def playerSay(self, player, say, type, channel):
        pass # Override me
        
class PlayerTalking(CreatureTalking):
    def message(self, message, msgType=enum.MSG_INFO_DESCR, color=0, value=0, pos=None):
        stream = self.packet()
        stream.message(self, message, msgType, color, value, pos)
        stream.send(self.client)

    def lmessage(self, message, msgType=enum.MSG_INFO_DESCR, color=0, value=0, pos=None):
        self.message(self.l(message), msgType, color, value, pos)
        
    def lcmessage(self, context, message, msgType=enum.MSG_INFO_DESCR, color=0, value=0, pos=None):
        self.message(self.lc(context, message), msgType, color, value, pos)
    
    def lcpmessage(self, context, singular, plural, n, msgType=enum.MSG_INFO_DESCR, color=0, value=0, pos=None):
        self.message(self.lcp(context, singular, plural, n), msgType, color, value, pos)
    
    def lpmessage(self, singular, plural, n, msgType=enum.MSG_INFO_DESCR, color=0, value=0, pos=None):
        self.message(self.lp(singular, plural, n), msgType, color, value, pos)
        
    def orangeStatusMessage(self, message, msgType=enum.MSG_STATUS_CONSOLE_ORANGE, color=0, value=0, pos=None):
        stream = self.packet()
        stream.message(self, message, msgType, color, value, pos)
        stream.send(self.client)
        
    def windowMessage(self, text):
        stream = self.packet(0x15)
        stream.string(text)
        stream.send(self.client)

    def cancelMessage(self, message):
        if self.raiseMessages:
            raise MsgCancel(message)
        self.message(message, MSG_STATUS_SMALL)

    def notPossible(self):
        if self.raiseMessages:
            raise MsgNotPossible
        self.cancelMessage(_l(self, "Sorry, not possible."))

    def cantUseObjectThatFast(self):
        if self.raiseMessages:
            raise MsgCantUseObjectThatFast
        self.cancelMessage(_l(self, "You cannot use objects that fast."))
        
    def notPickupable(self):
        self.cancelMessage(_l(self, "You cannot take this object."))

    def tooHeavy(self):
        self.cancelMessage(_l(self, "This object is too heavy for you to carry."))

    def outOfRange(self):
        self.cancelMessage(_l(self, "Destination is out of range."))

    def notEnoughRoom(self):
        self.cancelMessage(_l(self, "There is not enough room."))

    def exhausted(self):
        self.cancelMessage(_l(self, "You are exhausted."))

    def needMagicItem(self):
        self.cancelMessage(_l(self, "You need a magic item to cast this spell."))

    def notEnough(self, word):
        self.cancelMessage(_l(self, "You do not have enough %s." % _l(self, word)))

    def onlyOnCreatures(self):
        self.cancelMessage(_l(self, "You can only use it on creatures."))

    def unmarkedPlayer(self):
        if self.raiseMessages:
            raise MsgUnmarkedPlayer
        self.cancelMessage(_l(self, "Turn secure mode off if you really want to attack unmarked players."))
        
    # Channel system
    def openChannels(self):
        channels = game.chat.getChannels(self)
        
        # Add guild chat.
        if self.guild():
            channels[CHANNEL_GUILD] = self.guild().chatChannel
            
        # Add party channel.
        if self.party():
            channels[CHANNEL_PARTY] = self.party().chatChannel
            
        channels2 = game.scriptsystem.get("requestChannels").run(creature=self, channels=channels)
        if type(channels2) is dict:
            channels = channels2

        with self.packet() as stream:
            stream.openChannels(channels)

    def openChannel(self, id):

        if (game.scriptsystem.get("joinChannel").run(creature=self, channelId=id)):
            if id == CHANNEL_GUILD:
                # Guild channel.
                channel  = self.guild().chatChannel
            elif id == CHANNEL_PARTY:
                # Party channel.
                channel = self.party().chatChannel
            else:
                channel = game.chat.getChannel(id)

            if not channel:
                self.cancelMessage(_l(self, "Channel not found."))
                return
            
            stream = self.packet()
            stream.openChannel(channel)
            stream.send(self.client)

            channel.addMember(self)

    def openPrivateChannel(self, between):
        # Self open
        if not self.isChannelOpen(between):
            self._openChannels[between.name()] = [0xFFFF, between]
            if between.isPlayer():
                stream = self.packet(0xAD)
            else:
                stream = self.packet(0xB2)
                stream.uint16(0xFFFF)

            stream.string(between.name())
            stream.send(self.client)

        # Notify between if required.
        if not between.isChannelOpen(self):
            between.openPrivateChannel(self)

        return 0xFFFF

    def closePrivateChannel(self, between):
        if between.name() in self._openChannels:
            betweenObj = self._openChannels[between.name()]
            stream = self.packet(0xB3)
            stream.uint16(betweenObj[0])
            stream.send(self.client)

    def closeChannel(self, id):
        channel = game.chat.getChannel(id)
        channel.removeMember(self)

        game.scriptsystem.get("leaveChannel").run(creature=self, channelId=id)

    def isChannelOpen(self, between):
        try:
            return self._openChannels[between.name()]
        except:
            return False

    def channelMessage(self, text, channelType=enum.MSG_CHANNEL, channelId=0):
        if channelId == CHANNEL_GUILD:
            channel = self.guild().chatChannel
        elif channelId == CHANNEL_PARTY:
            channel = self.party().chatChannel
        else:
            channel = game.chat.getChannel(channelId)
        try:
            members = channel.members
        except:
            members = []

        members2 = game.scriptsystem.get("getChannelMembers").run(channelId, creature=self, channelId=channelId, text=text, type=channelType, members=members)
        if not members and type(members2) != list:
            return False

        elif type(members2) == list:
            members = members2

        if not members:
            return False # No members

        # At to the channel archives:
        
        messageId = channel.addMessage(self, text, channelType)
        
        for player in members:
            stream = player.packet(0xAA)
            stream.uint32(messageId)
            stream.string(self.data["name"])
            if self.isPlayer():
                stream.uint16(self.data["level"])
            else:
                stream.uint16(0)
            stream.uint8(stream.const(channelType))
            if channelType in (MSG_CHANNEL_MANAGEMENT, MSG_CHANNEL, MSG_CHANNEL_HIGHLIGHT):
                stream.uint16(channelId)

            stream.string(text)
            stream.send(player.client)

        return True

    def privateChannelMessage(self, text, receiver, channelType=enum.MSG_CHANNEL):
        player = getPlayer(receiver)
        if player:
            stream = player.packet(0xAA)
            stream.uint32(1)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"])
            stream.uint8(stream.const(channelType))
            stream.string(text)
            stream.send(player.client)

            return True
            
        return False
        
    def isPrivate(self, name):
        try:
            return self.openChannels[name]
        except:
            pass

    def notifyPrivateSay(self, sayer, text):
        pass # Not supported yet
        
    def handleSay(self, channelType, channelId, reciever, text):
        if len(text) > config.maxLengthOfSay:
            self.message(_l(self, "Message too long"))
            return

        splits = text.split(" ")
        mode = channelType
        if channelId == 1:
            if splits[0] == "#y":
                mode = enum._MSG_SPEAK_YELL
                del splits[0]
            elif splits[0] == "#w":
                mode = enum._MSG_SPEAK_WHISPER
                del splits[0]

        doRegex = True

        if len(splits) > 1:
            d = game.scriptsystem.get("talkactionFirstWord").run(splits[0], creature=self, text=' '.join(splits[1:]))

            if d != None:
                doRegex = False
            if not d and d != None:
                return
        
        
        d = game.scriptsystem.get("talkaction").run(text, creature=self, text=text)

        if d != None:
            doRegex = False
        if not d and d != None:
            return
            
        if doRegex:
            d = game.scriptsystem.get("talkactionRegex").run(text, creature=self, text=text)

            if not d and d != None:
                return
                
        if channelType in (enum._MSG_SPEAK_SAY, enum._MSG_SPEAK_YELL, enum._MSG_SPEAK_WHISPER):
            if mode == enum._MSG_SPEAK_SAY:
                self.say(text)

            elif mode == enum._MSG_SPEAK_YELL:
                self.yell(text)

            elif mode == enum._MSG_SPEAK_WHISPER:
                self.whisper(text)

        elif channelType == enum._MSG_CHANNEL:
            self.channelMessage(text, MSG_CHANNEL, channelId)

        #elif channelType == enum.MSG_PRIVATE_TO:
        else:
            self.privateChannelMessage(text, reciever, MSG_PRIVATE_FROM)

        for creature in getCreatures(self.position):
            creature.playerSay(self, text, channelType, channelId or reciever)
