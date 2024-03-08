import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 700
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create a 3x3 grid with initial pieces
grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
grid[0][0] = grid[0][1] = grid[0][2] = 'O'
grid[2][0] = grid[2][1] = grid[2][2] = 'X'

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('X and O Game')

# Function to draw the grid
def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)

# Function to draw 'X' and 'O' pieces
def draw_pieces():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 'X':
                pygame.draw.line(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE),
                                 ((col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE), 2)
                pygame.draw.line(screen, BLACK, ((col + 1) * CELL_SIZE, row * CELL_SIZE),
                                 (col * CELL_SIZE, (row + 1) * CELL_SIZE), 2)
            elif grid[row][col] == 'O':
                pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2, 2)

# Function to check if the move is valid
def is_valid_move(row, col):
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and grid[row][col] == ' '

# Function to check for a winner
def check_winner():
    # Check rows and columns, excluding the first and last rows
    for i in range(1, GRID_SIZE - 1):
        if grid[i][0] == grid[i][1] == grid[i][2] != ' ' or grid[0][i] == grid[1][i] == grid[2][i] != ' ':
            return True

    # Check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2] != ' ' or grid[0][2] == grid[1][1] == grid[2][0] != ' ':
        return True

    return False

# Function to check if the grid is full (tie)
def is_full():
    return all(cell != ' ' for row in grid for cell in row)

# Function to check if there are obstacles between two positions
def no_obstacles_between(start_row, start_col, end_row, end_col):
    delta_row = end_row - start_row
    delta_col = end_col - start_col

    step_row = 1 if delta_row > 0 else -1 if delta_row < 0 else 0
    step_col = 1 if delta_col > 0 else -1 if delta_col < 0 else 0

    row, col = start_row + step_row, start_col + step_col

    while row != end_row or col != end_col:
        if grid[row][col] != ' ':
            return False
        row += step_row
        col += step_col

    return True

# Function to move the piece to the specified position
def move_piece(piece, row, col):
    grid[row][col] = piece

# Main game loop
running = True
current_piece = 'X'
selected_piece = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_row = mouse_y // CELL_SIZE
            clicked_col = mouse_x // CELL_SIZE

            if selected_piece is None:
                # Select a piece
                if grid[clicked_row][clicked_col] == current_piece:
                    selected_piece = (clicked_row, clicked_col)
            else:
                # Move the selected piece to an unoccupied space without jumping over other pieces
                if is_valid_move(clicked_row, clicked_col) and no_obstacles_between(selected_piece[0], selected_piece[1], clicked_row, clicked_col):
                    move_piece(current_piece, clicked_row, clicked_col)
                    grid[selected_piece[0]][selected_piece[1]] = ' '
                    selected_piece = None

                    # Check for a winner
                    if check_winner():
                        print(f"Player {current_piece} wins!")
                        running = False
                    elif is_full():
                        print("It's a tie!")
                        running = False

                    current_piece = 'O' if current_piece == 'X' else 'X'

    # Draw the grid and pieces
    screen.fill(WHITE)
    draw_grid()
    draw_pieces()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
