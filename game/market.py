import copy

Markets = {}

class Offer(object):
    def __init__(self, playerId, itemId, price, expire, amount, type=0):
        self.id = 0
        self.playerId = playerId
        self.itemId = itemId
        self.price = price
        self.expire = expire
        self.amount = amount
        self.counter = 0
        self.playerName = ""
        self.type = type
        self.marketId = 0
        self.expireCallback = None
        expireIn = expire - time.time()
        if expireIn <= 0:
            print("Expired offer")
        else:
            self.expireCallback = callLater(expireIn, self.expireOffer)

    @gen.coroutine
    def insert(self):
        self.id = yield sql.runOperationLastId("INSERT INTO `market_offers`(`world_id`, `market_id`, `player_id`, `item_id`, `amount`, `created`, `price`, `anonymous`, `type`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", config.worldId, self.marketId, self.playerId, self.itemId, self.amount, self.expire-config.marketOfferExpire, self.price, 1 if self.playerName == "Anonymous" else 0, self.type)
        self.counter = self.id & 0xFFFF

    def save(self):
        if not self.id:
            self.insert()
        else:
            sql.runOperation("UPDATE market_offers SET `player_id` = %s, `item_id` = %s, `amount` = %s, `price` = %s, `type` = %s WHERE `id` = %s", self.playerId, self.itemId, self.amount, self.price, self.type, self.id)

    def player(self):
        return loadPlayerById(self.playerId)

    @gen.coroutine
    def expireOffer(self):
        # Already expired?
        if self.type == 0: return

        # System offers?
        if not self.playerId: return

        player = yield self.player()
        if self.type == MARKET_OFFER_BUY:
            player.modifyBalance(self.price * self.amount)
        else:
            item = Item(self.itemId)
            count = self.amount
            depot = player.getDepot(player.marketDepotId)
            if player.depotMarketCache:
                try:
                    player.depotMarketCache[self.itemId] += self.amount
                except:
                    player.depotMarketCache[self.itemId] = self.amount

            if item.stackable:
                while count > 0:
                    depot.append(Item(self.itemId, min(100, count)))
                    count -= min(100, count)
            else:
                while count > 0:
                    depot.append(Item(self.itemId))
                    count -= 1

    @gen.coroutine
    def handleBuy(self, seller, amount):
        print("handleBuy")

        # Verify item.
        if not self.itemId in seller.depotMarketCache[seller.marketDepotId] or not seller.depotMarketCache[seller.marketDepotId][self.itemId] >= amount:
            return

        # Statistics
        Markets[self.marketId].buyTransaction(self, seller, amount)

        # Give seller money.
        seller.modifyBalance(amount * self.price)

        self.amount -= amount

        if self.amount == 0:
            self.type = 0

        self.save()

        # Take item.
        item = Item(self.itemId)
        depot = seller.getDepot(seller.marketDepotId)
        tamount = amount
        def takeItems(items):
            global tamount
            for item in copy.copy(items):
                if item.itemId == self.itemId:
                    orgCount = item.count
                    item.count = max(0, item.count - tamount)
                    tamount -= orgCount - item.count
                    if tamount == 0:
                        return
                if item.container:
                    takeItems(items)
                    if tamount == 0:
                        return

        takeItems(depot)

        # Give item
        # System offer. Then ignore it.
        if self.playerId != 0:
            player = yield self.player()
            depot = player.getDepot(player.marketDepotId)
            if item.stackable:
                while amount > 0:
                    depot.append(Item(self.itemId, min(100, amount)))
                    amount -= min(100, amount)
            else:
                while amount > 0:
                    depot.append(Item(self.itemId))
                    amount -= 1
        
    @gen.coroutine
    def handleSell(self, buyer, amount):
        print("handleSell")

        # Verify money.
        if not buyer.getBalance() >= amount * self.price:
            return

        Markets[self.marketId].buyTransaction(self, buyer, amount)

        # Take buyer money..
        price = (amount * self.price)
        buyer.modifyBalance(-price)

        self.amount -= amount

        if self.amount == 0:
            self.type = 0

        self.save()

        # Give buyer item.
        item = Item(self.itemId)
        depot = buyer.getDepot(buyer.marketDepotId)
        if item.stackable:
            while amount > 0:
                depot.append(Item(self.itemId, min(100, amount)))
                amount -= min(100, amount)
        else:
            while amount > 0:
                depot.append(Item(self.itemId))
                amount -= 1

        # Give seller money.
        # System, then ignore it.
        if self.playerId != 0:
            player = yield self.player()
            player.modifyBalance(price)

