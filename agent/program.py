# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, constants, exceptions, board
from .gameboard import GameBoard
from .mcts import MCTS

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Agent:
    # STATIC VARIABLES
    testBoard = GameBoard()
    testTurnCounter = 1 # ASDF test

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
        print(f"\n====================================ITERATION {Agent.testTurnCounter}====================================")
        mcts = MCTS()
        timeLimit = 10

        if (Agent.testTurnCounter <= 343):  # stupidity test
            bestMove = mcts.search(self.testBoard, timeLimit)
            return bestMove
        else:
            return


    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """

        match action:
            case SpawnAction(cell):
                # print(f"Testing: {color} Spawn at {cell}")
                # update the board here bc it's already been tested by this point, so it's valid
                Agent.testBoard.updateBoard(color, action)

                # pass
            case SpreadAction(cell, direction):
                # print(f"Testing: {color} Spread from {cell}, {direction}")
                # update the board here bc it's already been tested by this point, so it's valid
                Agent.testBoard.updateBoard(color, action)

                # pass

        # Test Prints
        #print(Agent.testBoard.board)  # our representation of the board
        tiles = [(key, value) for key, value in Agent.testBoard.board.items() if value.colour is not None]  # printing locations with a colour on it
        # print(tiles)
        # print(Agent.testBoard.getWinner())
        Agent.testTurnCounter += 1

