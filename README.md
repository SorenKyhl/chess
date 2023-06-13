
"""
# Chess But You Only Have Pawns
Functional Implementation; no OOP


# Current Features:
    - core game loop: players take turn selecting and moving pieces
    - basic pawn logic: moving and captures
        - not implemented: first move two spaces, en passant, queen promotion


# Not Implemented:
    - all pieces aside from pawn
    - check and checkmate logic
    - draw and stalemate logic
    - points counter to show who has more material on the board


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
