from constants import TETROMINO_SHAPES, COLORS, INITIAL_SPAWN_X, INITIAL_SPAWN_Y
import random

class Shape:
    def __init__(self, x, y, shape_type, rotation_state, color):
        self.x = x
        self.y = y
        self.shape_type = shape_type
        self.rotation_state = rotation_state
        self.color = color

        # validate shape_type
        if shape_type not in TETROMINO_SHAPES:
            raise ValueError(f"Invalid shape type: {shape_type}")
        
    def __repr__(self):
        return f"Shape(type={self.shape_type}, rotation={self.rotation_state}, position=({self.x},{self.y}))"

    def image(self):
        # pick a tetromino from TETROMINO_SHAPES
        piece = TETROMINO_SHAPES[self.shape_type]
        safe_rotation = self.rotation_state % 4
        return piece[safe_rotation]
        
    def rotate(self):
        # rotate the piece 90 degrees clockwise
        self.rotation_state = (self.rotation_state + 1) % 4

    def rotate_back(self):
        # rotate the piece 90 degrees counter clockwise
        self.rotation_state = (self.rotation_state - 1) % 4

    def get_width(self):
        return len(self.image()[0])
    
    def get_height(self):
        return len(self.image())
    
    def get_bounding_box(self):
        pass # TODO: implement for collision detection

# factory function
def get_random_shape():
    shape_type = random.choice(list(TETROMINO_SHAPES.keys()))
    color = COLORS[shape_type]
    x = INITIAL_SPAWN_X
    y = INITIAL_SPAWN_Y

    return Shape(x, y, shape_type, 0, color)