from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, constants, exceptions, board

class GameBoard:
    def __init__(self):
        self.board = {}