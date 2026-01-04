"""
To run this you'll need py5 (py5coding.org) with an imported mode runner
More about this at https://abav.lugaralgum.com/como-instalar-py5/index-EN.html

Use arrows to play, up arrow to rotate, "s" key to restart.
"""

well = {}  # a dictionary for the walls and already fallen piecess
falling_piece = []   # will contain ((x,y), color) tuples, the piece components
pieces = (
    [((x, y), 'green'  ) for x, y in ((6, 0), (7, 0), (6, 1), (7, 1))], # O
    [((x, y), 'blue'   ) for x, y in ((4, 0), (5, 0), (6, 0), (6, 1))], # J
    [((x, y), 'yellow' ) for x, y in ((4, 1), (5, 1), (6, 1), (6, 0))], # L
    [((x, y), 'red'    ) for x, y in ((4, 0), (5, 0), (6, 0), (7, 0))], # I
    [((x, y), 'cyan'   ) for x, y in ((5, 0), (5, 1), (6, 1), (6, 2))], # S
    [((x, y), 'magenta') for x, y in ((6, 0), (6, 1), (5, 1), (5, 2))], # N
    [((x, y), 'orange' ) for x, y in ((4, 0), (5, 0), (6, 0), (5, 1))], # T
)

W, H, S = 10, 20, 25   # well Width, well Height, single block size
frame_sample = 12  # a smaller number makes it faster, a bigger number slower
score = 0

def setup():
    size(525, 525)
    text_align(CENTER, CENTER)
    text_size(80)
    stroke(0)
    start()    # prepare well and first falling piece
    no_loop()  # to start paused
    
def start():
    global game_over, score
    game_over, score = False, 0
    well.clear()
    for y in range(H + 1):  # set vertical well wall blocks
        well[0, y] = 'darkgray'
        well[W + 1, y] = 'darkgray'
    for x in range(1, W + 1):  # set blocks at bottom of the well
        well[x, H] = 'darkgray'
    falling_piece[:] = random_choice(pieces)
    loop()  # reactivates draw if it is paused
    
def draw():
    global game_over, score
    background(0)
    for (x, y), block_color in list(well.items()) + falling_piece:
        fill(block_color)
        square(x * S, y * S, S)
    fill(200)
    text(score, W * S + (width - W * S) / 2, S * 2)
    if frame_count == 1:  # first game starts paused, with instructions
         draw_message('keys:\n←↓→ to move\n↑ to rotate\n"s" to start')
    elif game_over:
         draw_message('GAME OVER\npress "s"\nto restart')
         no_loop()  # pause draw on "game over"
    elif frame_count % frame_sample == 0:
        if check_move(falling_piece, 0, 1):
            move_falling_piece(0, 1)
        else:
            add_falling_piece_to_well()
            falling_piece[:] = random_choice(pieces)
            if not check_move(falling_piece):
                game_over = True
        r = check_filled_row()
        if r != -1:
            collapse_on_row(r)
            score += 1

def draw_message(msg):
    fill(0)
    text(msg, width / 2, height / 2)
    fill(255)
    text(msg, width / 2 - 3, height / 2 - 3)

def add_falling_piece_to_well():
    for (x, y), block_color in falling_piece:
        well[x, y] = block_color

def check_move(p, h=0, v=0):
    for (x, y), _ in p:
        if well.get((x + h, y + v)):
            return False
    return True

def move_falling_piece(h, v):
    falling_piece[:] = (((x + h, y + v), bc) for (x, y), bc in falling_piece)

def check_filled_row():
    for r in range(H):
        filled_blocks = 0
        for c in range(1, W + 1):
            if well.get((c, r)):
                filled_blocks += 1
        if filled_blocks == W:
            return r  # return first filled row found
    return -1  # tell that no filled row was found

def collapse_on_row(row):
    for r in range(row, -1, -1):  # moving upwards, starting from passed row
        for c in range(1, W):     # clear row
            well.pop((c, r), None)
        for c in range(1, W):     # move blocks down to it
            if block_color := well.get((c, r - 1)):  # get block from one row up
                well[c, r] = block_color
    
def rounded_falling_piece_centroid():
    positions = ((x, y) for (x, y), _ in falling_piece)
    xs, ys = zip(*positions)
    return (max(xs) + min(xs)) // 2, (max(ys) + min(ys)) // 2

def rotated_falling_piece():
    cx, cy = rounded_falling_piece_centroid() # causes -1 offset on y, corrected later...
    translated_fp = (((x - cx, y - cy), b) for (x, y), b in falling_piece) 
    return tuple(((y + cx, -x + cy + 1), b) for (x, y), b in translated_fp) # note cy + 1

def key_pressed():
    if key == 's':
        start()
    elif key_code == LEFT and check_move(falling_piece, -1, 0):
        move_falling_piece(-1, 0)
    elif key_code == RIGHT and check_move(falling_piece, 1, 0):
        move_falling_piece(1, 0)
    elif key_code == DOWN and check_move(falling_piece, 0, 1):
        move_falling_piece(0, 1)
    elif key_code == UP and check_move(rp := rotated_falling_piece()):
        falling_piece[:] = rp