class Market(object):
    def __init__(self, id):
        self.id = id

        # Lookup cache.
        self.items = {} # itemId -> Count.

        # Offers.
        self._saleOffers = []
        self._buyOffers = []

        # Transaction statistics.
        self.buyStatistics = {} # itemId -> [count, total price, lowest price, highest price]
        self.saleStatistics = {}

    def addSaleOffer(self, offer):
        offer.marketId = self.id

        if offer.itemId in self.items:
            self.items[offer.itemId] += offer.amount or 1
        else:
            self.items[offer.itemId] = offer.amount or 1
        self._saleOffers.append(offer)

    def addBuyOffer(self, offer):
        offer.marketId = self.id

        self._buyOffers.append(offer)

    def buyOffers(self, player):
        entries = []
        for entry in self._buyOffers:
            if entry.playerId == player.data["id"] and entry.type == MARKET_OFFER_BUY:
                entries.append(entry)

        return entries

    def saleOffers(self, player):
        entries = []
        for entry in self._saleOffers:
            if entry.playerId == player.data["id"] and entry.type == MARKET_OFFER_SALE:
                entries.append(entry)

        return entries

    def getSaleOffers(self, itemId, exclude=None):
        entries = []
        for entry in self._saleOffers:
            if entry.itemId == itemId and entry.type == MARKET_OFFER_SALE and (exclude is None or entry.playerId != exclude):
                entries.append(entry)

        return entries

    def getBuyOffers(self, itemId, exclude=None):
        entries = []
        for entry in self._buyOffers:
            if entry.itemId == itemId and entry.type == MARKET_OFFER_BUY and (exclude is None or entry.playerId != exclude):
                entries.append(entry)

        return entries

    def findOffer(self, expire, counter):
        for entry in self._saleOffers:
            if entry.expire == expire and entry.counter == counter:
                return entry

        for entry in self._buyOffers:
            if entry.expire == expire and entry.counter == counter:
                return entry

    
    def removeOffer(self, offer):
        try:
            self._saleOffers.remove(offer)
            self.items[offer.itemId] -= offer.amount
        except:
            self._buyOffers.remove(offer)

        offer.expireOffer()
        offer.type = 0
        if offer.expireCallback:
            offer.expireCallback.cancel()
            offer.expireCallback = None    
        offer.save()


    def size(self):
        return len(self.items)

    def getItems(self):
        for itemId in self.items:
            yield (itemId, self.items[itemId])

    def saleTransaction(self, offer, who, count):
        try:
            transactions = self.saleStatistics[offer.itemId]
            transactions[0] += count
            transactions[1] += offer.price*count
            if offer.price < transactions[2]:
                transactions[2] = offer.price
            if offer.price > transactions[3]:
                transactions[3] = offer.price
        except:
            self.saleStatistics[offer.itemId] = [count, offer.price*count, offer.price, offer.price]

        # Insert SQL.
        sql.runOperation("INSERT INTO market_history(`offer_id`, `player_id`, `amount`, `time`, `type`) VALUES(%s, %s, %s, %s, %s)", offer.id, who.data["id"], count, time.time(), MARKET_OFFER_SALE)

    def buyTransaction(self, offer, who, count):
        try:
            transactions = self.buyStatistics[offer.itemId]
            transactions[0] += count
            transactions[1] += offer.price*count
            if offer.price < transactions[2]:
                transactions[2] = offer.price
            if offer.price > transactions[3]:
                transactions[3] = offer.price
        except:
            self.buyStatistics[offer.itemId] = [count, offer.price*count, offer.price, offer.price]

        # Insert SQL.
        sql.runOperation("INSERT INTO market_history(`offer_id`, `player_id`, `amount`, `time`, `type`) VALUES(%s, %s, %s, %s, %s)", offer.id, who.data["id"], count, time.time(), MARKET_OFFER_BUY)

@gen.coroutine
def load():
    global Markets
    
    expired = time.time() - config.marketOfferExpire
    x = yield sql.runQuery("SELECT mo.`id`, mo.`market_id`, mo.`player_id`, mo.`item_id`, mo.`amount`, mo.`created`, mo.`price`, mo.`anonymous`, mo.`type`, (SELECT `name` FROM players p WHERE p.`id` = mo.`player_id`) as `player_name` FROM `market_offers` mo WHERE mo.`world_id` = %s AND mo.`type` != 0", config.worldId)
    for entry in (x):
        if not entry["market_id"] in Markets:
            Markets[entry["market_id"]] = Market(entry["market_id"])
        market = Markets[entry["market_id"]]
        offer = Offer(entry["player_id"], entry["item_id"], entry["price"], entry["created"]+config.marketOfferExpire,entry["amount"], entry["type"])

        offer.id = entry["id"]
        offer.counter = offer.id & 0xFFFF

        if entry["anonymous"]:
            offer.playerName = "Anonymous"
        else:
            offer.playerName = entry["player_name"]

        if entry["created"] < expired:
            offer.expire()
            offer.type = 0
            offer.save()

        elif entry["type"] == MARKET_OFFER_SALE:
            market.addSaleOffer(offer)

        else:
            market.addBuyOffer(offer)

        # Statistics.
        for history in (yield sql.runQuery("SELECT o.`item_id`, h.`type`, COUNT(h.`id`) as `count`, SUM(o.`price`) * COUNT(h.`amount`) as `total`, MAX(o.`price`) as `max`, MIN(o.`price`) as `min` FROM `market_history` h, `market_offers` o WHERE o.`id` = h.`offer_id` GROUP BY o.`item_id`")):
            if history["type"] == MARKET_OFFER_BUY:
                market.buyStatistics[history['item_id']] = [history['count'], history['total'], history['min'], history['max']]
            else:
                market.saleStatistics[history['item_id']] = [history['count'], history['total'], history['min'], history['max']]

def newMarket(id):
    global Markets
    market = Market(id)
    
    Markets[id] = market

    return market

def getMarket(id):
    try:
        return Markets[id]
    except:
        return newMarket(id)


