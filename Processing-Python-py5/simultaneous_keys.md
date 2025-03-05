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

The solutions to this issue involve creating a structure that stores the state of the keys, indicating whether the key is pressed at that moment, and that can be modified by the events of pressing or releasing a key. At first, for our example, the structure could simply be a pair of global variables, used as*flags* for the state of the keys, `a_pressed` and `b_pressed`.

```python

a_apertada = False
b_apertada = False

def setup():
    size(256,256)
    text_align(CENTER, CENTER)
    text_size(20)
    stroke_weight(3)
        
def draw():
    background(0, 200, 200)
    
    if a_apertada:
        fill(200, 0, 0) 
        rect(64, 96, 64, 64)
        fill(255)
        text('a', 96, 128)
        
    if b_apertada:
        fill(0, 0, 200) 
        rect(128, 96, 64, 64)
        fill(255)
        text('b', 160, 128)
        
def key_pressed():
    global a_apertada, b_apertada
    if key == 'a':
        a_apertada = True
    if key == 'b':
        b_apertada = True        

def key_released():
    global a_apertada, b_apertada
    if key == 'a':
        a_apertada = False
    if key == 'b':
        b_apertada = False        
```

![](assets/teclas_simultaneas\_1.gif)

#### Notes

- If you release a key when the *focus of* your operating system is not on the *sketch* window, the `key_released()` event will not be triggered, and the *sketch* will not know that the key has been released!

- In the final keyboard versions of the [PONG game in this repository](../pong), we used exactly this strategy, without which the gaming experience would be greatly impaired.

### A lot of keys

But what if the number of keys we want to identify is very large? Do we have to make a bunch of global variables and a bunch of `if` conditionals inside `key_pressed()` and `key_released`? That doesn't sound very elegant!

So let's explore a strategy of storing the keys that have been pressed in a data structure called a*set*, removing them from the set when they are released. It's worth noting that sets don't keep the order in which their items were added, and items are unique; a set never has duplicate items.

To add an item to a set we use `set.add(item)`, and to remove `set.discard(item)`. This last operation, *discard*, does nothing if the item doesn't exist in the set.

In Python, we can tell if an item exists within a collection (such as lists, tuples, deques and sets) with the keyword `in` used as an operator, and this is much more computationally efficient in a large set than in a large list or tuple! In the example below, if `'b' in keys_pressed` is true, the background turns black.

```python
teclas_apertadas = set()  # conjunto (set) vazio

def setup():
    size(512,256)
    text_align(CENTER, CENTER)
    text_size(20)
    stroke_weight(3)
        
def draw():
    if 'b' in teclas_apertadas:
        background(0)
    else:
        background(100, 0, 200)
    
    for i, k in enumerate(teclas_apertadas):
        x = i * 64
        fill(0, x, 255 - i * 32) 
        rect(x, 96, 64, 64)
        fill(255)
        text(str(k), x + 32, 128)
    
def key_pressed():
    teclas_apertadas.add(key)    
    
def key_released():
    teclas_apertadas.discard(key)
```

![](assets/teclas_simultaneas\_2.gif)

Did you see a `65535` in the middle of the keys?

It means that a`CODED` key has been pressed, like `SHIFT`, for example. We need to remember that some keys are labelled slightly differently, the so-called *coded* keys. When `key == CODED` you need to use the `key_code` variable to find out which key was pressed (or released), usually by comparing it with a numeric constant like the one here:

`UP DOWN LEFT RIGHT ALT CONTROL SHIFT`

Note that `TAB`, `ENTER` and some other *uncoded* keys were also not shown correctly in the previous example. Certain non-coded keys, which can be identified using a `key`, need to be found by comparing the `key` with special constants or *strings*:

    BACKSPACE '\b'
    TAB       '\t'
    ENTER     '\n'
    RETURN    '\r'
    ESC       '\x1b'
    DELETE    '\x7f'

Let's make some adjustments to the code to identify and display these keys more elegantly!

To do this, we'll use another data structure called a **dictionary***(dict*). This maps (creates a correspondence between)*keys* and*values*. It's very quick to look up a value linked to a key in a dictionary.

