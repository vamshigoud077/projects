# -*- coding: utf-8 -*-
# function to print the puzzle in zig zag mode#
import math
def printThePuzzle(listpuzzle, display):
    for tile in listpuzzle:
        if(listpuzzle.index(tile) % 3 ==0):  
            print('\n')
        print(str(tile), end="      ") 
    
    if display:    
        print('\n')
        print('\t ||')
        print('\t ||')
        print('\t ||')
        print('\t \/')
        



