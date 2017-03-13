from test.framework import FrameworkTestGame, async_test

class TestCondition(FrameworkTestGame):
    def test_addCondition(self):
        condition = Condition(CONDITION_FIRE, length=10, damage=1)
        self.player.condition(condition)

        self.assertTrue(self.player.conditions)
        self.assertTrue(condition.creature)

    def test_hascondition(self):
        condition = Condition(CONDITION_FIRE, length=10, damage=1)
        self.player.condition(condition)

        self.assertTrue(self.player.hasCondition(CONDITION_FIRE))

    def test_getcondition(self):
        condition = Condition(CONDITION_FIRE, length=10, damage=1)
        self.player.condition(condition)

        self.assertEqual(self.player.getCondition(CONDITION_FIRE), condition)

    def test_copycondition(self):
        condition = Condition(CONDITION_FIRE, length=10, damage=1)

        condition2 = condition.copy()

        self.assertEqual(condition.type, condition2.type)

    @async_test
    def test_boost(self):
        boost = Boost("speed", 1000, 0.2)
        
        originalSpeed = self.player.speed
        
        self.player.condition(boost)
        
        self.assertEqual(self.player.speed, originalSpeed + 1000)
        
        def revert():
            self.assertEqual(self.player.speed, originalSpeed)
            
        yield gen.Task(IOLoop.instance().add_timeout, time.time() + 0.3)
        revert()
        
    @async_test
    def test_multiboost(self):
        boost = Boost(["health", "healthmax"], [1000, 1000], 0.2)
        
        originalHealth = self.player.data["health"]
        originalHealthMax = self.player.data["healthmax"]
        
        self.player.condition(boost)
        
        self.assertEqual(self.player.data["health"], originalHealth + 1000)
        self.assertEqual(self.player.data["healthmax"], originalHealthMax + 1000)
        
        def revert():
            self.assertEqual(self.player.data["health"], originalHealth)
            self.assertEqual(self.player.data["healthmax"], originalHealthMax)
            
        yield gen.Task(IOLoop.instance().add_timeout, time.time() + 0.3)
        revert()

    @async_test        
    def test_boostskill(self):
        boost = Boost(SKILL_SWORD, 10, 0.2)
        
        originalSkill = self.player.getActiveSkill(SKILL_SWORD)
        
        self.player.condition(boost)
        
        self.assertEqual(self.player.getActiveSkill(SKILL_SWORD), originalSkill + 10)
        
        def revert():
            self.assertEqual(self.player.getActiveSkill(SKILL_SWORD), originalSkill)
            
        yield gen.Task(IOLoop.instance().add_timeout, time.time() + 0.3)
        revert()

   
    def test_process(self):
        condition = Condition(CONDITION_FIRE, length=10, every=2, damage=1)
        preHealth = self.player.data['health']

        # (10 / 2) * 1 = 5
        self.player.condition(condition)

        self.assertTrue(self.player.hasCondition(CONDITION_FIRE))
        condition.process()

        self.assertEqual(self.player.data['health'], preHealth - 5)

        # It should also no longer be active.
        self.assertFalse(self.player.hasCondition(CONDITION_FIRE))

    def test_countdownCondition(self):
        condition = CountdownCondition(CONDITION_POISON, 1)
        preHealth = self.player.data['health']

        self.player.condition(condition)
        
        self.assertTrue(self.player.hasCondition(CONDITION_POISON))
        self.assertEqual(self.player.getCondition(CONDITION_POISON), condition)        
        
        condition.process()

        self.assertLess(self.player.data['health'], preHealth) # It can be 99 or 98. It's random.

    def test_repeatCondition(self):
        condition = RepeatCondition(CONDITION_POISON, 1, 10)
        preHealth = self.player.data['health']

        self.player.condition(condition)

        self.assertTrue(self.player.hasCondition(CONDITION_POISON))
        self.assertEqual(self.player.getCondition(CONDITION_POISON), condition)

        condition.process()

        self.assertEqual(self.player.data['health'], preHealth - 10)

    def test_percentCondition(self):
        condition = PercentCondition(CONDITION_POISON, 10, 0.5, 5) # Should give us: 10, 5, 3, 2, 1 = 21.
        preHealth = self.player.data['health']

        self.player.condition(condition)

        self.assertTrue(self.player.hasCondition(CONDITION_POISON))
        self.assertEqual(self.player.getCondition(CONDITION_POISON), condition)

        condition.process()

        self.assertEqual(self.player.data['health'], preHealth - 21)
