# Endless Legend 2 ROI (TI-Nspire CX II)
# Edit the table directly:
# arrows/enter move, digits type,
# del deletes, clear empties the
# field, esc quits.
from math import ceil
from ti_system import *
from ti_draw import *

# Weights: value of 1 unit in Dust.
# 1 Prod = 3 Dust = 1.5 Food = 0.5 Sci
# 1 Influence = 2.5 Dust
W_PROD = 3.0
W_FOOD = 2.0
W_DUST = 1.0
W_SCI = 6.0
W_INFL = 2.5

# get_key() names. The guide only
# confirms digits and "esc"; the
# others are a best guess.
K_UP = ("up",)
K_DOWN = ("down",)
K_LEFT = ("left",)
K_RIGHT = ("right",)
K_NEXT = ("enter", "return", "tab")
K_DEL = ("del", "backspace")
K_CLEAR = ("clear",)
K_QUIT = ("esc",)
# Show the last key name in the
# title bar (for testing).
SHOW_KEY = False

# Text position in a row. Tune if
# the text sits too high or low.
TY = 14
TX = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (225, 225, 225)
NAVY = (30, 40, 90)
GREEN = (0, 130, 60)
RED = (190, 30, 30)
SEL = (255, 225, 90)

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

def box(x, y, w, h, c):
  set_color(c[0], c[1], c[2])
  fill_rect(x, y, w, h)

def text(x, y, s, c=BLACK):
  set_color(c[0], c[1], c[2])
  draw_text(x, y + TY, s)

def val(i):
  s = txt[i]
  if s == "" or s == ".":
    return 0.0
  return float(s)

def cell(i, sel):
  x = 138 + 90*(i // N)
  y = 37 + 17*(i % N)
  box(x, y, 82, 16, SEL if sel else WHITE)
  text(x + TX, y, txt[i] or "0")

def static():
  clear()
  box(0, 0, 318, 18, NAVY)
  text(6, 1, "Endless Legend 2 ROI", WHITE)
  box(0, 19, 318, 17, GREY)
  text(22, 19, "Res")
  text(76, 19, "Wt")
  text(138 + TX, 19, "Cost")
  text(228 + TX, 19, "Gain/t")
  for r in range(N):
    name, col, w = ROWS[r]
    y = 37 + 17*r
    box(6, y + 3, 10, 10, col)
    text(22, y, name)
    text(76, y, "x" + str(w))
  set_color(0, 0, 0)
  draw_line(0, 123, 317, 123)
  text(6, 125, "as Prod")
  text(6, 182, "Arrows/Enter: move")
  text(6, 196, "Del/Clear: delete  Esc: quit")

def result():
  cost = 0.0
  gain = 0.0
  for r in range(N):
    cost += val(r) * ROWS[r][2]
    gain += val(r + N) * ROWS[r][2]
  box(138, 125, 180, 16, WHITE)
  text(138 + TX, 125, f(cost / W_PROD))
  text(228 + TX, 125, f(gain / W_PROD))
  if gain > 0:
    t = cost / gain
    n = ceil(t - 1e-9)
    box(0, 144, 318, 35, GREEN)
    text(6, 145, "Payback: {} turns".format(n), WHITE)
    text(6, 161, "exact: " + f(t) + " turns", WHITE)
  else:
    box(0, 144, 318, 35, RED)
    text(6, 153, "No yield: no payback", WHITE)

def roi():
  use_buffer()
  static()
  for i in range(2 * N):
    cell(i, i == 0)
  result()
  paint_buffer()
  i = 0
  fresh = True  # next digit overwrites
  while True:
    k = get_key(1)  # waits for a key
    j = i
    if k in K_QUIT:
      break
    elif k in K_DOWN or k in K_NEXT:
      j = (i + 1) % (2 * N)
    elif k in K_UP:
      j = (i - 1) % (2 * N)
    elif k in K_LEFT:
      j = i % N
    elif k in K_RIGHT:
      j = i % N + N
    elif k in K_DEL:
      txt[i] = "" if fresh else txt[i][:-1]
      fresh = False
    elif k in K_CLEAR:
      txt[i] = ""
      fresh = False
    elif k in "0123456789." and len(k) == 1:
      s = "" if fresh else txt[i]
      fresh = False
      if len(s) < 7 and (k != "." or "." not in s):
        txt[i] = s + k
    if j != i:
      cell(i, False)
      i = j
      fresh = True
    cell(i, True)
    result()
    if SHOW_KEY:
      box(230, 0, 88, 18, NAVY)
      text(232, 1, str(k)[:8], WHITE)
    paint_buffer()

roi()
