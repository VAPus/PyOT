SERVER_VERSION = "1.0.0-alpha4"

### Light ###
#: No light.
LIGHTLEVEL_NONE = 0

#: Light with a touch.
LIGHTLEVEL_TORCH = 7

#: Full light within a area.
LIGHTLEVEL_FULL = 27

#: Light over the entier world.
LIGHTLEVEL_WORLD = 255

### Light colors ###
#: Dark light.
LIGHTCOLOR_NONE = 0

#: Default, orange light.
LIGHTCOLOR_DEFAULT = 206 # Orange

#: White light.
LIGHTCOLOR_WHITE = 215

### Slots ###
SLOT_WHEREEVER = 0
SLOT_FIRST = 1
#: Inventory slot for the head.
SLOT_HEAD = SLOT_WHEREEVER
#: Inventory slot for the necklace.
SLOT_NECKLACE = SLOT_FIRST
#: Inventory slot for the backpack.
SLOT_BACKPACK = 2
#: Inventory slot for the armor.
SLOT_ARMOR = 3
#: Inventory slot for the right hand.
SLOT_LEFT = 4
#: Inventory slot for the left hand.
SLOT_RIGHT = 5 
#: Inventory slot for legs.
SLOT_LEGS = 6
#: Inventory slot for feets.
SLOT_FEET = 7
#: Inventory slot for the rings.
SLOT_RING = 8
#: Inventory slot for the ammonition.
SLOT_AMMO = 9
#what is 10? are 10-12 correct?
SLOT_PURSE = 10

SLOT_LAST = SLOT_PURSE

SLOT_CLIENT_FIRST = 1
SLOT_CLIENT_SLOTS = 10 # We don't send purse

# Skills
SKILL_FIRST = 0
#: Skill ID for fisting.
SKILL_FIST = SKILL_FIRST
#: Skill ID for clubs.
SKILL_CLUB = 1
#: Skill ID for swords.
SKILL_SWORD = 2
#: Skill ID for axes.
SKILL_AXE = 3
#: Skill ID for distance weapons.
SKILL_DISTANCE = 4
#: Skill ID for shielding.
SKILL_SHIELD = 5
#: Skill ID for fishing.
SKILL_FISH = 6
SKILL_ROD = 6 # Hu? TFS hack.
SKILL_LAST = SKILL_FISH

#: For skill callback
MAGIC_LEVEL = 7

# Chat
# BASE PROTOCOL ENUMS:
_MSG_NONE                       = 0x00
_MSG_SPEAK_SAY                  = 0x01
_MSG_SPEAK_WHISPER              = 0x02
_MSG_SPEAK_YELL                 = 0x03
_MSG_PRIVATE_FROM               = 0x04
_MSG_PRIVATE_TO                 = 0x05
_MSG_CHANNEL_MANAGEMENT         = 0x06
_MSG_CHANNEL                    = 0x07
_MSG_CHANNEL_HIGHLIGHT          = 0x08
_MSG_SPEAK_SPELL                = 0x09
_MSG_NPC_FROM                   = 0x0A
_MSG_NPC_TO                     = 0x0B
_MSG_GAMEMASTER_BROADCAST       = 0x0C
_MSG_GAMEMASTER_CHANNEL         = 0x0D
_MSG_GAMEMASTER_PRIVATE_FROM    = 0x0E
_MSG_GAMEMASTER_PRIVATE_TO      = 0x0F
_MSG_SPEAK_MONSTER_SAY          = 0x22
_MSG_SPEAK_MONSTER_YELL         = 0x23
_MSG_STATUS_CONSOLE_RED         = 0x0C # Red message in the console
_MSG_STATUS_DEFAULT             = 0x10 # White message at the bottom of the game window and in the console
_MSG_STATUS_WARNING             = 0x11 # Red message in game window and in the console
_MSG_EVENT_ADVANCE              = 0x12 # White message in game window and in the console
_MSG_STATUS_SMALL               = 0x13 # White message at the bottom of the game window"
_MSG_INFO_DESCR                 = 0x14 # Green message in game window and in the console
_MSG_DAMAGE_DEALT               = 0x15
_MSG_DAMAGE_RECEIVED            = 0x16
_MSG_HEALED                     = 0x17
_MSG_EXPERIENCE                 = 0x18
_MSG_DAMAGE_OTHERS              = 0x19
_MSG_HEALED_OTHERS              = 0x1A
_MSG_EXPERIENCE_OTHERS          = 0x1B
_MSG_EVENT_DEFAULT              = 0x1C # White message at the bottom of the game window and in the console
_MSG_LOOT                       = 0x1D
_MSG_TRADE_NPC                  = 0x1E
_MSG_CHANNEL_GUILD              = 0x1F # SPEAK_CHANNEL_W(?) guild messages.
_MSG_PARTY_MANAGEMENT           = 0x20
_MSG_PARTY                      = 0x21
_MSG_EVENT_ORANGE               = 0x22 # Orange message in the console
_MSG_STATUS_CONSOLE_ORANGE      = 0x23 # Orange message in the console
_MSG_REPORT                     = 0x24
_MSG_HOTKEY_USE                 = 0x25
_MSG_TUTORIAL_HINT              = 0x26
_MSG_STATUS_CONSOLE_BLUE        = 0xFF

