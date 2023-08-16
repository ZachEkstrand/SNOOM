import math

RES = WIDTH, HEIGHT = 1024, 600
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 30

PLAYER_ANGLE = 0
PLAYER_SPEED = 0.05
LOOK_SENSITIVITY = 1.5
PLAYER_ROT_SPEED = 800
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100
PLAYER_STARTING_AMMO = 15

FLOOR_COLOR = (134, 168, 203)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 32

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2