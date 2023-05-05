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

        # Random Spread
        match Agent.testTurnCounter:
            case 1:
                return SpawnAction(HexPos(0, 0))
            case 2:
                return SpawnAction(HexPos(3, 3))
            case 3:
                return SpawnAction(HexPos(0, 1))
            case 4:
                return SpawnAction(HexPos(3, 4))
            case _:
                location, direction = self.randomSpread()
                print(location, direction)
                return SpreadAction(location, direction)

        # # Random Spawn
        # location = self.randomSpawn()
        #
        # # Random Spread at end
        # if self.testTurnCounter == 49:
        #     return SpreadAction()
        #
        # return SpawnAction(location)


    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        # print(f"\t\t\tACTION NUMBER: {Agent.testTurnCounter}")
        # print(Agent.testBoard.board)
        Agent.testTurnCounter += 1

        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                # update the board here bc it's already been tested by this point, so it's valid
                Agent.testBoard.updateBoard(color, action)

                # pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                # update the board here bc it's already been tested by this point, so it's valid
                Agent.testBoard.updateBoard(color, action)

                # pass

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