# SCRIPT ALIAS ENUMS
MSG_NONE                       = '_MSG_NONE'
MSG_SPEAK_SAY                  = '_MSG_SPEAK_SAY'
MSG_SPEAK_WHISPER              = '_MSG_SPEAK_WHISPER'
MSG_SPEAK_YELL                 = '_MSG_SPEAK_YELL'
MSG_PRIVATE_FROM               = '_MSG_PRIVATE_FROM'
MSG_PRIVATE_TO                 = '_MSG_PRIVATE_TO'
MSG_CHANNEL_MANAGEMENT         = '_MSG_CHANNEL_MANAGEMENT'
MSG_CHANNEL                    = '_MSG_CHANNEL'
MSG_CHANNEL_HIGHLIGHT          = '_MSG_CHANNEL_HIGHLIGHT'
MSG_SPEAK_SPELL                = '_MSG_SPEAK_SPELL'
MSG_NPC_FROM                   = '_MSG_NPC_FROM'
MSG_NPC_TO                     = '_MSG_NPC_TO'
MSG_GAMEMASTER_BROADCAST       = '_MSG_GAMEMASTER_BROADCAST'
MSG_GAMEMASTER_CHANNEL         = '_MSG_GAMEMASTER_CHANNEL'
MSG_GAMEMASTER_PRIVATE_FROM    = '_MSG_GAMEMASTER_PRIVATE_FROM'
MSG_GAMEMASTER_PRIVATE_TO      = '_MSG_GAMEMASTER_PRIVATE_TO'
MSG_SPEAK_MONSTER_SAY          = '_MSG_SPEAK_MONSTER_SAY'
MSG_SPEAK_MONSTER_YELL         = '_MSG_SPEAK_MONSTER_YELL'
MSG_STATUS_CONSOLE_RED         = '_MSG_STATUS_CONSOLE_RED'
MSG_STATUS_DEFAULT             = '_MSG_STATUS_DEFAULT '
MSG_STATUS_WARNING             = '_MSG_STATUS_WARNING'
MSG_EVENT_ADVANCE              = '_MSG_EVENT_ADVANCE'
MSG_STATUS_SMALL               = '_MSG_STATUS_SMALL'
MSG_INFO_DESCR                 = '_MSG_INFO_DESCR'
MSG_DAMAGE_DEALT               = '_MSG_DAMAGE_DEALT'
MSG_DAMAGE_RECEIVED            = '_MSG_DAMAGE_RECEIVED'
MSG_HEALED                     = '_MSG_HEALED'
MSG_EXPERIENCE                 = '_MSG_EXPERIENCE'
MSG_DAMAGE_OTHERS              = '_MSG_DAMAGE_OTHERS'
MSG_HEALED_OTHERS              = '_MSG_HEALED_OTHERS'
MSG_EXPERIENCE_OTHERS          = '_MSG_EXPERIENCE_OTHERS'
MSG_EVENT_DEFAULT              = '_MSG_EVENT_DEFAULT'
MSG_LOOT                       = '_MSG_LOOT'
MSG_TRADE_NPC                  = '_MSG_TRADE_NPC'
MSG_CHANNEL_GUILD              = '_MSG_CHANNEL_GUILD'
MSG_PARTY_MANAGEMENT           = '_MSG_PARTY_MANAGEMENT'
MSG_PARTY                      = '_MSG_PARTY'
MSG_EVENT_ORANGE               = '_MSG_EVENT_ORANGE'
MSG_STATUS_CONSOLE_ORANGE      = '_MSG_STATUS_CONSOLE_ORANGE'
MSG_REPORT                     = '_MSG_REPORT'
MSG_HOTKEY_USE                 = '_MSG_HOTKEY_USE'
MSG_TUTORIAL_HINT              = '_MSG_TUTORIAL_HINT'
MSG_STATUS_CONSOLE_BLUE        = '_MSG_STATUS_CONSOLE_BLUE'

