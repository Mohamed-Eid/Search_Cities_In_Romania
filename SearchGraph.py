import sys

# SearchGraph.py
#
# Implementation of iterative deepening search for use in finding optimal routes
# between locations in a graph. In the graph to be searched, nodes have names
# (e.g. city names for a map).
#
# An undirected graph is passed in as a text file (first command line argument). 
#
# Usage: python SearchGraph.py graphFile startLocation endLocation
# 
# Author: Richard Zanibbi, RIT, Nov. 2011
# Edited By: Pavan Prabhakar Bhat (pxb8715@rit.edu)

def read_graph(filename):
    """Read in edges of a graph represented one per line,
	using the format: srcStateName destStateName"""
    edges = {}

    inFile = open(filename)
    for line in inFile:
        roadInfo = line.split()

        # Skip blank lines, read in contents from non-empty lines.
        if (len(roadInfo) > 0):
            srcCity = roadInfo[0]
            destCity = roadInfo[1]

            if srcCity in edges:
                edges[srcCity] = edges[srcCity] + [destCity]
            else:
                edges[srcCity] = [destCity]

            if destCity in edges:
                edges[destCity] = edges[destCity] + [srcCity]
            else:
                edges[destCity] = [srcCity]

    return edges


######################################
# Add functions for search, output
# etc. here
######################################

# Global variables
# Contains string of visited states
visitedPaths = ""
# Contains final path from source to destination
finalPath = []
# Contains the total level of depth for each iteration
countOfDepth = 0
# Contains the source state
tempVar = ""


def iterativeDFS(source, destination, maxDepth, edges):
    '''
    Outer function to perform iterative deepening search.
    :param source: Starting state
    :param destination: Destination state
    :param maxDepth: Maximum number of depths that IDS can perform
    :param edges: List of edges in the map
    :return: List of final path
    '''
    global countOfDepth, visitedPaths, tempVar
    tempVar = source

    # Check to perform if the source and destination is not in edges list
    if source not in edges.keys() or destination not in edges.keys():
        finalPath.append('FAIL')
        return finalPath

    for limit in range(maxDepth):
        # visited = source
        # print(source)
        countOfDepth = limit
        if depthLimitSearch(source, destination, limit, edges):
            # prints all the visited states
            print(visitedPaths)
            finalPath.append(tempVar)
            finalPath.reverse()
            return finalPath
    # State not found. Hence, Fail.
    finalPath.append("FAIL")
    return finalPath


def depthLimitSearch(source, destination, limit, edges):
    '''
    Inner function that performs a depth limited search
    :param source: Current starting state from the edge list
    :param destination: Final destination state
    :param limit: Current depth to which DLS needs to be performed
    :param edges: List of edges in the map
    :return: Boolean True or False
    '''
    global countOfDepth, visitedPaths, tempVar, finalPath

    # Indents the visited states and appends the paths in visitedPaths
    if (countOfDepth-limit) <= 0:
        visitedPaths += '\n' + source
    else:
        visitedPaths += ('\n' + '\t' * (countOfDepth - limit)) + source

    # Checks if the the final destination has been reached
    if source == destination:
        return True

    # Checks whether all the depths have been traversed for the current iteration
    if limit < 1:
        return False

    # Temporary variable to remove the backward link from the edge-list data structure
    temp = []

    # Iterates over all connected states of a current state for a given depth
    for adjacentNode in edges[source]:
        # Removes the backward connection to visited nodes for eg.  connection between Arad - Zerind will remove Zering - Arad from the edges list
        temp = edges[adjacentNode]
        if source in temp:
            temp.remove(source)
            edges[adjacentNode] = temp
        #     Performs a recursive call to the DLS function with limit - 1
        if depthLimitSearch(adjacentNode, destination, limit - 1, edges):
            # Appends the final path once the destination state is reached
            finalPath.append(adjacentNode)
            return True
    return False


#########################
# Main program
#########################
def main():
    if len(sys.argv) != 4:
        print('Usage: python SearchGraph.py graphFilename startNode goalNode')
        return
    else:
        # Create a dictionary (i.e. associative array, implemented as a hash
        # table) for edges in the map file, and define start and end states for
        # the search. Each dictionary entry key is a string for a location,
        # associated with a list of strings for the adjacent states (cities) in
        # the state space.
        print("Loading graph: " + sys.argv[1])
        edges = {}
        edges = read_graph(sys.argv[1])
        start = sys.argv[2]
        goal = sys.argv[3]
        print("  done.\n")

        # Comment out the following lines to hide the graph description.
        print("-- Adjacent Cities (Edge Dictionary Data) ------------------------")
        for location in edges.keys():
            s = '  ' + location + ':\n     '
            s = s + str(edges[location])
            print(s)

        if not start in edges.keys():
            print("Start location is not in the graph.")
        else:

            print('')
            print('-- States Visited ----------------')
            # program will need to show the search tree - prints the visited states while the function iterativeDFS is executing
            solution = iterativeDFS(start, goal, 1000, edges)
            print('')
            print('--  Solution for: ' + start + ' to ' + goal + '-------------------')
            print(solution)  # program will need to provide solution path or indicate failure.
            print('')

# Execute the main program.
main()
