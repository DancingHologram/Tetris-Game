from constants import *
import pygame
import random

class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# choose chape from the 7 tetronimos
def get_random_shape():
    shape_type = random.choice(TETROMINO_SHAPES.keys())
    color = COLORS[shape_type]
    return Shape(BOARD_WIDTH // 2, 0, color)

# image of the shape on the board
def draw_shape(screen, shape):
    shape_matrix = TETROMINO_SHAPES[shape.color]
    for i in range(len(shape_matrix)):
        for j in range(len(shape_matrix[i])):
            if shape_matrix[i][j] == 1:
                pygame.draw.rect(screen, shape.color, (BOARD_ORIGIN_X + (shape.x + j) * TILE_SIZE, BOARD_ORIGIN_Y + (shape.y + i) * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# rotate the shape clockwise
def rotate_shape(shape):
    shape_matrix = ROTATION_STATES[shape.color]
    rotated_matrix = list(zip(*shape_matrix[::-1]))
    ROTATION_STATES[shape.color] = rotated_matrix

# define the shape class and its properties (position, color, rotation state)
def create_shape():
    shape_type = random.choice(list(TETROMINO_SHAPES.keys()))
    color = COLORS[shape_type]
    return Shape(BOARD_WIDTH // 2, 0, color)