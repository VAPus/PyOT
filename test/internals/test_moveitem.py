from test.framework import FrameworkTestGame, async_test

class TestMoveItem(FrameworkTestGame):
    def init(self):
        # Turn off ammo slot only for ammo.
        self.overrideConfig("ammoSlotOnlyForAmmo", False)
        
    def test_bug992(self):
        """ Aga bug #992. Drop item from ammo slot. http://vapus.net/forum/pyot-opentibia-server-287/debug-serious-bugs-thread-2925-100/#post31503 """
        
        # Turn on raises.
        self.player.toggleRaiseMessages()
        
        # Make some gold
        item = Item(idByName('gold coin'), 10)
        
        # Place to inventory
        self.assertTrue(self.player.itemToInventory(item, SLOT_AMMO))
        
        # Assert position.
        self.assertIs(self.player.inventory[SLOT_AMMO], item)
        position = Position(0xFFFF, SLOT_AMMO+1, 0)
        
        # Move to ground.
        newPosition = self.player.positionInDirection(SOUTH)
        self.assertTrue(moveItem(self.player, position, newPosition))
        
        # Is it there?
        found = False
        for _item in newPosition.getTile().getItems():
            if _item.itemId == item.itemId:
                found = True
                
        self.assertTrue(found)
        
        self.player.toggleRaiseMessages()
       
    def test_bug59(self):
        " Issue #59 part 2. http://vapus.net/forum/project.php?issueid=59 "
        
        # Make some gold
        item = Item(idByName('gold coin'), 100)
        
        # Place to inventory.
        self.player.itemToInventory(item, SLOT_AMMO)
        
        # Split stack.
        # Move to ground.
        position = Position(0xFFFF, SLOT_AMMO+1, 0)
        
        self.assertTrue(moveItem(self.player, position, self.player.position, 50))
        
        # Is it still there?
        self.assertEqual(self.player.inventory[SLOT_AMMO], item)
        
        # Correct count?
        self.assertEqual(item.count, 50)
  
    def test_stack(self):
        " Reverse of the above. "
        
        # Make some gold
        item = Item(idByName('gold coin'), 50)
        item2 = Item(idByName('gold coin'), 50)
        item2.place(self.player.position)
        stack = self.player.position.getTile().findStackpos(item2)
        groundPosition = self.player.position.setStackpos(stack)
        
        # Place to inventory.
        self.player.itemToInventory(item, SLOT_AMMO)
        
        # Move stack from ground to inventory.
        position = Position(0xFFFF, SLOT_AMMO+1, 0)
        
        self.assertTrue(moveItem(self.player, groundPosition, position, 50))
        
        # Is it still there?
        self.assertEqual(self.player.inventory[SLOT_AMMO], item)
        
        # And not on the ground?
        self.assertFalse(item2 in self.player.position.getTile())
        
        # Correct count?
        self.assertEqual(item.count, 100)
        

    def test_move_ground(self):
        # Make some gold.
        item = Item(idByName('gold coin'), 10)
        item.place(self.player.position)
        
        # Move.
        self.assertTrue(moveItem(self.player, item.position, self.player.positionInDirection(SOUTH), 10))

        things = self.player.position.getTile()
        self.assertNotIn(item, things)
        
        ok = False
        for thing in self.player.positionInDirection(SOUTH).getTile():
            if thing.itemId == item.itemId:
                ok = True
                
        self.assertTrue(ok)
   
    def test_closebag(self):
        # Make a bag.
        item = Item(idByName('bag'))
        self.player.itemToInventory(item, SLOT_BACKPACK)

        # Open bag.
        self.player.openContainer(item)
        
        # Move to ground.
        newPosition = self.player.position.copy()
        newPosition.x += 2
        self.assertTrue(moveItem(self.player, Position(0xFFFF, SLOT_BACKPACK+1, 0), newPosition))
        self.assertFalse(item.openIndex)

    def test_move_ground_no_count(self):
        # Make some gold.
        item = Item(idByName('gold coin'), 10)
        item.place(self.player.position)
        
        self.assertEqual(self.player.position, item.position)
        
        # Move.
        self.assertTrue(moveItem(self.player, item.position, self.player.positionInDirection(SOUTH)))

        things = self.player.position.getTile()
        self.assertNotIn(item, things)
        
        ok = False
        for thing in self.player.positionInDirection(SOUTH).getTile():
            if thing.itemId == item.itemId:
                ok = True
                
        self.assertTrue(ok)


    def test_move_ammo_bag_ground(self):
        self.player.toggleRaiseMessages()

        # Make some arrows
        item = Item(idByName('crystal arrow'), 100)

        # Make a bag.
        bag = Item(idByName('bag'))

        # Place to inventory.
        self.player.itemToInventory(item, SLOT_AMMO)
        self.player.itemToInventory(bag, SLOT_BACKPACK)

        # Open bag.
        self.player.openContainer(bag)

        # Move to bag.
        position = Position(0xFFFF, SLOT_AMMO+1, 0)
        bagPosition = Position(0xFFFF, SLOT_BACKPACK+1, 0)

        self.assertTrue(moveItem(self.player, position, bagPosition, 100))

        self.assertFalse(config.ammoSlotOnlyForAmmo)

        # Move to ground.
        self.assertTrue(moveItem(self.player, Position(0xFFFF, bag.openIndex+64,0), self.player.position))

        # Is it still there?
        self.assertEqual(self.player.inventory[SLOT_AMMO], None)

        self.player.toggleRaiseMessages()

    def test_move_to_self(self):
        # Make a gold coin 
        item = Item(idByName('gold coin'), 1)

        # Make a bag.
        bag = Item(idByName('bag'))

        # Place to inventory
        self.player.itemToInventory(bag, SLOT_BACKPACK)

        # Item to bag.
        self.player.itemToContainer(bag, item)

        # Open bag.
        self.player.openContainer(bag)

        # Move to bag.
        self.assertFalse(moveItem(self.player, Position(0xFFFF, bag.openIndex+64, 0), Position(0xFFFF, SLOT_BACKPACK+1, 0)))

    def test_dual_handed(self):
        # Make a dual handed sword
        item = Item(7449)

        self.assertEqual(item.slotType, "two-handed")

        # Place it.
        self.player.itemToInventory(item, SLOT_RIGHT)

        # Make a shield
        item = Item(2509)
        
        # Place it.
        item.place(self.player.position)

        # Move it. Shouldn't work.
        self.assertFalse(moveItem(self.player, item.position, Position(0xFFFF, SLOT_LEFT-1, 0)))

    def test_courpse_to_corpse_stack(self):
        " Bug #78 "
        # Set meat to 100%.
        wolf = getMonster("Wolf")
        if not wolf.prepared:
            wolf.prepare()

        for loot in wolf.lootTable:
           if loot[0] == idByName('meat'):
               loot[1] = 100.0

        # Spawn and kill two wolfs
        position1 = self.player.positionInDirection(NORTH)
        position2 = self.player.positionInDirection(SOUTH)

        wolf1 = wolf.spawn(position1, spawnDelay=0)
        wolf2 = wolf.spawn(position2, spawnDelay=0)

        wolf1.modifyHealth(-1000)
        wolf2.modifyHealth(-1000)

        # Make sure they are dead.
        self.assertFalse(wolf1.alive)
        self.assertFalse(wolf2.alive)

        # Get the corpses.
        corpse1 = position1.getTile().findItem(wolf.data["corpse"])
        corpse2 = position2.getTile().findItem(wolf.data["corpse"])

        self.assertTrue(corpse1)
        self.assertTrue(corpse2)

        # Open corpses.
        self.player.use(corpse1)
        self.player.use(corpse2)

        # Find meat and move from corpse1 to corpse2.
        for index in range(len(corpse1.container)):
            if corpse1.container[index].itemId == idByName('meat'):
                break

        # Move
        self.assertTrue(moveItem(self.player, Position(0xFFFF, 64, index), Position(0xFFFF, 65, 3)))

        # Find new meat.
        for item in corpse2.container:
            if item.itemId == idByName('meat'):
                self.assertGreater(item.count, 1)
                break

        self.assertEqual(item.itemId, idByName('meat'))

    def test_courpse_to_corpse_specific_stack(self):
        " Bug #78 "

        # Set meat to 100%.
        wolf = getMonster("Wolf")
        if not wolf.prepared:
            wolf.prepare()

        for loot in wolf.lootTable:
           if loot[0] == idByName('meat'):
               loot[1] = 100.0

        # Spawn and kill two wolfs
        position1 = self.player.positionInDirection(NORTH)
        position2 = self.player.positionInDirection(SOUTH)

        wolf1 = wolf.spawn(position1, spawnDelay=0)
        wolf2 = wolf.spawn(position2, spawnDelay=0)

        wolf1.modifyHealth(-1000)
        wolf2.modifyHealth(-1000)

        # Get the corpses.
        corpse1 = position1.getTile().findItem(wolf.data["corpse"])
        corpse2 = position2.getTile().findItem(wolf.data["corpse"])

        # Open corpses.
        self.player.use(corpse1)
        self.player.use(corpse2)

        # Find meat and move from corpse1 to corpse2.
        for index in range(len(corpse1.container)):
            if corpse1.container[index].itemId == idByName('meat'):
                break

        for index2 in range(len(corpse2.container)):
            if corpse2.container[index2].itemId == idByName('meat'):
                break

        # Move
        try:
            self.assertTrue(moveItem(self.player, Position(0xFFFF, 64, index), Position(0xFFFF, 65, index2)))
        except:
            self.fail("Corpse Indexes failed.")

        # Find new meat.
        for item in corpse2.container:
            if item.itemId == idByName('meat'):
                self.assertGreater(item.count, 1)
                break

        self.assertEqual(item.itemId, idByName('meat'))

    def test_bug93(self):
        # Make two bags. Place them on the ground.
        bag1 = Item(idByName('bag'))
        bag2 = Item(idByName('bag'))

        bag1.place(Position(1001, 1000, 7))
        bag2.place(Position(1001, 1000, 7))

        # Open bags. 
        self.player.openContainer(bag2)

        for id2, bag in self.player.openContainers.items():
            if bag == bag2:
                break
        for id1, bag in self.player.openContainers.items():
            if bag == bag1:
                break

        # Verify position.
        bag1Pos= bag1.verifyPosition()
        bag2Pos = bag2.verifyPosition()

        self.assertEqual(bag1, bag1Pos.getTile().getThing(bag1Pos.stackpos))

        # Move bag1 into bag2. This works.
        self.assertTrue(moveItem(self.player, bag1Pos, Position(0xFFFF, 64 + id2, 0)))

        # Move bag2 into bag1. This shouldn't work.
        self.assertFalse(moveItem(self.player, bag2Pos, Position(0xFFFF, 64 + id1, 0)))

    def test_relocate(self):
        coin = Item(idByName('gold coin'))

        coin.place(Position(1000, 1001, 7))

        relocate(Position(1000, 1001, 7), Position(1001, 1000, 7))

        self.assertIn(coin, Position(1001, 1000, 7).getTile())

    def test_117_p9(self):
        " http://vapus.net/forum/project.php?issueid=117 "

        coin = Item(idByName('gold coin'), 70)

        coin2 = Item(idByName('gold coin'), 80)

        bag = Item(idByName('bag'))
        self.player.inventory[SLOT_BACKPACK] = bag
        
        # Move coins to bag.
        self.player.addItem(coin)
        self.player.addItem(coin2)
        
        self.assertEqual(bag.size(), 2)
        self.assertEqual(bag.container[1].count, 100)
        self.assertEqual(bag.container[0].count, 50)

        bag.container[1].count = 60

        bag.position = Position(0xFFFF, SLOT_BACKPACK+1, 0)
        bag.creature = self.player
        self.player.use(bag)

        self.assertTrue(moveItem(self.player, Position(0xFFFF, 64, 0), Position(0xFFFF, 64, 1)))

        self.assertEqual(bag.size(), 2)
        self.assertEqual(bag.container[1].count, 100)
        self.assertEqual(bag.container[0].count, 10)


    def test_bug119(self):
        " http://vapus.net/forum/project.php?issueid=119 "

        bag = Item(idByName('bag'))
        bag.position = Position(0xFFFF,SLOT_BACKPACK+1, 0)
        bag.creature = self.player

        self.player.inventory[SLOT_BACKPACK] = bag

        self.player.use(bag)

        rope = Item(idByName('rope'))
        coin = Item(idByName('gold coin'), 1)

        self.player.addItem(coin)
        self.player.addItem(rope)

        self.assertEqual(bag.size(), 2)
        self.assertEqual(bag.container[0].name, "rope")

        self.assertTrue(moveItem(self.player, Position(0xFFFF, 64, 1), Position(0xFFFF, 64, 0)))

        self.assertEqual(bag.size(), 2)


    def test_consistant_weight(self):

        self.player.toggleRaiseMessages()

        if self.player.inventory[SLOT_BACKPACK]:
            self.player.inventory[SLOT_BACKPACK].remove()

        bag = Item(idByName('bag'))
        bag.place(Position(0xFFFF,SLOT_AMMO+1, 0), self.player)

        weight = self.player.inventoryWeight

        self.assertTrue(moveItem(self.player, bag.position, Position(0xFFFF, SLOT_BACKPACK+1, 0)))

        self.assertEqual(weight, self.player.inventoryWeight)
        self.player.toggleRaiseMessages()


    def test_groundstack(self):
        " http://vapus.net/forum/distributions-227/%5B8-6-9-71%5D-pyot-v1-0-alpha3-6061-6/#post32628 "


        gold1 = Item(idByName("gold coin"), 10)
        gold2 = Item(idByName("gold coin"), 10)

        gold1.place(Position(1000, 1001, 7))
        gold2.place(Position(1001, 1000, 7))

        self.assertTrue(moveItem(self.player, gold2.position, gold1.position))

        self.assertEqual(gold1.count, 20)
        self.assertNotIn(gold2, gold1.position.getTile())
    
