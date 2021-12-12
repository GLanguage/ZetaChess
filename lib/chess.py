from enum import Enum

class Piece(Enum):
    K = 0
    Q = 1
    R = 2
    B = 3
    N = 4
    P = 5

pieceMoves = {
    Piece.K: (1, [(1, 1), (1, 0), (1, -1), (-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1)]),
    Piece.Q: (-1, [(1, 1), (1, 0), (1, -1), (-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1)]),
    Piece.R: (-1, [(1, 0), (-1, 0), (0, 1), (0, -1)]),
    Piece.B: (-1, [(1, 1), (1, -1), (-1, 1), (-1, -1)]),
    Piece.N: (1, [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]),
}

def vec_add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def vec_times(v1, k):
    return (v1[0] * k, v1[1] * k)

class Board:
    def __init__(self):
        self.size = 8
        self.pieces = {} # {(x, y): (player, category)}
    def __getitem__(self, coord):
        return self.pieces.get(coord)
    def isLegalCoord(self, coord):
        return 1 <= coord[0] and coord[0] <= self.size and 1 <= coord[1] and coord[1] <= self.size
    def generatePieceMoves(self, coord):
        if pieceMoves[self[coord][1]][0] == 1:
            return [vec_add(coord, d) for d in pieceMoves[self[coord][1]][1] \
                if self.isLegalCoord(vec_add(coord, d)) \
                    and ((not self[vec_add(coord, d)]) or self[vec_add(coord, d)][0] != self[coord][0])]
        elif pieceMoves[self[coord][1]][0] == -1:
            return [vec_add(coord, vec_times(d, l)) for d, l in zip(pieceMoves[self[coord][1]][1], range(1, self.size)) \
                if self.isLegalCoord(vec_add(coord, vec_times(d, l))) \
                    and ((not self[vec_add(coord, vec_times(d, l))]) or self[vec_add(coord, vec_times(d, l))][0] != self[coord][0])]
    def generateMoves(self, player):
        moves = []
        for coord in self.pieces:
            if self[coord][0] != player:
                continue
            if self[coord][1] == Piece.P:
                pMoves = []
                if self.isLegalCoord(vec_add(coord, 0, player)) and not self[vec_add(coord, 0, player)]:
                    moves.append((coord, vec_add(coord, 0, player)))
                pMoves += [(coord, vec_add(coord, dx, player)) for dx in [1, -1] \
                    if self.isLegalCoord(vec_add(coord, dx, player)) \
                        and self[vec_add(coord, dx, player)] and self[vec_add(coord, dx, player)][0] != self[coord][0]]
                moves += pMoves
            else:
                moves += [(coord, move) for move in self.generatePieceMoves(coord)]
        return moves

def applyMove(pieces, coord, move):
    orig = -1
    dest = -1
    for i in range(len(pieces)):
        if pieces[i][0] == coord:
            orig = i
        elif pieces[i][0] == move:
            dest = i
    res = 0
    pieces[orig][0] = move
    if dest >= 0:
        if pieces[dest][2] == Piece.K:
            res = pieces[orig][1]
        pieces.pop(dest)
    return pieces, res
