import pygame
import random
import sys
import copy

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = 50
GRID_X_OFFSET = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_Y_OFFSET = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2 - 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SELECTED_COLOR = (173, 216, 230)
CONFLICT_COLOR = (255, 200, 200)

class Sudoku:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sudoku")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)
        self.small_font = pygame.font.SysFont('Arial', 20)
        
        # Game state
        self.board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.solution = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.initial_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected_cell = None
        self.game_over = False
        self.difficulty = "medium"  # easy, medium, hard
        
        # Start new game
        self.new_game()
    
    def new_game(self):
        """Generate a new Sudoku puzzle"""
        # Generate a complete valid Sudoku solution
        self.generate_complete_board()
        
        # Copy the solution
        self.solution = copy.deepcopy(self.board)
        
        # Remove numbers based on difficulty
        cells_to_remove = {
            "easy": 30,
            "medium": 40,
            "hard": 50
        }.get(self.difficulty, 40)
        
        self.remove_numbers(cells_to_remove)
        
        # Store the initial board state
        self.initial_board = copy.deepcopy(self.board)
        
        # Reset game state
        self.selected_cell = None
        self.game_over = False
    
    def generate_complete_board(self):
        """Generate a complete valid Sudoku board using backtracking"""
        # Fill diagonal 3x3 boxes first (they don't affect each other)
        for box in range(0, GRID_SIZE, 3):
            self.fill_box(box, box)
        
        # Fill remaining cells using backtracking
        self.solve_board()
    
    def fill_box(self, row, col):
        """Fill a 3x3 box with random numbers 1-9"""
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums[i * 3 + j]
    
    def is_valid(self, num, row, col):
        """Check if placing num at (row, col) is valid"""
        # Check row
        for x in range(GRID_SIZE):
            if self.board[row][x] == num:
                return False
        
        # Check column
        for x in range(GRID_SIZE):
            if self.board[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def solve_board(self):
        """Solve the Sudoku board using backtracking"""
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(num, i, j):
                            self.board[i][j] = num
                            if self.solve_board():
                                return True
                            self.board[i][j] = 0
                    return False
        return True
    
    def remove_numbers(self, count):
        """Remove 'count' numbers from the board to create a puzzle"""
        cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
        random.shuffle(cells)
        
        for i in range(count):
            row, col = cells[i]
            self.board[row][col] = 0
    
    def get_cell_from_pos(self, pos):
        """Get cell coordinates from mouse position"""
        x, y = pos
        
        # Check if click is within the grid
        if (x < GRID_X_OFFSET or x >= GRID_X_OFFSET + GRID_SIZE * CELL_SIZE or
            y < GRID_Y_OFFSET or y >= GRID_Y_OFFSET + GRID_SIZE * CELL_SIZE):
            return None
        
        # Calculate cell coordinates
        col = (x - GRID_X_OFFSET) // CELL_SIZE
        row = (y - GRID_Y_OFFSET) // CELL_SIZE
        
        return (row, col)
    
    def is_conflict(self, row, col, num):
        """Check if placing num at (row, col) would create a conflict"""
        if num == 0:
            return False
            
        # Temporarily place the number
        original_value = self.board[row][col]
        self.board[row][col] = 0
        
        # Check if the number is valid in this position
        is_conflict = not self.is_valid(num, row, col)
        
        # Restore the original value
        self.board[row][col] = original_value
        
        return is_conflict
    
    def is_game_over(self):
        """Check if the game is over (board is complete and valid)"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = self.board[row][col]
                if value == 0 or value != self.solution[row][col]:
                    return False
        return True
    
    def draw_grid(self):
        """Draw the Sudoku grid"""
        # Draw cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = GRID_X_OFFSET + col * CELL_SIZE
                y = GRID_Y_OFFSET + row * CELL_SIZE
                
                # Determine cell color
                if self.selected_cell == (row, col):
                    cell_color = SELECTED_COLOR
                elif self.selected_cell and self.is_conflict(row, col, self.board[row][col]):
                    cell_color = CONFLICT_COLOR
                else:
                    cell_color = WHITE
                
                # Draw cell
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, cell_color, cell_rect)
                
                # Draw number if not empty
                if self.board[row][col] != 0:
                    # Determine text color
                    if self.initial_board[row][col] != 0:
                        text_color = BLACK
                    elif self.is_conflict(row, col, self.board[row][col]):
                        text_color = RED
                    else:
                        text_color = BLUE
                    
                    text = self.font.render(str(self.board[row][col]), True, text_color)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)
                
                # Draw cell border
                pygame.draw.rect(self.screen, GRAY, cell_rect, 1)
        
        # Draw thick borders for 3x3 boxes
        for i in range(0, GRID_SIZE + 1, 3):
            # Horizontal lines
            pygame.draw.line(
                self.screen, BLACK,
                (GRID_X_OFFSET, GRID_Y_OFFSET + i * CELL_SIZE),
                (GRID_X_OFFSET + GRID_SIZE * CELL_SIZE, GRID_Y_OFFSET + i * CELL_SIZE),
                3
            )
            # Vertical lines
            pygame.draw.line(
                self.screen, BLACK,
                (GRID_X_OFFSET + i * CELL_SIZE, GRID_Y_OFFSET),
                (GRID_X_OFFSET + i * CELL_SIZE, GRID_Y_OFFSET + GRID_SIZE * CELL_SIZE),
                3
            )
    
    def draw_buttons(self):
        """Draw control buttons"""
        button_y = GRID_Y_OFFSET + GRID_SIZE * CELL_SIZE + 30
        
        # New Game button
        new_game_rect = pygame.Rect(GRID_X_OFFSET, button_y, 120, 40)
        pygame.draw.rect(self.screen, LIGHT_GRAY, new_game_rect)
        pygame.draw.rect(self.screen, BLACK, new_game_rect, 2)
        new_game_text = self.small_font.render("New Game", True, BLACK)
        text_rect = new_game_text.get_rect(center=new_game_rect.center)
        self.screen.blit(new_game_text, text_rect)
        
        # Difficulty buttons
        diff_x = GRID_X_OFFSET + 140
        for difficulty in ["easy", "medium", "hard"]:
            diff_rect = pygame.Rect(diff_x, button_y, 80, 40)
            
            # Highlight current difficulty
            if difficulty == self.difficulty:
                pygame.draw.rect(self.screen, GREEN, diff_rect)
            else:
                pygame.draw.rect(self.screen, LIGHT_GRAY, diff_rect)
            
            pygame.draw.rect(self.screen, BLACK, diff_rect, 2)
            diff_text = self.small_font.render(difficulty.capitalize(), True, BLACK)
            text_rect = diff_text.get_rect(center=diff_rect.center)
            self.screen.blit(diff_text, text_rect)
            
            diff_x += 90
        
        # Check solution button
        check_rect = pygame.Rect(GRID_X_OFFSET + 410, button_y, 120, 40)
        pygame.draw.rect(self.screen, LIGHT_GRAY, check_rect)
        pygame.draw.rect(self.screen, BLACK, check_rect, 2)
        check_text = self.small_font.render("Check", True, BLACK)
        text_rect = check_text.get_rect(center=check_rect.center)
        self.screen.blit(check_text, text_rect)
        
        return new_game_rect, check_rect
    
    def draw_info(self):
        """Draw game information"""
        info_y = 50
        
        # Title
        title_text = self.font.render("SUDOKU", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, info_y))
        self.screen.blit(title_text, title_rect)
        
        # Game over message
        if self.game_over:
            win_text = self.font.render("Congratulations! You solved it!", True, GREEN)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, info_y + 40))
            self.screen.blit(win_text, win_rect)
    
    def handle_button_click(self, pos, new_game_rect, check_rect):
        """Handle button clicks"""
        x, y = pos
        
        # New Game button
        if new_game_rect.collidepoint(pos):
            self.new_game()
            return
        
        # Difficulty buttons
        button_y = GRID_Y_OFFSET + GRID_SIZE * CELL_SIZE + 30
        diff_x = GRID_X_OFFSET + 140
        for difficulty in ["easy", "medium", "hard"]:
            diff_rect = pygame.Rect(diff_x, button_y, 80, 40)
            if diff_rect.collidepoint(pos):
                self.difficulty = difficulty
                self.new_game()
                return
            diff_x += 90
        
        # Check solution button
        if check_rect.collidepoint(pos):
            self.game_over = self.is_game_over()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            new_game_rect, check_rect = self.draw_buttons()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        # Check if a button was clicked
                        self.handle_button_click(event.pos, new_game_rect, check_rect)
                        
                        # Otherwise, select a cell
                        cell = self.get_cell_from_pos(event.pos)
                        if cell and self.initial_board[cell[0]][cell[1]] == 0:
                            self.selected_cell = cell
                
                elif event.type == pygame.KEYDOWN:
                    if self.selected_cell and not self.game_over:
                        row, col = self.selected_cell
                        
                        # Only allow editing non-initial cells
                        if self.initial_board[row][col] == 0:
                            # Number keys 1-9
                            if pygame.K_1 <= event.key <= pygame.K_9:
                                num = event.key - pygame.K_0
                                self.board[row][col] = num
                            
                            # Delete/Backspace to clear cell
                            elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                                self.board[row][col] = 0
                            
                            # Arrow keys to navigate
                            elif event.key == pygame.K_UP and row > 0:
                                self.selected_cell = (row - 1, col)
                            elif event.key == pygame.K_DOWN and row < GRID_SIZE - 1:
                                self.selected_cell = (row + 1, col)
                            elif event.key == pygame.K_LEFT and col > 0:
                                self.selected_cell = (row, col - 1)
                            elif event.key == pygame.K_RIGHT and col < GRID_SIZE - 1:
                                self.selected_cell = (row, col + 1)
            
            # Check if game is over
            if not self.game_over and self.is_game_over():
                self.game_over = True
            
            # Draw everything
            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_buttons()
            self.draw_info()
            
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()

if __name__ == "__main__":
    try:
        game = Sudoku()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)