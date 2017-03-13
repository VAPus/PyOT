def defaultBrainFeaturePriority(monster):
        # Walking
        if monster.target: # We need a target for this code check to run
            # Chance of retargeting?
            if monster.base._targetChange and random.randint(0, 99) < monster.base._targetChance and monster.data["health"] > monster.base._runOnHealth and monster.distanceStepsTo(monster.target.position) > 1:
                monster.targetCheck()
                if not monster.target:
                    
                    return True
                
            # If target is out of sight, stop following it and begin moving back to base position
            if not monster.canTarget(monster.target.position) or monster.target.data["health"] < 1 or not monster.target.alive or monster.data["health"] <= monster.base._runOnHealth:
                monster.intervals = {} # Zero them out
                if monster.master:
                    monster.target = monster.master
                    monster.targetMode = 2
                    #monster.walk_to(monster.master.position, -1, False)
                    return
                else:
                    monster.target = None
                    monster.targetMode = 0
                
                if config.monsterWalkBack:
                    monster.walk_to(monster.spawnPosition, 0, True) # Yes, last step might be diagonal to speed it up
                elif not hasSpectators(monster.position, (15, 15)):
                    call_later(2, monster.teleport, monster.spawnPosition)
                    
                return
            
            elif monster.distanceStepsTo(monster.target.position) > monster.base._targetDistance:
                # When we reach our destination, can we target check
                def __walkComplete(x):
                    if not x:
                        # Walk not possible. Loose target
                        monster.target = None
                        monster.targetMode = 0
                        return

                    # Are we OK?
                    if monster.distanceStepsTo(monster.target.position) <= monster.base._targetDistance:
                        monster.turnAgainst(monster.target.position)
                            
                # Begin autowalking
                monster.walk_to(monster.target.position, -monster.base._targetDistance, __walkComplete)
                    
            elif monster.targetMode == 1:
                # First stratigic manuver
                _time = time.time()
                for id, spell in enumerate(monster.base.defenceSpells):
                    key = "s%d"%id
                    if not key in monster.intervals or monster.intervals[key]+spell[0] < _time:
                        if spell[2](monster):
                            try:
                                spell[1](None, monster, monster.position, monster.position, monster, strength=spell[3])
                                    
                            except:
                                spell[1](monster, spell[3])
                                
                            monster.intervals[key] = _time
                            return True # Until next brain tick
                
                # Summons
                if len(monster.activeSummons) < monster.base.maxSummon:
                    for summon in monster.base.summons:
                        if random.randint(0, 99) < summon[1]:
                            try:
                                creature = monster.summon(summon[0], monster.positionInDirection(random.randint(0,3)))
                            except:
                                print("%s tries to summon a invalid monster '%s'" % (monster.name(), summon[0]))
                                
                            break
                """else:
                    for summon in monster.activeSummons[:]:
                        if not summon.alive:
                            monster.activeSummons.remove(summon)"""

                # Turn against our target.
                monster.turnAgainst(monster.target.position)

                # Attack attacks
                for id, spell in enumerate(monster.base.spellAttacks):
                    key = "a%d"%id
                    if not key in monster.intervals or monster.intervals[key]+spell[0] < _time:
                        if monster.inRange(monster.target.position, spell[3], spell[3]) and spell[2](monster):
                            try:
                                check = spell[1](None, monster, monster.position, monster.target.position, monster.target, strength=spell[4])
                                    
                            except:
                                check = spell[1](monster, spell[4])
                                
                            monster.intervals[key] = _time
                            if check:
                                return  True  # Until next brain tick
                            
                # Melee attacks
                if monster.base.meleeAttacks and monster.inRange(monster.target.position, 1, 1):
                    attack = random.choice(monster.base.meleeAttacks)
                    if monster.lastMelee + attack[0] <= _time and attack[1](monster):
                        if attack[3] and random.randint(0,99) < attack[4]:
                            monster.target.condition(attack[3], attack[5])
                            
                        check = monster.target.onHit(monster, -random.randint(0, round(attack[2] * config.monsterMeleeFactor)), PHYSICAL)
                        monster.lastMelee = _time
                        if check:
                            return True	 # If we do have a target and deals damage, we stop here
                # Distance attacks
                elif monster.base.distanceAttacks:
                    distance = random.choice(monster.base.distanceAttacks)
                    if monster.lastDistance + distance[0] <= _time and distance[3](monster):
                        check = monster.target.onHit(monster, -random.randint(0, round(distance[1] * config.monsterMeleeFactor)), DISTANCE)
                        monster.lastDistance = _time
                        if check:
                            monster.shoot(monster.position, monster.target.position, distance[2]) #not sure if this will work.
                            return True # If we do have a target, we stop here


