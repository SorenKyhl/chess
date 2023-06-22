
"""
# Chess Game
![example workflow](https://github.com/SorenKyhl/chess/actions/workflows/python-app.yml/badge.svg)

# Current Features:
    - core game loop: players take turn selecting and moving pieces
    - basic piece logic: moving and captures
    - check and checkmate logic
	- material points counter

# Not Implemented:
    - draw and stalemate logic
    - en passant
    - pawn promotion

# todo:
    - make board class for easier access to pieces

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
