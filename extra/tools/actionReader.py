from xml.dom.minidom import parse

dom = parse("actions.xml")
searchFor = raw_input("Search For: ")
list = []
for element in dom.getElementsByTagName("action"):
	if element.getAttribute("script") == searchFor:
		list.append(int(element.getAttribute("itemid")))

print list
