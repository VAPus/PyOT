PANDA_TEDDY = 5080
MYSTERIOUS_VOODOO_SKULL =  5669
ENIGMATED_VOODOO_SKULL = 5670
STUFFED_DRAGON = 5791
SANTA_DOLL = 6512
ORACLE_FIGURINE = 8974
TIBIACITY_ENCICLOPEDIA = 8977
GOLDEN_NEWSPAPPER = 8981
NORSEMAN_DOLL = 8982
TOY_SPIDER = 9006
CHRISTMAS_CARD = 6388

usedDolls = {PANDA_TEDDY:6568, MYSTERIOUS_VOODOO_SKULL:5670, ENIGMATED_VOODOO_SKULL:None, STUFFED_DRAGON:6566, SANTA_DOLL:6567, ORACLE_FIGURINE:8975, TIBIACITY_ENCICLOPEDIA:9002, GOLDEN_NEWSPAPPER:None, NORSEMAN_DOLL:8985, TOY_SPIDER:9007, CHRISTMAS_CARD:None}

DOLLS = {\
5080: ("Hug me.",),\
5669: (\
"It's not winning that matters, but winning in style.",\
"Today's your lucky day. Probably.",\
"Do not meddle in the affairs of dragons, for you are crunchy and taste good with ketchup.",\
"That is one stupid question.",\
"You'll need more rum for that.",\
"Do or do not. There is no try.",\
"You should do something you always wanted to.",\
"If you walk under a ladder and it falls down on you it probably means bad luck.",\
"Never say 'oops'. Always say 'Ah, interesting!'",\
"Five steps east, fourteen steps south, two steps north and seventeen steps west!"),\
5791: ("Fchhhhhh!", "Zchhhhhh!", "Grooaaaaar*cough*", "Aaa... CHOO!", "You... will.... burn!!"),\
6388: ("Merry Christmas ",),\
6512: (\
"Ho ho ho",\
"Jingle bells, jingle bells...",\
"Have you been naughty?",\
"Have you been nice?",\
"Merry Christmas!",\
"Can you stop squeezing me now... I'm starting to feel a little sick."),\
8974: ("ARE YOU PREPARED TO FACE YOUR DESTINY?"),\
8977: (\
"Weirdo, you're a weirdo! Actually all of you are!",\
"Pie for breakfast, pie for lunch and pie for dinner!",\
"All hail the control panel!",\
"I own, Tibiacity owns, perfect match!",\
"Hug me! Feed me! Hail me!"),\
        8981: (\
"It's news to me.",
"News, updated as infrequently as possible!",\
"Extra! Extra! Read all about it!",\
"Fresh off the press!"),\
8982: ("Hail TibiaNordic!", "So cold..", "Run, mammoth!"),\
}

@register("use", DOLLS.keys())
def onUse(creature, thing, position, **k):
    if not thing.itemId in DOLLS: return

    rand = random.randint(0, len(DOLLS[thing.itemId])-1)
    sound = DOLLS[thing.itemId][rand]

    if thing.itemId == STUFFED_DRAGON:
        if rand == 2:
            creature.magicEffect(EFFECT_POFF)
        elif rand == 3:
            creature.magicEffect(EFFECT_FIREAREA)
        elif rand == 4:
            creature.hit(None, -1, PHYSICAL, EFFECT_EXPLOSIONHIT)

    elif thing.itemId == MYSTERIOUS_VOODOO_SKULL:
        creature.magicEffect(EFFECT_MAGIC_READ)
    elif thing.itemId == CHRISTMAS_CARD:
        magicEffect(position, EFFECT_SOUND_YELLOW)
        sound = sound + creature.name()


    creature.say(sound, 'MSG_SPEAK_MONSTER_SAY')
    thing.transform(usedDolls[thing.itemId])

    thing.decay()

