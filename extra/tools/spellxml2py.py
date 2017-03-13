from xml.dom.minidom import parse

spells = parse("spells.xml")
generated = ""
def idToGroup(id):
    if id == 1:
        return "ATTACK_GROUP"
    elif id == 2:
        return "HEALING_GROUP"
    elif id == 3:
        return "SUPPORT_GROUP"
    elif id == 4:
        return "SPECIAL_GROUP"
        
for conjure in spells.getElementsByTagName("conjure"):
    vocations = []

    for voc in conjure.getElementsByTagName("vocation"):
        vocations.append(int(voc.getAttribute("id")))
    if vocations:
        vocations = repr(tuple(vocations))
    else:
        vocations = "None"
    mlevel = conjure.getAttribute("maglv") or "0"
    text = '\nconjure = spell.Spell("%s", "%s", icon=%s, group=SUPPORT_GROUP)' % (conjure.getAttribute("name"), conjure.getAttribute("words"), conjure.getAttribute("icon"))
    text += "\nconjure.require(mana=%s, level=%s, maglevel=%s, soul=%s, learned=%s, vocations=%s)" % (conjure.getAttribute("mana"), conjure.getAttribute("lvl"), mlevel, conjure.getAttribute("soul") or "0", conjure.getAttribute("needlearn") or "0", vocations)
    text += "\nconjure.use(%s)" % (conjure.getAttribute("reagentId") or "2260")
    text += "\nconjure.cooldowns(%s, %s)" % (str(int(conjure.getAttribute("exhaustion") or "0")/1000) or "0", str(int(conjure.getAttribute("groups").split(",")[1])/1000))
    text += "\nconjure.targetEffect(callback=spell.conjure(%s, %s))" % (conjure.getAttribute("conjureId"), conjure.getAttribute("conjureCount") or "1")
    #text = 'spell.conjureRune("%s", make=%s, icon=%s, mana=%s, level=%s, mlevel=%s, soul=%s, use=%s, makeCount=%s, vocations=%s, teached=%s)\n' % (conjure.getAttribute("words"), conjure.getAttribute("conjureId"), conjure.getAttribute("icon"), conjure.getAttribute("mana"), conjure.getAttribute("lvl"), mlevel, conjure.getAttribute("soul") or "0", conjure.getAttribute("reagentId") or "2260", conjure.getAttribute("conjureCount") or "1", vocations, conjure.getAttribute("needlearn") or "0")

    for rune in spells.getElementsByTagName("rune"):
        if conjure.getAttribute("conjureId") == rune.getAttribute("id"):
            
            if rune.getAttribute("needtarget"):
                text += "\n\n# Incomplete! Target rune."
                text += "\nrune = spell.Rune(%s, icon=%s, count=%s, target=TARGET_TARGET, group=%s)" % (rune.getAttribute("id"), rune.getAttribute("icon"), rune.getAttribute("charges"), idToGroup(rune.getAttribute("groups").split(",")[0]))
                text += "\nrune.cooldowns(%s, %s)" % (str(int(rune.getAttribute("exhaustion") or "0")/1000) or "0", str(int(rune.getAttribute("groups").split(",")[1])/1000))
                text += "\nrune.require(mana=%s, level=%s, maglevel=%s)" % (rune.getAttribute("mana") or "0", rune.getAttribute("lvl") or "0", mlevel)
                text += "\nrune.targetEffect() # TODO"
                text += "\nrune.effects() # TODO"
                
                #spell.targetRune(rune=%s, level=%s, mlevel=%s, icon=%s, group=%s, effect=<TODO>, callback=<TODO>, cooldown=%s, useCount=%s)" % (rune.getAttribute("id"),rune.getAttribute("level"),rune.getAttribute("maglv"),rune.getAttribute("icon"),rune.getAttribute("groups").split(",")[0],rune.getAttribute("groups").split(",")[1],rune.getAttribute("charges"))
            elif rune.getAttribute("blocktype") == "solid":
                text += "\n\n# Incomplete! Field rune."
                text += "\nrune = spell.Rune(%s, icon=%s, count=%s, target=TARGET_AREA, group=%s)" % (rune.getAttribute("id"), rune.getAttribute("icon"), rune.getAttribute("charges"), idToGroup(rune.getAttribute("groups").split(",")[0]))
                text += "\nrune.cooldowns(%s, %s)" % (str(int(rune.getAttribute("exhaustion") or "0")/1000) or "0", str(int(rune.getAttribute("groups").split(",")[1])/1000))
                text += "\nrune.require(mana=%s, level=%s, maglevel=%s)" % (rune.getAttribute("mana") or "0", rune.getAttribute("lvl") or "0", mlevel)
                text += "\nrune.targetEffect() # TODO"
                text += "\nrune.effects() # TODO"
                
            else:
                text += "\n\n# Incomplete! Self target rune?"
                text += "\nrune = spell.Rune(%s, icon=%s, count=%s, target=TARGET_TARGET, group=%s)" % (rune.getAttribute("id"), rune.getAttribute("icon"), rune.getAttribute("charges"), idToGroup(rune.getAttribute("groups").split(",")[0]))
                text += "\nrune.cooldowns(%s, %s)" % (str(int(rune.getAttribute("exhaustion") or "0")/1000) or "0", str(int(rune.getAttribute("groups").split(",")[1])/1000))
                text += "\nrune.require(mana=%s, level=%s, maglevel=%s)" % (rune.getAttribute("mana") or "0", rune.getAttribute("lvl") or "0", mlevel)
                text += "\nrune.targetEffect() # TODO"
                text += "\nrune.effects() # TODO"
                
    with open("spells/%s.py" % conjure.getAttribute("name"), "wb") as f:
        f.write(text)
    
