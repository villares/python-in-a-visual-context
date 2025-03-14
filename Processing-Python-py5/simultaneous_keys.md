## Detecting simultaneous keystrokes

The issue of identifying simultaneously pressed keys can arise when we are developing an interactive *sketch*, and in particular if we are creating a game, where more people interact simultaneously using the keyboard, also whenever the interface becomes more complex and needs keys in combination.

### Understanding the problem

Running the following code you'll notice that the `key` variable points to a value that describes the last key that was pressed (or released) on the keyboard. This can be a problem if you need to show when **a** and **b** are pressed simultaneously.

Be sure to run it and try it out!

```python
def setup():
    size(256,256)
    text_align(CENTER, CENTER)
    text_size(20)
    stroke_weight(3)
        
def draw():
    background(200, 200, 0)
    
    if key == 'a':
        fill(200, 0, 0) 
        rect(64, 96, 64, 64)
        fill(255)
        text('a', 96, 128)
        
    if key == 'b':
        fill(0, 0, 200) 
        rect(128, 96, 64, 64)
        fill(255)
        text('b', 160, 128)
        
```

![](assets/teclas_simultaneas\_0.gif)

A modification can prevent a key from being displayed when it is released and also from appearing when it is no longer being pressed, but this still doesn't solve the problem of simultaneous keystrokes:

```python
    if is_key_pressed and key == 'a':
        fill(200, 0, 0) 
        rect(64, 96, 64, 64)
        fill(255)
        text('a', 96, 128)
        
    if is_key_pressed and key == 'b':
        fill(0, 0, 200) 
        rect(128, 96, 64, 64)
        fill(255)
        text('b', 160, 128)
```

### A first solution

The solutions to this issue involve creating a structure that stores the state of the keys, indicating whether the key is pressed at that moment, and that can be modified by the events of pressing or releasing a key. At first, for our example, the structure could simply be a pair of global variables, used as *flags* for the state of the keys, `a_pressed` and `b_pressed`.

```python

a_pressed = False
b_pressed = False

def setup():
    size(256,256)
    text_align(CENTER, CENTER)
    text_size(20)
    stroke_weight(3)
        
def draw():
    background(0, 200, 200)
    
    if a_pressed:
        fill(200, 0, 0) 
        rect(64, 96, 64, 64)
        fill(255)
        text('a', 96, 128)
        
    if b_pressed:
        fill(0, 0, 200) 
        rect(128, 96, 64, 64)
        fill(255)
        text('b', 160, 128)
        
def key_pressed():
    global a_pressed, b_pressed
    if key == 'a':
        a_pressed = True
    if key == 'b':
        b_pressed = True        

def key_released():
    global a_pressed, b_pressed
    if key == 'a':
        a_pressed = False
    if key == 'b':
        b_pressed = False        
```

![](assets/teclas_simultaneas\_1.gif)

#### Notes

- If you release a key when the *focus of* your operating system is not on the *sketch* window, the `key_released()` event will not be triggered, and the *sketch* will not know that the key has been released!

- In the final keyboard versions of the [PONG game in this repository](../pong), we used exactly this strategy, without which the gaming experience would be greatly impaired.

### A lot of keys

But what if the number of keys we want to identify is very large? Do we have to make a bunch of global variables and a bunch of `if` conditionals inside `key_pressed()` and `key_released`? That doesn't sound very elegant!

So let's explore a strategy of storing the keys that have been pressed in a data structure called a **set**, removing them from the set when they are released. It's worth noting that sets don't keep the order in which their items were added, and items are unique; a set never has duplicate items.

To add an item to a set we use `set.add(item)`, and to remove `set.discard(item)`. This last operation, *discard*, does nothing if the item doesn't exist in the set.

In Python, we can tell if an item exists within a collection (such as lists, tuples, deques and sets) with the keyword `in` used as an operator, and this is much more computationally efficient in a large set than in a large list or tuple! In the example below, if `'b' in keys_pressed` is true, the background turns black.

