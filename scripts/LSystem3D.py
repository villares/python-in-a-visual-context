from py5_tools import animated_gif

axiom = 'X'
rules = {
    'X': 'F+[[X]-X]-F[-FX]+X',
    'F': 'FF',
    }
passo = 5
angle = 25  # angle em graus
interations = 5

def setup():
    global sequence
    size(600, 600, P3D)
    starting_sequence = axiom
    for _ in range(interations):
        sequence = ""
        for symbol in starting_sequence:
            sequence += rules.get(symbol, symbol)
        starting_sequence = sequence
    print(len(sequence))
    animated_gif('LSystem-3D.gif', duration=0.1, frame_numbers=range(1, 361, 6))

def draw():
    background(240, 240, 200)
    stroke_weight(2)
    angle = 25  # changing this dinamycally is a fun... 
    translate(width / 2, height * 0.9)
    rotate_y(radians(frame_count))
    for symbol in sequence:
        if symbol == 'X':  
            pass  # X does nothing, you could try making it do something...
        elif symbol == 'F':   # else if 
                line(0, 0, 0, -passo)
                translate(0, -passo)
                rotate_y(radians(-angle))  # without this it will be all on a plane
        elif symbol == '+':
            rotate(radians(-angle)) 
        elif symbol == '-':
            rotate(radians(angle))
        elif symbol == '[':
            push_matrix()
        elif symbol == ']':
            pop_matrix()