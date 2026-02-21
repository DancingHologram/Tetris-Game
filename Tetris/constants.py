import pygame

# screen display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# game board
TILE_SIZE = 40
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_ORIGIN_X = (SCREEN_WIDTH - (BOARD_WIDTH * TILE_SIZE)) // 2
BOARD_ORIGIN_Y = (SCREEN_HEIGHT - (BOARD_HEIGHT * TILE_SIZE)) // 2

# color palette dictionary
COLORS = {
    "I": (0, 255, 255),     # Cyan (I-piece)
    "O": (255, 255, 0),     # Yellow (O-piece)
    "T": (128, 0, 128),     # Purple (T-piece)
    "S": (0, 255, 0),       # Green (S-piece)
    "Z": (255, 0, 0),       # Red (Z-piece)
    "J": (0, 0, 255),       # Blue (J-piece)
    "L": (255, 165, 0)      # Orange (L-piece)
}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Config filepaths
HIGH_SCORE_FILE = "high_score.bin"
CONTROLS_CONFIG_FILE = "controls.bin"

# Button colors
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_DISABLED_COLOR = (70, 70, 70)
BUTTON_TEXT_COLOR = WHITE
BUTTON_BORDER_COLOR = WHITE

# Margins and boundaries
MARGIN = 20
LEFT_BOUNDARY = MARGIN
RIGHT_BOUNDARY = SCREEN_WIDTH - MARGIN
TOP_BOUNDARY = MARGIN
BOTTOM_BOUNDARY = SCREEN_HEIGHT - MARGIN

# Tetromino shapes
TETROMINO_SHAPES = {
    "I":[
        [[1,1,1,1]],
        [[1],[1],[1],[1]],
        [[1,1,1,1]],
        [[1],[1],[1],[1]]
    ],
    "O":[
        [[1,1],[1,1]],
        [[1,1],[1,1]],
        [[1,1],[1,1]],
        [[1,1],[1,1]]
    ],
    "T":[
        [[0,1,0],
         [1,1,1]],                                  # Rotation 0
        [[1,0],
         [1,1],
         [1,0]],                                    # Rotation 1
        [[1,1,1],
         [0,1,0]],                                  # Rotation 2
        [[0,1],
         [1,1],
         [0,1]]                                     # Rotation 3
    ],
    "S":[
        [[0,1,1],
         [1,1,0]],                                   # Rotation 0
        [[1,0],
         [1,1],
         [0,1]],                                     # Rotation 1
        [[0,1,1],
         [1,1,0]],                                   # Rotation 2
        [[1,0],
         [1,1],
         [0,1]]                                      # Rotation 3
    ],
    "Z":[
        [[1,1,0],
         [0,1,1]],                                   # Rotation 0
        [[0,1],
         [1,1],
         [1,0]],                                     # Rotation 1
        [[1,1,0],
         [0,1,1]],                                   # Rotation 2
        [[0,1],
         [1,1],
         [1,0]]                                      # Rotation 3
    ],
    "J":[
        [[1,0,0],
         [1,1,1]],                                   # Rotation 0
        [[1,1],
         [1,0],
         [1,0]],                                     # Rotation 1
        [[1,1,1],
         [0,0,1]],                                   # Rotation 2
        [[0,1],
         [0,1],
         [1,1]]                                      # Rotation 3
    ],
    "L":[
        [[0,0,1],
         [1,1,1]],                                   # Rotation 0
        [[1,0],
         [1,0],
         [1,1]],                                     # Rotation 1
        [[1,1,1],
         [1,0,0]],                                   # Rotation 2
        [[1,1],
         [0,1],
         [0,1]]                                      # Rotation 3
    ]
}

# Game mechanics
DEFAULT_DROP_SPEED = 60
INITIAL_SPAWN_X = BOARD_WIDTH // 2
INITIAL_SPAWN_Y = 0

# Scoring
SCORE_SINGLE_LINE = 100
SCORE_DOUBLE_LINE = 300
SCORE_TRIPLE_LINE = 500
SCORE_TETRIS = 800

# Default control maps
DEFAULT_CONTROLS = {
    'LEFT': pygame.K_LEFT,
    'RIGHT': pygame.K_RIGHT,
    'DOWN': pygame.K_DOWN,
    'ROTATE': pygame.K_UP,
    'HARD_DROP': pygame.K_SPACE,
    'PAUSE': pygame.K_p
}