from constants import *
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
