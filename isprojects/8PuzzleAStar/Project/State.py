# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 20:13:56 2019

@author: chaitanya
"""

class State:

    def __init__(self, state, parent, move, depth, cost, CumulativeCost):

        self.state = state

        self.parent = parent

        self.move = move

        self.depth = depth

        self.cost = cost

        self.CumulativeCost = CumulativeCost  # Cumulative cost is f(n) = g(n) + h(n)#

        if self.state:
            self.sequence = ''.join(str(e) for e in self.state)

    def __eq__(self, other):
        return self.sequence == other.sequence

    def __lt__(self, other):
       return self.CumulativeCost < other.CumulativeCost