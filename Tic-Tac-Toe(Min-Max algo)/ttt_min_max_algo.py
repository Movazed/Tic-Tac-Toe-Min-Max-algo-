import sys      
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Define Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen Dimensions
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK)

# Game Board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Function to Draw Grid Lines
def draw_grid_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

# Function to Draw Figures (Circles and Crosses)
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, WHITE, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), 
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), 
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)

# Function to Mark a Square
def mark_square(row, col, player):
    board[row][col] = player
    
# Function to Check if a Square is Available
def is_square_available(row, col):
    return board[row][col] == 0

# Function to Check if the Board is Full
def is_board_full():
    return not (board == 0).any()

# Function to Check for a Win
def check_winner(player):
    # Vertical Check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    # Horizontal Check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # Diagonal Check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

# Minimax Algorithm for AI
def minimax(board, depth, is_maximizing):
    if check_winner(2):
        return 1
    elif check_winner(1):
        return -1
    elif is_board_full():
        return 0 
    
    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax(board, depth + 1, True)
                    board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

# Function to Determine the Best Move for AI
def find_best_move():
    best_score = -float('inf')
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)   
    if move:
        mark_square(move[0], move[1], 2)
        return True
    return False

# Function to Restart the Game
def restart_game():
    screen.fill(BLACK)
    draw_grid_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# Draw Initial Grid
draw_grid_lines()

# Game Loop Variables
current_player = 1
game_over = False

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE
                
            if is_square_available(mouseY, mouseX):
                mark_square(mouseY, mouseX, current_player)
                if check_winner(current_player):
                    game_over = True
                current_player = current_player % 2 + 1
                
                if not game_over and current_player == 2:
                    if find_best_move():
                        if check_winner(2):
                            game_over = True
                        current_player = current_player % 2 + 1
                
                if not game_over and is_board_full():
                    game_over = True
                        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                current_player = 1
                
    if not game_over:
        draw_figures()
    else:
        if check_winner(1):
            draw_figures()
            draw_grid_lines(GREEN)
        elif check_winner(2):
            draw_figures()
            draw_grid_lines(RED)
        else:
            draw_figures()
            draw_grid_lines(GRAY)
    
    pygame.display.update()