# Colors
COLOR_BLACK                     = 0
COLOR_BLUE                      = 5
COLOR_GREEN                     = 18
COLOR_LIGHTGREEN                = 66
COLOR_DARKBROWN                 = 78
COLOR_LIGHTBLUE                 = 89
COLOR_MAYABLUE                  = 95
COLOR_DARKRED                   = 108
COLOR_DARKPURPLE                = 112
COLOR_BROWN                     = 120
COLOR_GREY                      = 129
COLOR_TEAL                      = 143
COLOR_DARKPINK                  = 152
COLOR_PURPLE                    = 154
COLOR_DARKORANGE                = 156
COLOR_RED                       = 180
COLOR_PINK                      = 190
COLOR_ORANGE                    = 192
COLOR_DARKYELLOW                = 205
COLOR_YELLOW                    = 210
COLOR_WHITE                     = 215

# Fluids
FLUID_EMPTY                     = 0x00
FLUID_BLUE                      = 0x01
FLUID_PURPLE                    = 0x02
FLUID_BROWN                     = 0x03
FLUID_RED                       = 0x05
FLUID_GREEN                     = 0x06
FLUID_YELLOW                    = 0x08
FLUID_WHITE                     = 0x09

FLUID_NONE                      = FLUID_EMPTY
FLUID_WATER                     = FLUID_BLUE
FLUID_BLOOD                     = FLUID_RED
FLUID_BEER                      = FLUID_BROWN
FLUID_SLIME                     = FLUID_GREEN
FLUID_LEMONADE                  = FLUID_YELLOW
FLUID_MILK                      = FLUID_WHITE
FLUID_MANA                      = FLUID_PURPLE

FLUID_LIFE                      = FLUID_RED + 8
FLUID_OIL                       = FLUID_BROWN + 8
FLUID_URINE                     = FLUID_YELLOW + 8
FLUID_COCONUTMILK               = FLUID_WHITE + 8
FLUID_WINE                      = FLUID_PURPLE + 8

FLUID_MUD                       = FLUID_BROWN + 16
FLUID_FRUITJUICE                = FLUID_YELLOW + 16

FLUID_LAVA                      = FLUID_RED + 24
FLUID_RUM                       = FLUID_BROWN + 24
FLUID_SWAMP                     = FLUID_GREEN + 24

FLUID_TEA                       = FLUID_BROWN + 32
FLUID_MEAD                      = FLUID_BROWN + 40

# Compatibility stuff
FLUID_ENERGY                    = FLUID_NONE
FLUID_UNDEAD                    = FLUID_NONE
FLUID_FIRE                      = FLUID_NONE

# Floorchange
FLOORCHANGE_DOWN                = 0x00
FLOORCHANGE_UP                  = 0x01


# Directions
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
SOUTHWEST = 4
SOUTHEAST = 5
NORTHWEST = 6
NORTHEAST = 7

# Splashes
SMALLSPLASH = 2019
SMALLSPLASHES = (2019, 2020, 2021)
FULLSPLASH = 2016
FULLSPLASHES = (2016, 2017, 2018)

# Damage types
PHYSICAL = 0 #damage from physical spells, is reduce by physical percent only
FIRE = 1
EARTH = 2
ENERGY = 3
ICE = 4
HOLY = 5
DEATH = 6
DROWN = 7
MELEE = 8 #damage from a melee and distance weapoans?, is reduce by physical percent + armor/shielding
DISTANCE = 9
LIFEDRAIN = 10
MANADRAIN = 11

# Monster attack types
#MELEE = 0
TARGET_SPELL = 1
SELF_SPELL = 2

