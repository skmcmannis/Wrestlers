#Creates a graph of wrestlers and their rivalries (imported from an external file), then
# analyzes the graph to determine which wrestlers are 'babyfaces' and which are 'heels', as
# well as whether or not all rivalries are between a babyface and a heel. The program
# determines if all rivalries are legitimate (between a babyface and a heel), and outputs
# which wrestlers are babyfaces and which are heels
#Author: Shawn McMannis
#Last mod date: 5/12/19


from itertools import islice
from collections import deque


#Data type for vertices
class vertex(object):
    def __init__(self, name, ethic, index):
        self.name = name
        self.ethic = ethic
        self.color = "white"
        self.distance = 0
        self.parent = None
        self.adjacent = []
        self.index = index


#Performs a breadth-first search of the graph
def BFS(graph, source):

    #Queue to track nodes to vertices
    queue = deque([source])

    #While the queue is not empty
    while queue:
        #Pop the first vertex off of the queue
        current = queue.popleft()

        #Search the adjacency list of the current vertex
        for entry in current.adjacent:
            if adj[entry].color == "white":
                adj[entry].color = "grey"
                adj[entry].distance = current.distance + 1
                adj[entry].parent = current.index
                #Copy the edge to the list of edges
                tup = (entry, current.index)
                edges.append(tup)
                queue.append(adj[entry])
        
        #Add the edge to the list of edges (necessary here to capture the last edge)
        check1 = (entry, current.index)
        check2 = (current.index, entry)
        if check1 not in edges and check2 not in edges:
            edges.append(check1)

        current.color = "black"

#Analyzes the edges to verify that all rivalries are legitimate. Returns 1 if so, 0 otherwise
def CheckEdges(edges):

    #Process the edge list, one edge at a time
    for edge in edges:
        if adj[edge[0]].ethic == adj[edge[1]].ethic:
            return 0
    return 1


#main

#Adjacency list array
adj = []

#Tracks index when creating adjacency list array
ind = 0

#Stores the edges
edges = []

#Open import file
with open("wrestler2.txt", "r") as importFile:

    #Set number of wrestlers included in input file
    numWrestlers = list(islice(importFile, 1))
    numWrestlers = int(numWrestlers[0])

    #Slice wrestlers
    wrestlers = list(islice(importFile, numWrestlers))

    #Create the adjacency list
    for wrestler in wrestlers:
        wrestler = wrestler.strip()
        tempVert = vertex(wrestler, None, ind)
        ind = ind + 1
        adj.append(tempVert)
    
    #Set number of rivalries included in the input file
    numRivalries = list(islice(importFile, 1))
    numRivalries = int(numRivalries[0])

    #Slice rivalries
    rivalries = list(islice(importFile, numRivalries))

    for i in range(0, len(rivalries)):
        temp = rivalries[i].split()
        w1 = temp[0].split()
        w1 = str(w1[0])
        w2 = temp[1].split()
        w2 = str(w2[0])

        #Add rivalries to the adjacency list
        for j in range(0, len(adj)):

            #Add rivalry to first wrestler
            if w1 == adj[j].name:
                #Find the index in adj[] that corresponds to w2
                for k in range(0, len(adj)):
                    if w2 == adj[k].name:
                        adj[j].adjacent.append(k)

            #Add rivalry to second wrestler
            if w2 == adj[j].name:
                #Find the index in adj[] that corresponds to w1
                for k in range(0, len(adj)):
                    if w1 == adj[k].name:
                        adj[j].adjacent.append(k)

    #Run the BFS algorithm as long as there are remaining white vertices
    for p in range(0, len(adj)):
        if adj[p].color == "white":
            BFS(adj, adj[p])

    #Assign babyface/heel status based on distance
    for r in range(0, len(adj)):
        #Assign all even distances to babyface and odd distances to heel
        if adj[r].distance % 2 == 0:
            adj[r].ethic = "babyface"
        else:
            adj[r].ethic = "heel"

    #Analyze edges to ensure all rivalries are legitimate
    possible = CheckEdges(edges)

    #Produce terminal output
    if possible == 1:
        print("Yes")
        print("Babyfaces:"),
        for wrestler in adj:
            if wrestler.ethic == "babyface":
                print(wrestler.name),
        print("")
        print("Heels:"),
        for wrestler in adj:
            if wrestler.ethic == "heel":
                print(wrestler.name),
    else:
        print("Impossible")