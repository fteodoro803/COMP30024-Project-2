from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, constants, exceptions, board

class Piece:
    def __init__(self, location: HexPos, colour: PlayerColor, power: int):
        self.location = location
        self.colour = colour
        self.power = power
        self.children = {}

    def __repr__(self):
        # return f"({self.location.q},{self.location.r}, {self.colour}, {self.power})"
        return f"({self.colour},{self.power})"



class GameBoard:
    def __init__(self):
        self.board = self.generateBoard()
        self.power = 0
        self.numTurns = 0

    def updateBoard(self, colour: PlayerColor, action: Action):
        location = (action.cell.r, action.cell.q)
        hexLocation = HexPos(action.cell.r, action.cell.q)

        match action:
            case SpawnAction(cell):
                self.board[location] = Piece(hexLocation, colour, 1)
                self.power += 1
            case SpreadAction(cell, direction):
                # gets successive locations
                current = self.board[location]  # Node
                nextHexLocation = hexLocation.__add__(action.direction)  # Neighbour Hex Location

                # remove root
                self.board[location] = Piece(hexLocation, None, 0)  # Placeholder/Empty Locations

                for i in range(current.power):  # should this be minus 1? in the case the power is more than one?
                    nextCoordinate = (nextHexLocation.r, nextHexLocation.q)  # Neighbour Coordinate
                    temp = self.board[nextCoordinate]

                    nextNode = Piece(HexPos(temp.location.r, temp.location.q), colour, temp.power + 1)
                    if nextNode.power < 7:  # assigning if power <= 6
                        self.board[nextCoordinate] = nextNode
                    else:  # remove stack if power > 6
                        nextNode = Piece(HexPos(nextNode.location.r, nextNode.location.q), None, 0)
                        self.board[nextCoordinate] = nextNode


                    # continues Spread to next neighbour
                    nextHexLocation = nextNode.location.__add__(action.direction)

        self.numTurns += 1
        print(f"UpdateBoard: power={self.power}, moves={self.numTurns}")


    def generateBoard(self):
        gameBoard = {}
        for r in range(constants.BOARD_N):
            for q in range(constants.BOARD_N):
                location = (r, q)
                hexLocation = HexPos(r, q)
                gameBoard[(r, q)] = Piece(hexLocation, None, 0)  # Placeholder/Empty Locations

        return gameBoard

    # def isTerminal(self):

    def getWinner(self):  # !!!!! this the same as isTerminal?
        bluePower = sum([value.power for value in self.board.values() if value.colour is PlayerColor.BLUE])
        redPower = sum([value.power for value in self.board.values() if value.colour is PlayerColor.RED])

        # Winner in regular Gameplay
        if bluePower == 0 and self.numTurns > 2:
            return PlayerColor.RED
        elif redPower == 0 and self.numTurns > 2:
            return PlayerColor.BLUE

        # No more Turns
        if self.numTurns == 343:
            if (abs(bluePower-redPower) >= 2):
                if (bluePower > redPower):
                    return PlayerColor.BLUE
                else:
                    return PlayerColor.RED

        # No more Tokens
        if redPower == 0 and bluePower == 0 and self.numTurns > 0:
            return None

        return None