# TargetTypes
TARGET_DIRECTION = 0
TARGET_CASTER_AREA = 1
TARGET_TARGET_AREA = 2

# Magic effects
EFFECT_DRAWBLOOD = 1
EFFECT_LOSEENERGY = 2
EFFECT_POFF = 3
EFFECT_BLOCKHIT = 4
EFFECT_EXPLOSIONAREA = 5
EFFECT_EXPLOSIONHIT = 6
EFFECT_FIREAREA = 7
EFFECT_YELLOW_RINGS = 8
EFFECT_GREEN_RINGS = 9
EFFECT_HITAREA = 10
EFFECT_TELEPORT = 11
EFFECT_ENERGYHIT = 12
EFFECT_MAGIC_BLUE = 13
EFFECT_MAGIC_RED = 14
EFFECT_MAGIC_GREEN = 15
EFFECT_HITBYFIRE = 16
EFFECT_HITBYPOISON = 17
EFFECT_MORTAREA = 18
EFFECT_SOUND_GREEN = 19
EFFECT_SOUND_RED = 20
EFFECT_POISONAREA = 21
EFFECT_SOUND_YELLOW = 22
EFFECT_SOUND_PURPLE = 23
EFFECT_SOUND_BLUE = 24
EFFECT_SOUND_WHITE = 25
EFFECT_BUBBLES = 26
EFFECT_CRAPS = 27
EFFECT_GIFT_WRAPS = 28
EFFECT_FIREWORK_YELLOW = 29
EFFECT_FIREWORK_RED = 30
EFFECT_FIREWORK_BLUE = 31
EFFECT_STUN = 32
EFFECT_SLEEP = 33
EFFECT_WATERCREATURE = 34
EFFECT_GROUNDSHAKER = 35
EFFECT_HEARTS = 36
EFFECT_FIREATTACK = 37
EFFECT_ENERGYAREA = 38
EFFECT_SMALLCLOUDS = 39
EFFECT_HOLYDAMAGE = 40
EFFECT_BIGCLOUDS = 41
EFFECT_ICEAREA = 42
EFFECT_ICETORNADO = 43
EFFECT_ICEATTACK = 44
EFFECT_STONES = 45
EFFECT_SMALLPLANTS = 46
EFFECT_CARNIPHILA = 47
EFFECT_PURPLEENERGY = 48
EFFECT_YELLOWENERGY = 49
EFFECT_HOLYAREA = 50
EFFECT_BIGPLANTS = 51
EFFECT_CAKE = 52
EFFECT_GIANTICE = 53
EFFECT_WATERSPLASH = 54
EFFECT_PLANTATTACK = 55
EFFECT_TUTORIALARROW = 56
EFFECT_TUTORIALSQUARE = 57
EFFECT_MIRRORHORIZONTAL = 58
EFFECT_MIRRORVERTICAL = 59
EFFECT_SKULLHORIZONTAL = 60
EFFECT_SKULLVERTICAL = 61
EFFECT_ASSASSIN = 62
EFFECT_STEPSHORIZONTAL = 63
EFFECT_BLOODYSTEPS = 64
EFFECT_STEPSVERTICAL = 65
EFFECT_YALAHARIGHOST = 66
EFFECT_BATS = 67
EFFECT_SMOKE = 68
EFFECT_INSECTS = 69
EFFECT_DRAGONHEAD = 70
EFFECT_ORCSHAMAN = 71
EFFECT_ORCSHAMAN_FIRE = 72
EFFECT_THUNDER = 73
EFFECT_FERUMBRAS = 74
EFFECT_CONFETTIHORIZONTAL = 75
EFFECT_CONFETTIVERTICAL = 76
EFFECT_NONE = 0

