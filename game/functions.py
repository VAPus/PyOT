"""A collection of functions that almost every other component requires"""
from collections import deque
from tornado import gen
import time
import game.map
import config
import math
from . import sql
from . import otjson
import sys
import random
import game.vocation
import game.resource
import game.scriptsystem
import game.errors
import glob
import game.protocol
from . import logger
import game.chat
import re
import subprocess
import platform
import os
import game.deathlist
import game.ban
import itertools

import pickle

# Some half important constants
globalStorage = {'storage':{}, 'objectStorage':{}}
saveGlobalStorage = False
jsonFields = 'storage',
pickleFields = 'objectStorage',
groups = {}
globalize = ["magicEffect", "summonCreature", "relocate", "transformItem", "placeItem", "calculateWalkPattern", "getCreatures", "getPlayers", "getSpectators", "placeInDepot", "townNameToId", "townIdToName", "getTibiaTime", "getLightLevel", "getPlayerIDByName", "positionInDirection", "updateTile", "saveAll", "teleportItem", "getPlayer", "townPosition", "broadcast", "loadPlayer", "loadPlayerById", "getHouseByPos", "moveItem", "mail", "hasSpectators", "hasZLevelSpectators", "fastPickler"]

# Just a inner funny call
def looper(function, time):
    """Looper decorator"""

    function()
    call_later(time, looper, function, time)

def loopDecorator(time):
    """Loop function decorator.

    :param time: Run the function every ``time`` seconds.
    :type time: float (seconds).

    """

    def _decor(f):
        def new_f(*args, **kwargs):
            if f(*args, **kwargs) != False:
                call_later(time, new_f, *args, **kwargs)

        def _first(*args, **kwargs):
            call_later(0, new_f, *args, **kwargs)
        _first.__doc__ = f.__doc__
        return _first
    return _decor

# This one calculate the tiles on the way
# Calculate walk patterns
def calculateWalkPattern(creature, fromPos, to, skipFields=0, diagonal=True):
    """Calculate the route from ``fromPos`` to ``to``.

    :param fromPos: Start position.
    :type fromPos: list or tuple.

    :param to: Destination position.
    :type to: list or tuple.

    :param skipFields: Don't walk the last steps to the destination. Useful if you intend to walk close to a target.
    :type skipFields: int or None.

    :param diagonal: Allow diagonal walking?
    :type diagonal: bool.

    """
    pattern = deque()
    currPos = fromPos
    fpX = fromPos.x
    fpY = fromPos.y
    tX = to.x
    tY = to.y
    direction = None
    # First diagonal if possible
    if abs(fpX - tX) == 1 and abs(fpY - tY) == 1:
        if fpY > fpY:
            direction = 6
        else:
            direction = 4

        if fpX < fpX:
            direction += 1

    elif fpY == tY and abs(fpX - tX) == 1:
        diff = fpX - tX
        if diff == 1:
            direction = WEST
        elif diff == -1:
            direction = EAST
    elif fpX == tX and abs(fpY - tY) == 1:
        diff = fpY - tY
        if diff == 1:
            direction = NORTH
        elif diff == -1:
            direction = SOUTH


    if direction != None:
        newPos = positionInDirection(currPos, direction)

        isOk = True
        for item in game.map.getTile(newPos).getItems():
            if item.solid:
                isOk = False
                break

        if isOk:
            currPos = newPos
            pattern.append(direction)

    if not pattern:
        # Try pathfinder.
        pattern = pathfinder.findPath(creature, fromPos.z, fromPos.x, fromPos.y, to.x, to.y, fromPos.instanceId, True if skipFields else False)
        #print pattern
        if not pattern:
            return None

    # Fix for diagonal things like items
    """if len(pattern) > 2 and diagonal == True:
        last, last2 = pattern[len(pattern)-2:len(pattern)]
        if abs(last-last2) == 1:
            del pattern[len(pattern)-2:len(pattern)]
            if last == 0: # last = north, last2 must be east/west
                last = 6 + (0 if last2 == 3 else 1)
            elif last == 2: # last = south, last2 must be east/west
                last = 4 + (0 if last2 == 3 else 1)

            elif last == 1: # last = east, last2 must be
                last = 1 + (6 if last2 == 0 else 4)
            elif last == 3: # last = west, last2 must be
                last = 0 + (6 if last2 == 0 else 4)
            pattern.append(last)"""
    if skipFields < 0:
        for x in range(skipFields):
            pattern.pop()
    elif skipFields < 0:
        for x in range(-skipFields):
            pattern.popleft()
    return pattern

