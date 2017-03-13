# This is a shadow of the main branch, 9.1
from . import base
import sys
import math
import game.const
import game.item
from struct import pack

p860 = sys.modules["game.protocols.860"]
provide = [871]

def verify(): return True

class Packet(base.BasePacket):
    maxOutfits = 25
    protocolEnums = {}
    protocolEnums["_MSG_NONE"] = 0
    protocolEnums["_MSG_SPEAK_SAY"] = 0x01
    protocolEnums["_MSG_SPEAK_WHISPER"] = 0x02
    protocolEnums["_MSG_SPEAK_YELL"] = 0x03
    protocolEnums["_MSG_NPC_TO"] = 0x04
    protocolEnums["_MSG_NPC_FROM"] = 0x05
    protocolEnums["_MSG_PRIVATE_FROM"] = 0x06
    protocolEnums["_MSG_PRIVATE_TO"] = 0x06
    protocolEnums["_MSG_CHANNEL_MANAGEMENT"] = 0x07
    protocolEnums["_MSG_CHANNEL"] = 0x08
    

    protocolEnums["_MSG_GAMEMASTER_CHANNEL"] = 0x0A
    protocolEnums["_MSG_GAMEMASTER_PRIVATE_TO"] = 0x0B
    protocolEnums["_MSG_CHANNEL_HIGHLIGHT"] = 0x0C
    protocolEnums["_MSG_SPEAK_MONSTER_SAY"] = 0x0D
    protocolEnums["_MSG_EVENT_ORANGE"] = 0x0D
    protocolEnums["_MSG_SPEAK_MONSTER_YELL"] = 0x0E
    protocolEnums["_MSG_STATUS_CONSOLE_ORANGE"] = 0x0E
    protocolEnums["_MSG_STATUS_WARNING"] = 0x0F
    
    protocolEnums["_MSG_EVENT_ADVANCE"] = 0x10
    protocolEnums["_MSG_STATUS_DEFAULT"] = 0x11
    protocolEnums["_MSG_EVENT_DEFAULT"] = 0x12
    protocolEnums["_MSG_INFO_DESCR"] = 0x13
    protocolEnums["_MSG_STATUS_SMALL"] = 0x14
    protocolEnums["_MSG_STATUS_CONSOLE_BLUE"] = 0x15    
    protocolEnums["_MSG_STATUS_CONSOLE_RED"] = 0x16
    
    #Temporary
    protocolEnums["_MSG_HEALED"] = 0x11
    
    # Alias
    protocolEnums["_MSG_DAMAGE_RECEIVED"] = protocolEnums["_MSG_EVENT_DEFAULT"]
    protocolEnums["_MSG_DAMAGE_DEALT"] = protocolEnums["_MSG_EVENT_DEFAULT"]
    protocolEnums["_MSG_LOOT"] = protocolEnums["_MSG_INFO_DESCR"]
    protocolEnums["_MSG_PARTY"] = protocolEnums["_MSG_INFO_DESCR"]
    protocolEnums["_MSG_HOTKEY_USE"] = protocolEnums["_MSG_INFO_DESCR"]
    protocolEnums["_MSG_PARTY_MANAGEMENT"] = protocolEnums["_MSG_INFO_DESCR"]
    protocolEnums["_MSG_TRADE_NPC"] = protocolEnums["_MSG_INFO_DESCR"]
    protocolEnums["_MSG_EXPERIENCE"] = protocolEnums["_MSG_EVENT_ADVANCE"]
    
    # Skulls
    protocolEnums['SKULL_ORANGE'] = 0 # Don't send orange skulls
    
    def const(self, key):
        return self.protocolEnums[key]
    # Couple of things from 8.6
    def item(self, item, count=None):
        if isinstance(item, game.item.Item):
            cid = item.cid
            if cid > 11703:
                if item.solid:
                    self.uint16(100)
                elif item.pickable and item.movable:
                    if item.containerSize:
                        self.uint16(1987)
                    elif item.weaponType:
                        self.uint16(3264)
                    elif item.usable:
                        self.uint16(110)
                    else:
                        self.uint16(1780)
                else:
                    self.uint16(104)
                    
            else:    
                self.uint16(cid)

                if item.stackable:
                    self.uint8(item.count or 1)
                elif item.type == 11 or item.type == 12:
                    self.uint8(item.fluidSource or 0)
                """if item.animation:
                    self.uint8(0xFE)""" # No animations in 8.6
            
        else:
            self.uint16(item)
            if count:
                self.uint8(count)
    
    def tileDescription(self, tile, player):
        count = 0
        for item in tile.topItems():  
            self.item(item)
            count += 1
            if count == 10:
                return
        if not tile.things: return
        for creature in tile.creatures():
            if creature.isMonster() and creature.hasCondition(CONDITION_INVISIBLE):
                continue

            known = False
            removeKnown = 0
            if player:
                known = creature in player.knownCreatures
                    
                if not known:
                    if len(player.knownCreatures) > self.maxKnownCreatures:
                        removeKnown = player.checkRemoveKnown()
                        if not removeKnown:
                            player.exit("Too many creatures in known list. Please relogin")
                            return
                    player.knownCreatures.add(creature)
                    creature.knownBy.add(player)
                    
                    self.creature(creature, known, removeKnown, player)
                else:
                    # Bugged?
                    if creature.creatureType != 0 and creature.brainEvent:
                        self.raw(pack("<HIB", 99, creature.clientId(), creature.direction))
                        self.length += 7
                    else:
                        self.creature(creature, True, creature.cid, player) # Not optimal!

            if creature.creatureType != 0 and not creature.brainEvent:
                creature.base.brain.beginThink(creature, False)
                    
            count += 1
            if count == 10:
                return
                
        for item in tile.bottomItems():
            self.item(item)
            count += 1
            if count == 10:
                return
        
    def creature(self, creature, known, removeKnown=0, player=None):
        if known:
            self.uint16(0x62)
            self.uint32(creature.clientId())
        else:
            self.uint16(0x61)
            self.uint32(removeKnown) # Remove known
            self.uint32(creature.clientId())
            #self.uint8(creature.creatureType)
            self.string(creature.name())
        
        self.uint8(int(round((float(creature.data["health"]) / creature.data["healthmax"]) * 100))) # Health %
        self.uint8(creature.direction) # Direction
        self.outfit(creature.outfit, creature.addon, creature.mount if creature.mounted else 0x00)
        self.uint8(creature.lightLevel) # Light
        self.uint8(creature.lightColor) # Light
        self.uint16(int(creature.speed)) # Speed
        self.uint8(creature.getSkull(player)) # Skull
        self.uint8(creature.getShield(player)) # Party/Shield
        if not known:
            self.uint8(creature.getEmblem(player)) # Emblem
        self.uint8(creature.solid) # Can't walkthrough
        
    def skills(self, player):
        self.uint8(0xA1) # Skill type
        for x in range(SKILL_FIRST, SKILL_LAST+1):
            self.uint8(player.skills[x]) # Value / Level
            currHits = player.data["skill_tries"][x]
            goalHits = player.skillGoals[x]
            if currHits < 1:
                self.uint8(0)
            else:
                self.uint8(int(round((currHits / goalHits) * 100))) # %
        
    def status(self, player):
        self.uint8(0xA0)
        self.uint16(player.data["health"])
        self.uint16(player.data["healthmax"])
        self.uint32(player.data["capacity"] - player.inventoryWeight) # TODO: Free Capacity
        #self.uint32(player.data["capacity"] * 100) # TODO: Cap
        self.uint64(player.data["experience"]) # TODO: Virtual cap? Experience
            
        if player.data["level"] > 0xFFFF:
            self.uint16(0xFFFF)
        else:
            self.uint16(player.data["level"]) # TODO: Virtual cap? Level
            
        self.uint8(int(math.ceil(float(config.levelFormula(player.data["level"]+1)) / player.data["experience"]))) # % to next level, TODO
        self.uint16(player.data["mana"]) # mana
        self.uint16(player.data["manamax"]) # mana max
        self.uint8(player.data["maglevel"]) # TODO: Virtual cap? Manalevel
        #self.uint8(1) # TODO: Virtual cap? ManaBase
        self.uint8(int(player.data["manaspent"] / int(config.magicLevelFormula(player.data["maglevel"], player.getVocation().mlevel)))) # % to next level, TODO
        self.uint8(player.data["soul"]) # TODO: Virtual cap? Soul
        self.uint16(min(42 * 60, int(player.data["stamina"] / 60))) # Stamina minutes
        #self.uint16(player.speed) # Speed
        
        #self.uint16(0x00) # Condition

    def openChannel(self, channel):
        self.uint8(0xAC)
        self.uint16(channel.id)
        self.string(channel.name)

    def message(self, player, message, msgType=MSG_STATUS_DEFAULT, color=0, value=0, pos=None):
        self.uint8(0xB4)
        self.uint8(self.const(msgType))
        self.string(message)
        
class Protocol(base.BaseProtocol):
    Packet = Packet
