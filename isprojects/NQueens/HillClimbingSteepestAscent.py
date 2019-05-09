import random
from copy import deepcopy
import numpy as np

import sys


sys.setrecursionlimit(10000)


# method to return the heuristic values such as number of attacks for any given state of the board#
def attack_heuristic(board):
    h = 0
    for i in range(0, len(board[0])):
        for j in range(0, len(board[0])):
            if board[i][j] == 1:

                x = i
                while x < len(board[0]):
                    x = x + 1
                    if x < len(board[0]):
                        if board[x][j] == 1:
                            h = h+1

                x = i
                y = j
                while y < len(board[0]) and x < len(board[0]):
                    y = y + 1
                    x = x + 1
                    if y < len(board[0]) and x < len(board[0]):
                        if board[x][y] == 1:
                            h = h+1

                x = i
                y = j
                while 0 <= y and x < len(board[0]):
                    y = y - 1
                    x = x + 1
                    if 0 <= y and x < len(board[0]):
                        if board[x][y] == 1:
                            h = h + 1

    return h


def GenerateChildBoards(h_board):
    heuristic_board = np.copy(h_board)
    for i in range(0, len(h_board[0])):
        for j in range(0, len(h_board[0])):
            temp_board = np.copy(h_board)
            if h_board[i][j] == 0:
                for k in range(0, len(h_board[0])):
                    if h_board[i][k] == 1:
                        temp_board[i][k] = 0
                        break
                temp_board[i][j] = 1
                h_val = attack_heuristic(temp_board)
                heuristic_board[i][j] = h_val
    return heuristic_board

# move all the queens to the possible moves and return the succesor childs#
def MoveTheQueen(current_board, counter):
    parent_h = attack_heuristic(current_board)
    if parent_h != 0:
        successor_board_heuristic = GenerateChildBoards(current_board)
        len_board = len(current_board[0]) * len(current_board[0])
        list_h_s = np.zeros((len_board - len(current_board[0])), np.dtype(int))
        k = 0
        for i in range(0, len(current_board[0])):
            for j in range(0, len(current_board[0])):
                if current_board[i][j] == 0:
                    list_h_s[k] = successor_board_heuristic[i][j]
                    k = k + 1
        child_board = np.copy(current_board)
        value = list_h_s.min()
        if value < parent_h:
            row, col = generateRandomIndex(current_board, successor_board_heuristic, value)
            row = int(row)
            col = int(col)
            itr = len(current_board[0]) - 1
            while itr >= 0:
                if current_board[row][itr] == 1:
                    child_board[row][itr] = 0
                    child_board[row][col] = 1
                itr = itr - 1
            print("Move")
            print(child_board)
            return MoveTheQueen(child_board, counter + 1)
        else:
            print("Fail")
            return counter, "F"
    else:
        print("Reached Goal")
        return counter, "G"

# generate random integers. #
def generateRandomIndex(current_board, successor_board_heuristic, value):
    dict_index = {}
    k = 0
    for i in range(0, len(current_board[0])):
        for j in range(0, len(current_board[0])):
            if current_board[i][j] == 0:
                if successor_board_heuristic[i][j] == value:
                    dict_index[k] = str(i) + "," + str(j)
                    k = k + 1

    ind = random.randint(0, len(dict_index) - 1)
    s = str(dict_index.get(ind))
    index = s.split(",")
    return index[0], index[1]

# init programme to create the board game and initiate the board with values. #
def CreateBoardGame():
    board_size = int(input("Enter number of queens: "))
    x = 0
    ExecutionCycle = int(input("Enter the number of times to run the board : "))
    # board_size = 8
    
    board = np.zeros((board_size, board_size), np.dtype(int))
    board = np.reshape(board, (-1, board_size))
    counter_avg = ExecutionCycle
    f_counter = 0
    g_counter = 0
    f_step_count = 0
    g_step_count = 0
    while counter_avg > 0:
        for i in range(0, board_size):
            y = random.randint(0, board_size - 1)
            for j in range(0, board_size):
                if j == y:
                    board[i][j] = 1
                else:
                    board[i][j] = 0
        current_board = np.copy(board)
        print("Initial Board")
        print(current_board)
        steps_count, goal_test = MoveTheQueen(current_board, 1)
        if goal_test == "F":
            f_counter = f_counter + 1
            f_step_count = steps_count + f_step_count
        else:
            g_counter = g_counter + 1
            g_step_count = steps_count + g_step_count
        counter_avg = counter_avg - 1
    print("---------Rates--------- ")
    print("Failure rate: ", round((f_counter/ExecutionCycle) * 100, 2), " Success rate: ", round((g_counter/ExecutionCycle) * 100, 2), " total ", ExecutionCycle)
    print("--------Average Steps count--------- ")
    if f_counter != 0:
        print("Failure average steps: ", str(round((f_step_count / f_counter), 2)))
    else:
        print("Failure average steps: ", 0)
    if g_counter != 0:
        print("Success average steps: ", str(round((g_step_count / g_counter), 2)))
    else:
        print("Success average steps: ", 0)

class NQueenHillClimbing:
   CreateBoardGame()