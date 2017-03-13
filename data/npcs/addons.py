#I think this can be shorten :p
addons = genNPC("Addons", (152, 39, 122, 125, 37, 3, 2212))
addons.setWalkable(False)
outfits = ('Citizen', 'Hunter', 'Mage', 'Knight', 'Warrior', 'Summoner', 'Nobleman', 'Oriental', 'Wizard', 'Assassin', 'Beggar', 'Shaman', 'Barbarian', 'Druid', 'Pirate', 'Norseman', 'Jester', 'Brotherhood', 'Hunter', 'Yalaharian', 'Newly Wed', 'Warmaster', 'Wayfarer', 'Elementalist', 'Afflicted')
mounts = ('Black Sheep', 'Blazerbringer', 'Crystal Wolf', 'Draptor', 'Dromedary', 'King Scorpion', 'Kingly Deer', 'Midnight Panther', 'Mule', 'Racing Bird', 'Rapid Boar', 'Rented Horse', 'Shadow Draptor', 'Stampor', 'Tamed Panda', 'Tiger Slug', 'Tin Lizzard', 'Titanica', 'Undead Cavebear', 'Uniwheel', 'War Bear', 'Fire War Horse', 'Brown War Horse', 'Widow Queen')

addons.greet("Greetings %(playerName)s.. Will you help me? If you do, I'll reward you with nice outfits and mounts! Just say {addon} or {mount} if you don't know what to do.")
class Addon(game.npc.ClassAction):
    def action(self):
        self.on.onSaid('addon', self.test)
        self.on.onSaid('mount', self.mount)
    def test(self, npc, player):
        npc.sayTo(player, "I can give you citizen, hunter, knight, mage, nobleman, summoner, warrior, barbarian, druid, wizard, oriental, pirate, assassin,beggar, shaman, norseman, nighmare, jester, yalaharian and brotherhood outfits.")
        word = yield
        word =word.title()
        if word in outfits:
            player.addOutfit(word)
            player.addOutfitAddon(word, 1)
            player.addOutfitAddon(word, 2)
            npc.sayTo(player, "Now you can wear %s outfit"  % word)
            npc.sayTo(player, "You may say {addon} or {mount} to get another one or {bye}.")            
    def mount(self, npc, player):
        npc.sayTo(player, "I can give you Black Sheep, Blazerbringer, Crystal Wolf, Draptor, Dromedary, King Scorpion, Kingly Deer, Midnight Panther, Mule, Racing Bird, Rapid Boar, Rented Horse, Shadow Draptor, Stampor, Tamed Panda, Tiger Slug, Tin Lizzard, Titanica, Undead Cavebear, Uniwheel, War Bear, Fire War Horse, Brown War Horse and Widow Queen mounts.")
        word = yield
        word =word.title()
        if word in mounts:
            player.addMount(word.title())
            npc.sayTo(player, "You can now use %s" % word)        
            npc.sayTo(player, "You may say {addon} or {mount} to get another one or {bye}.")
addons.module(Addon)