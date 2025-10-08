import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = (SCREEN_WIDTH - GRID_WIDTH * CELL_SIZE) // 2
GRID_Y_OFFSET = (SCREEN_HEIGHT - GRID_HEIGHT * CELL_SIZE) // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Tetris piece shapes
SHAPES = [
    # I-piece
    [['.....',
      '..#..',
      '..#..',
      '..#..',
      '..#..']],
    
    # O-piece
    [['.....',
      '.....',
      '.##..',
      '.##..',
      '.....']],
    
    # T-piece
    [['.....',
      '.....',
      '.#...',
      '###..',
      '.....']],
    
    # S-piece
    [['.....',
      '.....',
      '.##..',
      '##...',
      '.....']],
    
    # Z-piece
    [['.....',
      '.....',
      '##...',
      '.##..',
      '.....']],
    
    # J-piece
    [['.....',
      '.#...',
      '.#...',
      '##...',
      '.....']],
    
    # L-piece
    [['.....',
      '..#..',
      '..#..',
      '.##..',
      '.....']]
]

# Colors for each piece
SHAPE_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.game_over = False
        self.score = 0
        
    def get_new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(SHAPE_COLORS)
        return {
            'shape': shape,
            'color': color,
            'x': GRID_WIDTH // 2 - 2,
            'y': 0,
            'rotation': 0
        }
    
    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(
                    GRID_X_OFFSET + x * CELL_SIZE,
                    GRID_Y_OFFSET + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(self.screen, self.grid[y][x], rect)
                pygame.draw.rect(self.screen, GRAY, rect, 1)
    
    def draw_piece(self):
        piece = self.current_piece
        shape = piece['shape'][piece['rotation']]
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '#':
                    rect = pygame.Rect(
                        GRID_X_OFFSET + (piece['x'] + x) * CELL_SIZE,
                        GRID_Y_OFFSET + (piece['y'] + y) * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    pygame.draw.rect(self.screen, piece['color'], rect)
                    pygame.draw.rect(self.screen, GRAY, rect, 1)
    
    def check_collision(self, dx=0, dy=0, rotation=None):
        piece = self.current_piece
        if rotation is None:
            rotation = piece['rotation']
        
        shape = piece['shape'][rotation]
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '#':
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT):
                        return True
                    
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return True
        
        return False
    
    def lock_piece(self):
        piece = self.current_piece
        shape = piece['shape'][piece['rotation']]
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '#':
                    grid_y = piece['y'] + y
                    grid_x = piece['x'] + x
                    
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = piece['color']
        
        self.clear_lines()
        self.current_piece = self.get_new_piece()
        
        if self.check_collision():
            self.game_over = True
    
    def clear_lines(self):
        lines_to_clear = []
        
        for y in range(GRID_HEIGHT):
            if all(cell != BLACK for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
            self.score += 100
    
    def rotate_piece(self):
        piece = self.current_piece
        new_rotation = (piece['rotation'] + 1) % len(piece['shape'])
        
        if not self.check_collision(rotation=new_rotation):
            piece['rotation'] = new_rotation
    
    def move_piece(self, dx, dy):
        if not self.check_collision(dx, dy):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
            return True
        return False
    
    def drop_piece(self):
        if not self.move_piece(0, 1):
            self.lock_piece()
    
    def draw_info(self):
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (50, 50))
        
        if self.game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
    
    def run(self):
        fall_time = 0
        fall_speed = 500  # milliseconds
        
        running = True
        while running:
            dt = self.clock.tick(30)
            fall_time += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.__init__()
                    else:
                        if event.key == pygame.K_LEFT:
                            self.move_piece(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move_piece(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.drop_piece()
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            while self.move_piece(0, 1):
                                pass
                            self.lock_piece()
            
            if not self.game_over:
                if fall_time >= fall_speed:
                    self.drop_piece()
                    fall_time = 0
            
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece()
            self.draw_info()
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    try:
        game = Tetris()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)