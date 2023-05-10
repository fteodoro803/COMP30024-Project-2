import copy

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, constants

# Stores Data for each Location on the Board
class Token:
    def __init__(self, location: HexPos, colour: PlayerColor, power: int):
        self.location = location
        self.colour = colour
        self.power = power
        self.children = {}

    def __repr__(self):
        return f"({self.colour},{self.power})"


# Holds the Data of the Board
class GameBoard:
    def __init__(self):
        self.board = self.generateBoard()
        self.power = 0
        self.numTurns = 0
        self.lastMove = None

    ### BOARD ###
    # Applies changes to the Board
    def updateBoard(self, colour: PlayerColor, action: Action) -> None:
        location = (action.cell.r, action.cell.q)
        hexLocation = HexPos(action.cell.r, action.cell.q)

        match action:
            case SpawnAction(cell):
                self.board[location] = Token(hexLocation, colour, 1)
                self.power += 1
            case SpreadAction(cell, direction):
                # gets successive locations
                current = self.board[location]
                nextHexLocation = hexLocation.__add__(action.direction)  # Neighbour Hex Location

                # remove root
                self.board[location] = Token(hexLocation, None, 0)  # Placeholder/Empty Locations

                for i in range(current.power):  # consideration for Power
                    nextCoordinate = (nextHexLocation.r, nextHexLocation.q)  # Neighbour Coordinate
                    temp = self.board[nextCoordinate]

                    nextNode = Token(HexPos(temp.location.r, temp.location.q), colour, temp.power + 1)
                    if nextNode.power < 7:  # assigning if power <= 6
                        self.board[nextCoordinate] = nextNode
                    else:  # remove stack if power > 6
                        nextNode = Token(HexPos(nextNode.location.r, nextNode.location.q), None, 0)
                        self.board[nextCoordinate] = nextNode

                    # continues Spread to next neighbour
                    nextHexLocation = nextNode.location.__add__(action.direction)

        self.numTurns += 1

    ### SUPPORT ###
    # Initialises Board
    def generateBoard(self):
        gameBoard = {}
        for r in range(constants.BOARD_N):
            for q in range(constants.BOARD_N):
                location = (r, q)
                hexLocation = HexPos(r, q)
                gameBoard[(r, q)] = Token(hexLocation, None, 0)

        return gameBoard

    ### MCTS ###
    # Evaluates board to determine Winner
    def getWinner(self) -> (bool, PlayerColor, int):
        bluePower = sum([value.power for value in self.board.values() if value.colour is PlayerColor.BLUE])
        redPower = sum([value.power for value in self.board.values() if value.colour is PlayerColor.RED])
        score = 0
        isTerminalState = False

        # Winner in regular Gameplay
        if bluePower == 0 and self.numTurns > 2:  # red win
            score = redPower
            isTerminalState = True
            return isTerminalState, PlayerColor.RED, score
        elif redPower == 0 and self.numTurns > 2:  # blue win
            score = bluePower
            isTerminalState = True
            return isTerminalState, PlayerColor.BLUE, score

        # No more Turns
        if self.numTurns == 343-1:
            if (abs(bluePower-redPower) >= 2):
                isTerminalState = True
                if (bluePower > redPower):
                    score = bluePower-redPower
                    return isTerminalState, PlayerColor.BLUE, score
                else:
                    score = redPower-bluePower
                    return isTerminalState, PlayerColor.RED, score

        # No more Tokens
        if redPower == 0 and bluePower == 0 and self.numTurns > 0:
            score = 0
            isTerminalState = True
            return isTerminalState, None, score

        return isTerminalState, None, 0

    # Return List of Opponent's next possible Positions from SpreadAction
    def getOpponentNextPositions(self) -> [HexPos]:
        spreads = self.spreadOptions(self.getOtherPlayer())
        locations = []

        for spread in spreads:
            position = spread[0]
            direction = spread[2]

            power = spread[1]
            for p in range(power):
                nextHexLocation = position.__add__(direction)
                locations.append(nextHexLocation)
                position = nextHexLocation
        return locations

    # Prevents spawning in a Location within Range of an Opponent
    def spawnOptions(self) -> [SpawnAction]:
        opponentSpreadPieces = self.getOpponentNextPositions()
        playerCells = [value.location for value in self.board.values() if value.colour is self.getCurrentPlayer()]
        randomSpawns = [value.location for value in self.board.values() if value.colour is None]
        smartSpawns = []            # locations out of range of an opponent/cannot be Spread to immediately
        defendedSmartSpawns = []    # Defended means tradeable by a Piece of the same Colour

        for location in randomSpawns:
            if location not in opponentSpreadPieces:
                smartSpawns.append(location)
            else:   # allows spawning in range of opponent, if piece is defended/tradeable
                isAdjacent = False
                for direction in HexDir:
                    adjacentCell = location.__add__(direction)
                    if adjacentCell in playerCells and adjacentCell not in opponentSpreadPieces:
                        isAdjacent = True
                if isAdjacent:
                    defendedSmartSpawns.append(location)

        if len(defendedSmartSpawns) > 0:    # smart spawn positions
            return defendedSmartSpawns
        elif len(smartSpawns) > 0:       # semi-random spawn positions
            return smartSpawns
        else:
            return randomSpawns     # random spawn positions

    # Prevents Spreading to a Location in range of Opponent
    def smartSpread(self, colour: PlayerColor) -> []:
        spreads = self.spreadOptions(colour)
        opponentSpreadPieces = self.getOpponentNextPositions()
        playerLocations = [value.location for value in self.board.values() if value.colour is colour]
        smartSpreads = []

        for spread in spreads:
            location = spread[0]
            power = spread[1]
            direction = spread[2]

            if power == 1:      # ensures that when it spreads, it doesn't spread to something in range of opponent
                nextHexLocation = location.__add__(direction)
                if nextHexLocation not in opponentSpreadPieces:
                    smartSpreads.append(spread)

                # spread in tradeable position
                else:
                    isAdjacent = False
                    for direction in HexDir:
                        adjacentCell = nextHexLocation.__add__(direction)
                        if adjacentCell in playerLocations and adjacentCell not in opponentSpreadPieces and adjacentCell != location:
                            isAdjacent = True
                    if isAdjacent:
                        smartSpreads.append(spread)
            else:
                smartSpreads.append(spread)

        if len(smartSpreads) == 0:
            return spreads
        return smartSpreads

    # Getting List of Spread options for a Player
    def spreadOptions(self, colour: PlayerColor) -> []:
        pieces = [value for value in self.board.values() if
                      value.colour is colour]

        spreads = []

        for piece in pieces:
            for direction in HexDir:
                spreads.append((piece.location, piece.power, direction))

        return spreads


    def getCurrentPlayer(self) -> PlayerColor:
        if self.numTurns % 2 == 0:
            return PlayerColor.RED
        else:
            return PlayerColor.BLUE

    def getOtherPlayer(self) -> PlayerColor:
        if self.numTurns % 2 == 0:
            return PlayerColor.BLUE
        else:
            return PlayerColor.RED

    # returns States of legal States of a Board and the Move applied to reach the State
    def getLegalMoves(self):  # -> [(GameBoard, Action)]
        priorityMoves = []      # moves that are determined to be immediately beneficial to current Player
        moves = []              # valid moves

        nextPlayer = self.getCurrentPlayer()

        # spread moves
        for spread in self.smartSpread(nextPlayer):
            newBoard = copy.deepcopy(self) # use deepcopy instead of copy or else all the boards will be the same
            newBoard.updateBoard(nextPlayer, SpreadAction(spread[0], spread[2]))

            # prioritises Moves that claim an opponent's Token
            if newBoard.getPlayerPower(nextPlayer) > self.getPlayerPower(nextPlayer):
                priorityMoves.append((newBoard, SpreadAction(spread[0], spread[2])))
                moves.append((newBoard, SpreadAction(spread[0], spread[2])))
            else:
                moves.append((newBoard, SpreadAction(spread[0], spread[2])))

        # spawn moves
        if self.power < 49:
            for spawn in self.spawnOptions():  # creates future boards
                newBoard = copy.deepcopy(self)  # use deepcopy instead of copy or else all the boards will be the same
                newBoard.updateBoard(nextPlayer, SpawnAction(spawn))
                moves.append((newBoard, SpawnAction(spawn)))

        # if there are good moves, return only those
        if len(priorityMoves) > 0:
            return priorityMoves
        else:
            return moves

    # Returns Power of a Player
    def getPlayerPower(self, colour: PlayerColor) -> int:
        return sum([value.power for value in self.board.values() if value.colour is colour])
