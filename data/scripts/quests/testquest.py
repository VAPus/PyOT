# The quest itself
quest = genQuest("The hello world")
quest.mission("Say hello world")
quest.description("Simply type 'hello world' to finish this quest")

# Some actions to deal with it
@register("talkaction", "begin quest")
def startQuest(creature, **k):
    creature.say("Wow, a quest just began")
    creature.beginQuest("The hello world")
    
    return False
    
@register("talkaction", "hello world")
def endQuest(creature, **k):
    if creature.isPlayer() and creature.questStarted("The hello world") and not creature.questCompleted("The hello world"):
        creature.finishQuest("The hello world")


# Another example quest, with missions this time

q = genQuest("The hunger games")
q.mission("Look at yourself.")
q.description("That's a pretty clear objective, no?")
q.mission("Look at the wolf.")
q.description("It isn't getting any harder, is it?")
q.mission("Look at the scorpion.")
q.description("You like forkfeeding, right?")


# Type 'missions quest' to start this quest.
# It doesn't check if you've already started or done it, so you can start over indefinately.

@register("talkaction", "missions quest")
def letsRoll(creature, **k):
    creature.say("Shit has just got serious, so I'll better check my questlog.")
    creature.beginQuest(q) 
    return False

@register("lookAt", "creature")
def annoyingQuest(creature, thing, **k):
	player = creature # more natural?
	if not player.questStarted(q) or player.questCompleted(q):
		return True
	
	if player == thing and player.questProgress(q) == 0:
		player.say("I've just looked at myself. Mission accomplished!")
		player.progressQuest(q)	# sets the mission as 'completed'
		player.progressQuestMission(q)	# advances to next mission
	elif thing.name() == "Wolf" and player.questProgress(q) == 1:
		player.say("I did it! I can do anything!")
		player.progressQuest(q)
		player.progressQuestMission(q)
	elif thing.name() == "Scorpion" and player.questProgress(q) == 2:
		player.say("A hero like me is always there to save the day!")
		player.progressQuest(q)
		player.finishQuest(q)
	return True