@register("talkactionFirstWord", '/i')
@access("CREATEITEM")
def makeitem(creature, text):
    try:
        count = 1
        if ' ' in text:
            count = int(text.split(" ")[1])
        text = int(text.split(" ")[0])
        if True: # text >= 1000:
            while count:
                rcount = min(100, count)
                newitem = Item(text, rcount)
                if newitem.pickable:
                    creature.addItem(newitem)
                else:
                    newitem.place(creature.position)

                count -= rcount
    except:
        creature.message("Invalid Item!")
         
    return False


# Create item by name ex: /in magic longsword, 1

@register("talkactionFirstWord", '/in')
@access("CREATEITEM")
def createItemByName(creature, text):
    itemid = game.item.idByName(text.split(",")[0].strip())
    if not itemid:
        creature.message("No such item.")
    else:
        count = text.split(",")[1].strip() if "," in text else 1
        item = Item(itemid, int(count))
        creature.addItem(item)
        creature.magicEffect(EFFECT_MAGIC_GREEN)
    return False