# Animation
ANIMATION_SPEAR = 1
ANIMATION_BOLT = 2
ANIMATION_ARROW = 3
ANIMATION_FIRE = 4
ANIMATION_ENERGY = 5
ANIMATION_POISONARROW = 6
ANIMATION_BURSTARROW = 7
ANIMATION_THROWINGSTAR = 8
ANIMATION_THROWINGKNIFE = 9
ANIMATION_SMALLSTONE = 10
ANIMATION_DEATH = 11
ANIMATION_LARGEROCK = 12
ANIMATION_SNOWBALL = 13
ANIMATION_POWERBOLT = 14
ANIMATION_POISON = 15
ANIMATION_INFERNALBOLT = 16
ANIMATION_HUNTINGSPEAR = 17
ANIMATION_ENCHANTEDSPEAR = 18
ANIMATION_REDSTAR = 19
ANIMATION_GREENSTAR = 20
ANIMATION_ROYALSPEAR = 21
ANIMATION_SNIPERARROW = 22
ANIMATION_ONYXARROW = 23
ANIMATION_PIERCINGBOLT = 24
ANIMATION_WHIRLWINDSWORD = 25
ANIMATION_WHIRLWINDAXE = 26
ANIMATION_WHIRLWINDCLUB = 27
ANIMATION_ETHEREALSPEAR = 28
ANIMATION_ICE = 29
ANIMATION_EARTH = 30
ANIMATION_HOLY = 31
ANIMATION_SUDDENDEATH = 32
ANIMATION_FLASHARROW = 33
ANIMATION_FLAMMINGARROW = 34
ANIMATION_SHIVERARROW = 35
ANIMATION_ENERGYBALL = 36
ANIMATION_SMALLICE = 37
ANIMATION_SMALLHOLY = 38
ANIMATION_SMALLEARTH = 39
ANIMATION_EARTHARROW = 40
ANIMATION_EXPLOSION = 41
ANIMATION_CAKE = 42
ANIMATION_TARSALARROW = 44
ANIMATION_VORTEXBOLT = 45
ANIMATION_PRISMATICBOLT = 48
ANIMATION_CRYSTALLINEARROW = 49
ANIMATION_DRILLBOLT = 50
ANIMATION_ENVENOMEDARROW = 51
ANIMATION_NONE = 0

# Item types
ITEM_TYPE_NONE        = 0
ITEM_TYPE_DEPOT       = 1
ITEM_TYPE_MAILBOX     = 2
ITEM_TYPE_TRASHHOLDER = 3
ITEM_TYPE_CONTAINER   = 4
ITEM_TYPE_DOOR        = 5
ITEM_TYPE_MAGICFIELD  = 6
ITEM_TYPE_TELEPORT    = 7
ITEM_TYPE_BED         = 8

# Modes
OFFENSIVE = 1
BALANCED = 2
DEFENSIVE = 3

STAND = 0
CHASE = 1

SECURE = 1

# Attack strategy
TARGETSTRATEGY_NONE = 0
TARGETSTRATEGY_NORMAL = 1
TARGETSTRATEGY_LOWEST = 2
TARGETSTRATEGY_HIGHEST = 3

# Money map, id => value. Have to be ordered from highest to lowest, otherwise it will be bugs
# TODO Move to money loading
MONEY_MAP = ((2160, 10000), (2152, 100), (2148, 1))

# Mailstuff
ITEM_PARCEL           = 2595
ITEM_PARCEL_STAMPED   = 2596
ITEM_LETTER           = 2597
ITEM_LETTER_STAMPED   = 2598
ITEM_LABEL            = 2599

# Shields
SHIELD_NONE = 0
SHIELD_MEMBER_INVITE = 1
SHIELD_LEADER_INVITE = 2
SHIELD_MEMBER = 3
SHIELD_LEADER = 4

SHIELD_MEMBER_SHAREDEXP = 5
SHIELD_LEADER_SHAREDEXP = 6
SHIELD_MEMBER_NOSHAREDEXP_BLINK = 7
SHIELD_LEADER_NOSHAREDEXP_BLINK = 8
SHIELD_MEMBER_NOSHAREDEXP = 9
SHIELD_LEADER_NOSHAREDEXP = 10

# Emblem
EMBLEM_NONE = 0
EMBLEM_GREEN = 1
EMBLEM_RED = 2
EMBLEM_BLUE = 3

# Skull
SKULL_NONE = 0
SKULL_YELLOW = 1
SKULL_GREEN = 2
SKULL_WHITE = 3
SKULL_RED = 4
SKULL_BLACK = 5
SKULL_ORANGE = 6

SKULL_JUSTIFIED = (SKULL_WHITE, SKULL_BLACK, SKULL_RED)
SKULL_FIGHTBACK = (SKULL_YELLOW, SKULL_ORANGE)

# Gender
MALE = 0
FEMALE = 1

