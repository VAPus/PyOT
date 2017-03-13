AltSystemTest = genNPC("AltSystemTest", (130, 39, 122, 125, 37, 0, 2212), "AltSystemTest the test char")
AltSystemTest.setWalkable(False)

playersWhoGotFreeIcecream = set()
# This below is somethat that more or less utilize ALL features in the simple spaek system. I use it as a test. Below is a commented out more realistic example for a small talk i suppose. Want it to look nicer, put the functions out as defs instead of lambdas.
def giveIcecream(player, **k):
    player.say("Yum!")
    playersWhoGotFreeIcecream.add(player)
    
AltSystemTest.speakTree({(lambda player, **k: player not in playersWhoGotFreeIcecream, "Hello, what do you want?", "Why are you back, I already gave you icecream! Ow well, what do you want this time?"):
    {"icecream":
        {"What flavour?":
            {"chocolate": ("Here you go!", giveIcecream ),
            "!": "We don't serve that, sorry!",
            }
        }
    }
}, "We serve icecream you know! :)")

"""
AltSystemTest.speakTree({"Hello, what do you want?":
    {"icecream":
        {"What flavour?":
            {"chocolate": ("Here you go!", lambda player, **k: player.say("Yum!") ),
            "!": "We don't serve that, sorry!",
            }
        }
    }
})"""