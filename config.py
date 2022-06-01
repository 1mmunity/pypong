# do not change if you dont know what these are
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (27, 27, 27)
ORANGE = (255, 179, 0)
YELLOW = (255, 213, 0)

SCALE_FACTOR = 1 # scale factor for the game, this is used to scale the game to a smaller screen or bigger, and maintaining the same aspect ratio
BALL_XVELOCITY_FASTER_OVER_TIME = (True, 1.03) # enable to make ball xvelocity faster every time it hits a paddle

BALL_RADIUS = 5*SCALE_FACTOR
Y_CHANGE_PADDLE = 8*SCALE_FACTOR
Y_CHANGE_BALL = 8*SCALE_FACTOR
BALL_VELOCITY_DEFAULT = 5*SCALE_FACTOR # x
TEXT1_SIZE = round(30*SCALE_FACTOR)
TEXT2_SIZE = round(20*SCALE_FACTOR)
TEXT3_SIZE = round(12*SCALE_FACTOR)
TEXT4_SIZE = round(8*SCALE_FACTOR)
HIT_SOUND = ('sounds/blip.mp3', .15) # sound, volume
LOSE_SOUND = ('sounds/hit.mp3', .05)
FONT_SOURCE = 'fonts/PressStart.ttf'
ICON_SOURCE = 'icons/pypong.png'

(PW, PH) = (10*SCALE_FACTOR, 100*SCALE_FACTOR)
(w, h) = (750*SCALE_FACTOR, 500*SCALE_FACTOR)