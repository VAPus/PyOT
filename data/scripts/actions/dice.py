@register("use", range(5792, 5797+1))
def onUse(creature, thing, position, **k):
    rolled = random.randint(1,6)
    creature.say("%s rolled a %d" % (creature.name(), rolled),'MSG_SPEAK_MONSTER_SAY')
    thing.transform(5791 + rolled)
    
    magicEffect(position, EFFECT_CRAPS)