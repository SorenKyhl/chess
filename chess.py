import os
import copy
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
    if type(piece) is str:
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
    return (piece != 0) and (player_from_piece(piece) == player)


def valid_move(square_from: ChessSquare, square_to: ChessSquare, board: ChessBoard) -> bool:
    """check whether the piece at square_from can move to square_to"""
    piece = get_piece(square_from, board)
    if not piece:
        return False

    return indices(square_to) in get_valid_squares(piece, square_from, board)


def attacking_squares(board: ChessBoard, player: ChessPlayer) -> Set[BoardIndices]:
    squares = set()
    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            square_from = square_from_indices((i,j))
            if player_from_piece(piece) == player:
                squares = squares.union(get_valid_squares(piece, square_from, board, attack_only=True))
    return squares


def opponent(player: ChessPlayer) -> ChessPlayer:
    """returns the integer representation of the opponent"""
    return 0 if player else 1


def player_to_string(player: ChessPlayer) -> str:
    return "white" if player else "black"


def get_valid_squares(piece: ChessPiece, square: ChessSquare, board: ChessBoard, attack_only=False) -> Set[BoardIndices]:
    """return set of valid squares for the input piece at the given square
    if attack_only: only return valid attacking squares, not move squares 
    (only relevant for pawns)"""
    player = player_from_piece(piece)

    if piece == 0:
        valid_squares = set()
    elif type(piece) is str and piece.lower() == "p":
        valid_squares = get_pawn_valid_squares(board, square, player, attack_only)
    elif type(piece) is str and piece.lower() == "r":
        valid_squares = get_rook_valid_squares(board, square, player)
    elif type(piece) is str and piece.lower() == "b":
        valid_squares = get_bishop_valid_squares(board, square, player)
    elif type(piece) is str and piece.lower() == "q":
        valid_squares = get_queen_valid_squares(board, square, player)
    elif type(piece) is str and piece.lower() == "n":
        valid_squares = get_knight_valid_squares(board, square, player)
    elif type(piece) is str and piece.lower() == "k":
        valid_squares = get_king_valid_squares(board, square, player)
    else:
        valid_squares = set()

    return valid_squares


def get_pawn_move_squares(board: ChessBoard, square: ChessSquare, player: ChessPlayer) -> Set[BoardIndices]:
    valid_squares = set()
    row, col = indices(square)
    direction = -1 if player else 1

    #TODO make sure thid doesn't go out of bounds
    if not board[row + direction][col]:
        # move pawn forward
        valid_squares.add((row + direction, col))

    # first move two squares
    if (player and square[1] == "2") or (not player and square[1] == "7"):
        if not board[row+direction][col] and not board[row+2*direction][col]:
            valid_squares.add((row + 2*direction, col))

    return valid_squares


def get_pawn_attack_squares(board: ChessBoard, square: ChessSquare, player: ChessPlayer) -> Set[BoardIndices]:
    valid_squares = set()
    row, col = indices(square)
    direction = -1 if player else 1

    if col > 0 and player_from_piece(board[row + direction][col-1]) == opponent(player):
        # capture left
        valid_squares.add((row + direction, col-1))
    if col < 7 and player_from_piece(board[row + direction][col+1]) == opponent(player):
        # capture right
        valid_squares.add((row + direction, col+1))

    return valid_squares


def get_pawn_valid_squares(board: ChessBoard, square: ChessSquare, player: ChessPlayer, attack_only=False) -> Set[BoardIndices]:
    """return set of valid squares for a pawn at the given square
    if attack_only: return only the squares a pawn threatens to attack"""
    valid_squares = set()

    valid_squares = valid_squares.union(get_pawn_attack_squares(board, square, player))
    if not attack_only:
        valid_squares = valid_squares.union(get_pawn_move_squares(board, square, player))

    return valid_squares


def in_bounds(index: int) -> bool:
    return index >= 0 and index <= 7


def get_rook_valid_squares(board: ChessBoard, square: ChessSquare, player: ChessPlayer) -> Set[BoardIndices]:
    valid_squares = set()
    row, col = indices(square)

    dirs = [-1, 1]
    for x_dir in dirs:
        row_to = row + x_dir
        while in_bounds(row_to):
            piece = board[row_to][col]
            if piece:
                if player_from_piece(piece) == opponent(player):
                    valid_squares.add((row_to, col))
                break

            valid_squares.add((row_to, col))
            row_to += x_dir

    for y_dir in dirs:
        col_to = col + y_dir
        while in_bounds(col_to):
            piece = board[row][col_to]
            if piece:
                if player_from_piece(piece) == opponent(player):
                    valid_squares.add((row, col_to))
                break
            valid_squares.add((row, col_to))
            col_to += y_dir

    return valid_squares

def get_bishop_valid_squares(board: ChessBoard, square: ChessSquare, player: ChessPlayer) -> Set[BoardIndices]:

    valid_squares = set()
    row, col = indices(square)

    dirs = [-1, 1]
    for x_dir in dirs:
        for y_dir in dirs:
            row_to = row + x_dir
            col_to = col + y_dir
            while in_bounds(row_to) and in_bounds(col_to):
                piece = board[row_to][col_to]
                if piece:
                    if player_from_piece(piece) == opponent(player):
                        valid_squares.add((row_to, col_to))
                    break
                valid_squares.add((row_to, col_to))

                row_to += x_dir
                col_to += y_dir

    return valid_squares