# Spectator list
def getSpectators(pos, radius=(8,6), ignore=()):
    """Gives you the spectators (:class:`service.gameserver.GameProtocol`) in the area.

    :param pos: Position of the center point.
    :type pos: list or tuple.
    :param radius: Radius from center point to check for players.
    :type radius: list or tuple.
    :param ignore: known spectators to ignore in the set.
    :type ignore: list, tuple or set.

    :rtype: set of :class:`service.gameserver.GameProtocol`

    """

    players = set()
    for player in game.player.allPlayersObject:
        if player.canSee(pos, radius) and player.client and player.client.ready and player not in ignore:
            players.add(player.client)

    return players

def hasSpectators(pos, radius=(8,6), ignore=()):
    """ Returns True if anyone can see the position, otherwise False. """
    for player in game.player.allPlayersObject:
        if player.canSee(pos, radius) and player not in ignore: return True

    return False

def hasZLevelSpectators(pos, radius=(8,6), ignore=()):
    """ Returns True if anyone can see the position, otherwise False. """
    for player in game.player.allPlayersObject:
        if pos.z == player.position.z and player.canSee(pos, radius) and player not in ignore: return True

    return False

def getCreatures(pos, radius=(8,6), ignore={}):
    """Gives you the creatures in the area.

    :param pos: Position of the center point.
    :type pos: list or tuple.
    :param radius: Radius from center point to check for creatures.
    :type radius: list or tuple.
    :param ignore: known creatures to ignore in the set.
    :type ignore: list, tuple or set.

    :rtype: set of :class:`game.creature.Creature` compatible objects

    """

    creatures = set()

    for creature in game.creature.allCreaturesObject:
        if creature.canSee(pos, radius) and creature not in ignore:
            creatures.add(creature)
    return creatures


def getPlayers(pos, radius=(8,6), ignore=()):
    """Gives you the players in the area.

    :param pos: Position of the center point.
    :type pos: list or tuple.
    :param radius: Radius from center point to check for players.
    :type radius: list or tuple.
    :param ignore: known players to ignore in the set.
    :type ignore: list, tuple or set.

    :rtype: set of :class:`game.player.Player` compatible objects

    """

    players = set()

    for player in game.player.allPlayersObject:
        if player.canSee(pos, radius) and player not in ignore:
            players.add(player)

    return players


# Calculate new position by direction
def positionInDirection(nposition, direction, amount=1):
    """Gives the position in a direction

    :param nposition: Current position.
    :type nposition: list.

    :param direction: The direction.
    :type direction: int (range 0-7).

    :param amount: Amount of steps in that direction.
    :type amount: int.

    :rtype: list.
    :returns: New position.

    """

    position = nposition.copy() # Make a copy of current position.

    if direction == 0:
        position.y = nposition.y - amount
    elif direction == 1:
        position.x = nposition.x + amount
    elif direction == 2:
        position.y = nposition.y + amount
    elif direction == 3:
        position.x = nposition.x - amount
    elif direction == 4:
        position.y = nposition.y + amount
        position.x = nposition.x - amount
    elif direction == 5:
        position.y = nposition.y + amount
        position.x = nposition.x + amount
    elif direction == 6:
        position.y = nposition.y - amount
        position.x = nposition.x - amount
    elif direction == 7:
        position.y = nposition.y - amount
        position.x = nposition.x + amount
    return position

def updateTile(pos, tile):
    """ Send the update to a tile to all who can see the position.
    *Note that this function does NOT replace the known tile in :mod:`game.map`'s knownMap array.*

    :param pos: Position of tile.
    :type pos: list or tuple.
    :param tile: The tile that replace the currently known tile at the position.
    :type tile: Tile of type :class:`game.map.Tile`.

    """

    for spectator in getSpectators(pos):
        stream = spectator.packet(0x69)
        stream.position(pos)
        stream.tileDescription(tile, spectator.player)
        stream.uint8(0x00)
        stream.uint8(0xFF)
        stream.send(spectator)

