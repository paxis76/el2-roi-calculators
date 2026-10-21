# Endless Legend 2 ROI (NumWorks)
# Edit the table directly:
# arrows/OK/EXE move, digits type,
# Backspace empties the field,
# Shift then Backspace resets all,
# Back quits.
from math import ceil
from kandinsky import fill_rect, draw_string
from ion import *

# Weights: value of 1 unit in Dust.
# 1 Prod = 3 Dust = 1.5 Food = 0.5 Sci
# 1 Influence = 2.5 Dust
W_PROD = 3.0
W_FOOD = 2.0
W_DUST = 1.0
W_SCI = 6.0
W_INFL = 2.5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (225, 225, 225)
NAVY = (30, 40, 90)
GREEN = (0, 130, 60)
RED = (190, 30, 30)
SEL = (255, 225, 90)

DIGITS = (KEY_ZERO, KEY_ONE, KEY_TWO, KEY_THREE,
          KEY_FOUR, KEY_FIVE, KEY_SIX, KEY_SEVEN,
          KEY_EIGHT, KEY_NINE)
KEYS = DIGITS + (KEY_DOT, KEY_BACKSPACE, KEY_SHIFT,
                 KEY_UP, KEY_DOWN, KEY_LEFT,
                 KEY_RIGHT, KEY_OK, KEY_EXE)

# Rows: name, color, weight
ROWS = (("Prod", (200, 110, 30), W_PROD),
        ("Food", (90, 170, 60), W_FOOD),
        ("Dust", (220, 180, 0), W_DUST),
        ("Sci", (40, 120, 220), W_SCI),
        ("Infl", (150, 80, 180), W_INFL))
N = len(ROWS)
# 2*N cells: 0..N-1 = cost,
# N..2N-1 = gain/turn (row = i % N)
txt = [""] * (2 * N)

def f(v):
  return "{:.1f}".format(v)

def right(s, x, y, fg=BLACK, bg=WHITE):
  # Right-align: chars are 10 px wide
  draw_string(s, x - 10*len(s), y, fg, bg)

def val(i):
  s = txt[i]
  if s == "" or s == ".":
    return 0.0
  return float(s)

def cell(i, sel):
  x = 222 + 92*(i // N)
  y = 37 + 20*(i % N)
  bg = SEL if sel else WHITE
  fill_rect(x - 82, y, 84, 19, bg)
  right(txt[i] or "0", x, y + 1, BLACK, bg)

def static():
  fill_rect(0, 0, 320, 222, WHITE)
  fill_rect(0, 0, 320, 18, NAVY)
  draw_string("Endless Legend 2 ROI", 6, 0, WHITE, NAVY)
  fill_rect(0, 18, 320, 18, GREY)
  draw_string("Res", 24, 18, BLACK, GREY)
  draw_string("Wt", 80, 18, BLACK, GREY)
  right("Cost", 220, 18, BLACK, GREY)
  right("Gain/t", 312, 18, BLACK, GREY)
  for r in range(N):
    name, col, w = ROWS[r]
    y = 37 + 20*r
    fill_rect(8, y + 5, 10, 10, col)
    draw_string(name, 24, y + 1)
    draw_string("x" + str(w), 80, y + 1)
  fill_rect(0, 137, 320, 1, BLACK)
  draw_string("as Prod", 8, 139)
  draw_string("Bksp:field  Shift+Bksp:reset", 6, 204)

def result():
  cost = 0.0
  gain = 0.0
  for r in range(N):
    cost += val(r) * ROWS[r][2]
    gain += val(r + N) * ROWS[r][2]
  fill_rect(100, 139, 220, 18, WHITE)
  right(f(cost / W_PROD), 220, 139)
  right(f(gain / W_PROD), 312, 139)
  if gain > 0:
    t = cost / gain
    n = ceil(t - 1e-9)
    fill_rect(0, 160, 320, 42, GREEN)
    draw_string("Payback: {} turns".format(n),
                8, 162, WHITE, GREEN)
    draw_string("exact: " + f(t) + " turns",
                8, 182, WHITE, GREEN)
  else:
    fill_rect(0, 160, 320, 42, RED)
    draw_string("No yield: no payback",
                8, 172, WHITE, RED)

def getkey():
  # Wait for one key press + release
  while True:
    for k in KEYS:
      if keydown(k):
        while keydown(k):
          pass
        return k

def roi():
  static()
  for i in range(2 * N):
    cell(i, i == 0)
  result()
  i = 0
  fresh = True  # next digit overwrites
  shift = False
  while True:
    k = getkey()
    j = i
    if k == KEY_SHIFT:
      shift = True
      continue
    if k in (KEY_DOWN, KEY_OK, KEY_EXE):
      j = (i + 1) % (2 * N)
    elif k == KEY_UP:
      j = (i - 1) % (2 * N)
    elif k == KEY_LEFT:
      j = i % N
    elif k == KEY_RIGHT:
      j = i % N + N
    elif k == KEY_BACKSPACE and shift:
      # Reset all fields, back to the first
      for c in range(2 * N):
        txt[c] = ""
        cell(c, False)
      j = 0
      fresh = True
    elif k == KEY_BACKSPACE:
      txt[i] = ""
      fresh = False
    else:
      ch = "." if k == KEY_DOT else str(DIGITS.index(k))
      s = "" if fresh else txt[i]
      fresh = False
      if len(s) < 7 and (ch != "." or "." not in s):
        txt[i] = s + ch
    shift = False
    if j != i:
      cell(i, False)
      i = j
      fresh = True
    cell(i, True)
    result()

roi()
