"""this was a work in progress for one of T. Hoffman's problems"""

# To be command line input
graphStr = """ERI	NEW	WAR	CLA	PGH	SCR	STA	HAR	ALL	PHI
0	#	95	100	#	#	#	#	#	#
90	0	#	85	40	#	#	#	#	#
#	#	0	#	#	225	#	#	#	#
#	#	#	0	#	260	235	#	#	#
#	#	#	90	0	#	250	#	#	#
#	#	#	#	#	0	#	#	85	#
#	#	#	#	#	105	0	#	90	80
#	#	#	#	200	#	80	0	#	85
#	#	#	#	#	#	#	#	0	#
#	#	#	#	#	#	#	#	95	0"""

INITIAL = "ERI"
END = "PHI"

split = graphStr.split("\n")
names = split[0].split("\t")
length = len(names)
initial = names.index(INITIAL)
end = names.index(END)

graph = []
for x in range(1, length + 1):
    graph.append(split[x].split("\t"))


distances = [float("inf") for x in range(length)]
unvisited = [x for x in range(length)]

current = initial
currentDistance = 0
while (current != None):
    print "CURRENT:", current
    print "UNVISITED:", unvisited
    unvisited.remove(current)
    min = unvisited[0]
    minDistance = graph[current][min]
    for unv in unvisited:
        unvDistance = graph[current][unv]
        if unvDistance != '#':
            unvDistanceValue = int(unvDistance)
            print "DISTANCE to", unv, ":", unvDistanceValue
            if currentDistance + unvDistanceValue < distances[unv]:
                print currentDistance, "+", unvDistanceValue, " < ", distances[unv]
                distances[unv] = currentDistance + unvDistanceValue
        if distances[unv] < minDistance:
            min = unv
            minDistance = distances[min]
    currentDistance += minDistance
    if end not in unvisited or minDistance == float("inf"):
        current = None;
        print "done"
    else:
        current = min
        print current