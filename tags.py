'''
    From 'ml-latest-small/tags.csv', create json file 'tags.json' with all movieIDs
    and corresponding descriptive tags

    eg. 12345 ['funny', 'cute', 'charming']
'''

from collections import defaultdict

tagFile = open("ml-latest-small/tags.csv", "r")
output = open("tags.json", "w")

tags = tagFile.read().strip().split("\n")

tags = tags[1:]

d = defaultdict(list)

for line in tags:
    l = line.split(",")
    userID = l[0]
    movieID = l[1]
    tag = l[2]

    d[movieID].append(tag)

output.write("{")

for i in d:
    s = i + ": " + str(d[i]) + ",\n"
    output.write(s)
    #print(i, d[i])

output.write("}\n")

tagFile.close()
output.close()
