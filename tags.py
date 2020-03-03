from collections import defaultdict

tagFile = open("ml-latest-small/tags.csv", "r")

tags = tagFile.read().strip().split("\n")

tags = tags[1:]

d = defaultdict(list)

for line in tags:
    l = line.split(",")
    userID = l[0]
    movieID = l[1]
    tag = l[2]

    d[movieID].append(tag)

for i in d:
    print(i, d[i])

tagFile.close()
