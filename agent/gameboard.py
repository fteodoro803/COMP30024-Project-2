from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, constants, exceptions, board

class Node:
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

    def updateBoard(self, colour: PlayerColor, action: Action):
        location = (action.cell.r, action.cell.q)
        hexLocation = HexPos(action.cell.r, action.cell.q)

        match action:
            case SpawnAction(cell):
                self.board[location] = Node(hexLocation, colour, 1)
            case SpreadAction(cell, direction):
                # gets successive locations
                current = self.board[location]  # Node
                nextHexLocation = hexLocation.__add__(action.direction)  # Neighbour Hex Location

                for i in range(current.power):
                    nextCoordinate = (nextHexLocation.r, nextHexLocation.q)  # Neighbour Coordinate
                    temp = self.board[nextCoordinate]

                    nextNode = Node(HexPos(temp.location.r, temp.location.q), colour, temp.power + 1)
                    self.board[nextCoordinate] = nextNode

                    # continues Spread to next neighbour
                    nextHexLocation = nextNode.location.__add__(action.direction)

                # remove root
                self.board[location] = Node(hexLocation, None, 0)  # Placeholder/Empty Locations


    def generateBoard(self):
        gameBoard = {}
        for r in range(constants.BOARD_N):
            for q in range(constants.BOARD_N):
                location = (r, q)
                hexLocation = HexPos(r, q)
                gameBoard[(r, q)] = Node(hexLocation, None, 0)  # Placeholder/Empty Locations

        return gameBoard
