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
        # print(f"\n====================================ITERATION {Agent.testTurnCounter}====================================")
        # print(referee['time_remaining'])
        # print(referee)
        mcts = MCTS()
        timeLimit = 30
        # print(f"total={Agent.testBoard.getPlayerPower(PlayerColor.RED)+Agent.testBoard.getPlayerPower(PlayerColor.BLUE)} | redPower={Agent.testBoard.getPlayerPower(PlayerColor.RED)}, bluePower={Agent.testBoard.getPlayerPower(PlayerColor.BLUE)}")

        # Random Spawn and Spread Together
        # location = self.randomSpawn()
        # if self.testTurnCounter >= 50:  # Random Spread at end
        #     location, direction = self.randomSpread()
        #     return SpreadAction(location, direction)
        # return SpawnAction(location)

        # if (Agent.testTurnCounter <= 343):  # full gameplay test
        #     if (self._color == PlayerColor.RED and Agent.testTurnCounter < 42):
        #         return SpawnAction(self.randomSpawn())
        #     if self._color == PlayerColor.RED:
        #         bestMove = mcts.search(self.testBoard, timeLimit)
        #         return bestMove
        #     if self._color == PlayerColor.BLUE and Agent.testTurnCounter < 20:
        #         return SpawnAction(self.randomSpawn())
        #
        #     else:
        #         # action = self.randomSpread()
        #         # return SpreadAction(action[0], action[1])
        #         bestMove = mcts.search(self.testBoard, timeLimit)
        #         return bestMove
        #     # bestMove = mcts.search(self.testBoard, timeLimit)
        #     # return bestMove

        # if (Agent.testTurnCounter <= 343):  # stupidity test
        #     if (Agent.testTurnCounter < 40):
        #         return SpawnAction(self.randomSpawn())
        #     elif (self._color == PlayerColor.RED):
        #         bestMove = mcts.search(self.testBoard, timeLimit)
        #         return bestMove
        #     else:
        #         return SpawnAction(self.randomSpawn())
        # else:
        #     return


        #LMS
        if (Agent.testTurnCounter < 10 and PlayerColor.RED):
            return SpawnAction(self.randomSpawn())
        else:
            bestMove = mcts.search(self.testBoard, timeLimit)
            return bestMove


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

    def randomSpawn(self) -> HexPos:
        # get Locations where Board is empty
        emptyLocations = [key for key, value in Agent.testBoard.board.items() if value.colour is None]  # https://note.nkmk.me/en/python-dict-get-key-from-value/

        if not emptyLocations:
            return HexPos(0, 0)  # intentionally wrong. no more valid spaces

        randomLocation = emptyLocations[random.randint(0, len(emptyLocations)-1)]  # gets random location from empty location list

        return HexPos(randomLocation[0], randomLocation[1])

    def randomSpread(self) -> (HexPos, HexDir):
        # get Locations of current Player
        locations = [key for key, value in Agent.testBoard.board.items() if value.colour is self._color]
        # print(locations)

        # choose random Location to Move
        randomLocation = locations[random.randint(0, len(locations)-1)]  # gets random location from empty location list
        # print(randomLocation)

        # choose random Direction
        randomDirection = random.choice(list(HexDir))
        # print(randomDirection)

        randomHex = HexPos(randomLocation[0], randomLocation[1])

        return randomHex, randomDirection


