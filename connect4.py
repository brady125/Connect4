import numpy as np
import pygame
import sys
import math

# starts pygame
pygame.init()
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ROW_COUNT = 6
COLUMN_COUNT = 7

# get the size of a certain square for the board (think of the tables as boxes)
SQUARE_SIZE = 100
# cuts a big whole into the square so the connect 4 coin can be visible
RADIUS = int(SQUARE_SIZE/2 - 5)
# Game over font
myfont = pygame.font.SysFont('monospace', 75)

# creates board using numpy module


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# puts a users piece on the board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for x in range(ROW_COUNT):
        if board[x][col] == 0:
            return x

# in order for the numbers to start at the bottom of the board I flipped the board on the x-axis


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and \
                    board[row][col+1] == piece and \
                    board[row][col+2] == piece and \
                    board[row][col+3] == piece:
                return True
    # Check vertical locations for win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and \
                    board[row+1][col] == piece and \
                    board[row+2][col] == piece and \
                    board[row+3][col] == piece:
                return True
    # Checked positively sloped locations for win
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][col] == piece and \
                    board[row+1][col+1] == piece and \
                    board[row+2][col+2] == piece and \
                    board[row+3][col+3] == piece:
                return True
    # Checked negatively slopped diaganols
    for col in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT-3):
            if board[row][col] == piece and \
                    board[row+1][col+1] == piece and \
                    board[row+2][col+2] == piece and \
                    board[row+3][col+3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r *
                             SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2.0)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(
                    c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE+SQUARE_SIZE/2.0)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE+SQUARE_SIZE/2.0)), RADIUS)

    pygame.display.update()


board = create_board()
game_over = False
turn = 0

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE

size = (width, height)
RADIUS = int(SQUARE_SIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()


while not game_over:

    for event in pygame.event.get():
        # pygame commands
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            # the circle is visible to the user before placing
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(
                    screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(
                    screen, YELLOW, (posx, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # so that the ending move doesn't have the circle still visible
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (30, 10))
                        game_over = True
            else:

                posx = event.pos[0]
                # have the columns go 0-7
                col = int(math.floor(posx/SQUARE_SIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    if winning_move(board, 2):
                        label = myfont.render("Player 1 wins!!", 1, YELLOW)
                        screen.blit(label, (30, 10))
                        game_over = True
                        break
            print_board(board)
            draw_board(board)
            # make turns
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
