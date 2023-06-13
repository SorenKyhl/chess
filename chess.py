import os
from typing import List, Union, Tuple, Set

ChessSquare = str
ChessPiece = Union[str, int]
ChessBoard = List[List[ChessPiece]]
ChessPlayer = int
BoardIndices = Tuple[int,int]

def print_board(board: ChessBoard):
    """print board state to console"""
    rank = 8
    for row in board:
        row_string = str(rank) + " "
        for piece in row:
            row_string += str(piece) + " "
        rank -= 1
        print(row_string)
    print("  a b c d e f g h")


def valid_square(square: ChessSquare) -> bool:
    """determine if the input string is a valid chess square"""
    return (len(square) == 2 
            and square[0].isalpha() 
            and square[1].isnumeric() 
            and square[0] >= "a"
            and square[0] <= "h"
            and int(square[1]) >= 1
            and int(square[1]) <= 8
            )


def indices(square: ChessSquare) -> BoardIndices:
    """takes chess square string and returns board indices"""
    if not valid_square(square):
        raise ValueError

    row = 8 - int(square[1])
    col = ord(square[0]) - ord("a")
    return (row, col)


def square_from_indices(idx: BoardIndices) -> ChessSquare:
    """returns chess square corresponding to the input board indices"""
    rank = str(8 - idx[0])
    file = chr(ord("a") + idx[1])
    return file + rank


def player_from_piece(piece: ChessPiece) -> ChessPlayer:
    """
    returns which player owns the piece: white 1, black 0
    white pieces are represented with uppercase characters (e.g. "R", "Q")
    black pieces are represented with lowercase characters (e.g. "r", "q")
    returns -1 if neither player owns the piece
    """
    if piece:
        return piece.isupper()
    else:
        return -1


def get_piece(square: ChessSquare, board: ChessBoard) -> ChessPiece:
    """returns the piece at the given chess square"""
    idx = indices(square)
    return board[idx[0]][idx[1]]


def valid_piece(square: ChessSquare, player: ChessPlayer, board: ChessBoard) -> bool:
    """check whether the piece at the input chess square is owned by the player"""
    piece = get_piece(square, board)
    return piece and player_from_piece(piece) == player


def valid_move(square_from: ChessSquare, square_to: ChessSquare, board: ChessBoard) -> bool:
    """check whether the piece at square_from can move to square_to"""
    piece = get_piece(square_from, board)
    if not piece:
        return False

    return indices(square_to) in get_valid_squares(piece, square_from, board)


def opponent(player: ChessPlayer) -> ChessPlayer:
    """returns the integer representation of the opponent"""
    return 0 if player else 1

def player_to_string(player: ChessPlayer) -> str:
    return "white" if player else "black"


def get_valid_squares(piece: ChessPiece, square: ChessSquare, board: ChessBoard) -> Set[BoardIndices]:
    """return set of valid squares for the input piece at the given square"""
    player = player_from_piece(piece)

    if piece.lower() == "p":
        # pawn
        valid_squares = get_pawn_valid_squares(board, square, player)
    else:
        valid_squares = set()

    return valid_squares

def get_pawn_valid_squares(board: ChessBoard, square: ChessSquare, player: ChessPlayer) -> Set[BoardIndices]:
    """return set of valid squares for a pawn at the given square"""
    valid_squares = set()
    row, col = indices(square)

    direction = -1 if player else 1

    if not board[row + direction][col]:
        # move pawn forward
        valid_squares.add((row + direction, col))
    if player_from_piece(board[row + direction][col-1]) == opponent(player) and col > 0:
        # capture right
        valid_squares.add((row + direction, col-1))
    if player_from_piece(board[row + direction][col+1]) == opponent(player) and col < 7:
        # capture left
        valid_squares.add((row + direction, col+1))

    return valid_squares


def remove_piece(square: ChessSquare, board: ChessBoard) -> ChessBoard:
    """remove piece at the given chess square"""
    idx = indices(square)
    board[idx[0]][idx[1]] = 0
    return board


def set_piece(square: ChessSquare, board: ChessBoard, piece: ChessPiece) -> ChessBoard:
    """assign piece at the given chess square"""
    idx = indices(square)
    board[idx[0]][idx[1]] = piece
    return board


def move_piece(square_from: ChessSquare, square_to: ChessSquare, board: ChessBoard) -> ChessBoard:
    """move piece from one chess square to another"""
    piece = get_piece(square_from, board)
    board = remove_piece(square_from, board)
    board = set_piece(square_to, board, piece)
    return board


def select_piece(board: ChessBoard, player) -> ChessSquare:
    """select a valid piece to move"""
    while True:
        square_from = input("select a piece: \n")
        if not  valid_square(square_from):
            print("Invalid square: input a square acccording to it's rank and file\n")
            continue

        if valid_piece(square_from, player, board):
            print("valid piece selection")
            break
        else:
            print("invalid piece selection")

    return square_from

def print_valid_move_squares(square_from: ChessSquare, board: ChessBoard):
    piece = get_piece(square_from, board)
    valid_squares = get_valid_squares(piece, square_from, board)

    print("valid moves:")
    print([square_from_indices(idx) for idx in valid_squares])

def select_move(board: ChessBoard, square_from: ChessSquare) -> bool:
    """select move and carry out move if valid. 
    the user can elect to cancel the move and select a different piece
    returns: [bool] move_success"""

    while True:
        square_to = input("Select a move. (To select a different piece, enter \"x\") \n")
        if square_to == "x":
            return False

        if not valid_square(square_from):
            print("Invalid square: input a square acccording to it's rank and file\n")
            continue

        if valid_move(square_from, square_to, board):
            board = move_piece(square_from, square_to, board)
            print("valid move selection")
            break
        else:
            print("invalid move selection")

    return True


def main():
    board = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ["P","P","P","P","P","P","P","P"],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]

    player = 1

    while True:
        os.system("clear")
        print("Chess Game")
        print("White: uppercase, Black: lowercase")
        print(player_to_string(player) +"'s turn")
        print_board(board)

        square_from = select_piece(board, player)
        print_valid_move_squares(square_from, board)
        move_success = select_move(board, square_from)

        if not move_success:
            continue

        player = opponent(player)
        
        print_board(board)

if __name__ == "__main__":
    main()
    




