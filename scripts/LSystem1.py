axiom = "F"
rules = {
    #"X": "F[+G[+X]]-G[-X]+X",
    'F': 'F[+F-F+FO]F[-F+F-FO]',
          }
step = 2
angle = 22
interations = 6  # the substitution rules are applied 4 time
xo, yo = 300, 500

def setup():
    global sequence
    size(600, 600)
    sequence = generate_sequence(interations, axiom, rules)
    print(len(sequence))

def draw():
    background(200, 240, 240)
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
        elif symbol == 'G':
            translate(0, -step) # a step without drwing
        elif symbol == "F":
            line(0, 0, 0, -step)
            translate(0, -step)
        elif symbol == "+":
            rotate(radians(angle))
        elif symbol == "-":
            rotate(radians(-angle))
        elif symbol == "[":
            push_matrix()
        elif symbol == "]":
            pop_matrix()
        elif symbol == 'O':
            push_style()
            fill(255)
            no_stroke()
            circle(0, 0, step * 2)
            pop_style()
            
def key_pressed():
    global step, angle, interations, sequence
    if key == 'z':
        step *= 2  # step = step - 1
    if key == 'x':
        step /= 2
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