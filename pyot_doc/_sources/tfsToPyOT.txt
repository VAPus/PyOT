************************************
  A TFS to PyOT script function map
************************************
************************************

:Author: Stian (:vapus:`members/stian`)

:Release: |release|

:Date: |today|


**NB! This page is work in progress!**

There is 175 functions left to document.

First some important class (type) names:

    **Creature** means it's part of any creature (:class:`game.creature.Creature`)

    **Player** means it's only part of a player (:class:`game.player.Player`)

    **Item** means it's a item (:class:`game.item.Item`)

    **Position** is a position object (:class:`game.map.Position`)

    **StackPosition** is a position object with stack (:class:`game.map.StackPosition`)

    **<>** are used when the value is literaly inlined to the command

.. function:: getCreatureHealth(cid)

    Equal to::

        Creature.data["health"]

.. function:: getCreatureMaxHealth(cid[, ignoreModifiers = false])

    Equal to::

        Creature.data["healthmax"]

.. function:: getCreatureMana(cid)

    Equal to::

        Player.data["mana"]

.. function:: getCreatureMaxMana(cid[, ignoreModifiers = false])

    Equal to::

        Player.data["manamax"]

.. function:: getCreatureHideHealth(cid)

    Equal to::

        Creature.getHideHealth()

.. function:: doCreatureSetHideHealth(cid, hide)

    Equal to::

        Creature.hideHealth(hide)

.. function:: getCreatureSpeakType(cid)

    Equal to::

        Creature.defaultSpeakType

.. function:: doCreatureSetSpeakType(cid, type)

    Equal to::

        Creature.defaultSpeakType = type

.. function:: getCreatureLookDirection(cid)

    Equal to::

        Creature.direction

.. function:: getPlayerLevel(cid)

    Equal to::

        Player.data["level"]

.. function:: getPlayerExperience(cid)

    Equal to::

        Player.data["experience"]

.. function:: getPlayerMagLevel(cid[, ignoreModifiers = false])

    Equal to::

        Player.data["maglevel"]

.. function:: getPlayerSpentMana(cid)

    Equal to::

        Player.data["manaspent"]

