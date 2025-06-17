axiom = "X"
rules = {"X": "F+[[X]-X]-F[-FX]+X",
         "F": "FF"
          }
step = 10
angle = 25
interations = 4  # the substitution rules are applied 4 time
xo, yo = 300, 500

def setup():
    global sequence
    size(600, 600)
    sequence = generate_sequence(interations, axiom, rules)
    print(len(sequence))

def draw():
    background(240, 240, 200)
    translate(xo, yo)
    draw_sequence(sequence, step, angle)

def generate_sequence(num, axiom, rules):
    """
    Generate an L-System sequence from a starting sequence (axiom),
    repeating a number (num) of times the replacements described
    by a dictionary (rules);
    """
    starting_sequence = axiom
    for i in range(num):
        new_sequence = ""
        for symbol in starting_sequence:
            replacement = rules.get(symbol, symbol)
            new_sequence = new_sequence + replacement
        starting_sequence = new_sequence
    return new_sequence

def draw_sequence(symbols, step, angle):
    """
    Draw from reading a sequence of symbols according to 
    some "drawing rules" for each symbol. Size is controlled 
    by a step value, and the rotations by an angle value.
    """
    for symbol in symbols:
        if symbol == 'X':  
            pass  # does nothing
        
        if symbol == "F":
            line(0, 0, 0, -step)
            translate(0, -step)
        if symbol == "+":
            rotate(radians(angle))
        if symbol == "-":
            rotate(radians(-angle))
        if symbol == "[":
            push_matrix()
        if symbol == "]":
            pop_matrix()

def key_pressed():
    global step, angle, interations, sequence
    if key == 'z':
        step -= 1  # step = step - 1
    if key == 'x':
        step += 1
    if key == 'a':
        angle -= 1
    if key == 's':
        angle += 1
    if key == 'q':
        interations -= 1
        sequence = generate_sequence(interations, axiom, rules)
        print(len(sequence))
    if key == 'w':
        interations += 1
        sequence = generate_sequence(interations, axiom, rules)
        print(len(sequence))