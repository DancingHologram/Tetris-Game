import pygame
from constants import *
import shapes
import button

# drop tetronimos by one row
def drop(shape):
    shape.y += 1

# check for collision with the bottom of the board or other pieces
def check_collision(board, shape):
    for i in range(len(shape.image())):
        for j in range(len(shape.image()[i])):
            if shape.image()[i][j] == 1:
                if shape.y + i >= BOARD_HEIGHT or board[shape.y + i][shape.x + j] != 0:
                    return True
    return False

# lock the shape in place on the board
def lock_shape(board, shape):
    for i in range(len(shape.image())):
        for j in range(len(shape.image()[i])):
            if shape.image()[i][j] == 1:
                board[shape.y + i][shape.x + j] = shape.color

# clear completed lines and return the number of lines cleared
def clear_lines(board):
    lines_cleared = 0
    for i in range(len(board)):
        if all(x != 0 for x in board[i]):
            del board[i]
            board.insert(0, [0] * BOARD_WIDTH)
            lines_cleared += 1
    return lines_cleared

# check for game over condition
def check_game_over(board):
    for j in range(BOARD_WIDTH):
        if board[0][j] != 0:
            return True
    return False

# move the shape left or right
def move(shape, direction, board):
    if direction == 'left':
        shape.x -= 1
        if check_collision(board, shape):
            shape.x += 1
    elif direction == 'right':
        shape.x += 1
        if check_collision(board, shape):
            shape.x -= 1

# rotate the shape
def rotate(shape, board):
    shape.rotate()
    if check_collision(board, shape):
        shape.rotate()  # rotate back if there is a collision

# hard drop the shape
def hard_drop(shape, board):
    while not check_collision(board, shape):
        shape.y += 1
    shape.y -= 1  # move back up one row to the last valid position