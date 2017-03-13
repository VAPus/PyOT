mailboxes = (2593,)

def parseText(text):
    lines = text.split("\n")
    if lines >= 2:
        townId = townNameToId(lines[1])
        if townId:
            return (lines[0], townId)

# When we're working with IO blocking behavior such as SQL (which might be needed in case of placeInDepot) we are required to use callbacks to deal with result)
@register('useWith', mailboxes)
@register('dropOnto', mailboxes)
@gen.coroutine        
def onSendParcelOrLetter(creature, position, thing, onThing, **k):
    # Is it a letter perhaps?
    onId = onThing.itemId
    if onId == ITEM_LETTER:
        if not onThing.text:
            creature.lmessage("To whom shall this letter be sent?", onPos=position)
            return
        parse = parseText(onThing.text)
        
        if not parse:
            creature.lmessage("Did you spell it right?", onPos=position)
            
        onThing.itemId = ITEM_LETTER_STAMPED # We need to change the Id before the placeInDepot takes place in case the player is offline, the data is saved right away
        result = yield placeInDepot(parse[0], parse[1], onThing)
        
        if not result:
            onThing.itemId = ITEM_LETTER # Convert the item back to it's original Id
            creature.lmessage("Did you spell it right?", onPos=position)
            return
            
    elif onId == ITEM_PARCEL:
        found = None
        for item in onThing.container:
            if item.itemId == ITEM_LABEL:
                found = item
                break
                
        if not found or not found.text:
            creature.lmessage("To whom shall this parcel be sent?", onPos=position)
            return            

        parse = parseText(found.text)

        if not parse:
            creature.lmessage("Did you spell it right?", onPos=position)
            
        onThing.itemId = ITEM_PARCEL_STAMPED
        result = yield placeInDepot(parse[0], parse[1], onThing)

        if not result:
            onThing.itemId = ITEM_PARCEL # Convert the item back to it's original Id
            creature.lmessage("Did you spell it right?", onPos=position)
            return

    else:
        creature.lmessage("It's not a package or letter.")
