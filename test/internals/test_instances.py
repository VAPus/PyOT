from test.framework import FrameworkTestGame, async_test

class TestInstances(FrameworkTestGame):
    def init(self):
        # Turn off protection zones.
        self.overrideConfig("protectedZones", False)

    def test_newinstance(self):
        # Make a instance.
        instanceId = game.map.newInstance()
        self.assertNotEqual(instanceId, None)
        self.assertIn(instanceId, game.map.instances)
        
    def test_loadmap(self):
        instanceId = game.map.newInstance()
        Position(1000,1000,7, instanceId).getTile() # Loads.
        
        #self.assertIn(instanceId, game.map.knownMap)
    
    def test_item_on_instance(self):
        # Make a item
        item  = Item(7449)
        
        # Place on a instance.
        instanceId = game.map.newInstance()
        self.assertNotEqual(instanceId, 0)

        position = Position(1000,1001,7,instanceId)
        
        status = item.place(position)
        self.assertTrue(status)

        self.assertIn(item, position.getTile())
        self.assertNotIn(item, (Position(1000, 1001, 7).getTile() or []))
    

    def test_can_notsee(self):
        # Make a item
        item  = Item(7449)
        
        # Place on a instance.
        instanceId = game.map.newInstance()
        position = Position(1000,1001,7,instanceId)
        
        item.place(position)
        
        self.assertFalse(self.player.canSee(position))
    
    

    def test_can_notsee_reverse(self):
        # Make a item
        item  = Item(7449)
        
        # Place on a default
        instanceId = game.map.newInstance()
        position = Position(1000,1001,7)
        
        item.place(position)
        
        self.player.setInstance(instanceId)
        self.assertFalse(self.player.canSee(position))
    
    def test_cansee(self):
        # Make a item
        item  = Item(7449)
        
        # Place on a instance.
        instanceId = game.map.newInstance()
        position = Position(1000,1001,7,instanceId)
        
        item.place(position)
        
        self.player.setInstance(instanceId)
        
        self.assertTrue(self.player.canSee(position))
    
    def test_move_across_instances(self):
        # Make a item
        item  = Item(7449)
        
        # Place on a instance.
        instanceId = game.map.newInstance()
        
        position = Position(1000,1001,7)
        iPosition = Position(1000,1001,7,instanceId)
        
        item.place(position)
        
        self.player.setInstance(instanceId)
        
        self.assertFalse(self.player.canSee(position))
        
        item.move(iPosition)
        
        self.assertTrue(self.player.canSee(iPosition))
        
        self.assertIn(item, iPosition.getTile())
        self.assertNotIn(item, (position.getTile() or []))

    
    def test_monster_spawn_pos(self):
        # Instance.
        instanceId = game.map.newInstance()
        position = Position(1000,1001,7,instanceId)
        
        self.player.setInstance(instanceId)

        # A wolf.
        baseWolf = getMonster("Wolf")
        
        wolf = baseWolf.spawn(position, spawnDelay=0)

        self.assertIn(wolf, list(position.getTile().creatures()))

        self.assertTrue(self.player.canSee(wolf.position))

        # Cleanup.
        wolf.despawn()

        
    
