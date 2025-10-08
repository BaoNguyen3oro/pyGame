# Python Games Collection

This repository contains classic games implemented in Python using Pygame.

## Installation

1. Make sure you have Python installed (version 3.13 or newer)
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Games

### Snake

A classic Snake game where you control a snake to eat food and grow longer.

#### How to Run
```
python snake.py
```

#### Game Controls
- **Arrow Keys**: Move the snake (Up, Down, Left, Right)
- **Space**: Restart game (when game over)
- **ESC**: Quit game

#### Game Rules
- Control the snake to eat red food squares
- The snake grows longer each time it eats food
- Avoid hitting the walls or the snake's own body
- Game speed increases as your score gets higher
- Game ends when the snake collides with walls or itself

#### Features
- Classic snake movement mechanics
- Collision detection for walls and self-collision
- Score tracking (+10 points per food)
- Progressive difficulty (speed increases with score)
- Visual grid for better gameplay
- Game over screen with restart functionality

### Tetris

A classic Tetris game where you arrange falling blocks to complete lines.

#### How to Run
```
python tetris.py
```

#### Game Controls
- **Left Arrow**: Move piece to the left
- **Right Arrow**: Move piece to the right
- **Down Arrow**: Soft drop (move piece down faster)
- **Up Arrow**: Rotate piece
- **Space**: Hard drop (instantly drop piece to the bottom)
- **R**: Restart game (when game over)

#### Game Rules
- Pieces fall from the top of the screen
- Move and rotate pieces to fit them together at the bottom
- Complete horizontal lines to clear them and earn points
- Game ends when pieces reach the top of the screen
- Each cleared line awards 100 points

#### Features
- All 7 classic Tetris pieces (I, O, T, S, Z, J, L)
- Piece rotation and movement
- Collision detection
- Line clearing with scoring
- Game over detection
- Restart functionality

### Sudoku

A classic Sudoku puzzle game with three difficulty levels.

#### How to Run
```
python sudoku.py
```

#### Game Controls
- **Mouse Click**: Select a cell
- **Number Keys (1-9)**: Place a number in the selected cell
- **Delete/Backspace**: Clear the selected cell
- **Arrow Keys**: Navigate between cells

#### Game Rules
- Fill the 9×9 grid with digits so that each column, each row, and each of the nine 3×3 subgrids contains all of the digits from 1 to 9
- Black numbers are given clues and cannot be changed
- Blue numbers are your entries
- Red numbers indicate conflicts with Sudoku rules
- The game is complete when all cells are filled correctly

#### Features
- Three difficulty levels: Easy, Medium, Hard
- Automatic puzzle generation
- Conflict detection and highlighting
- Game completion detection
- New game generation
- Visual feedback for selected cells and conflicts

## Enjoy the games!