```python
pressed_keys = set()  # creates an empty set

def setup():
    size(512,256)
    text_align(CENTER, CENTER)
    text_size(20)
    stroke_weight(3)
        
def draw():
    if 'b' in pressed_keys:
        background(0)
    else:
        background(100, 0, 200)
    
    for i, k in enumerate(pressed_keys):
        x = i * 64
        fill(0, x, 255 - i * 32) 
        rect(x, 96, 64, 64)
        fill(255)
        text(str(k), x + 32, 128)
    
def key_pressed():
    pressed_keys.add(key)    
    
def key_released():
    pressed_keys.discard(key)
```

![](assets/teclas_simultaneas\_2.gif)

Did you see a `65535` in the middle of the keys?

It means that a *coded* key has been pressed, modifier keys, like `SHIFT`, and the arrows keys, mostly. These keys are treated slightly differently. When the `key` variable is equal to the `CODED` constant (`key == CODED` is `True`) you'll need to use the `key_code` variable to find out which key was pressed (or released), usually by comparing it with one of the following numeric constants:

`UP DOWN LEFT RIGHT ALT CONTROL SHIFT`

Note that `TAB`, `ENTER` and some other keys, that are not *coded*, were also not shown correctly in the previous example. Certain "normal", *not-coded* keys, which can be identified directly using the `key` variable, need to be found by comparing `key` with some special constants or *strings*:

    BACKSPACE '\b'
    TAB       '\t'
    ENTER     '\n'
    RETURN    '\r'
    ESC       '\x1b'
    DELETE    '\x7f'

Let's make some adjustments to the code to identify and display these keys more elegantly!

To do this, we'll use another data structure called a **dictionary** (or dict). This maps (creates a correspondence between) *keys* and *values*, and it's very quick to look up a value corresponding to a key in a Python dictionary.

If you know for sure that the key exists in the dictionary, you can look it up using the form `dictionary[key]`, but that can cause your program to stop and display an error, a *KeyError Exception*, if the key doesn't exist in the dictionary. When you're not sure if the key is there, or it's part of the strategy to look for keys that might not be there, then you can use `dictionary.get(key, value_if_there_is_no_key)`.

```python
pressed_keys = set()  # empty set
# dicionário {key: 'name shown'}
names = {UP: '↑',
         DOWN: '↓',
         LEFT: '←',
         RIGHT: '→',
         ALT: 'Alt',
         CONTROL: 'Ctrl',
         SHIFT: 'Shift',
         BACKSPACE: 'Bcksp',
         TAB: 'Tab',
         ENTER: 'Enter',
         RETURN: 'Return',
         ESC: 'Esc',
         DELETE: 'Del',
         524: 'Meta',
         525: 'Menu',
         65406: 'AltGr',
         155: 'Insert',
         36: 'Home',
         35: 'End',
         33: 'PgUp',
         34: 'PgDwn',
         144: 'NumLk',
         ' ': 'space',
         }

def setup():
    size(512, 256)
    text_align(CENTER, CENTER)
    text_size(15)
    stroke_weight(3)

def draw():
    # instead of 'b' the spacebar makes the background black
    if ' ' in pressed_keys:
        background(0)
    else:
        background(50, 200, 50)
    
    for i, k in enumerate(sorted(pressed_keys)):
        # checks for special key names
        n = names.get(k, k)  # if k not in dictionary show k!   
        x = i * 64
        fill(0, x / 2, 200)
        rect(x, 96, 64, 64)
        fill(255)
        text(n, x + 32, 128)

def key_pressed():
    if key != CODED:
        pressed_keys.add(key)
    else:
        pressed_keys.add(key_code)

    if key == ESC:
         print('ESC')
         intercept_escape()  # this stops your sketch from quitting with ESC!

def key_released():
    if key != CODED:
        pressed_keys.discard(key)
    else:
        pressed_keys.discard(key_code)
```

![](assets/teclas_simultaneas\_3.gif)

#### Notes

