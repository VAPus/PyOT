from generator import *

map = Map(640,640, ground=Item(4608)) # Make a 640x640 map filled with water

area = Area(150,150, ground=RSItem(106,108,109)) # Make a 150x150 area, with Random Static item (from 106 or 108)

monster = Monster('Kongra') # Make a Kongra
for x in xrange(0, 10):
    for y in xrange(0,10):
        area.add(90+(x*5), 90+(y*5), monster) # Put Kongra on this part of the area

area.border(0, Item(4632), Item(4634), Item(4633), Item(4635), northeast=Item(4638), northwest=Item(4639), southeast=Item(4636), southwest=Item(4637) )
area.border(1, Item(231), Item(231), Item(231), Item(231))
area.border(2, north=Item(833), south=Item(834), east=Item(835), west=Item(837), northeast=Item(843), northwest=Item(842), southwest=Item(844), southeast=Item(845), behavior=merger) 
map.merge(area, 40, 40) # Put the area into the map

map.compile() # Compile the map

