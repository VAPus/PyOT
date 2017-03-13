# Should we handle applying all flag bonuses here?
@register("login")

def onLogin(creature):
	# There should be a function to quickly check for group ie: creature.getAccessLevel()
	# then it's just:
	"""
	if creature.getAccessLevel() < 1:
		return True
	"""
	# ... and we can keep checking for flags of priviledged users.
	if creature.hasGroupFlag("SPEED"):
		creature.setSpeed(1500)
	return True