for instant in spells.getElementsByTagName("instant"):
    vocations = []

    for voc in instant.getElementsByTagName("vocation"):
        vocations.append(int(voc.getAttribute("id")))
    if vocations:
        vocations = repr(tuple(vocations))
    else:
        vocations = "None"
    mlevel = instant.getAttribute("maglv") or "0"
    
    if int(instant.getAttribute("selftarget") or 0) or int(instant.getAttribute("needtarget") or 0):
        text = '\ninstant = spell.Spell("%s", "%s", icon=%s, group=%s)' % (instant.getAttribute("name"), instant.getAttribute("words"), instant.getAttribute("icon"), idToGroup(rune.getAttribute("groups").split(",")[0]))
        text += "\ninstant.require(mana=%s, level=%s, maglevel=%s, learned=%s, vocations=%s)" % (instant.getAttribute("mana") or "0", instant.getAttribute("lvl") or "0", mlevel, instant.getAttribute("needlearn") or "0", vocations)
        text += "\ninstant.cooldowns(%s, %s)" % (str(int(instant.getAttribute("exhaustion") or "0")/1000) or "0", str(int(instant.getAttribute("groups").split(",")[1])/1000))
        text += "\ninstant.targetEffect() # TODO"
        text += "\ninstant.effects() # TODO"
    else:
        text = '\ninstant = spell.Spell("%s", "%s", icon=%s, group=%s)' % (instant.getAttribute("name"), instant.getAttribute("words"), instant.getAttribute("icon"), idToGroup(rune.getAttribute("groups").split(",")[0]))
        text += "\ninstant.require(mana=%s, level=%s, maglevel=%s, learned=%s, vocations=%s)" % (instant.getAttribute("mana") or "0", instant.getAttribute("lvl") or "0", mlevel, instant.getAttribute("needlearn") or "0", vocations)
        text += "\ninstant.cooldowns(%s, %s)" % (str(int(instant.getAttribute("exhaustion") or "0")/1000) or "0", str(int(instant.getAttribute("groups").split(",")[1])/1000))
        text += "\ninstant.targetEffect() # TODO"
        text += "\ninstant.effects() # TODO"
        
    with open("spells/%s.py" % instant.getAttribute("name"), "wb") as f:
        f.write(text)