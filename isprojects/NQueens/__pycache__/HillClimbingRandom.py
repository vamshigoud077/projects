# -*- coding: utf-8 -*-

import random
from copy import deepcopy
import numpy as np
import sys


sys.setrecursionlimit(10000)


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


def h_board_creator(h_board):
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


def movement_queen(current_board, counter, restart_counter, b_size, fail_count):
    # print("Counter ", counter)
    parent_h = attack_heuristic(current_board)
    # print("Parent Heuristic ", parent_h)
    if parent_h != 0:
        successor_board_heuristic = h_board_creator(current_board)
        # print("Successor Board ")
        # print(successor_board_heuristic)
        len_board = len(current_board[0]) * len(current_board[0])
        list_h_s = np.zeros((len_board - len(current_board[0])), np.dtype(int))
        k = 0
        for i in range(0, len(current_board[0])):
            for j in range(0, len(current_board[0])):
                if current_board[i][j] == 0:
                    list_h_s[k] = successor_board_heuristic[i][j]
                    k = k + 1

        # print("list h ", list_h_s)
        child_board = np.copy(current_board)
        value = list_h_s.min()
        # print("value ", value)

        if value < parent_h:
            row, col = random_index_h(current_board, successor_board_heuristic, value)
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
            return movement_queen(child_board, counter + 1, restart_counter, b_size, fail_count)
        else:
            restart_board = np.zeros((b_size, b_size), np.dtype(int))
            restart_board = np.reshape(restart_board, (-1, b_size))
            for i in range(0, b_size):
                y = random.randint(0, b_size - 1)
                for j in range(0, b_size):
                    if j == y:
                        restart_board[i][j] = 1
                    else:
                        restart_board[i][j] = 0
            print("Restart Board")
            print(restart_board)
            return movement_queen(restart_board, counter + 1, restart_counter + 1, b_size, fail_count + 1)
    else:
        print("Reached Goal")
        return counter, "G", restart_counter, fail_count


def random_index_h(current_board, successor_board_heuristic, value):
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
    # print("random", ind)
    index = s.split(",")
    return index[0], index[1]


class NQueenHillClimbing:
    bsize = int(input("Enter size of board: "))
    x = 0
    total = int(input("Enter the number of times to calculate average : "))
    # bsize = 8
    board = np.zeros((bsize, bsize), np.dtype(int))
    board = np.reshape(board, (-1, bsize))
    counter_avg = total
    f_counter = 0
    g_counter = 0
    f_step_count = 0
    g_step_count = 0
    r_count = 0
    r_step_count = 0
    fail_counter = 0
    while counter_avg > 0:
        for i in range(0, bsize):
            y = random.randint(0, bsize - 1)
            for j in range(0, bsize):
                if j == y:
                    board[i][j] = 1
                else:
                    board[i][j] = 0
        current_board = np.copy(board)
        print("Initial Board")
        print(current_board)
        steps_count, goal_test, restart_count, fails = movement_queen(current_board, 1, 0, bsize, fail_counter)
        if goal_test == "G":
            g_counter = g_counter + 1
            g_step_count = steps_count + g_step_count
            r_count = r_count + 1
            r_step_count = restart_count + r_step_count
            f_step_count = fails + f_step_count
        else:
            f_counter = f_counter + 1
        counter_avg = counter_avg - 1
    print("Rates: ")
    print("Failure rate: ", round((f_counter / total) * 100, 2), " Success rate: ", round((g_counter / total) * 100, 2),
          " total ", total)
    print("Average Steps count: ")
    if f_counter != 0:
        print("Failure average steps: ", round((f_step_count / f_counter), 2))
    else:
        print("Failure average steps: ", 0)
    if g_counter != 0:
        print("Success average steps: ", round((g_step_count / g_counter), 2))
    else:
        print("Success average steps: ", 0)
    print("Average Random Restarts steps ", round((r_step_count/r_count), 2))