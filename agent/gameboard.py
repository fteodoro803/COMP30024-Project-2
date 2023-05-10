import copy

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
        self.lastMove = None

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
        # print(f"UpdateBoard: power={self.power}, moves={self.numTurns}, nextPlayer={self.getNextPlayer()}")


    def generateBoard(self):
        gameBoard = {}
        for r in range(constants.BOARD_N):
            for q in range(constants.BOARD_N):
                location = (r, q)
                hexLocation = HexPos(r, q)
                gameBoard[(r, q)] = Piece(hexLocation, None, 0)  # Placeholder/Empty Locations

        return gameBoard

    def getWinner(self) -> (bool, PlayerColor, int):  # !!!!! this the same as isTerminal? -> (terminal_state, winner)
        bluePower = sum([value.power for value in self.board.values() if value.colour is PlayerColor.BLUE])
        redPower = sum([value.power for value in self.board.values() if value.colour is PlayerColor.RED])
        score = 0

        # Winner in regular Gameplay
        if bluePower == 0 and self.numTurns > 2:
            score = redPower - bluePower
            return True, PlayerColor.RED, score
        elif redPower == 0 and self.numTurns > 2:
            score = bluePower - redPower
            return True, PlayerColor.BLUE, score

        # No more Turns
        if self.numTurns == 343-1:
            if (abs(bluePower-redPower) >= 2):
                if (bluePower > redPower):
                    score = bluePower-redPower
                    return True, PlayerColor.BLUE, score
                else:
                    score = redPower-bluePower
                    return True, PlayerColor.RED, score

        # No more Tokens
        if redPower == 0 and bluePower == 0 and self.numTurns > 0:
            score = 0
            return True, None, score

        return False, None, 0

    def getOpponentNextPositions(self):
        opponentSpreads = self.spreadOptions(self.getOtherPlayer())
        opponentSpreadPieces = []
        for spread in opponentSpreads:
            position = spread[0]
            direction = spread[2]
            for iter in range(spread[1]):
                nextHexLocation = position.__add__(direction)
                opponentSpreadPieces.append(nextHexLocation)
                position = nextHexLocation
        return opponentSpreadPieces

    def spawnOptions(self) -> [SpawnAction]:
        opponentSpreadPieces = self.getOpponentNextPositions()
        playerCells = [value.location for value in self.board.values() if value.colour is self.getCurrentPlayer()]
        emptyCells = [value.location for value in self.board.values() if value.colour is None]
        spawns = []
        smartSpawns = []

        for cell in emptyCells:
            if cell not in opponentSpreadPieces:
                spawns.append(cell)
            else:
                isAdjacent = False
                for direction in HexDir:
                    adjacentCell = cell.__add__(direction)
                    if adjacentCell in playerCells and adjacentCell not in opponentSpreadPieces:
                        isAdjacent = True
                if isAdjacent:
                    smartSpawns.append(cell)

        if len(smartSpawns) > 0:
            return smartSpawns
        else:
            return spawns

    def smartSpread(self, colour):
        spreads = self.spreadOptions(self.getCurrentPlayer())
        opponentSpreadPieces = self.getOpponentNextPositions()
        smartSpreads = []

        for spread in spreads:
            if spread[1] == 1:
                nextHexLocation = spread[0].__add__(spread[2])
                if nextHexLocation not in opponentSpreadPieces:
                    smartSpreads.append(spread)
            else:
                smartSpreads.append(spread)
        if len(smartSpreads) == 0:
            return spreads
        return smartSpreads


    def spreadOptions(self, colour):
        pieces = [value for value in self.board.values() if
                      value.colour is colour]

        spreads = []

        for piece in pieces:
            for direction in HexDir:
                spreads.append((piece.location, piece.power, direction))

        return spreads


    def getCurrentPlayer(self):
        if self.numTurns % 2 == 0:
            return PlayerColor.RED
        else:
            return PlayerColor.BLUE

    def getOtherPlayer(self):
        if self.numTurns % 2 == 0:
            return PlayerColor.BLUE
        else:
            return PlayerColor.RED

    def getLegalMoves(self) -> Action:   # why are we doing so much processin? idk if we need to do any copying here, just do a random move coz that's all we need anyway
        goodMoves = []
        moves = []  # GameBoards

        nextPlayer = self.getCurrentPlayer()

        for spread in self.smartSpread(nextPlayer):
            newBoard = copy.deepcopy(self) # use deepcopy instead of copy or else all the boards will be the same
            newBoard.updateBoard(nextPlayer, SpreadAction(spread[0], spread[2]))

            # important for the report --> efficiency of the program
            # currently only choosing the most recent guy -- want to determine the best choice out of the power increasing moves
            if newBoard.getPlayerPower(nextPlayer) > self.getPlayerPower(nextPlayer):
                goodMoves.append((newBoard, SpreadAction(spread[0], spread[2])))
                moves.append((newBoard, SpreadAction(spread[0], spread[2])))
            else:
                moves.append((newBoard, SpreadAction(spread[0], spread[2])))

        # print(self.spawnOptions())
        if self.power < 49:
            for spawn in self.spawnOptions():  # creates future boards
                newBoard = copy.deepcopy(self)  # use deepcopy instead of copy or else all the boards will be the same
                newBoard.updateBoard(nextPlayer, SpawnAction(spawn))
                # goodMoves.append() if it fits some criteria
                moves.append((newBoard, SpawnAction(spawn)))
        # print(f"# GOOD MOVES: {len(goodMoves)}")
        # print(f"# MOVES: {len(moves)}")
        if len(goodMoves) > 0:
            return goodMoves
        else:
            return moves

    def getPlayerPower(self, colour: PlayerColor):
        return sum([value.power for value in self.board.values() if value.colour is colour])
