# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, constants, exceptions, board
from agent.gameboard import GameBoard

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Node:
    def __init__(self):
        self.children = {}

class Agent:
    # STATIC VARIABLES
    testBoard = board.Board() #  ASDF arbitrary rn
    testCounter = 0 # ASDF test

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        match self._color:
            case PlayerColor.RED:
                return SpawnAction(HexPos(3, 3))
            case PlayerColor.BLUE:
                # This is going to be invalid... BLUE never spawned!
                return SpawnAction(HexPos(3, 3))

        #return SpawnAction(self.randomSpawn())

        # match Agent.testCounter:
        #     case 0:  # red turn 1
        #         Agent.testBoard.apply_action(SpawnAction(HexPos(0, 0)))
        #         return SpawnAction(HexPos(0,0))
        #     case 1:  # blue turn 1
        #         Agent.testBoard.apply_action(SpawnAction(HexPos(3, 3)))
        #         return SpawnAction(HexPos(3,3))
        #     case 2:
        #         # testCoords = HexPos(0, 0)
        #         # print(f"\tSPREAD: {SpreadAction(testCoords, HexDir.Up).cell}")
        #         # print(f"\t({testCoords}) --> ({testCoords.__add__(HexDir.Up)})")
        #         # return SpreadAction(HexPos(0,0), HexDir.Up)
        #
        #         return SpawnAction(HexPos(0,1))
        #     case 3:
        #         return SpawnAction(HexPos(3,4))
        #     case 4:
        #         testCoords = HexPos(0,1)
        #         print(f"\tSPREAD: {SpreadAction(testCoords, HexDir.UpLeft).cell}")
        #         print(f"\t({testCoords}) --> ({testCoords.__add__(HexDir.UpLeft)})")
        #         return SpreadAction(HexPos(0,1), HexDir.UpLeft)
        #     case 5:
        #         return SpawnAction(HexPos(3,5))
        #     case 6:
        #         testCoords = HexPos(0,0)
        #         print(f"\tSPREAD: {SpreadAction(testCoords, HexDir.Up).cell}")
        #         print(f"\t({testCoords}) --> ({testCoords.__add__(HexDir.Up)})")
        #         return SpreadAction(HexPos(0,0), HexDir.Up)
        #     case 7: # intentional exception test
        #         self.testBoard.
        #     case _:  # else
        #         # print(f"\tAT (1,6): {HexPos.}")
        #         return SpawnAction(HexPos(0,0))  # intentional failure

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        print(f"\t\t\tACTION NUMBER: {Agent.testCounter}")
        Agent.testCounter += 1

        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                # update the board here bc it's already been tested by this point, so it's valid
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                # update the board here bc it's already been tested by this point, so it's valid
                pass


    def randomSpawn(self): # testing spawn
        randomR = random.randint(0, constants.BOARD_N-1)
        randomQ = random.randint(0, constants.BOARD_N-1)
        return HexPos(randomR, randomQ)