# Conditions
CONDITION_NONE = 0,
CONDITION_POISON = 1 << 0
CONDITION_FIRE = 1 << 1
CONDITION_ENERGY = 1 << 2
CONDITION_DRUNK = 1 << 3
CONDITION_MANASHIELD = 1 << 4
CONDITION_PARALYZE = 1 << 5
CONDITION_HASTE = 1 << 6
CONDITION_INFIGHT = 1 << 7
CONDITION_DROWN = 1 << 8
CONDITION_FREEZING = 1 << 9
CONDITION_DAZZLED = 1 << 10
CONDITION_CURSED = 1 << 11
CONDITION_BUFF = 1 << 12
CONDITION_PZBLOCK = 1 << 13
CONDITION_PROTECTIONZONE = 1 << 14
CONDITION_BLEED = 1 << 15
CONDITION_HUNGRY = 1 << 16

CONDITION_PHYSICAL = "PHYSICAL"
CONDITION_OUTFIT = "OUTFIT"
CONDITION_INVISIBLE = "INVISIBLE"
CONDITION_LIGHT = "LIGHT"
CONDITION_EXHAUST = "EXHAUST"
CONDITION_REGENERATEHEALTH = "REGENERATEHEALTH"
CONDITION_REGENERATEMANA = "REGENERATIEMANA"
CONDITION_SOUL = "SOUL"
CONDITION_MUTED = "MUTED"
CONDITION_ATTRIBUTES = "ATTRIBUTES"
CONDITION_PACIFIED = "PACIFIED"
CONDITION_GAMEMASTER = "GAMEMASTER"
CONDITION_HUNTING = "HUNTING"

# Conditon flags
CONDITION_IGNORE = 0
CONDITION_LATER = 1
CONDITION_ADD = 2
CONDITION_MODIFY = 3
CONDITION_REPLACE = 4


#spell information
TARGET_AREA = 0
TARGET_SELF = 1
TARGET_TARGET = 2
TARGET_TARGETSELF = 3
TARGET_TARGETONLY = 4

ATTACK_GROUP = 1
HEALING_GROUP = 2
SUPPORT_GROUP = 3
SPECIAL_GROUP = 4

AREA_ONE = (0,0),

#strike
AREA_WAVE1 = TARGET_DIRECTION, (0,)

AREA_WAVE2 = TARGET_DIRECTION, (0,), \
(-1, 0, 1)

AREA_WAVE4 = TARGET_DIRECTION, (0,), \
(-1, 0, 1), \
(-1, 0, 1), \
(-2, -1, 0, 1, 2)

AREA_WAVE42 = TARGET_DIRECTION, (0,), \
(0,), \
(-1, 0, 1), \
(-1, 0, 1)

AREA_WAVE5 = TARGET_DIRECTION, (0,), \
(0,), \
(-1, 0, 1), \
(-1, 0, 1), \
(-1, 0, 1)

AREA_WAVE6 = TARGET_DIRECTION, (0,), \
(0,), \
(-1, 0, 1), \
(-1, 0, 1), \
(-1, 0, 1), \
(-2, -1, 0, 1, 2)

AREA_WAVE7 = TARGET_DIRECTION, (0,), \
(0,), \
(-1, 0, 1), \
(-1, 0, 1), \
(-1, 0, 1), \
(-2, -1, 0, 1, 2), \
(-2, -1, 0, 1, 2)

AREA_WAVE72 = TARGET_DIRECTION, (0,), \
(-1, 0, 1), \
(-1, 0, 1), \
(-2, -1, 0, 1, 2), \
(-2, -1, 0, 1, 2), \
(-3, -2, -1, 0, 1, 2, 3), \
(-3, -2, -1, 0, 1, 2, 3) 
#(-3, -2, -1, 0, 1, 2, 3)  does it go this far?

AREA_WAVE8 = TARGET_DIRECTION, (0,), \
(0,), \
(-1, 0, 1), \
(-1, 0, 1), \
(-1, 0, 1), \
(-2, -1, 0, 1, 2), \
(-2, -1, 0, 1, 2), \
(-2, -1, 0, 1, 2)

AREA_BEAM4 = TARGET_DIRECTION,(0,), (0,), (0,), (0,)

