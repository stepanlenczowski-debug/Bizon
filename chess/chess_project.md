# Chess Game

## Project Description
The goal of this project is to create a simple visual chess game in Python using the `pygame` library. The program allows you to display a chessboard, select a piece, and make moves between squares. The project is designed for beginners or students learning game programming and mouse event handling.

## Features
- Display 8x8 chessboard with classic square colors
- Draw chess pieces as text symbols (`K`, `Q`, `R`, `B`, `N`, `P` for white and lowercase letters for black)
- Select a piece with left mouse click
- Make moves by changing piece position in the game matrix
- Automatically alternate turns between white and black pieces
- Pawn promotion when reaching the opposite end
- Piece movement tracking for castling validation
- Castling support (when valid conditions are met)

## Technical Details
- Language: Python
- Library: `pygame`
- Algorithms:
  - Simple mouse click handling for piece selection and movement
  - Turn switching after each completed move
  - Movement tracking for special moves
- Data Structure:
  - `board` as list of lists (`list[list[str]]`) represents current piece placement
  - Each cell contains a piece character or empty string
- Main Functions:
  - `draw_board(selected_sq, moves)` – draws the chessboard and highlights selected square and valid moves
  - `draw_pieces()` – renders all pieces according to `board`
  - `get_valid_moves(r, c)` – calculates valid moves for a piece
  - `handle_click(mouse_pos, selected_sq, moves, turn)` – processes mouse clicks
  - `perform_move(start_r, start_c, end_r, end_c, is_white)` – executes moves including special moves
  - `main()` – main game loop

## User Guide
1. Open terminal in the `chess` folder
2. Run the program with:
   ```bash
   python chess.py
   ```
3. The game window will open
4. Click on a square with a piece to select it
5. Click on a destination square to move the piece
6. The program automatically alternates turns between white and black
7. Close the window by clicking the X button or pressing the exit key

## Piece Movement Rules
- **Pawn (P/p)**: Moves forward one square (two on first move), captures diagonally
- **Rook (R/r)**: Moves any number of squares horizontally or vertically
- **Knight (N/n)**: Moves in L-shape (2+1 squares)
- **Bishop (B/b)**: Moves any number of squares diagonally
- **Queen (Q/q)**: Combines rook and bishop movement
- **King (K/k)**: Moves one square in any direction

## Special Moves
- **Pawn Promotion**: When a pawn reaches the opposite end, it automatically promotes to a Queen
- **Castling**: King and Rook can perform castling (when both haven't moved previously and there are no pieces between them)

## Limitations and Future Improvements
- Program doesn't enforce check or checkmate detection
- No en passant capture
- No undo functionality
- No move history
- Possible improvements:
  - Add check/checkmate detection
  - Implement en passant
  - Add undo/redo functionality
  - Display move history
  - Add AI opponent
  - Add sound effects and animations
  - Implement time controls for blitz chess