def defaultBrainFeature(monster):
        ret = defaultBrainFeaturePriority(monster)
        if ret is not None:
            return False if ret == False else None

        # Only run this check if there is no target, we are hostile and targetChance checksout
        if not monster.master:
            if not monster.target and monster.base._hostile and monster.data["health"] > monster.base._runOnHealth:
                monster.targetCheck()
                if monster.target:
                    return True # Prevent random walking
                
            return
        else:
            if not monster.master.alive:
                monster.master = None # I've become independant
            elif monster.master.target and monster.master.targetMode == 1:
                # Target change
                if monster.master.target != monster.target and monster.master.target != monster:
                    monster.target = monster.master.target
                    monster.targetMode = 1
                    
                    # When we reach our destination, can we target check
                    def __walkComplete(x):
                        # Are we OK?
                        if monster.distanceStepsTo(monster.target.position) <= monster.base._targetDistance:
                            monster.turnAgainst(monster.target.position)
                        elif monster.canTarget(monster.target.position):
                            monster.walk_to(monster.target.position, -monster.base._targetDistance, __walkComplete)
                            
                    # Begin autowalking
                    monster.walk_to(monster.target.position, -monster.base._targetDistance, __walkComplete)
                    
                    # If the target moves, we need to recalculate, if he moves out of sight it will be caught in next brainThink
                    def __followCallback(who):
                        if monster.target == who:
                            # Steps below is the old way of doing it, slow and ugly!
                            """monster.stopAction()
                            monster.walk_to(monster.target.position, -monster.base._targetDistance, lambda x: monster.turnAgainst(monster.target.position))
                            """
                            if monster.canTarget(monster.target.position):
                                monster.walk_to(monster.target.position, -monster.base._targetDistance, __walkComplete)
                            else:
                                monster.target = None
                                monster.targetMode = 0
                                    
                            if monster.target:
                                # We shall be called again later
                                monster.target.scripts["onNextStep"].append(__followCallback)
                            
                    monster.target.scripts["onNextStep"].append(__followCallback)
                    return True
                
                return
            elif not monster.inRange(monster.master.position, 1, 1):
                # Follow the master
                monster.target = monster.master
                monster.targetMode = 2

                # When we reach our destination, can we target check
                def __walkComplete(x):
                    # Are we OK?
                    if monster.distanceStepsTo(monster.target.position) <= monster.base._targetDistance:
                        monster.turnAgainst(monster.target.position)
                    elif monster.canTarget(monster.target.position):
                        monster.walk_to(monster.target.position, -monster.base._targetDistance, __walkComplete)
                    else:
                        monster.target = None
                        monster.targetMode = 0
                        
                # Begin autowalking
                monster.walk_to(monster.target.position, -monster.base._targetDistance, __walkComplete)
                    
                # If the target moves, we need to recalculate, if he moves out of sight it will be caught in next brainThink
                def __followCallback(who):
                    if monster.target == who:
                        # Steps below is the old way of doing it, slow and ugly!
                        """monster.stopAction()
                        monster.walk_to(monster.target.position, -monster.base._targetDistance, lambda x: monster.turnAgainst(monster.target.position))
                        """
                        if monster.canTarget(monster.target.position):
                            monster.walk_to(monster.target.position, -monster.base._targetDistance, __walkComplete)
                        else:
                            monster.target = None
                            monster.targetMode = 0
                             
                        if monster.target:
                            # We shall be called again later
                            monster.target.scripts["onNextStep"].append(__followCallback)
                            
                monster.target.scripts["onNextStep"].append(__followCallback)
                return True # Prevent random walking                

game.monster.regBrainFeature("default", defaultBrainFeature)