def transformItem(item, transformTo):
    """ Transform item to a new Id.

    :param item: The item you want to transform.
    :type item: Object of type :class:`game.item.Item`.

    :param transformTo: New itemID. Leave to 0 or None to delete the item.
    :type transformTo: int or None.

    """
    return item.transform(transformTo)

def teleportItem(item, fromPos, toPos):
    """ "teleport" a item from ``fromPos`` to ``toPos``

    :param item: The item you want to transform.
    :type item: :class:`game.item.Item`

    :param fromPos: From this position
    :type fromPos: :func:`tuple` or :func:`list`

    :param toPos: To this position
    :type toPos: :func:`tuple` or :func:`list`


    :rtype: :func:`int`
    :returns: New stack position


    """
    if fromPos.x != 0xFFFF:
        try:
            tile = fromPos.getTile()
            if not isinstance(fromPos, StackPosition):
                fromPos = fromPos.setStackpos(tile.findStackpos(item))

            tile.removeItem(item)
            for spectator in getSpectators(fromPos):
                stream = spectator.packet()
                stream.removeTileItem(fromPos, fromPos.stackpos)
                stream.send(spectator)
        except:
            pass

    newTile = toPos.getTile()
    if item.decayPosition:
            item.decayPosition = toPos
    toStackPos = newTile.placeItem(item)

    for spectator in getSpectators(toPos):
        stream = spectator.packet()
        stream.addTileItem(toPos, toStackPos, item)
        stream.send(spectator)

    return toStackPos

def placeItem(item, position):
    """ Place a item to a position

    :param item: The item to place.
    :type item: Object of type :class:`game.item.Item`.

    :param position: The position to place the item on.
    :type position: list or tuple.

    :rtype: int.
    :returns: Stack position of item.

    """
    #print "placeItem"
    stackpos = position.getTile().placeItem(item)
    for spectator in getSpectators(position):
        stream = spectator.packet()
        stream.addTileItem(position, stackpos, item)
        stream.send(spectator)
    return stackpos

def relocate(fromPos, toPos):
    """ Remove all movable items on fromPos tile, to toPos tile. """
    tile = fromPos.getTile()
    toTile = toPos.getTile()
    items = []
    for item in tile.getItems():
        if not item.movable: continue

        if item.position:
            item.position = toPos

        stackpos = toTile.placeItem(item)
        items.append(item)

    for item in items:
        tile.removeItem(item)

    updateTile(fromPos, tile)
    updateTile(toPos, toTile)

    for creature in tile.creatures():
        if creature.distanceStepsTo(toPos) == 1:
            creature.walkTo(toPos)
        else:
            creature.teleport(toPos)

# The development debug system
def explainPacket(packet):
    """ Explains the packet structure in hex

    :param packet: Packet to explain.
    :type packet: subclass of :class:`core.packet.TibiaPacket`.

    """

    #currPos = packet.pos
    #packet.pos = 0
    print("Explaining packet (type = {0}, length: {1}, content = {2})".format(hex(ord(packet.data[0])), len(packet.data), ' '.join( map(str, list(map(hex, list(map(ord, packet.data)))))) ))
    #packet.pos = currPos

