@register("lookAt", ("creature", "item"))
@access("KICK")
# I think it's better to show the position in default window, instead of merging it with description and looking for it in server log.
def givePosition(creature, thing, **pos):
	if creature.getStorage("showpos") == 'enabled':
		obj = pos['position']
		# it might look preetier, but wouldn't be as functional.
		creature.message('Position: /goto %s, %s, %s' % (obj.x, obj.y, obj.z), MSG_STATUS_CONSOLE_ORANGE)
	return True

@register('talkaction', '/showpos')
@access("KICK")
def showToggle(creature, text):
	show = 'enabled'

	if creature.getStorage("showpos") == 'enabled':
		show = 'disabled'
	
	creature.setStorage("showpos", show)
	creature.message("Position showing has been %s" % show)
	
	return False