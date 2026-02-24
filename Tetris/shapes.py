from constants import TETROMINO_SHAPES, COLORS, INITIAL_SPAWN_X, INITIAL_SPAWN_Y
import random

# Shape class
class Shape:
    def __init__(self, x, y, shape_type, rotation_state, color):
        # position
        # left top corner
        self.x = x
        # left top corner
        self.y = y
        # shape properties
        # type (I, O, T, S, Z, J, L)
        self.shape_type = shape_type
        # rotation state (0-3)
        self.rotation_state = rotation_state
        # color
        # set in constants by shape_type
        self.color = color

        # validate shape_type
        if shape_type not in TETROMINO_SHAPES:
            # invalid shape type
            raise ValueError(f"Invalid shape type: {shape_type}")

    # string representation    
    def __repr__(self):
        return f"Shape(type={self.shape_type}, rotation={self.rotation_state}, position=({self.x},{self.y}))"

    # get current image of the shape based on type and rotation
    def image(self):
        # pick a tetromino from TETROMINO_SHAPES
        piece = TETROMINO_SHAPES[self.shape_type]
        # choose correct rotation state
        safe_rotation = self.rotation_state % 4
        # return the 2D array
        return piece[safe_rotation]
        
    # rotate the shape clockwise
    def rotate(self):
        # rotate the piece 90 degrees clockwise
        self.rotation_state = (self.rotation_state + 1) % 4

    # rotate the shape counter clockwise
    def rotate_back(self):
        # rotate the piece 90 degrees counter clockwise
        self.rotation_state = (self.rotation_state - 1) % 4

    # get width and height of current shape image
    def get_width(self):
        # return number of columns
        return len(self.image()[0])
    
    def get_height(self):
        # return number of rows
        return len(self.image())
    
    def get_bounding_box(self):
        pass # TODO: implement for collision detection

# factory function
# creates a random shape at initial spawn position
def get_random_shape():
    # pick random shape type
    # use keys from TETROMINO_SHAPES as list
    shape_type = random.choice(list(TETROMINO_SHAPES.keys()))
    # get corresponding color
    color = COLORS[shape_type]
    # set initial position
    x = INITIAL_SPAWN_X
    y = INITIAL_SPAWN_Y
    # return the shape
    return Shape(x, y, shape_type, 0, color)