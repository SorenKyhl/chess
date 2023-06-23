import chess

def test_valid_square():
    assert(chess.valid_square("a1"))
    assert(chess.valid_square("h8"))
    assert(chess.valid_square("e4"))
    assert(not chess.valid_square("4e"))
    assert(not chess.valid_square("e"))
    assert(not chess.valid_square("j1"))
    assert(not chess.valid_square("a9"))
    assert(not chess.valid_square("aa3"))


def test_to_indices():
    assert(chess.to_indices("a1") == (7,0))
    assert(chess.to_indices("h8") == (0,7))


def test_to_square():
    assert(chess.to_square((7,0)) == "a1")
    assert(chess.to_square((0,7)) == "h8")


def test_to_player():
    assert(chess.to_player("R") == 1)
    assert(chess.to_player("r") == 0)
    assert(chess.to_player(0) == -1)


def test_get_piece():
    board = chess.initial_board_state
    assert chess.get_piece("e4", board) == 0
    assert chess.get_piece("d8", board) == "q"
    assert chess.get_piece("d1", board) == "Q"

def test_player_owns_piece():
    board = chess.initial_board_state
    player = 1
    assert chess.player_owns_piece("e2", player, board) == True
    assert chess.player_owns_piece("e2", chess.opponent(player), board) == False
    assert chess.player_owns_piece("e7", player, board) == False
    assert chess.player_owns_piece("e7", chess.opponent(player), board) == True


def test_chess_board_class():
    board = chess.ChessBoardClass()
    assert board["e4"] == 0
    assert board["d8"] == "q"
    assert board["d1"] == "Q"



def test_enumerate_squares():
    all_squares = list(chess.enumerate_squares())
    assert len(all_squares) == 64
 
