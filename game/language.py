# Setup
import os, os.path, glob
import gettext
import config
import builtins


__all__ = []
LANGUAGES = {}

if config.enableTranslations:
    for mod in glob.glob(config.dataDirectory + "/language/*.mo"):
        modm = mod.split(os.sep)[-1].replace('.mo', '')
        if modm == "__init__":
            continue
        
        __all__.append(modm)

    # Initialize GNUTranslations (regular gettext is singel language only :()
    for language in __all__:
        LANGUAGES[language] = gettext.GNUTranslations(open(config.dataDirectory + "/language/%s.mo" % language, 'rb'))


# Functions
if LANGUAGES:
    def _l(creature, message):
        if type(creature) == str:
            return LANGUAGES[creature].gettext(message)

        return creature.l(message)

    def _lp(creature, singular, plural, n):
        if type(creature) == str:
            return LANGUAGES[creature].ngettext(singular, plural, n)
            
        return creature.lp(singular, plural, n)

    def _lc(creature, context, message):
        # We don't need to do this harder then the documentation say it is :p
        if type(creature) == str:
            # Must be done outside of the call to prevent error.
            return LANGUAGES[creature].gettext("%s\x04%s" % (context, message))

        return creature.lc(context, message)
        
        
    def _lcp(creature, context, singular, plural, n):
        # We don't need to do this harder then the documentation say it is :p
        # Note: Must be inlined, otherwise error in auto generation :(
        if type(creature) == str:
            return LANGUAGES[creature].ngettext("%s\x04%s" % (context, singular), "%s\x04%s" % (context, plural), n)

        return creature.lcp(context, singular, plural, n)
            

else:
    _l = lambda c,m: m
    _lp = lambda c,s,p,n: p if n != 1 else s
    _lc = lambda cr,c,m: m
    _lcp = lambda cr,c,s,p,n: p if n != 1 else s

builtins._l = _l
builtins._lc = _lc
builtins._lp = _lp
builtins._lcp = _lcp
builtins._ = lambda m: m