# Save system, async :)
def saveAll(force=False):
    """ Save everything, players, houses, global storage etc. """
    commited = False

    t = time.time()
    for player in list(game.player.allPlayers.values()):
        result = player._saveQuery(force)
        if result:
            sql.runOperation(*result)
            commited = True

    # Global storage
    if saveGlobalStorage or force:
        for field in globalStorage:
            type = ""
            if field in jsonFields:
                data = otjson.dumps(globalStorage[field])
                type = "json"
            elif field in pickleFields:
                data = fastPickler(globalStorage[field])
                type = "pickle"
            else:
                data = globalStorage[field]

            sql.runOperation("INSERT INTO `globals` (`key`, `data`, `type`) VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE `data` = %s", field, data, type, data)
            commited = True

    # Houses
    if game.map.houseTiles:
        for houseId, house in game.house.houseData.items():
            # House is loaded?
            if houseId in game.map.houseTiles:
                try:
                    items = house.data["items"].copy()
                except:
                    print("House id %d have broken items!" % houseId)
                    items = {} # Broken items

                for tile in game.map.houseTiles[houseId]:
                    _items = []
                    lastItem = None
                    bottom = tile.bottomItems()
                    if bottom:
                        for item in tile.bottomItems():
                            ic = item.count
                            if not item.fromMap and (ic == None or ic > 0):
                                if lastItem and lastItem.itemId == item.itemId and lastItem.stackable and lastItem.count < 100:
                                        # Stack.
                                        lCount = lastItem.count
                                        lastItem.count = min(100, lCount + ic)
                                        ic -= lastItem.count - lCount
                                        item.count = ic
                                if ic or ic == None:
                                    _items.append(item)
                                    lastItem = item
                    _items.reverse()
                    items[tile.position] = _items

                if items != house.data["items"]:
                    house.data["items"] = items
                    house.save = True # Force save
                if house.save:
                    print("Saving house ", houseId)
                    sql.runOperation("UPDATE `houses` SET `owner` = %s,`guild` = %s,`paid` = %s, `data` = %s WHERE `id` = %s", house.owner, house.guild, house.paid, fastPickler(house.data) if house.data else '', houseId)
                    house.save = False
                    commited = True
                else:
                    print("Not saving house", houseId)

    if force:
        print("Full (forced) save took: %f" % (time.time() - t))

    elif commited:
        print("Full save took: %f" % (time.time() - t))