def get_queen_valid_squares(board: ChessBoard, square: ChessSquare, player: ChessPlayer) -> Set[BoardIndices]:
    valid_squares = set()
    valid_squares = valid_squares.union(get_rook_valid_squares(board, square, player))
    valid_squares = valid_squares.union(get_bishop_valid_squares(board, square, player))
    return valid_squares


def get_knight_valid_squares(board: ChessBoard, square: ChessSquare, player: ChessPlayer) -> Set[BoardIndices]:
    valid_squares = set()
    row, col = indices(square)

    dirs = [[2, 1],
            [2, -1],
            [1, 2],
            [-1, 2],
            [-2, 1],
            [-2, -1],
            [1, -2],
            [-1, -2]]

    for dir in dirs:
        x_dir, y_dir = dir
        row_to = row + x_dir
        col_to = col + y_dir
        if in_bounds(row_to) and in_bounds(col_to):
            if player_from_piece(board[row_to][col_to]) == player:
                continue
            valid_squares.add((row_to, col_to))

    return valid_squares


def get_king_valid_squares(board: ChessBoard, square: ChessSquare, player: ChessPlayer) -> Set[BoardIndices]:
    valid_squares = set()
    row, col = indices(square)
    dirs = [-1, 0, 1]
    for x_dir in dirs:
        for y_dir in dirs:
            row_to = row + x_dir
            col_to = col + y_dir
            if in_bounds(row_to) and in_bounds(col_to):
                piece = board[row_to][col_to]
                if player_from_piece(piece) == opponent(player):
                    valid_squares.add((row_to, col_to))
                if not piece:
                    valid_squares.add((row_to, col_to))

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


def in_check(board: ChessBoard, player: ChessPlayer) -> bool:
    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            if piece and piece.lower() == 'k' and player_from_piece(piece) == player:
                king_square = square_from_indices((i,j))

    return indices(king_square) in attacking_squares(board, opponent(player))


def in_checkmate(board: ChessBoard, player: ChessPlayer) -> bool:
    """return if the player is in checkmate"""
    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            if piece and player_from_piece(piece) == player:
                # for all player's pieces, try to move them.
                square_from = square_from_indices((i,j))
                for indices_to in get_valid_squares(piece, square_from, board):
                    square_to = square_from_indices(indices_to)
                    # copy so the original board state isn't mutated
                    board_to = copy.deepcopy(board) 
                    board_to = move_piece(square_from, square_to, board_to)
                    if not in_check(board_to, player):
                        # if any move can be played, they are not in checkmate
                        return False
    return True


def select_move(board: ChessBoard, square_from: ChessSquare, player: ChessPlayer) -> bool:
    """select move and carry out move if valid. 
    the user can elect to cancel the move and select a different piece
    returns: [bool] move_success"""

    while True:
        square_to = input("Select a move. (To select a different piece, enter \"x\") \n")
        if square_to == "x":
            return False

        if not valid_square(square_to):
            print("Invalid square: input a square acccording to it's rank and file\n")
            continue

        if valid_move(square_from, square_to, board):
            board = move_piece(square_from, square_to, board)

            if in_check(board, player):
                print("You cannot move into check! ")
                board = move_piece(square_to, square_from, board) # move back
                continue # try a different move

            print("valid move selection")
            break
        else:
            print("invalid move selection")

    return True


def player_pieces(board: ChessBoard, player: ChessPlayer):
    pieces = {}
    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            if player_from_piece(piece) == player:
                pieces[piece] = (i, j)

    return pieces

def material_points(board: ChessBoard, player: ChessPlayer):
    """calculates the material points on the board for the given player"""
    piece_values = {"q": 9, "r": 5, "b": 3, "n": 3, "p": 1, "k": 0}
    pieces = player_pieces(board, player)
    return sum([piece_values[piece.lower()] for piece in pieces])


def print_material_points(board):
    white_points = material_points(board, 1)
    black_points = material_points(board, 0)

    print(f"white: {white_points}, black: {black_points}")
    print(f"material advantage: {white_points - black_points}")


def print_game_state(board: ChessBoard, player: ChessPlayer, move: float):
    """prints the status of the game and the current board state"""
    print("----Chess Game-----")
    print("White: uppercase, Black: lowercase")
    print(f"Move: {move}")
    print(f"{player_to_string(player)}'s turn")
    print_material_points(board)
    print_board(board)

def main():
    board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ["P","P","P","P","P","P","P","P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ]

    player = 1
    move = 1

    while True:
        os.system("clear")
        print_game_state(board, player, move)

        if in_checkmate(board, player):
            print("game over, you are in checkmate!!")
            break
        elif in_check(board, player):
            print("you are in check!!")

        square_from = select_piece(board, player)
        print_valid_move_squares(square_from, board)
        move_success = select_move(board, square_from, player)

        if move_success:
            player = opponent(player)
            move += 0.5
    
    print(f"{player_to_string(opponent(player))} wins!")

if __name__ == "__main__":
    main()
    




