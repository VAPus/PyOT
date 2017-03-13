@register("talkactionFirstWord", "/lang")
@register("talkactionFirstWord", "/language")

def setLang(creature, text):
	languages = { "norwegian": "nb_NO", "spanish": "es_ES", "english": "en_EN", "polish": "pl_PL" }
	text = text.strip().lower()

	if text in languages:
		creature.setLanguage(languages[text])
		creature.message("Your language has been changed to %s" % text, MSG_INFO_DESCR)
	else:
		s = "Available languages: "
		for key in languages.iterkeys():
			s += key + ", "
			
		creature.message("Unrecognized language. " + s[:-2] + ".", MSG_INFO_DESCR)
	return False