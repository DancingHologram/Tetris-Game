# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

# Colors
COLORS = {
    'I': (0, 255, 255),   # Cyan
    'O': (255, 255, 0),   # Yellow
    'T': (128, 0, 128),   # Purple
    'S': (0, 255, 0),     # Green
    'Z': (255, 0, 0),     # Red
    'J': (0, 0, 255),     # Blue
    'L': (255, 165, 0)    # Orange
}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# margins and screen boundaries
MARGIN = 40
LEFT_BOUNDARY = MARGIN
RIGHT_BOUNDARY = SCREEN_WIDTH - MARGIN
TOP_BOUNDARY = MARGIN
BOTTOM_BOUNDARY = SCREEN_HEIGHT - MARGIN

# Tetris Constants
TILE_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_ORIGIN_X = (SCREEN_WIDTH - BOARD_WIDTH * TILE_SIZE) // 2
BOARD_ORIGIN_Y = (SCREEN_HEIGHT - BOARD_HEIGHT * TILE_SIZE) // 2

# Tetromino shapes
TETROMINO_SHAPES = {
    'I': [[1, 1, 1, 1]],

    'O': [[1, 1],
          [1, 1]],

    'T': [[0, 1, 0],
          [1, 1, 1]],

    'S': [[0, 1, 1],
          [1, 1, 0]],

    'Z': [[1, 1, 0],
          [0, 1, 1]],

    'J': [[1, 0, 0],
          [1, 1, 1]],

    'L': [[0, 0, 1],
          [1, 1, 1]]
} 

# tetromino rotation states
ROTATION_STATES = {
    'I': [[[1, 1, 1, 1]],
          [[1],
           [1],
           [1],
           [1]]],
    'O': [[[1, 1],
           [1, 1]]],
    'T': [[[0, 1, 0],
           [1, 1, 1]],
          [[1, 0],
           [1, 1],
           [1, 0]],
          [[1, 1, 1],
           [0, 1, 0]],
            [[0, 1],
            [0, 1],
            [0, 1]]],
    'S': [[[0, 1, 1],
           [1, 1, 0]],
          [[1, 0],
           [1, 1],
           [0, 1]]],
    'Z': [[[1, 1, 0],       
           [0, 1, 1]],
          [[0, 1],
           [1, 1],
           [1, 0]]],
    'J': [[[1, 0, 0],
           [1, 1, 1]],
          [[1, 1],
            [1, 0],
            [1, 0]],
            [[1, 1, 1],
            [0, 0, 1]],
            [[0, 1],
            [0, 1],
            [1, 1]]],
    'L': [[[0, 0, 1],
           [1, 1, 1]],
          [[1, 0],
           [1, 0],
           [1, 1]],
          [[1, 1, 1],
           [1, 0, 0]],
          [[1, 1],
           [0, 1],
           [0, 1]]]
}

# game states
MENU = 'menu'
SETTINGS = 'settings'
SCORES = 'scores'
GAME = 'game'