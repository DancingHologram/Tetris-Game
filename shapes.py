from constants import *
import random

class Shape:
    def __init__(self, x, y, shape_type):
        self.x = x
        self.y = y
        self.shape_type = shape_type
        self.rotation_state = 0  # 0, 1, 2, or 3
        self.color = COLORS[shape_type]
    
    def image(self):
        """Returns the 2D array of the current rotation state"""
        return TETROMINO_SHAPES[self.shape_type][self.rotation_state]
    
    def rotate(self):
        """Rotate the shape 90 degrees clockwise"""
        self.rotation_state = (self.rotation_state + 1) % 4
    
    def rotate_back(self):
        """Rotate the shape 90 degrees counter-clockwise"""
        self.rotation_state = (self.rotation_state - 1) % 4


# choose shape from the 7 tetrominoes
def get_random_shape():
    shape_type = random.choice(list(TETROMINO_SHAPES.keys()))
    return Shape(BOARD_WIDTH // 2 - 1, 0, shape_type)