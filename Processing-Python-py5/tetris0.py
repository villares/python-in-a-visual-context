well = {}
falling_piece = [
    ((2, 2), 'blue'), ((3, 2), 'blue'),
    ((4, 2), 'blue'), ((4, 3), 'blue')
]

W = 10
H = 20
S = 25

def setup():
    size(525, 525)
    for y in range(H + 1):
        well[0, y] = 'gray'
        well[W + 1, y] = 'gray'
    for x in range(1, W + 1):
        well[x, H] = 'gray'
    
def draw():
    background(0)
    for (x, y), block_color in list(well.items()) + falling_piece:
        fill(block_color)
        square(x * S, y * S, S)
        
    if frame_count % 10 == 0 and check_move(0, 1):
        move_piece(0, 1)
                
def check_move(h, v):
    for (x, y), _ in falling_piece:
        if well.get((x + h, y + v)):
            return False
    return True

def move_piece(h, v):
    falling_piece[:] = (((x + h, y + v), bc) for (x, y), bc in falling_piece)

