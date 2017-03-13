spellBooks = 2175, 6120, 8900, 8901, 8902, 8903, 8904, 8918

@register('use', spellBooks)
def spellBook(creature, thing, **k):
    text = ""
    lists = {}

    for spellwords in game.spell.spells:
        spell = game.spell.spells[spellwords]
        
        if not spell[2] in lists:
            lists[spell[2]] = [spellwords]
        else:
            lists[spell[2]].append(spellwords)
    levels = lists.keys()
    levels.sort()
    for level in levels:
        text += "Spells for Level %d:\n" % level
        for spell in lists[level]:
            text += "  %s - %s : %s\n" % (spell, game.spell.spells[spell][1], game.spell.spells[spell][3])
        text += "\n"
    creature.textWindow(thing, text=text)