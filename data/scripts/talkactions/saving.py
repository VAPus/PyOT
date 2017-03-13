@register("talkaction", 'saveme')
@access("SAVEME")
def saveMe(creature, text):
    creature.save()
    return False
    

@register("talkaction", 'saveall')
@access("SAVEALL")
def saveAll(creature, text):
    saveAll()
    return False
