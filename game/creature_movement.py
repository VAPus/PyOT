
from game.map import placeCreature, removeCreature, getTile
from tornado import gen
import config
import traceback

class CreatureMovement(object):
    def stepDuration(self, ground):
        if not ground.speed:
            return (100.0 / self.speed) #- 0.05

        return (ground.speed / self.speed) #- 0.05
    
    def teleport(self, position, force=False):
        """if not self.actionLock(self.teleport, position):
            return False"""

        
        # 4 steps, remove item (creature), send new map and cords, and effects
        oldPosition = self.position.copy()
        target = self.target

        newTile = getTile(position)
        oldPosCreatures = set()
        if not newTile:
            raise game.errors.SolidTile("Tile doesn't exist") # Yea, it's fatal, even in force mode!
        
        if not force:
            for i in newTile.getItems():
                if i.solid:
                    raise game.errors.SolidTile()

        invisible = self.isMonster() and self.hasCondition(CONDITION_INVISIBLE)

        oldStackpos = 0
        if not invisible:
            try:
                oldStackpos = getTile(oldPosition).findStackpos(self)
                for spectator in getSpectators(oldPosition, ignore=(self,)):
                    stream = spectator.packet()
                    stream.removeTileItem(oldPosition, oldStackpos)
                    stream.magicEffect(oldPosition, 0x02)
                    stream.send(spectator)
                oldPosCreatures = getCreatures(oldPosition)
            except:
                pass # Just append creature
        
        stackpos = placeCreature(self, position)
        if not stackpos:
            raise game.errors.ImpossibleMove()
        
        removeCreature(self, oldPosition)
        
        if self.creatureType == 0 and self.client:
            with self.packet() as stream:
                if oldStackpos: 
                   stream.removeTileItem(oldPosition, oldStackpos)
                
                stream.uint8(0x64)
                stream.position(position)
                stream.mapDescription(Position(position.x - 8, position.y - 6, position.z), 18, 14, self)

                # If we're entering protected zone, fix icons
                pzStatus = newTile.getFlags() & TILEFLAGS_PROTECTIONZONE
                pzIcon = self.extraIcons & CONDITION_PROTECTIONZONE
                if pzStatus and not pzIcon:
                    self.setIcon(CONDITION_PROTECTIONZONE)
                    self.refreshConditions(stream)
                    self.cancelTarget(stream)
                    self.target = None
                    if self.isPlayer() and self.mounted:
                        call_later(0, self.changeMountStatus, False)

                elif not pzStatus and pzIcon:
                    self.removeIcon(CONDITION_PROTECTIONZONE)
                    self.refreshConditions(stream)

                #stream.magicEffect(position, 0x02)

        self.position = position        
        newPosCreatures = getCreatures(position)
        disappearFrom = oldPosCreatures - newPosCreatures
        appearTo = newPosCreatures - oldPosCreatures
        for creature2 in disappearFrom:
            game.scriptsystem.get('disappear').run(creature2=creature2, creature=self)

        for creature2 in appearTo:
            game.scriptsystem.get('appear').run(creature2=creature2, creature=self)


        if not invisible:
            for spectator in getSpectators(position, ignore=(self,)):
                stream = spectator.packet()
                stream.addTileCreature(position, stackpos, self, spectator.player)
                stream.magicEffect(position, 0x02)
                stream.send(spectator)

        if target and not self.canSee(target.position):
            self.cancelTarget()
            self.target = None
            self.targetMode = 0
            
        # Stairhop delay
        if self.isPlayer():
            self.lastStairHop = time.time()
            if target and not self.canSee(target.position):
                self.cancelTarget()
            
    def turn(self, direction):
        assert direction < 4
        if self.direction == direction:
            return

        if not self.alive: #or not self.actionLock(self.turn, direction):
            return

        self.direction = direction
        self.lastAction = time.time() + 0.15

        # Make package
        for spectator in getSpectators(self.position):
            stream = spectator.packet(0x6B)
            stream.position(self.position)
            stream.uint8(getTile(self.position).findStackpos(self))
            stream.uint16(0x63)
            stream.uint32(self.clientId())
            stream.uint8(direction)
            if spectator.version >= 953:
                stream.uint8(self.solid)
            stream.send(spectator)

    def reverseDirection(self):
        """ Used by pushing """

        direction = self.direction
        if direction == NORTH:
            return SOUTH
        elif direction == SOUTH:
            return NORTH
        elif direction == EAST:
            return WEST
        elif direction == WEST:
            return EAST

    def directionToPosition(self, position, diagonal=False):
        direction = None
        if diagonal:
            if position.y > self.position.y and position.x > self.position.x:
                return SOUTHEAST
            elif position.y > self.position.y and position.x < self.position.x:
                return SOUTHWEST
            elif position.y < self.position.y and position.x > self.position.x:
                return NORTHEAST
            elif position.y < self.position.y and position.x < self.position.x:
                return NORTHWEST

        # First north/south
        if position.y > self.position.y:
            direction = SOUTH
            
        elif position.y < self.position.y:
            direction = NORTH
            
        if position.x > self.position.x:
            direction = EAST

        elif position.x < self.position.x:
            direction = WEST

        return direction

    def turnAgainst(self, position):
        return self.turn(self.directionToPosition(position))
    
    def verifyMove(self, tile):
        """ This function verify if the tile is walkable in a regular state (pathfinder etc) """
        return True

    def clearMove(self, direction, failback=None):
        self.cancelWalk(direction % 4)
        self.walkPattern = None
        if failback: call_later(0, failback)
        return False
        
    def autoWalk(self, pattern=None, callback=None):
        """Autowalk the creature using the walk patterns. This binds the action slot."""
        
        delay = max(self.lastAction - time.time(), 0)
        if(pattern):
            self.walkPattern = pattern
        if delay:
            if self.action:
                remove_timeout(self.action)
            self.action = call_later(delay, self.handleAutoWalking, 0, callback)
        else:
            self.handleAutoWalking(0, callback)
          
    def walk_to(self, to, skipFields=0, diagonal=True):
        """Autowalk the creature using the walk patterns. This binds the action slot.

        :param creature: The creature to autowalk of type :class:`game.creature.Creature` or any subclass of it.
        :type creature: :class:`game.creature.Creature`.

        :param to: Destination position.
        :type to: list or tuple.

        :param skipFields: Don't walk the last steps to the destination. Useful if you intend to walk close to a target.
        :type skipFields: int.

        :param diagonal: Allow diagonal walking?
        :type diagonal: bool.

        :param callback: Call this function when the creature reach it's destination.
        :type callback: function.

        """
        if self.position.z != to.z:
            self.message("Change floor")
            return
            
        pattern = calculateWalkPattern(self, self.position, to, skipFields, diagonal)

        if pattern:
            self.autoWalk(pattern)    
            
    def handleAutoWalking(self, level=0, callback=None):
        """ This handles the actual step by step walking of the autowalker functions. Rarely called directly. """
        self.action = None
        if not self.walkPattern:
            return
            
        direction = self.walkPattern.popleft()

        res = self.move(direction, level=level, stopIfLock=True)
        
        if res and self.walkPattern:
            self.autoWalk()
        elif callback:
            callback(res)

    def move(self, direction, spectators=None, level=0, stopIfLock=False, failback=None, push=True, ignorestairhop=False):
        if not self.alive:
            return -1
        elif not self.data["health"] or not self.canMove or not self.speed:
            return False

        _time = time.time()
        
        # Don't use actionLock (TODO: Kill?) because we might get False, which would prevent us from moving later.
        if self.lastAction > _time:
            if not stopIfLock:
                call_later(self.lastAction - _time, self.move, direction, spectators, level, stopIfLock, failback, push, ignorestairhop)
            return False

         

        # Stairhop delay.
        isPlayer = self.isPlayer()
        if not ignorestairhop and isPlayer and _time - self.lastStairHop < config.stairHopDelay and level:
            return False
            
        oldPosition = self.position.copy()

        # Drunk?
        if self.hasCondition(CONDITION_DRUNK):
            directions = [0,1,2,3,4,5,6,7,direction] # Double the odds of getting the correct direction.
            directions.remove(self.reverseDirection()) # From a reality perspective, you are rarely that drunk.
            direction = random.choice(directions)

        # Recalculate position
        position = oldPosition.copy()
        if direction == 0:
            position.y -= 1
        elif direction == 1:
            position.x += 1
        elif direction == 2:
            position.y += 1
        elif direction == 3:
            position.x -= 1
        elif direction == 4:
            position.y += 1
            position.x -= 1
        elif direction == 5:
            position.y += 1
            position.x += 1
        elif direction == 6:
            position.y -= 1
            position.x -= 1
        elif direction == 7:
            position.y -= 1
            position.x += 1

        position.z += level
            
        # We don't walk out of the map!
        if position.x < 1 or position.y < 1 or position.x > game.map.mapInfo.width or position.y > game.map.mapInfo.height:
            return False

        # New Tile
        newTile = getTile(position)
        
        if not newTile:
            return False
        # oldTile
        oldTile = getTile(oldPosition)

        val = game.scriptsystem.get("move").run(creature=self)
        if val == False:
            return False


        # Deal with walkOff
        walkOffEvent = game.scriptsystem.get('walkOff')
        for item in oldTile:
            if item.isItem():
                val = walkOffEvent.run(thing=item, creature=self, position=oldPosition)
                if val == False:
                    return False
                    
        try:
            oldStackpos = oldTile.findStackpos(self)
        except:
            return False # Not on Tile.

        # PZ blocked?
        if (self.hasCondition(CONDITION_PZBLOCK) or self.getSkull() in SKULL_JUSTIFIED) and newTile.getFlags() & TILEFLAGS_PROTECTIONZONE:
            self.lmessage("You are PZ blocked")
            return False

        # Block movement, even if script stop us later.
        self.lastStep = _time
        delay = self.stepDuration(newTile[0]) * (config.diagonalWalkCost if direction > 3 else 1)
        self.lastAction = _time + delay
        
        # Deal with walkOn
        walkOnEvent = game.scriptsystem.get('walkOn')
        for thing in newTile:
            if thing.solid:
                if level and not thing.isCreature():
                    continue

                # Monsters might push. This should probably be a preWalkOn event, but well. Consider this a todo for v1.1 or something.
                if push and self.isMonster() and thing.isMonster() and self.base._pushCreatures and thing.isPushable(self):
                    # Push stuff here.

                        # Clear up the creatures actions.
                        thing.stopAction()
                        thing.clearMove(direction, failback)

                        if thing.move(thing.reverseDirection(), stopIfLock=True, push=False):
                            # We "must" break here. Assume the tile is good since another creature is on it. Iterator might be invalid at this point.
                            break
                        elif self.base._hostile and thing.isAttackable(self):
                            # We can attack the creature.
                            self.target = thing
                            self.targetMode = 1

                            # Deliver final blow.
                            thing.onHit(self, -thing.data['healthmax'], PHYSICAL)
                #self.turn(direction) # Fix me?
                self.notPossible()
                return False
                
            if thing.isItem():
                # Script.
                r = walkOnEvent.run(thing=thing, creature=self, position=position, fromPosition=oldPosition)
                if r == False:
                    return False
                
                # Prevent monsters from moving on teleports.
                teledest = thing.teledest
                if teledest:
                    if not isPlayer:
                        return False
                    try:
                        self.teleport(Position(teledest[0], teledest[1], teledest[2]), self.position.instanceId)
                        self.magicEffect(EFFECT_TELEPORT)
                    except:
                        print("%d (%s) got a invalid teledist (%s), remove it!" % (thing.itemId, thing, teledest))
                        del thing.teledest


        newStackPos = newTile.placeCreature(self)
        oldTile.removeCreature(self)

        # Clear target if we change level
        if level:
            self.cancelTarget()
            self.target = None
            self.targetMode = 0


        # Send to Player
        if isPlayer:
            # Mark for save
            self.saveData = True

            ignore = (self,)
            stream = self.packet()

            if (oldPosition.z != 7 or position.z < 8): # Only as long as it's not 7->8 or 8->7
                #stream = spectator.packet(0x6D)
                stream.uint8(0x6D)
                stream.position(oldPosition)
                stream.uint8(oldStackpos)
                stream.position(position)
            else:
                stream.removeTileItem(oldPosition, oldStackpos)

            # Levels
            if oldPosition.z > position.z:
                stream.moveUpPlayer(self, oldPosition)

            elif oldPosition.z < position.z:
                stream.moveDownPlayer(self, oldPosition)

            # Y movements
            if oldPosition.y > position.y:
                stream.uint8(0x65)
                stream.mapDescription(Position(oldPosition.x - 8, position.y - 6, position.z), 18, 1, self)
            elif oldPosition.y < position.y:
                stream.uint8(0x67)
                stream.mapDescription(Position(oldPosition.x - 8, position.y + 7, position.z), 18, 1, self)

            # X movements
            if oldPosition.x < position.x:
                stream.uint8(0x66)
                stream.mapDescription(Position(position.x + 9, position.y - 6, position.z), 1, 14, self)
            elif oldPosition.x > position.x:
                stream.uint8(0x68)
                stream.mapDescription(Position(position.x - 8, position.y - 6, position.z), 1, 14, self)

            # If we're entering protected zone, fix icons
            pzStatus = newTile.getFlags() & TILEFLAGS_PROTECTIONZONE
            pzIcon = self.extraIcons & CONDITION_PROTECTIONZONE
            if pzStatus and not pzIcon:
                self.setIcon(CONDITION_PROTECTIONZONE)
                self.refreshConditions(stream)
                if not level:
                    self.cancelTarget(stream)
                    self.target = None
                if isPlayer and self.mounted:
                    call_later(0, self.changeMountStatus, False) # This should be sent after the move is completed, I believe.

            elif not pzStatus and pzIcon:
                self.removeIcon(CONDITION_PROTECTIONZONE)
                self.refreshConditions(stream)


            stream.send(self.client)
            
        else:
            ignore = ()
            
        self.position = position
        self.direction = direction % 4
        
        oldPosCreatures = getPlayers(oldPosition, ignore=ignore)
        newPosCreatures = getPlayers(position, ignore=ignore)
        spectators = oldPosCreatures|newPosCreatures
        invisible = self.isMonster() and self.hasCondition(CONDITION_INVISIBLE)

        if not invisible:
            for spectator in spectators:
                canSeeNew = spectator in newPosCreatures

                canSeeOld = spectator in oldPosCreatures

                stream = spectator.packet()

                if not canSeeOld and canSeeNew:
                    stream.addTileCreature(position, newStackPos, self, spectator, resend=True)

                elif canSeeOld and not canSeeNew:
                    stream.removeTileItem(oldPosition, oldStackpos)
                    """spectator.knownCreatures.remove(self)
                    self.knownBy.remove(spectator)"""

                elif canSeeOld and canSeeNew:
                    if (oldPosition.z != 7 or position.z < 8) and oldStackpos < 10: # Only as long as it's not 7->8 or 8->7

                        stream.uint8(0x6D)
                        stream.position(oldPosition)
                        stream.uint8(oldStackpos)
                        stream.position(position)

                    else:
                        stream.removeTileItem(oldPosition, oldStackpos)
                        spectator.knownCreatures.remove(self)
                        self.knownBy.remove(spectator)
                        stream.addTileCreature(position, newStackPos, self, spectator)
                stream.send(spectator.client)

        if self.scripts["onNextStep"]:
            scripts = self.scripts["onNextStep"][:]
            self.scripts["onNextStep"] = []
            for script in scripts:
                script(self)

        # Deal with appear and disappear. Ahh the power of sets :)
        disappearFrom = oldPosCreatures - newPosCreatures
        appearTo = newPosCreatures - oldPosCreatures
        disappear_event = game.scriptsystem.get('disappear')
        for creature2 in disappearFrom:
            disappear_event.run(creature=creature2, creature2=self)
            disappear_event.run(creature=self, creature2=creature2)
            
        appear_event = game.scriptsystem.get('appear')
        for creature2 in appearTo:
            appear_event.run(creature=creature2, creature2=self)
            appear_event.run(creature=self, creature2=creature2)

        # Stairhop delay
        if level and isPlayer:
            self.lastStairHop = _time

        if isPlayer and self.target and not self.canSee(self.target.position):
            self.cancelTarget()

        return True
