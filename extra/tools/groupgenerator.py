import json

groupFlags = ["CREATEITEM", "TELEPORT", "SETHOUSEOWNER", "SAVEALL", "SAVESELF", "SPAWN", "RAID", "HOUSE", "MANAGESERVER", "MODIFYMAP", "KICK", "RELOAD", "BAN", "MUTE", "DEVELOPER"]
groupFlags.extend(["PREMIUM", "SPELLS", "SPEAK", "SPEED", "MOVE_ITEMS", "LOOT", "INVISIBLE", "INFINITE_SOUL", "INFINITE_MANA", "INFINITE_HEALTH", "INFINITE_STAMINA", "ATTACK", "IGNORED_BY_CREATURES", "TALK_ORANGE", "TALK_RED", "IMMUNE", "NO_EXHAUST"])
groupId = input("Group ID (unique!): ")
groupName = input("Group name: ")

flags = []
print("Just click enter for NO, and any other key for YES.\n")

for flag in groupFlags:
    ok = input("%s ?" % flag)
    if ok:
        flags.append(flag)

print("INSERT INTO `groups` VALUES(%s, '%s', '%s')" % (groupId, groupName, json.dumps(flags)))