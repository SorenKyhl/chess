
"""
# Chess Game
![example workflow](https://github.com/SorenKyhl/chess/actions/workflows/python-app.yml/badge.svg)

Functional Implementation; no OOP


# Current Features:
    - core game loop: players take turn selecting and moving pieces
    - basic pawn, knight, and sliding pieces logic: moving and captures
        - not implemented: en passant, queen promotion
    - check and checkmate logic
	- material points counter

# Not Implemented:
    - draw and stalemate logic

# todo:
    - make sure pawns don't move out of bounds

# Design Choices:
    - represent the board as a 2D array
        - pieces are represented as strings
            - white pieces are uppercase ("R", "Q")
            - black pieces are lowercase ("r", "q")
        - 0 (integer) represents no pieces
    - chess squares are referred to by their chess name ("e4")
        - can be converted to board indices and back
    - game loop:
        - user selects piece by entering valid chess square string
        - game prints valid places to move that piece
        - user selects a move from the set of valid moves
        - user can cancel the move and select a different piece
"""
