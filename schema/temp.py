import json
from sys import exit

x = open("/var/projects/tf2tags.com/tools/unusualSchema.json").read()

data = json.loads(x)
items = data["items"]

key = "X"
while True:
	key = raw_input("Key? ")
	if key == "":
		exit()

	dump = []
	for i in items:
		if i.get(key) and i.get(key) not in dump:
			dump.append(i[key])

	longest = 0
	for d in dump:
		print d
		if len(str(d)) > longest:
			longest = len(str(d))
			#print str(d)
	print len(dump), "results"
	print "Longest length:", longest