If you know that the key exists in the dictionary, you can look it up using the form dictionary `[key]` (which gives an error if the key doesn't exist in the dictionary). When you're not sure if the key is there, or it's part of the strategy to look for keys that might not be there, then you use `dictionary.get(key, value_if_there_is_no_key)`.

```python
teclas_apertadas = set()  # conjunto (set) vazio
# dicionário {tecla: 'nome para mostrar'}
nomes = {UP: '↑',
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
         ' ': 'espaço',
         }

def setup():
    size(512, 256)
    text_align(CENTER, CENTER)
    text_size(15)
    stroke_weight(3)

def draw():
    # em vez de 'b' agora o espaço deixa o fundo preto
    if ' ' in teclas_apertadas:
        background(0)
    else:
        background(50, 200, 50)
    
    for i, tecla in enumerate(sorted(teclas_apertadas)):
        # tendo `tecla` no dicionário pega o 'nome para mostrar'
        n = nomes.get(tecla, tecla)  # se não tiver, devolve `tecla` mesmo!   
        x = i * 64
        fill(0, x / 2, 200)
        rect(x, 96, 64, 64)
        fill(255)
        text(n, x + 32, 128)

def key_pressed():
    if key != CODED:
        teclas_apertadas.add(key)
    else:
        teclas_apertadas.add(key_code)

    # No Processing tradicional é possível impedir que ESC feche o sketch... no py5 ainda não é possível.
    if key == ESC:
         print('ESC')     

def key_released():
    if key != CODED:
        teclas_apertadas.discard(key)
    else:
        teclas_apertadas.discard(key_code)
```

![](assets/teclas_simultaneas\_3.gif)

#### Notes

- Since certain keys modify the effect of others, for example `SHIFT` makes the `1` key appear as `!`, then certain sequences can bring strange results:

  `Pressing` SHIFT, then ` 1,  `then releasing `SHIFT`, and finally releasing `1`. causes the sketch to miss the `!` key being 'released'. One possible solution is to keep track of only the `key_code of` the keys, which always remains the same, but we can convert the `key_code`, which is a number, into something more readable, in the case of unencoded keys, using chr()\`:

  ```python
  def key_pressed(): if key != CODED: keys_tightened.add(chr(key_code)) else: keys_tightened.add(key_code)def key_released(): if key != CODED: keys_tightened.discard(chr(key_code)) else: keys_tightened.discard(key_code) 
  ```

  Note that now `a` and `A` should appear as `A` and , `1` and `!` `as1`. Stay tuned and test to avoid surprises! On my computer, the `key_code` for `+` and `-` on the side numeric keypad, for example, appear as `k` and `m`.

<!---->

- `Sorted()` was used to obtain a sorted list from the set of `pressed_keys`

<!-- - Dentro do `keyPressed()` no <glossary variable="Processing">Processing</glossary> modo Python tinha um pequeno truque que impedia o *sketch*  de ser interrompido pela tecla `ESC`, mas não funciona mais -->

- In the dictionary I've added some key codes I've seen, being on Linux, the key codes and names may vary depending on your operating system.

### Combining strategies

The strategy of status indicators for keys, or adding and removing indicators for pressed keys in a*set* using `key_pressed()` and `key_released()` is good for knowing if a key is pressed at a given time, very useful especially for controls that can be pressed continuously.

On the other hand, *to toggle* a setting, something like switching an option on and off, for example, it may be better to use an indicator modified by a simple conditional in `keyTyped()``,key_pressed` `(`) or `key_released()`, to prevent a keystroke from triggering the action more than once.

In the example below, we'll use a dictionary to store a lot of information about two circles, including colours, and which keys can be used to change the position, plus a key to swap the outline colour for the fill colour, and vice versa.

Use `SHIFT` to turn the background colour animation on and off and the space bar to return the circles to their original position.

```python
teclas_apertadas = set()  # conjunto (set) vazio
pa = {'x': 128, 'y': 128,
      'fill': color(0, 0, 200), 'stroke': 0,
      'sobe': 'W', 'desce': 'S',
      'esq': 'A', 'dir': 'D',
      'inv': TAB}
pb = {'x': 384, 'y': 128,
      'fill': color(200, 0, 0), 'stroke': 255,
      'sobe': UP, 'desce': DOWN,
      'esq': LEFT, 'dir': RIGHT,
      'inv': ENTER}
players = (pa, pb)
anima_fundo = False
cor_fundo = 128

def setup():
    size(512, 256)
    text_align(CENTER, CENTER)
    text_size(15)
    stroke_weight(3)

def draw():
    global cor_fundo
    if anima_fundo:
        cor_fundo = abs(cor_fundo + sin(frame_count / 60.)) % 256
    background(cor_fundo)
    for p in players:
        # print(p)  # debug
        fill(p['fill'])
        stroke(p['stroke'])
        ellipse(p['x'], p['y'], 50, 50)
        # Ajusta a posição dos círculos
        if p['sobe'] in teclas_apertadas:
            p['y'] -= 1
        if p['desce'] in teclas_apertadas:
            p['y'] += 1
        if p['esq'] in teclas_apertadas:
            p['x'] -= 1
        if p['dir'] in teclas_apertadas:
            p['x'] += 1

def key_pressed():
    teclas_apertadas.add(key_code if key == CODED else chr(key_code))
    for p in players:
        if p['inv'] in teclas_apertadas:
            p['fill'], p['stroke'] = p['stroke'], p['fill']

def key_released():
    global anima_fundo
    teclas_apertadas.discard(key_code if key == CODED else chr(key_code))
    if key_code == SHIFT:
        anima_fundo = not anima_fundo
    if key == ' ':
        pa['x'], pa['y'] = 128, 128
        pb['x'], pb['y'] = 384, 128
```

![](assets/teclas_simultaneas\_4.gif)

#### Notes

- The key_typed`()` and key_pressed`()` functions are triggered as soon as the key is pressed, and are susceptible to automatic repetition after the key has been held down for a while, while `key_released()` is triggered only when the key is released.

## Exercise

- Could you add a third circle to the code?
- Change the colour or size of the circles depending on which keys are pressed?
