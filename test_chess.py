
import chess


def test_valid_square():
    assert(chess.valid_square("a1"))
    assert(chess.valid_square("h8"))
    assert(chess.valid_square("e4"))
    assert(not chess.valid_square("4e"))
    assert(not chess.valid_square("e"))
    assert(not chess.valid_square("j1"))
    assert(not chess.valid_square("a9"))


def test_indices():
    assert(chess.indices("a1") == (7,0))
    assert(chess.indices("h8") == (0,7))


def test_square_from_indices():
    assert(chess.square_from_indices((7,0)) == "a1")
    assert(chess.square_from_indices((0,7)) == "h8")


def test_player_from_piece():
    assert(chess.player_from_piece("R") == 1)
    assert(chess.player_from_piece("r") == 0)
    assert(chess.player_from_piece(0) == -1)
 