.. function:: getPlayerFood(cid)

    Equal to::

        No equalent (it's a Condition in PyOT so use Creature.getCondition())

.. function:: getPlayerAccess(cid)

    Equal to::

        PyOT doesn't have access levels, only access flags

.. function:: getPlayerGhostAccess(cid)

    Equal to::

        PyOT doesn't have access levels, only access flags

.. function:: getPlayerSkillLevel(cid, skill[, ignoreModifiers = false])

    Equal to::

        Player.getActiveSkill(skill) (with modifiers) and Player.skill[skill] (without modifers)

.. function:: getPlayerSkillTries(cid, skill)

    Equal to::

        Player.getSkillAttempts(skill)

.. function:: getPlayerTown(cid)

    Equal to::

        Player.data["town_id"]

.. function:: getPlayerVocation(cid)

    Equal to::

        Player.getVocation() (for the vocation object), Player.getVocationId() (for the Id)

.. function:: getPlayerIp(cid)

    Equal to::

        Player.getIP()

.. function:: getPlayerRequiredMana(cid, magicLevel)

    Equal to::

        config.magicLevelFormula(magicLevel, Vocation.mlevel)

.. function:: getPlayerRequiredSkillTries(cid, skillId, skillLevel)

    Somewhat equal to::

        config.skillFormula(skillLevel, Player.getVocation().meleeSkill)

.. function:: getPlayerItemCount(cid, itemid[, subType = -1])

    Equal to::

        Player.itemCount(Item)

.. function:: getPlayerMoney(cid)

    Equal to::

        Player.getMoney()

.. function:: getPlayerSoul(cid[, ignoreModifiers = false])

    Equal to::

        Player.data["soul"]

.. function:: getPlayerFreeCap(cid)

    Equal to::

        Player.freeCapasity()

.. function:: getPlayerLight(cid)

    Equal to::

        INVIDIDUAL PLAYER LIGHT NOT IMPLANTED (yet)

.. function:: getPlayerSlotItem(cid, slot)

    Equal to::

        Player.inventory[slot]

.. function:: getPlayerWeapon(cid[, ignoreAmmo = false])

    Equal to::

        Player.inventory[SLOT_RIGHT]

.. function:: getPlayerItemById(cid, deepSearch, itemId[, subType = -1])

    Equal to::

        Player.findItemById(itemId, count/subType)

.. function:: getPlayerDepotItems(cid, depotid)

    Equal to::

        Player.getDepot(depotId)

.. function:: getPlayerAccountId(cid)

    Equal to::

        Player.data["account_id"]

.. function:: getPlayerAccount(cid)

    Equal to::

        Grab it form SQL?

.. function:: getPlayerFlagValue(cid, flag)

    Equal to::

        We don't have such flags

.. function:: getPlayerCustomFlagValue(cid, flag)

    Equal to::

        We don't have such flags

.. function:: getPlayerPromotionLevel(cid)

    Figure it out from the vocation id

.. function:: doPlayerSetPromotionLevel(cid, level)

    Equal to::

        Change the vocation

.. function:: getPlayerGroupId(cid)

    Equal to::

        Player.data["group_id"]

.. function:: doPlayerSetGroupId(cid, newGroupId)

    Equal to::

        Player.data["group_id"] = newGroupId # Currently not saved!!!

.. function:: doPlayerSendOutfitWindow(cid)

    Equal to::

        Player.outfitWindow()

.. function:: doPlayerLearnInstantSpell(cid, name)

    Equal to::

        Player.learnSpell(name)

.. function:: doPlayerUnlearnInstantSpell(cid, name)

    Equal to::

        Player.unlearnSpell(name)

.. function:: getPlayerLearnedInstantSpell(cid, name)

    Equal to::

        Player.canUseSpell(name)

.. function:: getPlayerInstantSpellCount(cid)

    No equal

.. function:: getPlayerInstantSpellInfo(cid, index)

    No equal

.. function:: getInstantSpellInfo(cid, name)

    Something like this::

        game.spell.spells[name]

.. function:: getCreatureStorageList(cid)

    Equal to::

        Player.storage

.. function:: getCreatureStorage(uid, key)

    Equal to::

        Player.getStorage(key)

.. function:: doCreatureSetStorage(uid, key, value)

    Equal to::

        Player.setStorage(key, value)

.. function:: getStorageList()

    Equal to::

        engine.globalStorage

.. function:: getStorage(key)

    Equal to::

        Creature.getGlobal(key)

.. function:: doSetStorage(key, value)

    Equal to::

        Creature.setGlobal(key, value)

.. function:: getPlayersOnline()

    Something like this::

        len(game.player.allPlayers)

.. function:: getTileInfo(pos)

    Like this::

        Position.getTile().getFlags()

.. function:: getThingFromPos(pos[, displayError = true])

    Equal to::

        StackPosition.getThing()

.. function:: getThing(uid[, recursive = RECURSE _FIRST])

    No equal (unnecessary)

.. function:: doTileQueryAdd(uid, pos[, flags[, displayError = true]])

    No equal (unnecessary)

.. function:: doItemRaidUnref(uid)

    No equal (unnecessary)

.. function:: getThingPosition(uid)

    Equal to::

        thing.position

.. function:: getTileItemById(pos, itemId[, subType = -1])

    Equal to::

        Position.getTile().findItem(itemId)

.. function:: getTileItemByType(pos, type)

    Something like this::

        items = []
        for thing in pos.getTile().things:
            if isinstance(thing, Item) and thing.type == type:
                items.append(thing)

.. function:: getTileThingByPos(pos)

    Equal to::

        StackPosition.getThing()

.. function:: getTopCreature(pos)

    Equal to::

        Position.getTile().creatures()[0] (might raise an exception)

.. function:: doRemoveItem(uid[, count = -1])

    You may do something like this::

        item.modify(count)

        or

        item.remove()

.. function:: doPlayerFeed(cid, food)

    No equal (use Conditions)

.. function:: doPlayerSendCancel(cid, text)

    Equal to::

        Player.cancelMessage(text)

.. function:: doPlayerSendDefaultCancel(cid, ReturnValue)

    We got calls such as Player.notPossible()

.. function:: doTransformItem(uid, newId[, count/subType])

    Something like this::

        Item.transform(newId)

.. function:: doCreatureSay(uid, text[, type = SPEAK _SAY[, ghost = false[, cid = 0[, pos]]]])

    Something like this::

        Creature.say(text)

.. function:: doSendCreatureSquare(cid, color[, player])

    Equal to::

        Player.square(Creature, color)

.. function:: doSendMagicEffect(pos, type[, player])

    Some alternatives are::

        Creature.magicEffect(type)
        Creature.magicEffect(type, Position)
        magicEffect(Position, type)

.. function:: doSendDistanceShoot(fromPos, toPos, type[, player])

    Player.shoot(fromPos, toPos, type)

.. function:: doCreatureAddHealth(cid, health[, hitEffect[, hitColor[, force]]])

    Equal to::

        Creature.modifyHealth(health)

.. function:: doCreatureAddMana(cid, mana)

    Equal to::

        Creature.modifyMana(mana)

.. function:: setCreatureMaxHealth(cid, health)

    Equal to::

        Creature.data["healthmax"] += health

.. function:: setCreatureMaxMana(cid, mana)

    Equal to::

        Player.data["manamax"] += health

.. function:: doPlayerSetMaxCapacity(cid, cap)

    Equal to::

        Player.data["capasity"] = cap

.. function:: doPlayerAddSpentMana(cid, amount[, useMultiplier = true])

    Equal to::
        
        Player.modifySpentMana(amount)

.. function:: doPlayerAddSoul(cid, amount)

    Equal to::

        Player.modifySoul(amount)

.. function:: doPlayerAddItem(cid, itemid[, count/subtype = 1[, canDropOnMap = true[, slot = 0]]])

    Equal to::

        Player.addItem(Item(itemId[, count])[, placeOnGround = True])

.. function:: doPlayerAddItem(cid, itemid[, count = 1[, canDropOnMap = true[, subtype = 1[, slot = 0]]]])


    Equal to::

        Player.addItem(Item(itemId[, count])[, placeOnGround = True])

.. function:: doPlayerAddItemEx(cid, uid[, canDropOnMap = false[, slot = 0]])

    Not neseccary since we got no uid stuff, but Player.itemToUse(ItemObject) is possible.

.. function:: doPlayerSendTextMessage(cid, MessageClasses, message)

    Equal to::

        Player.message(message[, MessageClass])

.. function:: doPlayerSendChannelMessage(cid, author, message, SpeakClasses, channel)

.. function:: doPlayerSendToChannel(cid, targetId, SpeakClasses, message, channel[, time])

.. function:: doPlayerOpenChannel(cid, channelId)

    Equal to::

        Player.openChannel(channelId)

.. function:: doPlayerAddMoney(cid, money)

    Equal to::

        Player.addMoney(money)

.. function:: doPlayerRemoveMoney(cid, money)

    Equal to::

        Player.removeMoney(money)

    Note that this remove as much as possible if it's not enough, you should therefore vertify the amount.

.. function:: doPlayerTransferMoneyTo(cid, target, money)

    Equal to::

        Player.removeMoney(money)
        Player2.addMoney(money)

.. function:: doShowTextDialog(cid, itemid, text)

    Equal to::

        Player.textWindow(Item, text=text)

.. function:: doDecayItem(uid)

    Equal to::
        
        Item.decay()

.. function:: doCreateItem(itemid[, type/count], pos)

    Equal to::

        placeItem(Item(itemid, type/count), pos)
        or
        <Item>.place(pos)

.. function:: doCreateItemEx(itemid[, count/subType = -1])

    Equal to::

        Item(itemid, count)

.. function:: doTileAddItemEx(pos, uid)

    Equal to::

        placeItem(Item, pos)
        or
        <Item>.place(pos)

.. function:: doMonsterSetTarget(cid, target)

    Equal to::

        Creature.target = target

.. function:: doMonsterChangeTarget(cid)

    Equal to::

        Creature.target = None (?)

.. function:: getMonsterInfo(name)

    Somewhat equal to::

        getMonster(name)

    It give you the base class that every monster with that name is based on. Hench it's easy to grab information.

.. function:: doAddCondition(cid, condition)

    Equal to::

        Creature.condition(condition)

.. function:: doRemoveCondition(cid, type[, subId])

    Equal to::

        Creature.removeCondition(condition)

.. function:: doRemoveConditions(cid[, onlyPersistent])

    Equal to(?)::
        
        Creature.loseAllConditions()

.. function:: doRemoveCreature(cid[, forceLogout = true])

    Equal to::

        Creature.remove()

.. function:: doMoveCreature(cid, direction[, flag = FLAG _NOLIMIT])

    Equal to::

        Creature.move(direction)

.. function:: doSteerCreature(cid, position)

    Equal to::

        autoWalkCreatureTo(Creature, position)

.. function:: doPlayerSetPzLocked(cid, locked)

.. function:: doPlayerSetTown(cid, townid)

.. function:: doPlayerSetVocation(cid,voc)

.. function:: doPlayerRemoveItem(cid, itemid[, count[, subType = -1]])

    Equal to::

        Player.findItemById(itemid).modify(count) # or .remove()

.. function:: doPlayerAddExperience(cid, amount)

    Equal to::

        Player.modifyExperience(amount)

.. function:: doPlayerSetGuildId(cid, id)

.. function:: doPlayerSetGuildLevel(cid, level[, rank])

.. function:: doPlayerSetGuildNick(cid, nick)

.. function:: doPlayerAddOutfit(cid, looktype, addon)

    Equal to::

        Player.addOutfit(outfitName)

        # or

        Player.addOutfitAddon(outfitName, addon)

.. function:: doPlayerRemoveOutfit(cid, looktype[, addon = 0])

    Equal to::

        Player.removeOutfit(outfitName)

        # or:
        
        Player.removeOutfitAddon(outfitName, addon)

.. function:: doPlayerAddOutfitId(cid, outfitId, addon)

    See doPlayerAddOutfit

.. function:: doPlayerRemoveOutfitId(cid, outfitId[, addon = 0])

    See doPlayerRemoveOutfit

.. function:: canPlayerWearOutfit(cid, looktype[, addon = 0])

    Equal to::

        Player.canWearOutfit(outfitName)

        # for addon check:

        addon in Player.getAddonsForOutfit(outfitName)

.. function:: canPlayerWearOutfitId(cid, outfitId[, addon = 0])

    See canPlayerWearOutfit

.. function:: getCreatureCondition(cid, condition[, subId = 0])

    Equal to::

        Player.getCondition(condition[, subId])

.. function:: doCreatureSetDropLoot(cid, doDrop)

.. function:: getPlayerLossPercent(cid, lossType)

.. function:: doPlayerSetLossPercent(cid, lossType, newPercent)

.. function:: doPlayerSetLossSkill(cid, doLose)

.. function:: getPlayerLossSkill(cid)

.. function:: doPlayerSwitchSaving(cid)

    Equal to::

        Player.doSave = not Player.doSave

.. function:: doPlayerSave(cid[, shallow = false])

    Equal to::

        Player.save()

.. function:: isPlayerPzLocked(cid)

.. function:: isPlayerSaving(cid)

    Equal to::

        Player.doSave

.. function:: isCreature(cid)

    Equal to::

        Thing.isCreature()


.. function:: isMovable(uid)

    Equal to::

        Thing.movable

.. function:: getCreatureByName(name)

    Somewhat equal to::

        getMonster(name)
        getNPC(name)

.. function:: getPlayerByGUID(guid)

    No equal

.. function:: getPlayerByNameWildcard(name~[, ret = false])

    NOT IMPLANTED YET

.. function:: getPlayerGUIDByName(name[, multiworld = false])

    No equal

.. function:: getPlayerNameByGUID(guid[, multiworld = false[, displayError = true]])

    No equal

.. function:: doPlayerChangeName(guid, oldName, newName)

    Player.rename(newName)

.. function:: registerCreatureEvent(uid, eventName)

    Equal to::

        register(eventName, Creature, function)

.. function:: unregisterCreatureEvent(uid, eventName)

    Equal to::

        unregister(eventName, Creature, function)

.. function:: getContainerSize(uid)

    Equal to::

        len(Item.container.items)

.. function:: getContainerCap(uid)

    Equal to::

        Item.containerSize

.. function:: getContainerItem(uid, slot)

    Equal to::

        Item.container.getThing(slot)

.. function:: getHouseAccessList(houseid, listId)

    Equal to::

        House.data["doors"][listId]



.. function:: getHouseFromPos(pos)

    Equal to::

        getHouseByPos(Position)

.. function:: setHouseAccessList(houseid, listid, listtext)

    No equal, you got to modify House.data["doors"] directly.

.. function:: setHouseOwner(houseId, owner[, clean])

    Equal to::

        House.owner = owner

.. function:: doChangeSpeed(cid, delta)

    Equal to::

        Creature.setSpeed(Creature.speed + delta)

.. function:: getCreatureOutfit(cid)

    Equal to::

        Creature.outfit

.. function:: getCreatureLastPosition(cid)

    Equal to::

        Creature.position

.. function:: getCreatureName(cid)

    Equal to::

        Creature.name()

.. function:: getCreatureSpeed(cid)

    Equal to::

        Creature.speed

.. function:: getCreatureBaseSpeed(cid)

    Equal to::

        Creature.speed (we don't really deal with base right now)

.. function:: getCreatureTarget(cid)

    Equal to::

        Creature.target

.. function:: isInArray(array, value[, caseSensitive = false])

    Equal to::

        value in array

.. function:: addEvent(callback, delay, ...)

    Equal to::

        callLater(delay (in seconds!), callback, ....)

.. function:: stopEvent(eventid)

    Equal to::

        (return value of the event).stop()

.. function:: doPlayerPopupFYI(cid, message)

    Equal to::

        Player.windowMessage(message)

.. function:: doPlayerSendTutorial(cid, id)

    Equal to::

        Player.tutorial(id)

.. function:: doCreatureSetLookDirection(cid, dir)

    Equal to::

        Creature.turn(dir)

.. function:: getPlayerModes(cid)

    Equal to::

        Player.modes

.. function:: getCreatureMaster(cid)

    Equal to::

        Creature.master

.. function:: getItemIdByName(name[, displayError = true])

    Equal to::

        game.item.itemNames[name]

.. function:: getItemInfo(itemid)

    Equal to::

        game.item.items[itemid]

.. function:: getItemAttribute(uid, key)

    Equal to::

        Item.<key>

.. function:: doItemSetAttribute(uid, key, value)

    Equal to::

        Item.<key> = value

.. function:: doItemEraseAttribute(uid, key)

    Equal to::

        del Item.<key>

.. function:: getItemWeight(uid[, precise = true])

    Equal to::

        Item.weight

.. function:: getItemParent(uid)

    Equal to::

        Item.inContainer

.. function:: hasItemProperty(uid, prop)

    Item.<prop>

.. function:: hasPlayerClient(cid)

    Equal to::

        Player.client

.. function:: getDataDir()

    Always ./data

.. function:: getConfigFile()

    This function have no purpose.

.. function:: getConfigValue(key)

    Equal to::

        config.<key>

.. function:: doCreatureExecuteTalkAction(cid, text[, ignoreAccess = false[, channelId = CHANNEL _DEFAULT]])

    Equal to::

        Creature.say(text[,channelId = channelId])

.. function:: doReloadInfo(id[, cid])

    Somewhat equal to::

        reload()

    This reloads everything tho.

.. function:: doSaveServer([shallow = false])

    Equal to::

        engine.saveAll()

.. function:: loadmodlib(lib)

    See :func:`domodlib`

.. function:: domodlib(lib)

    See :keyword:`import`

    Somewhat equal to::

        import <lib>

.. function:: dodirectory(dir[, recursively = false])

    Somewhat equal to::

        from <dir> import *

    Or to::

        import dir.*

.. function:: doPlayerGiveItem(cid, itemid, amount, subType)

    Can be done like this::

        Player.addItem(Item(itemid, amount))

.. function:: doPlayerGiveItemContainer(cid, containerid, itemid, amount, subType)

    Like this::

        Player.addItemToContainer(ContainerItem, Item(itemid, amount))

.. function:: isPremium(cid)

        Desided by player access flags

.. function:: isNumeric(str)

    Equal to::

        type(str) == int

.. function:: playerExists(name)

    Equal to::

        True if getPlayer(name) else False

.. function:: getTibiaTime()

    Equal to::

        getTibiaTime()

.. function:: getHouseOwner(houseId)

    Like this::

        getHouseById(houseId).owner

.. function:: getHouseName(houseId)

    Like this::

        getHouseById(houseId).name

.. function:: getHouseRent(houseId)

    Like this::

        getHouseById(houseId).rent

.. function:: getHousePrice(houseId)

    Like this::

        getHouseById(houseId).price

.. function:: getHouseTown(houseId)

    Like this::

        getHouseById(houseId).town_id

.. function:: getHouseDoorsCount(houseId)

    Can be done like this::

        len(game.map.houseDoors[houseId])

.. function:: getHouseBedsCount(houseId)

    No equalent yet

.. function:: getHouseTilesCount(houseId)

    Like this::

        getHouseById(houseId).size

.. function:: getItemNameById(itemid)

    Equal to::

        itemAttribute(itemid, "name")

.. function:: getItemPluralNameById(itemid)

    Equal to::

        itemAttribute(itemid, "plural")

.. function:: getItemArticleById(itemid)

    Equal to::

        itemAttribute(itemid, "article")

.. function:: getItemName(uid)

    Equal to::

        Item.name

.. function:: getItemPluralName(uid)

    Equal to::

        Item.plural

.. function:: getItemArticle(uid)

    Equal to::

        Item.article

.. function:: getItemText(uid)

    Equal to::

        Item.text

.. function:: getItemSpecialDescription(uid)

    Equal to::

        Item.description

.. function:: getItemWriter(uid)

    Equal to::

        Item.writer

.. function:: getItemDate(uid)

    Equal to::

        Item.written

.. function:: getTilePzInfo(pos)

    Equal to::

        Position.getTile().getFlags() & TILEFLAGS_PROTECTIONZONE

.. function:: getTileZoneInfo(pos)

    Equal to::

        Position.getTile().getFlags()

.. function:: doSummonCreature(name, pos, displayError)

    Equal to::

        game.monster.getMonster(name).spawn(pos)

.. function:: getOnlinePlayers()

    Equal to::

        len(game.player.allPlayers)

.. function:: getPlayerByName(name)

    Equal to::

        getPlayer(name)

.. function:: isPlayer(cid)

    Equal to::

        Creature.isPlayer()

.. function:: isPlayerGhost(cid)

    Equal to::

        not Creature.alive

.. function:: isMonster(cid)

    Equal to::

        Creature.isMonster()

.. function:: isNpc(cid)

    Equal to::

        Creature.isNPC()

.. function:: doPlayerAddLevel(cid, amount, round)

    Equal to::

        Player.modifyLevel(amount)

.. function:: doPlayerAddMagLevel(cid, amount)

    Equal to::

        Player.modifyMagicLeve(amount)

.. function:: doPlayerAddSkill(cid, skill, amount, round)

    Equal to::

        Player.addSkillLevel(skill, amount)

.. function:: doCopyItem(item, attributes)

    Equal to::

        item.copy()

.. function:: doRemoveThing(uid)

    Equal to::

        Depends on where the item is.

.. function:: doChangeTypeItem(uid, subtype)

    Equal to::

        Item.count -= 1 (you need to refresh the item tho)

.. function:: doSetItemText(uid, text, writer, date)

    Equal to::

        Item.test = text
        Item.written = date
        Item.writtenBy = writer

.. function:: doItemSetActionId(uid, aid)

    Equal to::

        PyOT support multiple actions, so Item.actions.append("action") and Item.actions.remove("action")

.. function:: getFluidSourceType(itemid)

    Equal to::

        itemAttribute(itemid, "fluidSource")

.. function:: getDepotId(uid)

    Equal to::

        Depots are indexed based on depotid in player.

.. function:: getItemDescriptions(uid)

    Equal to::

        Item.description

.. function:: getItemWeightById(itemid, count, precision)

    Equal to::

        itemAttribute(itemid, "weight") * count

.. function:: getItemWeaponType(uid)

    Equal to::

        Item.weaponType

.. function:: isContainer(uid)

    Equal to::

        Item.container

.. function:: isItemStackable(itemid)

    Equal to::

        Item.stackable

.. function:: isItemContainer(itemid)

    Equal to::

        Item.container

.. function:: isItemFluidContainer(itemid)

    Equal to::

        Item.fluidSource

.. function:: isItemMovable(itemid)

    Equal to::

        Item.movable

.. function:: choose(...)

    Equal to::

        random.choice(Iter)

.. function:: getDistanceBetween(fromPosition, toPosition)

    Equal to::

        fromPosition.distanceTo(toPosition)

.. function:: getCreatureLookPosition(cid)

    Equal to::

        Creature.positionInDirection(Creature.direction)

.. function:: getPositionByDirection(position, direction, size)

    Equal to::

        positionInDirection(position, direction, size)

.. function:: doComparePositions(position, positionEx)

    Equal to::

        position == positionEx

.. function:: getArea(position, x, y)

    Equal to::

        We don't do areas like lua do.

.. function:: Position(x, y, z, stackpos)

    Equal to::

        Position(x, y, z) and StackPosition(z, y, z, stackpos)

.. function:: isValidPosition(position)

    Equal to::

        if getTile(position): True

.. function:: doCreateTeleport(itemid, topos, createpos)

    Equal to::

        Item.teledest = [X, Y, Z] # Yes, it's a list and NOT a Position object, there are a couple of reasons for this, but well.

.. function:: doCreateMonster(name, pos[, extend = false[, force = false[, displayError = true]]])

    Equal to::

        getMonster(name).spawn(pos)

.. function:: doCreateNpc(name, pos[, displayError = true])

    Equal to::

        getNPC(name).spawn(pos)

.. function:: doPlayerAddSkillTry(cid, skillid, n[, useMultiplier = true])

    Equal to::

        Player.skillAttempt(skillid[, n=1])

.. function:: doSummonMonster(cid, name)

    Equal to::

        monster = getMonster(name).spawn(Player.getPositionInDirection(Player.direction))
        monster.setMaster(Player)

.. function:: doPlayerAddMount(cid, mountId)

    Equal::

        Player.addMount(name)

.. function:: doPlayerRemoveMount(cid, mountId)

    Equal to::

        Player.removeMount(name)

.. function:: getPlayerMount(cid, mountId)

    Equal to::

        Player.canUseMount(name)

.. function:: doPlayerSetMount(cid, mountId)

    Equal to::

        Player.mount = mountid or mountname # both work in teory i suppose

.. function:: doPlayerSetMountStatus(cid, mounted)

    Equal to::

        Player.mounted = mounted

.. function:: getMountInfo([mountId])

    Equal to::

        mount = game.resource.getMount(mountname)

.. function:: doPlayerAddMapMark(cid, pos, type[, description])

    Equal to::

        Player.mapMarker(Position, Type[, description])

.. function:: doPlayerAddPremiumDays(cid, days)

    No equal

.. function:: getPlayerPremiumDays(cid)

    No equal

.. function:: getPlayerAccountManager(cid)

    No equal

.. function:: getPlayersByAccountId(accId)

    No equal

.. function:: getAccountIdByName(name)

    No equal

.. function:: getAccountByName(name)
    
    No equal

.. function:: getAccountIdByAccount(accName)

    No equal

.. function:: getAccountByAccountId(accId)

    No equal

.. function:: getIpByName(name)

    No equal

.. function:: getPlayersByIp(ip[, mask = 0xFFFFFFFF])

    No equal

** string actions (see pythons documentation instead) **
    string.split(str)

    Equal to::

        str.split(splitBy)
    string.trim(str)

    Equal to::

        str.trim()
    string.explode(str, sep, limit)

    Equal to::

        str.split(sep, limit)
    string.expand(str)

    Equal to::

        str += str

** part of the guild system, yet to be implanted **
.. function:: getPlayerGuildId(cid)

.. function:: getPlayerGuildName(cid)

.. function:: getPlayerGuildRankId(cid)

.. function:: getPlayerGuildRank(cid)

.. function:: getPlayerGuildNick(cid)

.. function:: getPlayerGuildLevel(cid)

.. function:: getPlayerGUID(cid)

.. function:: getPlayerNameDescription(cid)

.. function:: doPlayerSetNameDescription(cid, desc)

.. function:: getPlayerSpecialDescription(cid)

.. function:: doPlayerSetSpecialDescription(cid, desc)

.. function:: isSorcerer(cid)

.. function:: isDruid(cid)

.. function:: isPaladin(cid)

.. function:: isKnight(cid)

.. function:: isRookie(cid)

.. function:: isCorpse(uid)

.. function:: getContainerCapById(itemid) Item.containerSize

.. function:: getMonsterAttackSpells(name)

.. function:: getMonsterHealingSpells(name)

.. function:: getMonsterLootList(name)

.. function:: getMonsterSummonList(name)

.. function:: getDirectionTo(pos1, pos2)

.. function:: isInRange(position, fromPosition, toPosition)

.. function:: isItemRune(itemid)

.. function:: isItemDoor(itemid)

.. function:: getItemRWInfo(uid)

.. function:: getItemLevelDoor(itemid)

.. function:: getPartyLeader(cid)

.. function:: isInParty(cid)

.. function:: isPrivateChannel(channelId)

.. function:: doPlayerResetIdleTime(cid)

.. function:: doBroadcastMessage(text, class)

.. function:: doPlayerBroadcastMessage(cid, text, class, checkFlag, ghost)

.. function:: getBooleanFromString(input)

.. function:: doPlayerSetExperienceRate(cid, value)

.. function:: doPlayerSetMagicRate(cid, value)

.. function:: doShutdown()

.. function:: getHouseEntry(houseId)

.. function:: doWriteLogFile(file, text)

.. function:: getExperienceForLevel(lv)

.. function:: doMutePlayer(cid, time)

.. function:: getPlayerGroupName(cid)

.. function:: getPlayerVocationName(cid)

.. function:: getPromotedVocation(vid)

.. function:: doPlayerRemovePremiumDays(cid, days)

.. function:: getPlayerMasterPos(cid)

.. function:: doPlayerAddAddons(cid, addon)

.. function:: doPlayerWithdrawAllMoney(cid)

.. function:: doPlayerDepositAllMoney(cid)

.. function:: doPlayerTransferAllMoneyTo(cid, target)

.. function:: getMonthDayEnding(day)

.. function:: getMonthString(m)

.. function:: getArticle(str)

.. function:: doPlayerTakeItem(cid, itemid, amount)

.. function:: doPlayerBuyItem(cid, itemid, count, cost, charges)

.. function:: doPlayerBuyItemContainer(cid, containerid, itemid, count, cost, charges)

.. function:: doPlayerSellItem(cid, itemid, count, cost)

.. function:: doPlayerWithdrawMoney(cid, amount)

.. function:: doPlayerDepositMoney(cid, amount)

.. function:: doPlayerAddStamina(cid, minutes)

.. function:: doCleanHouse(houseId)

.. function:: doCleanMap()

.. function:: doRefreshMap()

.. function:: doGuildAddEnemy(guild, enemy, war, type)

.. function:: doGuildRemoveEnemy(guild, enemy)

.. function:: doUpdateHouseAuctions()

.. function:: getModList()

.. function:: getHighscoreString(skillId)

.. function:: getWaypointPosition(name)

.. function:: doWaypointAddTemporial(name, pos)

.. function:: getGameState()

.. function:: doSetGameState(id)

.. function:: doExecuteRaid(name)

.. function:: isIpBanished(ip[, mask])

.. function:: isPlayerBanished(name/guid, type)

.. function:: isAccountBanished(accountId[, playerId])

.. function:: doAddIpBanishment(...)

.. function:: doAddPlayerBanishment(...)

.. function:: doAddAccountBanishment(...)

.. function:: doAddNotation(...)

.. function:: doAddStatement(...)

.. function:: doRemoveIpBanishment(ip[, mask])

.. function:: doRemovePlayerBanishment(name/guid, type)

.. function:: doRemoveAccountBanishment(accountId[, playerId])

.. function:: doRemoveNotations(accountId[, playerId])

.. function:: doRemoveStatements(name/guid[, channelId])

.. function:: getNotationsCount(accountId[, playerId])

.. function:: getStatementsCount(name/guid[, channelId])

.. function:: getBanData(value[, type[, param]])

.. function:: getBanReason(id)

.. function:: getBanAction(id[, ipBanishment = false])

.. function:: getBanList(type[, value[, param]])

.. function:: getExperienceStage(level)

.. function:: getLogsDir()

.. function:: getCreatureSummons(cid)

.. function:: getTownId(townName)

.. function:: getTownName(townId)

.. function:: getTownTemplePosition(townId)

.. function:: getTownHouses(townId)

.. function:: getSpectators(centerPos, rangex, rangey[, multifloor = false])

.. function:: getVocationInfo(id)

.. function:: getGroupInfo(id[, premium = false])

.. function:: getVocationList()

.. function:: getGroupList()

.. function:: getChannelList()

.. function:: getTownList()

.. function:: getWaypointList()

.. function:: getTalkActionList()

.. function:: getExperienceStageList()

.. function:: getPlayerRates(cid)

.. function:: doPlayerSetRate(cid, type, value)

.. function:: getPlayerPartner(cid)

.. function:: doPlayerSetPartner(cid, guid)

.. function:: doPlayerFollowCreature(cid, target)

.. function:: getPlayerParty(cid)

.. function:: doPlayerJoinParty(cid, lid)

.. function:: doPlayerLeaveParty(cid[, forced = false])

.. function:: getPartyMembers(lid)

.. function:: getCreatureGuildEmblem(cid[, target])

.. function:: doCreatureSetGuildEmblem(cid, emblem)

.. function:: getCreaturePartyShield(cid[, target])

.. function:: doCreatureSetPartyShield(cid, shield)

.. function:: getCreatureSkullType(cid[, target])

.. function:: doCreatureSetSkullType(cid, skull)

.. function:: getPlayerSkullEnd(cid)

.. function:: doPlayerSetSkullEnd(cid, time, type)

.. function:: getPlayerBlessing(cid, blessing)

.. function:: doPlayerAddBlessing(cid, blessing)

.. function:: getPlayerStamina(cid)

.. function:: doPlayerSetStamina(cid, minutes)

.. function:: getPlayerBalance(cid)

.. function:: doPlayerSetBalance(cid, balance)

.. function:: getCreatureNoMove(cid)

.. function:: doCreatureSetNoMove(cid, block)

.. function:: getPlayerIdleTime(cid)

.. function:: doPlayerSetIdleTime(cid, amount)

.. function:: getPlayerLastLoad(cid)

.. function:: getPlayerLastLogin(cid)

.. function:: getPlayerTradeState(cid)

.. function:: doPlayerSendMailByName(name, item[, town[, actor]])

.. function:: getChannelUsers(channelId)

.. function:: getSearchString(fromPosition, toPosition[, fromIsCreature = false[, toIsCreature = false]])

.. function:: getClosestFreeTile(cid, targetpos[, extended = false[, ignoreHouse = true]])

.. function:: doTeleportThing(cid, newpos[, pushmove = true[, fullTeleport = true]])

.. function:: doSendAnimatedText(pos, text, color[, player])

.. function:: doAddContainerItemEx(uid, virtuid)

.. function:: doRelocate(pos, posTo[, creatures = true[, unmovable = true]])

.. function:: doCleanTile(pos[, forceMapLoaded = false])

.. function:: doConvinceCreature(cid, target)

.. function:: getMonsterTargetList(cid)

.. function:: getMonsterFriendList(cid)

.. function:: isSightClear(fromPos, toPos, floorCheck)

.. function:: doCreatureChangeOutfit(cid, outfit)

.. function:: doSetMonsterOutfit(cid, name[, time = -1])

.. function:: doSetItemOutfit(cid, item[, time = -1])

.. function:: doSetCreatureOutfit(cid, outfit[, time = -1])

.. function:: getWorldType()

.. function:: setWorldType(type)

.. function:: getWorldTime()

.. function:: getWorldLight()

.. function:: getWorldCreatures(type)

.. function:: getWorldUpTime()

.. function:: getGuildId(guildName)

.. function:: getGuildMotd(guildId)

.. function:: getPlayerSex(cid[, full = false])

.. function:: doPlayerSetSex(cid, newSex)

.. function:: numberToVariant(number)

.. function:: stringToVariant(string)

.. function:: positionToVariant(pos)

.. function:: targetPositionToVariant(pos)

.. function:: variantToNumber(var)

.. function:: variantToString(var)

.. function:: variantToPosition(var)

.. function:: doAddContainerItem(uid, itemid[, count/subType = 1])

.. function:: getHouseInfo(houseId[, displayError = true])

.. function:: getHouseByPlayerGUID(playerGUID)
