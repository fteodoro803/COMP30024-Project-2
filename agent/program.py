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
    board = GameBoard()
    turnCount = 1

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
        # print(f"\n====================================ITERATION {Agent.turnCount}====================================")
        time = referee['time_remaining']
        # print(f"referee={time}")

        # Maximising Time
        if time >= 4:  # if time runs out, don't run MCTS
            mcts = MCTS()
            bestMove = mcts.search(self.board)
            return bestMove
        else:

            return random.choice(Agent.board.getLegalMoves())[1]


    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """

        match action:
            case SpawnAction(cell):
                Agent.board.updateBoard(color, action)

            case SpreadAction(cell, direction):
                Agent.board.updateBoard(color, action)

        Agent.turnCount += 1

