# -*- coding: utf-8 -*-
from Utilities import printThePuzzle
from State import State
import math
import heapq
from heapq import heappush, heappop, heapify

initial_state = list()
goal_state = list()
goal_node = State
max_frontier_size = 0
max_search_depth = 0
explored = list()
frontier_heap = list()
heap_dictionary = {}
nodes_expanded = 0
nodes_generated = 0
SolvedPuzzle = list()
puzzle_len = 9
puzzle_side = 3

moves = list()

#print initial welcome messages and take the user input either Manhattan or Misplaced #
def printInitialMessages():
    print ("\n")
    print (" *********************** 8 puzzle *********************** ")
    print(" Choose the heuristic ")
    print("\n")
    print(" 1. Manhattan")
    print(" 2. Misplaced")
    
#function to print the manhattan heuristic function#
def manhattanHeuristic(node_list):
    TotalManhattanDistance = 0
    
    for iter in range(0,len(node_list)):
        presenttile = node_list[iter]     
        present_x = math.floor((iter)/3)
        present_y = (iter)%3     
        goal_index = goal_state.index(presenttile)     
        goal_x = math.floor(goal_index/3)
        goal_y = goal_index%3     
        TotalManhattanDistance = TotalManhattanDistance  + abs(present_x - goal_x) + abs(present_y  - goal_y)    
       
    return TotalManhattanDistance

#function to print the heuristic misplaced tiles#
def misplacedTiles(node_list):
    misplacedTiles = 0 # initializing misplaced tiles to zero # 
    
    for iter in range(0,len(node_list)):        
        if (node_list[iter] == 0):
            continue
        elif(node_list[iter] != goal_state[iter]):
            misplacedTiles = misplacedTiles + 1
            
    return misplacedTiles

#function to backtrace and find the solution from the goal state#
def backtrace():

    global moves, SolvedPuzzle
    current_node = goal_node
    SolvedPuzzle.append(current_node)
    while initial_state != current_node.state:

        if current_node.move == 1:
            movement = 'Up'
        elif current_node.move == 2:
            movement = 'Down'
        elif current_node.move == 3:
            movement = 'Left'
        else:
            movement = 'Right'

        moves.insert(0, movement)
        current_node = current_node.parent
        SolvedPuzzle.append(current_node)

    return moves

#function to print the solution#
def printTheSolution():
    global nodes_generated
    nodes_generated =  len(frontier_heap) + len(explored)
    backtrace()
    print("\n")
    print("\npath_to_goal: " + str(moves))
    print("\ncost_of_path: " + str(len(moves)))
    print("\nnodes_explored: " + str(nodes_expanded))
    print("\nnumber of elements left in frontier: " + str(len(frontier_heap)))
    print("\nsearch_depth: " + str(goal_node.depth))
    print("\nnodes generated: " + str(nodes_generated))
    
    SolvedPuzzle.reverse()
    
    for node in SolvedPuzzle:
        if SolvedPuzzle.index(node) == len(SolvedPuzzle) - 1:
            printThePuzzle(node.state, False)
        else:
            printThePuzzle(node.state, True)

    print("\n")
    print(" **************** GOAL STATE FOUND !!!!!! *************")
    
#function to execute AStarAlgorithm.#
def SearchAStar():
    
    global max_frontier_size, goal_node, max_search_depth,  nodes_expanded


    heuristicfunction = function_map[input_heuristic]
    
    cumulativeheuristic = heuristicfunction(initial_state) # heuristic function to generate f(n) value of root #
    
    StartNode = State(initial_state, None, None, 0, 0, cumulativeheuristic) #create start node#
    heapq.heapify(frontier_heap) #heapify the heap#
    heapq.heappush(frontier_heap, StartNode)  #push the start node to the heap#
    
    heap_dictionary[StartNode.sequence] = StartNode #Store dictionary of sequence and nodes#
    
    while frontier_heap:
        heapq.heapify(frontier_heap)
        popped_node = heapq.heappop(frontier_heap) #pop the least cost one#
        explored.append(popped_node)
        nodes_expanded += 1

        
        #goal test#
        if popped_node.state == goal_state:
            goal_node = popped_node #set the popped node to goal node# 
            return frontier_heap
        
        #continue if the goal test fails#
        #expand and store the nodes in negbors#
        neighbors = expand(popped_node)
        
        for neighbor in neighbors:
            neighbor.CumulativeCost = heuristicfunction(neighbor.state) + neighbor.cost
            
            #check if they are explored#
            if neighbor not in explored:
                if neighbor not in frontier_heap:
                    heapq.heappush(frontier_heap, neighbor) #push to frontier#
                    heap_dictionary[neighbor.sequence] = neighbor #push to the dictionary#    
                    #increase the depth#
                    if neighbor.depth > max_search_depth:
                        max_search_depth += 1
                    
                
                elif neighbor in frontier_heap and neighbor.CumulativeCost < frontier_heap[frontier_heap.index(neighbor)].CumulativeCost:
                    frontier_heap[frontier_heap.index(neighbor)] = neighbor #replace the highest cost with the least one#
                    heap_dictionary[neighbor.sequence] = neighbor
                    heapq.heapify(frontier_heap) #rearrange#
                    
                    #increase the depth#
                    if neighbor.depth > max_search_depth:
                        max_search_depth += 1
                    
        heapq.heapify(frontier_heap)
        
        if len(frontier_heap) > max_frontier_size:
            max_frontier_size = len(frontier_heap)
   
   
# functioon to the read puzzle values from the user#
def readTheBoard():
    global input_heuristic
    input_heuristic = input("\n Enter the Choice...")
    
    input_sequence = input("\n Enter the Start State \n")
    
    startState = input_sequence.split(",")
    for element in startState:
        initial_state.append(int(element)) # append initial state #
    
    goal_sequence = input("\n Enter the Goal State \n")
    goalState = goal_sequence.split(",")        
    for element in goalState:
        goal_state.append(int(element))       
    
    print("\nStart State  \n")
    printThePuzzle(initial_state, False)   
    print("\n\nGoal State  \n")
    printThePuzzle(goal_state, False)

#function to expand the nodes with all the possible movies and return neighbors#
def expand(node):

    neighbors = list()

    neighbors.append(State(move(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))

    nodes = [neighbor for neighbor in neighbors if neighbor.state]

    return nodes

#function to move the node and check the boundary of the puzzle.#
def move(state, position):

    new_state = state[:]

    index = new_state.index(0)

    if position == 1:  # move the tile up

        if index not in range(0, puzzle_side):

            temp = new_state[index - puzzle_side]
            new_state[index - puzzle_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 2:  # move the tile down

        if index not in range(puzzle_len - puzzle_side, puzzle_len):

            temp = new_state[index + puzzle_side]
            new_state[index + puzzle_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 3:  # move the tile left

        if index not in range(0, puzzle_len, puzzle_side):

            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 4:  # move the tile right

        if index not in range(puzzle_side - 1, puzzle_len, puzzle_side):

            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None


def main():
    printInitialMessages()
    readTheBoard()
    SearchAStar()
    printTheSolution()
    
    
function_map = {
    '1':manhattanHeuristic,
    '2':misplacedTiles
}


if __name__ == '__main__':
    main()


