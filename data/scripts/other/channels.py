import game.chat

# Register channels
# Note: This is NOT reload safe, well, thats a TODO

game.chat.openChannel("Counselor", 2)
game.chat.openChannel("World Chat", 3)
game.chat.openChannel("Staff", 4, public=False)
game.chat.openChannel("Advertising", 5)
game.chat.openChannel("Advertising-Rookgaard", 6)
game.chat.openChannel("Help", 7)
game.chat.openChannel("Private", 0xFFFF, public=False) # Also special