# Type /pos <whatever> for a list of saved locations.
# /pos save/goto/remove <name>

@register("talkactionFirstWord", "/pos")
@access("DEVELOPER")
def doPosMagic(creature, text):

	places = creature.getGlobalObject('Locations', {} )
	
	s = text.split(' ')
	if len(s) > 1:
		action, place = s[0], s[1]	
		if action == 'save':
			places[place] = creature.position.copy()
			creature.message('Location [%s] saved.' % place)
		elif action == 'goto':
			if place in places:
				creature.teleport(places[place])
				creature.magicEffect(EFFECT_TELEPORT)
			else:
				creature.message('There is no such place in database.')
		elif action == 'remove':
			if place in places:
				del places[place]
				creature.message('[%s] has been deleted from database.' % place)
			else:
				creature.message('There is no such place in database.')
	else:
		out = 'Available locations:'
		for k in places.iterkeys():
			out += ' [%s]' % k
		creature.message(out)
	
	creature.setGlobalObject('Locations', places)
	return False