# This is a shadow of the main branch, 9.1. TODO: Update for 8.54 changes
from . import base
import config
import math
import game.const
import game.item
from struct import pack

provide = []

def verify():
    return True
    
class Packet(base.BasePacket):
    maxKnownCreatures = 250
    maxOutfits = 25
    maxMounts = 0
    protocolEnums = {}
    protocolEnums["_MSG_NONE"] = 0
    protocolEnums["_MSG_SPEAK_SAY"] = 0x01
    protocolEnums["_MSG_SPEAK_WHISPER"] = 0x02
    protocolEnums["_MSG_SPEAK_YELL"] = 0x03
    protocolEnums["_MSG_NPC_TO"] = 0x04
    protocolEnums["_MSG_NPC_FROM"] = 0x05
    protocolEnums["_MSG_SPEAK_MONSTER_SAY"] = 0x13
    protocolEnums["_MSG_SPEAK_MONSTER_YELL"] = 0x14
    
    protocolEnums["_MSG_STATUS_CONSOLE_RED"] = 0x12
    protocolEnums["_MSG_EVENT_ORANGE"] = 0x13
    protocolEnums["_MSG_STATUS_CONSOLE_ORANGE"] = 0x14
    protocolEnums["_MSG_STATUS_WARNING"] = 0x15
    protocolEnums["_MSG_EVENT_ADVANCE"] = 0x16
    protocolEnums["_MSG_EVENT_DEFAULT"] = 0x17
    protocolEnums["_MSG_STATUS_DEFAULT"] = 0x18
    protocolEnums["_MSG_INFO_DESCR"] = 0x19
    protocolEnums["_MSG_STATUS_SMALL"] = 0x1A
    protocolEnums["_MSG_STATUS_CONSOLE_BLUE"] = 0x1B
    protocolEnums["_MSG_HEALED"] = 0x0C
    # Alias
    protocolEnums['_MSG_DAMAGE_RECEIVED'] = protocolEnums["_MSG_EVENT_DEFAULT"]
    protocolEnums['_MSG_DAMAGE_DEALT'] = protocolEnums["_MSG_EVENT_DEFAULT"]
    protocolEnums['_MSG_LOOT'] = protocolEnums["_MSG_INFO_DESCR"]
    protocolEnums['_MSG_EXPERIENCE'] = protocolEnums["_MSG_EVENT_ADVANCE"]
    
    # Skulls
    protocolEnums['SKULL_ORANGE'] = 0 # Don't send orange skulls
        
    def item(self, item, count=None):
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

            #Client Charges enters here too(?)
            # ONLY if there is REGULAR items, not SolidItem or StaticItem.
            if type(item) is Item:
                if item.stackable:
                    self.uint8(item.count or 1)
                elif item.type in (11, 12):
                    self.uint8(item.fluidSource or 0)
            
    def tileDescription(self, tile, player):
        count = 0
        for thing in tile:
            if thing.isItem():
                self.item(thing)
            else:
                if thing.hasCondition(CONDITION_INVISIBLE):
                    continue
                known = False
                removeKnown = 0
                if player:
                    known = thing in player.knownCreatures

                    if not known:
                        if len(player.knownCreatures) > self.maxKnownCreatures:
                            removeKnown = player.checkRemoveKnown()
                            if not removeKnown:
                                player.exit("Too many creatures in known list. Please relogin")
                                return
                        player.knownCreatures.add(thing)
                        thing.knownBy.add(player)

                        self.creature(thing, known, removeKnown, player)
                    else:
                        # Bugged?
                        if thing.creatureType != 0 and thing.brainEvent:
                            self.raw(pack("<HIB", 99, thing.clientId(), thing.direction))
                            self.length += 7
                        else:
                            self.creature(thing, True, thing.cid, player) # Not optimal!
                if thing.creatureType != 0 and not thing.brainEvent:
                    thing.base.brain.beginThink(thing, False)
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
        
    def status(self, player):
        self.uint8(0xA0)
        self.uint16(player.data["health"])
        self.uint16(player.data["healthmax"])
        self.uint32(player.data["capacity"] - player.inventoryWeight) # TODO: Free Capacity
        #self.uint32(player.data["capacity"] * 100) # TODO: Cap
        if player.data["experience"] <= 0x7FFFFFFF:
            self.uint32(player.data["experience"]) # TODO: Virtual cap? Experience
        else:
            self.uint32(0)
            
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

    def skills(self, player):
        self.uint8(0xA1) # Skill type
        for x in range(SKILL_FIRST, SKILL_LAST+1):
            self.uint8(player.skills[x]) # Value / Level
            #self.uint8(player.data["skills"][x]) # Base
            currHits = player.data["skill_tries"][x]
            goalHits = player.skillGoals[x]
            if currHits < 1:
                self.uint8(0)
            else:
                self.uint8(int(round((currHits / goalHits) * 100))) # %
                
    def outfit(self, look, addon=0, mount=0x00):
        
        self.uint16(look[0])
        if look[0] != 0:
            self.uint8(look[1])
            self.uint8(look[2])
            self.uint8(look[3])
            self.uint8(look[4])
            self.uint8(addon)
        else:
            self.uint16(look[1])
            
        #self.uint16(mount) # Mount

    def cooldownIcon(self, icon, cooldown):
        pass # Not sendt
        
    def cooldownGroup(self, group, cooldown):
        pass # Not sendt

    def violation(self, flag):
        self.uint8(0x0B)
        self.uint8(flag)

    def message(self, player, message, msgType=game.const.MSG_STATUS_DEFAULT, color=0, value=0, pos=None):
        self.uint8(0xB4)
        """if msgType in ('MSG_DAMAGE_DEALT', 'MSG_DAMAGE_RECEIVED', 'MSG_DAMAGE_OTHERS'):
            if pos:
                self.position(pos)
            else:
                self.position(self.position)
            self.uint8(color)
        elif msgType in ('MSG_EXPERIENCE', 'MSG_EXPERIENCE_OTHERS', 'MSG_HEALED', 'MSG_HEALED_OTHERS'):
            if pos:
                self.position(pos)
            else:
                self.position(self.position)
            self.uint8(color)
        else:"""
        self.uint8(self.const(msgType))
        self.string(message)
        
    def skull(creatureId, skull):
        if skull == SKULL_ORANGE: return
        self.uint8(0x90)
        self.uint32(creatureId)
        self.uint8(skull)

    def cancelTarget( self ):
        self.uint8( 0xA3 )
        
        
class Protocol(base.BaseProtocol):
    Packet = Packet
