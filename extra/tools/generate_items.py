#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Include the config
import sys
sys.path.append('../')
sys.path.append('../core')
import config

#assert sys.stdout.encoding == "UTF-8"
# Because mysql ain't that nice...
taken = set()

# Plural/article forms.
import inflect

INFLECT = inflect.engine()

# Items.
import game.item

# Hack.
from StringIO import StringIO
config.itemFile = "../"+config.itemFile
sys.stdout = StringIO()
game.item.loadItems()

import codecs
sys.stdout = codecs.getwriter('utf8')(sys.__stdout__)

for itemId in game.item.items:
    obj = game.item.items[itemId]
    if not "name" in obj: continue
    pin = False
    word = obj["name"]
        
    if word not in taken:
        print "# ID: %d" % itemId
        print 'msgid "%s"' % word
        pin = True

    plural = INFLECT.plural(word)
    if obj.get("flags", 0) & (1 << 7) and plural and plural != word and plural not in taken:
        pre = ""
        if not pin: 
            print "# This will bug!"
            pre = "# "
        print '%smsgid_plural "%s"' % (pre, plural)
        print '%smsgstr[0] ""' % pre
        print '%smsgstr[1] ""\n' % pre
        taken.add(plural)
        taken.add(word)

    elif pin:
        print 'msgstr ""\n'
        taken.add(word)
            
    if pin:
        article = INFLECT.a(word)
        if article:
            print 'msgid "%s"' % (article)
            print 'msgstr ""'
            print ""
       
    if "description" in obj and obj["description"] not in taken:
        print "# Description for ID: %d" % itemId
        print 'msgid "%s"' % obj["description"]
        print 'msgstr ""'
        print ""
        taken.add(obj["description"])

