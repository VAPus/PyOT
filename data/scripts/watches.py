watches = 1728, 1729, 1730, 1731, 1873, 1874, 1875, 1876, 1877, 1881, 2036, 6091, 6092, 8187

@register('use', watches)
def useWatch(creature, **k):
    time = getTibiaTime()
    creature.lmessage("The time is %(hours)02d:%(minutes)02d." % {"hours": time[0], "minutes": time[1]})