# Time stuff
def getTibiaTime():
    """ Return the Time inside the game.

    :rtype: tuple (hours, minutes, seconds).
    """

    seconds = int((time.time() - SERVER_START) % config.tibiaDayLength) * ((24*60*60) // config.tibiaDayLength)
    hours = seconds // 3600
    seconds = seconds - (hours * 3600)
    minutes = seconds // 60
    seconds = seconds % 60

    return (hours, minutes, seconds)

def getLightLevel():
    """ Get the light level relevant to the time of the day.

    :rtype: int.
    """

    tibiaTime = getTibiaTime()
    light = 0
    if tibiaTime[0] >= config.tibiaDayFullLightStart and tibiaTime[0] < config.tibiaDayFullLightEnds:
        return config.tibiaFullDayLight
    else:
        dayHours = 24 - (config.tibiaDayFullLightEnds - config.tibiaDayFullLightStart)
        hoursleft = (abs(24 - tibiaTime[0]) + config.tibiaDayFullLightStart) % 24

        if hoursleft >= 12:
            lightChange = ((config.tibiaFullDayLight - config.tibiaNightLight) // dayHours) * (hoursleft-12)
            return config.tibiaNightLight + lightChange
        else:
            lightChange = ((config.tibiaFullDayLight - config.tibiaNightLight) // dayHours) * (hoursleft)
            return config.tibiaFullDayLight - lightChange

LIGHT_LEVEL = config.tibiaFullDayLight

def checkLightLevel():
    """ Check if the lightlevel have changed and send updates to the players.

    """
    global LIGHT_LEVEL
    light = getLightLevel()
    if LIGHT_LEVEL != light:
        for c in game.player.allPlayersObject:
            if not c.client: continue
            with c.packet() as stream:
                stream.worldlight(light, LIGHTCOLOR_DEFAULT)

        LIGHT_LEVEL = light

# Player lookup and mail
# Usually blocking calls, but we're only called from scripts so i suppose it's ok
@gen.coroutine
def getPlayerIDByName(name):
    """ Returns the playerID based on the name.

    :rtype: int or None.

    """

    try:
        raise Return(game.player.allPlayers[name].data["id"])
    except:
        d = yield sql.runQuery("SELECT `id` FROM `players` WHERE `name` = %s", (name))
        if d:
            raise Return(d[0]['id'])
        else:
            return

def getPlayer(playerName):
    """ Returns the player with name `playerName`, this function only works for already loaded players. """
    try:
        return game.player.allPlayers[playerName]
    except:
        return None

def getCreatureByCreatureId(cid):
    """ Returns the creature with this id. """
    for creature in game.creature.allCreaturesObject:
        if creature.cid == cid:
            return creature

def townNameToId(name):
    """ Return the townID based on town name.

    :rtype: int or None.

    """

    for id in game.map.mapInfo.towns:
        if game.map.mapInfo.towns[id][0] == name:
            return id

def townIdToName(id):
    """ Returns the name of a down based on the id.

    :rtype: str or None.

    """

    try:
        return game.map.mapInfo.towns[id][0]
    except:
        return None

def townPosition(id):
    """ Returns the position of a town passed by id

    :rtype: list

    """

    return game.map.mapInfo.towns[id][1]

def broadcast(message, type='MSG_GAMEMASTER_BROADCAST', sendfrom="SYSTEM", level=0):
    """ Broadcasts a message to every player

    """
    for player in game.player.allPlayersObject:
        stream = player.packet(0xAA)

        # Make sure this player actually is online. TODO: Track them in a seperate list?
        if not stream: continue

        stream.uint32(0)
        stream.string(senfrom)
        stream.uint16(level)
        stream.uint8(stream.const(messageType))
        stream.string(message)
        stream.send(player.client)

@gen.coroutine
def placeInDepot(name, depotId, items):
    """ Place items into the depotId of player with a name. This can be used even if the player is offline.

    :param name: Player name.
    :type name: str.

    :param depotId: DepotID to place items into.
    :type depotId: int or str.

    :param items: Either one Item or a list of items to place into the depot.
    :type items: Either one object of type :class:`game.item.Item`, or a list of objects.

    :rtype: bool.
    :returns: True on success, False otherwise.

    """
    if not type(items) == list:
        items = [items]

    def __inPlace(place):
        for i in items:
            place.append(i)

    if name in game.player.allPlayers:
        try:
            __inPlace(game.player.allPlayers[name].depot[depotId])
        except:
            game.player.allPlayers[name].depot[depotId] = items
        raise Return(True)
    else:
        result = yield sql.runQuery("SELECT `depot` FROM `players` WHERE `name` = %s", (name))
        if result:
            result = pickle.loads(result[0]['depot'])
            try:
                __inPlace(result[depotId])
            except:
                result[depotId] = items
            result = fastPickler(result)
            sql.runOperation("UPDATE `players` SET `depot` = %s", result)
            raise Return(True)
        else:
            raise Return(False)

@gen.coroutine
def loadPlayer(playerName):
    """ Load player with name `playerName`, return result. """
    try:
        # Quick load :p
        raise Return(game.player.allPlayers[playerName])
    except KeyError:
        character = yield sql.runQuery("SELECT p.`id`,p.`name`,p.`world_id`,p.`group_id`,p.`account_id`,p.`vocation`,p.`health`,p.`mana`,p.`soul`,p.`manaspent`,p.`experience`,p.`posx`,p.`posy`,p.`posz`,p.`instanceId`,p.`sex`,p.`looktype`,p.`lookhead`,p.`lookbody`,p.`looklegs`,p.`lookfeet`,p.`lookaddons`,p.`lookmount`,p.`town_id`,p.`skull`,p.`stamina`, p.`storage`, p.`inventory`, p.`depot`, p.`conditions`, s.`fist`,s.`fist_tries`,s.`sword`,s.`sword_tries`,s.`club`,s.`club_tries`,s.`axe`,s.`axe_tries`,s.`distance`,s.`distance_tries`,s.`shield`,s.`shield_tries`,s.`fishing`, s.`fishing_tries`, (SELECT a.`language` FROM account AS `a` WHERE a.`id` = p.`account_id`) as `language`, g.`guild_id`, g.`guild_rank`, p.`balance` FROM `players` AS `p` LEFT JOIN player_skills AS `s` ON p.`id` = s.`player_id` LEFT JOIN player_guild AS `g` ON p.`id` = g.`player_id` WHERE p.`name` = %s AND p.`world_id` = %s", playerName, config.worldId)
        if not character:
            return
        cd = character[0]
        deathlist.loadDeathList(cd['id'])
        game.player.allPlayers[playerName] = game.player.Player(None, cd)
        raise Return(game.player.allPlayers[playerName])

@gen.coroutine
def loadPlayerById(playerId):
    """ Load a player with id `playerId`. Return result. """
    # Quick look
    for player in game.player.allPlayersObject:
        if player.data["id"] == playerId:
            raise Return(player)

    character = yield sql.runQuery("SELECT p.`id`,p.`name`,p.`world_id`,p.`group_id`,p.`account_id`,p.`vocation`,p.`health`,p.`mana`,p.`soul`,p.`manaspent`,p.`experience`,p.`posx`,p.`posy`,p.`posz`,p.`instanceId`,p.`sex`,p.`looktype`,p.`lookhead`,p.`lookbody`,p.`looklegs`,p.`lookfeet`,p.`lookaddons`,p.`lookmount`,p.`town_id`,p.`skull`,p.`stamina`, p.`storage`, p.`inventory`, p.`depot`, p.`conditions`, s.`fist`,s.`fist_tries`,s.`sword`,s.`sword_tries`,s.`club`,s.`club_tries`,s.`axe`,s.`axe_tries`,s.`distance`,s.`distance_tries`,s.`shield`,s.`shield_tries`,s.`fishing`, s.`fishing_tries`, (SELECT a.`language` FROM account AS `a` WHERE a.`id` = p.`account_id`) as `language`, g.`guild_id`, g.`guild_rank`, p.`balance` FROM `players` AS `p` LEFT JOIN player_skills AS `s` ON p.`id` = s.`player_id` LEFT JOIN player_guild AS `g` ON p.`id` = g.`player_id` WHERE p.`id` = %s AND p.`world_id` = %s", playerId, config.worldId)
    if not character:
        return
    cd = character[0]
    deathlist.loadDeathList(cd['id'])
    game.player.allPlayers[cd['name']] = game.player.Player(None, cd)
    raise Return(game.player.allPlayers[cd['name']])

def moveItem(player, fromPosition, toPosition, count=0):
    """ Move item (or `count` number of items) from `fromPosition` to `toPosition` (may be Position in inventory of `player`, or a StackPosition). """
    if fromPosition == toPosition:
        return True

    # TODO, script events.

    # Analyse a little.
    fromMap = False
    toMap = False

    if fromPosition.x != 0xFFFF:
        # From map
        fromMap = True

    if toPosition.x != 0xFFFF:
        toMap = True

    oldItem = None
    renew = False
    stack = True

    thing = player.findItem(fromPosition)
    destItem = None
    if toPosition.x == 0xFFFF or isinstance(toPosition, StackPosition):
        destItem = player.findItem(toPosition)
    if not thing:
        return False
    if thing.stackable and not count:
        count = thing.count
    if destItem and destItem == thing.inContainer:
        return False

    if thing.openIndex != None and not player.inRange(toPosition, 1, 1):
        player.closeContainer(thing)

    itemContainer = None
    if destItem:
        itemContainer = thing.inContainer
        if destItem == itemContainer:
            return False

    # Hacks.
    if fromPosition.x == 0xFFFF and not thing.creature:
        thing.creature = player
    if not thing.position:
        thing.position = fromPosition
    if destItem and not destItem.position:
        destItem.position = toPosition
    if thing.position.x == 0xFFFF and thing.position.y >= 64 and thing.inContainer == None:
        thing.inContainer = player.openContainers[thing.position.y - 64] # Should raise if it's not valid.
    # Some vertifications.
    if thing.stackable and count and count > thing.count:
        player.notPossible()
        return False

    elif not thing.movable or (toPosition.x == 0xFFFF and not thing.pickable):
        player.notPickupable()
        return False

    elif thing.openIndex != None and thing.openIndex == toPosition.y-64: # Moving into self
        player.notPossible()
        return False

    if destItem and (destItem.inContainer or destItem.container): # Recursive check.
        if destItem.container:
            container = destItem
        else:
            container = destItem.inContainer

        while container:
            if container == thing:
                player.notPossible()
                return False

            container = container.inContainer

    slots = thing.slots()

    # Can it be placed there?
    if (not destItem or destItem.container == None) and toPosition.x == 0xFFFF and toPosition.y < 64:
        if (toPosition.y-1) not in slots:
            if not config.ammoSlotOnlyForAmmo and (toPosition.y-1) == SLOT_AMMO:
                pass
            else:
                player.notPossible()
                return False

    if toPosition.x == 0xFFFF and toPosition.y-1 == SLOT_LEFT and player.inventory[SLOT_RIGHT] and player.inventory[SLOT_RIGHT].slotType == "two-handed":
        player.notPossible()
        return False

    elif toPosition.x == 0xFFFF and toPosition.y-1 == SLOT_RIGHT and thing.slotType == "two-handed" and player.inventory[SLOT_LEFT]:
        player.notPossible()
        return False

    if toPosition.x == 0xFFFF and player.freeCapacity() - ((thing.weight or 0) * (thing.count or 1)) < 0:
        player.tooHeavy()
        return False

    if fromPosition.x == 0xFFFF and fromPosition.y < 64 and (game.scriptsystem.get("unequip").run(creature=player, thing=player.inventory[fromPosition.y-1], slot = (fromPosition.y-1))) == False \
        or toPosition.x == 0xFFFF and toPosition.y < 64 and (game.scriptsystem.get("equip").run(creature=player, thing=thing, slot = (toPosition.y-1))) == False:
        return False

    # Special case when both items are the same and stackable.
    stacked = False
    if destItem and destItem.itemId == thing.itemId and destItem.stackable:
        _newItem = game.scriptsystem.get("stack").run(thing=thing, creature=player, position=fromPosition, onThing=destItem, onPosition=toPosition, count=count, end=False)
        if _newItem == None:
            newCount = min(100, destItem.count + count) - destItem.count
            destItem.modify(newCount)
            thing.modify(-newCount)

            return True

        elif isinstance(_newItem, Item):
            newItem = _newItem
            stacked = True

    # remove from fromPosition.
    if not stacked and count and thing.stackable:
        newItem = thing.copy()
        newItem.count = count

        thing.modify(-count)

    elif not stacked:
        newItem = thing # Easy enough.

    if destItem and destItem.containerSize:
        if (game.scriptsystem.get('dropOnto').run(thing=newItem, creature=player, position=fromPosition, onPosition=toPosition, onThing=destItem)) == False or \
           (game.scriptsystem.get('dropOnto').run(thing=destItem, creature=player, position=toPosition, onPosition=fromPosition, onThing=newItem)) == False:

            return False

        if not thing.stackable:
            thing.remove()

        #print "itemToContainer1"
        player.itemToContainer(destItem, newItem)
    else:
        if not thing.stackable:
            thing.remove()

    if toMap:
        #print "toMap called"
        # Place to ground.
        thisTile = toPosition.getTile()

        for item in thisTile.getItems():
            if (game.scriptsystem.get('dropOnto').run(thing=newItem, creature=player, position=fromPosition, onPosition=toPosition, onThing=item)) == False or \
               (game.scriptsystem.get('dropOnto').run(thing=item, creature=player, position=toPosition, onPosition=fromPosition, onThing=newItem)) == False:
                return False

        newItem.place(toPosition)
    else:
        if not destItem or not destItem.containerSize:
            if toPosition.y < 64:
                # Inventory.
                player.itemToInventory(newItem, toPosition.y-1)

            else:
                container = player.getContainer(toPosition.y-64)

                if (game.scriptsystem.get('dropOnto').run(thing=newItem, creature=player, position=fromPosition, onPosition=toPosition, onThing=container)) == False or \
                   (game.scriptsystem.get('dropOnto').run(thing=container, creature=player, position=toPosition, onPosition=fromPosition, onThing=newItem)) == False:
                    return False

                #print "itemToContainer2"
                player.itemToContainer(container, newItem)

            #if destItem and itemContainer:
            #    player.itemToContainer(itemContainer, destItem)
        elif not destItem.containerSize:
            # Move destItem.
            #print "destItem no container branch"
            if thing.inContainer and thing.inContainer != destItem:
                #print "itemToContainer3"
                player.itemToContainer(thing.inContainer, destItem)
            elif player.inventory[SLOT_BACKPACK]:
                #print "destItem backpack branch"
                if player.inventory[SLOT_BACKPACK] != destItem:
                    #print "itemToContainer4"
                    player.itemToContainer(player.inventory[SLOT_BACKPACK], destItem)
            else:
                print("XXX: In case of bug, do something here?")

    if thing.openIndex != None and not player.inRange(toPosition, 1, 1) and not toPosition.z == thing.position.z:
        player.closeContainer(thing)

    # Update everything. Lazy.
    #player.refreshInventory()
    #player.updateAllContainers()
    #player.refreshStatus()

    # Done.
    return True

# Helper calls
def summonCreature(name, position, master=None):
    """ Summons a monster with `name` on position, set master to `master`. """
    import game.monster
    creature = game.monster.getMonster(name).spawn(position, spawnDelay=0)
    if master:
        creature.setMaster(master)
    else:
        creature.setRespawn(False)
    return creature

def magicEffect(pos, type):
    """ Send a magic effect `type` on this position. """
    for spectator in getSpectators(pos):
        stream = spectator.packet()
        stream.magicEffect(pos, type)
        stream.send(spectator)

def getHouseByPos(pos):
    """ Return the House object on this position """
    return game.house.getHouseById(game.map.getHouseId(pos))

# Speed pickler
def fastPickler(obj):
    """ Just a allias for pickle.dumps with protocol highest protocol """
    return pickle.dumps(obj, 3)

@gen.coroutine
def executeCode(code):
    """ Used by execute protocol to run a piece of code """
    raise Exception("Need PY3 support...")
    try:
        if "yield " in code:
            newcode = []
            for p in code.split("\n"):
                newcode.append("    " + p)


            exec("""
@gen.coroutine
def _N():
%s
""" % '\n'.join(newcode))
            raise Return(otjson.dumps((yield _N())))
        else:
            exec(code)
    except Exception as e:
        raise Return(otjson.dumps(e.value))
    else:
        yield defer.maybeDeferred()

def mail(toPlayer, package, message="", town=0, ignoreLimits=True):
    """ Make a parcel, letter, if package is not already a parcel or letter. And send it. """
    name = toPlayer if isinstance(toPlayer, str) else toPlayer.name()

    if not isinstance(toPlayer, Player) and town == 0:
        town = 1
    elif town == 0:
        town = toPlayer.data['town_id']

    if isinstance(package, Item):
        label = None
        for item in package.container:
            if item.itemId == ITEM_LABEL:
                label = item
                break

        if not label or not label.text:
            return False

        lines = label.text.split("\n")
        if lines < 2:
            return False

        town = townNameToId(lines[1])
        if package.itemId != ITEM_PARCEL_STAMPED:
            package.itemId = ITEM_PARCEL_STAMPED
        pack = package

    elif isinstance(package, list):
        # make parcel.
        pack = Item(ITEM_PARCEL_STAMPED)
        label = Item(ITEM_LABEL)
        pack.placeItem(label)
        for item in package:
            pack.placeItem(item)

        label.text = "%s\n%s\n%s" % (name, townIdToName(town), message)
    else:
        # Letter.
        pack = Item(ITEM_LETTER_STAMPED)
        pack.text =  "%s\n%s\n%s" % (name, townIdToName(town), message)

    # Get mail depot
    if isinstance(toPlayer, Player):
        depot = toPlayer.getDepot(town)
        #if not ignoreLimits:
        #    return False

        depot.append(pack)
        toPlayer.setDepot(town, depot)
    else:
        return placeInDepot(toPlayer, town, pack)

    return True


def _allowProjectileVerify(position, blockWindow = False):
    " Verify position "
    tile = position.getTile()
    if not tile:
        return False

    for item in tile.getItems():
        if item.blockprojectile:
            return False

        if blockWindow and "window" in item.name:
            return False

    return True

def allowProjectile(position, position2, blockWindow = False):
    """ Can a projectile from positiongo to position2? Also used for item tossing. """

    xSteps = abs(position.x - position2.x)
    ySteps = abs(position.y - position2.y)

    xStep = -1 if position.x > position2.x else 1
    yStep = -1 if position.y > position2.y else 1

    tmpPosition = position.copy()

    # First we walk diagonal.
    while tmpPosition.x != position2.x and tmpPosition.y != position2.y:
        tmpPosition.x += xStep
        tmpPosition.y += yStep

        if not _allowProjectileVerify(tmpPosition, blockWindow):
            return False

    # X dir.
    while tmpPosition.x != position2.x:
        tmpPosition.x += xStep

        if not _allowProjectileVerify(tmpPosition, blockWindow):
            return False

    # Y dir.
    while tmpPosition.y != position2.y:
        tmpPosition.y += yStep

        if not _allowProjectileVerify(tmpPosition, blockWindow):
            return False

    return True