- Since certain keys modify the effect of others, for example `SHIFT` makes the `1` key appear as `!`, then certain sequences can bring strange results:

  Pressing `SHIFT`, then `1`, then releasing `SHIFT`, and finally releasing `1`, causes the sketch to miss the `!` key being "released". One possible solution is to keep track of only the `key_code` of the keys, which remains the same, and we can still convert the `key_code`, which is a number, into something more readable, in the case of keys that are "not coded" (`CODED` is `False`) , using `chr()`:

  ```python
  def key_pressed():
      if key != CODED:
          pressed_keys.add(chr(key_code))
      else:
          pressed_keys.add(key_code)

  def key_released():
      if key != CODED:
          pressed_keys.discard(chr(key_code))
      else:
          pressed_keys.discard(key_code) 
  ```
  Note that now `a` and `A` should appear as `A` and , `1` and `!` as `1`. Be careful and test to avoid surprises! On my computer, the `key_code` for `+` and `-` on the laterak numeric keypad, for example, appear as `k` and `m`.

- The Python built-in function `sorted()` was used to obtain a sorted list from the set of `pressed_keys`

- Check out py5's documentation on [`intercept_escape()`](https://py5coding.org/reference/sketch_intercept_escape.html) if you want to detect the `ESC` key and avoid letting it quit the sketch.

- In the dictionary I've added some key codes I've seen, being on Linux, the key codes and names may vary depending on your operating system.

### Combining strategies

The strategy of status indicators for keys, or adding and removing indicators for pressed keys in a *set* using `key_pressed()` and `key_released()` is good for knowing if a key is pressed at a given time, very useful especially for controls that can be pressed continuously.

On the other hand, *to toggle* a setting, something like switching an option on and off, for example, it may be better to use an indicator modified by a simple conditional in `keyTyped()``,key_pressed` `(`) or `key_released()`, to prevent a keystroke from triggering the action more than once.

In the example below, we'll use a dictionary to store a lot of information about two circles, including colours, and which keys can be used to change the position, plus a key to swap the outline colour for the fill colour, and vice versa.

Use `SHIFT` to turn the background colour animation on and off and the space bar to return the circles to their original position.

```python
pressed_keys = set()  # empty set
pa = {'x': 128, 'y': 128,
      'fill': color(0, 0, 200), 'stroke': 0,
      'up': 'W', 'down': 'S',
      'left': 'A', 'right': 'D',
      'inv': TAB}
pb = {'x': 384, 'y': 128,
      'fill': color(200, 0, 0), 'stroke': 255,
      'up': UP, 'down': DOWN,
      'left': LEFT, 'right': RIGHT,
      'inv': ENTER}
players = (pa, pb)
animate_bg = False
bg_color = 128

def setup():
    size(512, 256)
    text_align(CENTER, CENTER)
    text_size(15)
    stroke_weight(3)

def draw():
    global bg_color
    if animate_bg:
        bg_color = abs(bg_color + sin(frame_count / 60)) % 256
    background(bg_color)
    for p in players:
        # print(p)  # debug
        fill(p['fill'])
        stroke(p['stroke'])
        circle(p['x'], p['y'], 50)
        # Modify the player/circle's position
        if p['up'] in pressed_keys:
            p['y'] -= 1
        if p['down'] in pressed_keys:
            p['y'] += 1
        if p['left'] in pressed_keys:
            p['x'] -= 1
        if p['right'] in pressed_keys:
            p['x'] += 1

def key_pressed():
    pressed_keys.add(key_code if key == CODED else chr(key_code))
    for p in players:
        if p['inv'] in pressed_keys:
            p['fill'], p['stroke'] = p['stroke'], p['fill']

def key_released():
    global animate_bg
    pressed_keys.discard(key_code if key == CODED else chr(key_code))
    if key_code == SHIFT:
        animate_bg = not animate_bg
    if key == ' ':
        pa['x'], pa['y'] = 128, 128
        pb['x'], pb['y'] = 384, 128
```

![](assets/teclas_simultaneas\_4.gif)

#### Notes

- The key_typed`()` and key_pressed`()` functions are triggered as soon as the key is pressed, and are susceptible to the OS automatic repetition setting after the key has been held down for a while, while `key_released()` is triggered only when the key is released.

## Exercise

- Could you add a third circle to the code?
- Change the colour or size of the circles depending on which keys are pressed?
