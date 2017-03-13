# Autoconverted script for PyOT
# Untested. Please remove this message when the script is working properly!


allMounts = {\
5907: {"name": 'Bear', "type": "monster", "chance": 20, "failMsg": ["The bear ran away.", "Oh no! The slingshot broke.", "The bear is trying to hit you with its claws."], "successMsg": "You tamed the wild bear."},
13295: {"name": 'Black Sheep', "type": "monster", "chance": 25, "failMsg": ["Oh no! The reins were torn.", "The black sheep is trying to run away.", "The black sheep ran away."], "successMsg": "You tamed the black sheep."},
13293: {"name": 'Midnight Panther', "type": "monster", "chance": 40, "failMsg": ["The panther has escaped.", "The whip broke."], "successMsg": "You tamed the panther."},
13298: {"name": 'Terror Bird', "type": "monster", "chance": 14, "failMsg": ["The bird ran away.", "The terror bird is pecking you."], "successMsg": "You tamed the bird."},
13247: {"name": 'Boar', "type": "monster", "chance": 40, "failMsg": ["The boar has run away", "The boar attacks you."], "successMsg": "You tamed the boar."},
13305: {"name": 'Crustacea Gigantica', "type": "monster", "chance": 40, "failMsg": ["The crustacea has run away.", "The crustacea ate the shrimp."], "successMsg": "You have tamed the crustacea."},
13291: {"name": 'Undead Cavebear', "type": "monster", "chance": 40, "failMsg": ["The undead bear has run away."], "successMsg": "You have tamed the skeleton."},
13307: {"name": 'Wailing Widow', "type": "monster", "chance": 40, "failMsg": ["The widow has run away.", "The widow has eaten the sweet bait."], "successMsg": "You tamed the widow."},
13292: {"name": 'Tin Lizzard', "type": "npc", "chance": 40, "failMsg": ["The key broke inside."], "successMsg": "You have started the Tin Lizzard!"},
13294: {"name": 'Draptor', "type": "monster", "chance": 40, "failMsg": ["The draptor has fled.", "The draptor has run away."], "successMsg": "You tamed the draptor."},
13536: {"name": 'Crystal Wolf', "type": "monster", "chance": 40, "failMsg": ["The wolf has run away."], "successMsg": "You tamed the wolf."},
13539: {"name": 'White Deer', "type": "monster", "chance": 40, "failMsg": ["The deer has fled in fear.", "The cone broke."], "successMsg": "You tamed the deer."},
13538: {"name": 'Panda', "type": "monster", "chance": 40, "failMsg": ["Panda ate the leaves and ran away."], "successMsg": "You tamed the Panda."},
13535: {"name": 'Dromedary', "type": "monster", "chance": 40, "failMsg": ["Dromedary has run away."], "successMsg": "You have tamed Dromedary."},
13498: {"name": 'Sandstone Scorpion', "type": "monster", "chance": 40, "failMsg": ["The scorpion has vanished.", "Scorpion broken the sceptre."], "successMsg": "You tamed the Scorpion"},
13537: {"name": 'Donkey', "type": "monster", "chance": 40, "failMsg": ["The witch has esacped!"], "successMsg": "You tamed the Mule."},
13938: {"name": 'Uniwheel', "type": "npc", "chance": 40, "failMsg": ["This Uniwheel the oil is having no effect."], "successMsg": "You found a Uniwheel."},
13508: {"name": 'Slug', "type": "monster", "chance": 40, "failMsg": ["The slug has run away.", "The drug had no effect."], "successMsg": "You tamed the slug."},
13939: {"name": 'Fire Horse', "type": "monster", "chance": 15, "failMsg": ["The horse runs away.", "The horse ate the oats."], "successMsg": "You tamed the War Horse."}
}

actions = ["run", "break", "nothing"]

def doFailAction(creature, id, mount, pos, onThing):
    action = actions[id]
    if action == "run":
        magicEffect(pos, EFFECT_POFF)
        onThing.despawn()
        creature.say(mount.failMsg[id], 'MSG_SPEAK_MONSTER_SAY')
    elif action == "break":
        magicEffect(pos, EFFECT_BLOCKHIT)
        thing.modify(-1)
        creature.say(mount.failMsg[id], 'MSG_SPEAK_MONSTER_SAY')
    elif action == "nothing":
        magicEffect(pos, EFFECT_POFF)
        creature.say(mount.failMsg[id], 'MSG_SPEAK_MONSTER_SAY')
    return action

@register("useWith", (13295, 13294, 13293, 13298, 13247, 13305, 13291, 5907, 13307, 13292, 13938, 13939, 13508, 13535, 13536, 13537, 13538, 13539, 13498))
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    try:
        mount = allMounts[thing.itemId]
        if creature.canMount(mount["name"]):
            return
    except:
        return

    actionId, rand = random.randint(0, len(mount["failMsg"])-1), random.randint(1, 100)

    # Monster Mount
    if onThing.isMonster() and not onThing.isSummon() and mount["type"] == "monster":
        if mount["name"] == onThing.name():
            if rand > mount["chance"]:
                doFailAction(creature, actionId, mount, onPosition, onThing)
                return True
            else:
                creature.addMount(mount["name"])
                creature.orangeStatusMessage(mount["successMsg"])
                creature.say(mount["successMsg"], 'MSG_SPEAK_MONSTER_SAY')
                onThing.despawn()
                magicEffect(onPosition, EFFECT_POFF)
                thing.modify(-1)
                return True
        
    # NPC Mount
    elif onThing.isNPC() and not onThing.isMonster() and mount["type"] == "npc":
        if mount["name"] == onThing.name():
            if rand > mount["chance"]:
                doFailAction(creature, actionId, mount, onPosition, onThing)
                return True
            else:
                creature.addMount(mount["name"])
                creature.orangeStatusMessage(mount["successMsg"])
                creature.say(mount["successMsg"], 'MSG_SPEAK_MONSTER_SAY')
                magicEffect(onPosition, EFFECT_MAGIC_GREEN)
                thing.modify(-1)
                return True
    
    return
