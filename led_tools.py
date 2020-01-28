import Adafruit_WS2801 as ws
from random import randint 

dark = 0.4
WS_GREEN = ws.RGB_to_color(0, 0, 255)
WS_DGREEN = ws.RGB_to_color(0, 0, int(255*dark))
WS_RED = ws.RGB_to_color(255, 0, 0)
WS_DRED = ws.RGB_to_color(int(255*dark), 0, 0)
WS_YELLOW = ws.RGB_to_color(255, 0, 255)
WS_DYELLOW = ws.RGB_to_color(int(255*dark), 0, int(255*dark))
WS_BLUE = ws.RGB_to_color(0, 255, 0)
WS_DBLUE = ws.RGB_to_color(0, int(255*dark), 0)
WS_ORANGE = ws.RGB_to_color(255, 0, 60)
WS_DORANGE = ws.RGB_to_color(int(255*dark), 0, int(60*dark))
WS_CLEAR = ws.RGB_to_color(0, 0, 0)

PXL_CNT = 50
PXL_COL_CNT = 10

PXL_CLK = 18
PXL_DOUT  = 23
pixels = ws.WS2801Pixels(PXL_CNT, clk=PXL_CLK, do=PXL_DOUT)

led_matrix = []

def init_matrix():
    direction = 1
    for x in range(0, PXL_CNT/PXL_COL_CNT):
            led_matrix.append([])
            for y in range(0, PXL_COL_CNT):
                if direction == 1:
                    led_matrix[x].append(PXL_COL_CNT * x + y)
                else:
                    led_matrix[x].append(PXL_COL_CNT * x + PXL_COL_CNT - (y + 1))
            direction = direction * -1

def get_col_color(x, button):
    color = WS_CLEAR
    if button = False:
        if x == 0:
            color = WS_GREEN
        elif x == 1:
            color = WS_RED
        elif x == 2:
            color = WS_YELLOW
        elif x == 3:
            color = WS_BLUE
        elif x == 4:
            color = WS_ORANGE
    else:
        if x == 0:
            color = WS_DGREEN
        elif x == 1:
            color = WS_DRED
        elif x == 2:
            color = WS_DYELLOW
        elif x == 3:
            color = WS_DBLUE
        elif x == 4:
            color = WS_DORANGE
    return color

def move_pixel((new_x, new_y), (old_x, old_y)):        
    pixels.set_pixel(led_matrix[old_x][old_y], WS_CLEAR)
    if new_y >= 0: 
        pixels.set_pixel(led_matrix[new_x][new_y], get_col_color(new_x, False))
    pixels.show()

def drop_pixel((x, y)):
    move_pixel((x, y-1), (x, y))

def set_pixel((x, y)):
    set_pixel_clr(led_matrix[x][y], get_col_color(x, False))

def set_pixel_clr((x, y), color):
    if color == "rainbow":
        color = ws.RGB_to_color(randint(0,255), randint(0,255), randint(0,255))
    pixels.set_pixel(led_matrix[x][y], color)
    pixels.show()

def button_pixel_on(x):
    set_pixel_clr((x, PXL_COL_CNT-1), get_col_color(x, button=True))

def button_pixel_off(x):
    set_pixel_clr((x, PXL_COL_CNT-1), WS_CLEAR)