AREA_BEAM7 = TARGET_DIRECTION,(0,), (0,), (0,), (0,), (0,), (0,), (0,)

AREA_CIRCLE = TARGET_CASTER_AREA, (-1, 1), (0, -1), (0, 1)

AREA_CIRCLE2 = TARGET_CASTER_AREA, (-1, -2), (0, -2), (1, -2), \
(-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), \
(-2, 0), (-1, 0), (1, 0), (2, 0), \
(-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), \
(-1, 2), (0, 2), (1, 2)

AREA_CIRCLE3 = TARGET_CASTER_AREA, (-1, -3), (0, -3), (1, -3), \
(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), \
(-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), \
(-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3,0), \
(-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), \
(-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), \
(-1, 3), (0, 3), (1, 3)

AREA_CROSS = TARGET_CASTER_AREA, (0, -1), \
(-1, 0), (1, 0), \
(0, 1)

AREA_SQUARE = TARGET_CASTER_AREA, (-1, -1), (0, -1), (1, -1), \
(-1, 0), (1, 0), \
(-1, 1), (0, 1), (1, 1)

AREA_WALL = TARGET_DIRECTION, (-2, -1, 1, 2)

#may be incorrect
AREA_DIAGONALWALL = TARGET_DIRECTION, (-2, -1), \
(-1,), \
(-1, 0, 1), \
(1,), \
(1, 2)

AREA_UE5X5 = TARGET_CASTER_AREA, (0, -5), \
(-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4), \
(-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3), \
(-4, -2), (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2), \
(-4, -1), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), \
(-5, 0), (-4, 0), (-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3,0), (4, 0), (5, 0), \
(-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), \
(-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), \
(-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3), \
(-2, 4), (-1, 4), (0, 4), (1, 4), (2, 4), \
(0, 5)

AREA_UE6X6 = TARGET_CASTER_AREA, (0, -6), \
(-1, -5), (0, -5), (1, -5), \
(-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4), \
(-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3), \
(-4, -2), (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2), \
(-5, -1), (-4, -1), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1), \
(-6, 0), (-5, 0), (-4, 0), (-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3,0), (4, 0), (5, 0), (6, 0), \
(-5, 1), (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), \
(-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), \
(-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3), \
(-2, 4), (-1, 4), (0, 4), (1, 4), (2, 4), \
(-1, 5), (0, 5), (1, 5), \
(0, 6)

# Same as otserv use i suppose. Optimize them?
TILEFLAGS_NONE = 0
TILEFLAGS_PROTECTIONZONE = 1 << 0
TILEFLAGS_TRASHED = 1 << 1
TILEFLAGS_OPTIONALZONE = 1 << 2
TILEFLAGS_NOLOGOUT = 1 << 3
TILEFLAGS_HARDCOREZONE = 1 << 4
TILEFLAGS_STACKED = 1 << 5

# Some for convertions
INVENTORY_POSITION = 0xFFFF

# Some enums for ignore
FIRE_FIELDS = 1487, 1488, 1489, 1492, 1493, 1494, 1500, 1501, 1502, 10986, 10987, 10988
ENERGY_FIELDS = 1491, 1495, 1504, 10547
POISON_FIELDS = 1490, 1496, 2285, 12334, 12335

# Guild permission ids
GUILD_MEMBER = 1
GUILD_SUBLEADER = 1 << 1
GUILD_LEADER = 1 << 2
GUILD_HOUSE = 1 << 3
GUILD_MODERATE_HOUSE = 1 << 4
GUILD_WITHDRAW_MONEY = 1 << 5
GUILD_MANAGE_WARS = 1 << 6
GUILD_INVITE = 1 << 7
GUILD_PROMOTE = 1 << 8 # Upto own permissions except GUILD_PROMOTE unless LEADER.

# Special channel ids.
CHANNEL_OFFSET = 10
CHANNEL_PARTY = 1
CHANNEL_GUILD = 0

# Bans
BAN_ACCOUNT = 0
BAN_PLAYER = 1
BAN_IP = 2

# Dynamic container
DYNAMIC_CONTAINER = 0xFFFE

# Market.
MARKET_OFFER_OVER = 0
MARKET_OFFER_SALE = 1
MARKET_OFFER_BUY = 2

# Huamn corpse
HUMAN_CORPSE = 3058
