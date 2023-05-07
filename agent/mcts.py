import copy
import time

from referee.game import HexDir
from gameboard import *


class Node:
    def __init__(self, action: Action, parent, colour):
        self.action, self.parent, self.children = action, parent, []
        self.colour = colour
        self.wins, self.playouts = 0, 0

    def expand_node(self, state):
        if not state.isTerminal():
            for direction in HexDir:
                child = Node(direction, self)
                self.children.append(child)

    def update(self, result):
        self.playouts += 1
        if result == win:
            self.wins += 1

    def is_leaf(self):
        return len(self.children)==0

    def has_parent(self):
        return self.parent is not None

def mcts(state: GameBoard, time): #AND SPACE !!!!!!!!!!!!!!!!
    root_node = Node(None, None, colour)
    cumulativeTime = 0
    startTime = time.time()
    while cumulativeTime < time:
        temp_node, temp_state = root_node, copy.deepcopy(state)
        while not temp_node.is_leaf():
            temp_node = tree_policy_child(temp_node)
            temp_state.updateBoard(temp_node.action)
        temp_node.expand_node(temp_state)
        temp_node = tree_policy_child(temp_node)
        while not temp_state.isTerminal():
            temp_state = simulation_policy_child(temp_state)
        result = evaluate(temp_state)
        while temp_node.has_parent():
            temp_node.update(result)
            temp_node = temp_node.parent
        endTime = time.time()
        cumulativeTime += endTime - startTime

    return best_move(root_node)

def tree_policy_child(root_node):
    return root_node.children[0]

def simulation_policy_child(state):

def evaluate(state):

def best_move(children):
