axiom = "-X"
rules = {
    "X": "F+[[X]-X]-F[-FX]+X",
    "F": "FF"
}
step = 3
angle = 25
interations = 6  # repetitions (turns in the application of the rules)

def setup():
    size(600, 600)
    # generating the sequence
    starting_sequence = axiom
    for i in range(interations):
        sequence = ""
        for symbol in starting_sequence:
            replacement = rules.get(symbol, symbol)
            sequence = sequence + replacement
        starting_sequence = sequence
    # drawing the sequence    
    background(240, 240, 200)
    translate(100, 500)
    for symbol in sequence:
        if symbol == "F":
            line(0, 0, 0, -step)  # draw a line
            translate(0, -step)   # move the origin
        if symbol == "+":
            rotate(radians(-angle)) 
        if symbol == "-":
            rotate(radians(angle))  
        if symbol == "[":
            push_matrix()  # save the state (position and angle)
        if symbol == "]":
            pop_matrix()   # return to the last saved state
            
    save('out.png')