Banker = genNPC("Banker", (132, 39, 122, 125, 37, 3, 2212), "Banker.")
Banker.setWalkable(False)

Banker.greet("Hello %(playerName)s. What can I do for you today?")

def conversation(npc, player):
    command = (yield)
    balance = player.getBalance()
    if command == "withdraw":
        npc.sayTo(player, "How much?")
        amount = (yield)
        try:
            amount = int(amount)
        except:
            npc.sayTo(player, "Sorry, I don't understand!")
            return
        
        if amount < 0:
            npc.sayTo(player, "You can't withdraw a negative amount, deposit instead")
            return
        if amount > balance:
            npc.sayTo(player, "You don't have that much!")
            return
        
        balance -= amount
        npc.sayTo(player, "Alright, your new balance is %d gold" % balance)
        player.setBalance(balance)
        player.addMoney(amount)
        
    elif command == "balance":
        npc.sayTo(player, "You currently got %d gold on your account!" % balance)
        
    elif command == "deposit":
        onHandBalance = player.getMoney()
        npc.sayTo(player, "How much?")
        amount = (yield)
        try:
            amount = int(amount)
        except:
            npc.sayTo(player, "Sorry, I don't understand!")
            return
        
        if amount < 0:
            npc.sayTo(player, "You can't deposit a negative amount, withdraw instead")
            return
        if amount > onHandBalance:
            npc.sayTo(player, "You don't have that much on you!")
            return
        
        player.removeMoney(amount)
        balance += amount
        npc.sayTo(player, "Alright, your new balance is %d gold" % balance)
        player.setBalance(balance)
    else:
        npc.sayTo(player, "Ehm, I don't understand. Try again!")

Banker.module(conversation)