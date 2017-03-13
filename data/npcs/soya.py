soya = genNPC("Soya", (139, 132, 79, 97, 132, 0, 2212))
soya.setWalkable(False)

shop = soya.module('shop')
shop.offer('royal helmet', 5000, 10000)