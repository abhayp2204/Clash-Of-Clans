from .variables import *

def print_canvas():
    for i in range(CANVAS_HEIGHT):
        if(not LINES[i]):
            # continue
            pass
        for j in range(CANVAS_WIDTH):
            # Print([CANVAS[i][j]]*1)
            print(CANVAS[i][j], end="")
        print()
        
def set_border():
    # Horizontal borders
    for x in range(0, CANVAS_WIDTH):
        CANVAS[0][x] = "═"
        CANVAS[CANVAS_HEIGHT-1][x] = "═"
        
    # Vertical borders
    for y in range(0, CANVAS_HEIGHT):
        CANVAS[y][0] = "║"
        CANVAS[y][CANVAS_WIDTH-1] = "║"
        
    # Corners
    CANVAS[0][0] = "╔"
    CANVAS[0][CANVAS_WIDTH-1] = "╗"
    CANVAS[CANVAS_HEIGHT-1][0] = "╚"
    CANVAS[CANVAS_HEIGHT-1][CANVAS_WIDTH - 1] = "╝"