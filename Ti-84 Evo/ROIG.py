# EL2 ROI calculator (TI-84 Python)
# Graphic table version (ti_draw)
# Edit the table directly:
# arrows/enter move, digits type,
# clear empties the field, del
# resets all fields, mode quits.
from math import ceil
from ti_system import *
from ti_draw import *

# Weights: value of 1 unit of each
# resource, in Dust. Edit to taste.
# 1 Prod = 3 Dust = 1.5 Food = 0.5 Sci
W_PROD = 3.0
W_FOOD = 2.0
W_DUST = 1.0
W_SCI = 6.0
# 1 Influence = 2.5 Dust
W_INFL = 2.5

# wait_key() codes: TI-84 Evo
# (measured), then TI-84 Plus CE
# (from the CE guide).
K_RIGHT = (26, 1)
K_LEFT = (24, 2)
K_UP = (25, 3)
K_DOWN = (34, 4)
K_ENTER = (105, 5)
K_CLEAR = (45, 9)
K_QUIT = (22, 69)  # [mode]
K_DEL = (23, 10)
CHARS = {102: "0", 92: "1", 93: "2", 94: "3",
         82: "4", 83: "5", 84: "6", 72: "7",
         73: "8", 74: "9", 103: ".",
         142: "0", 143: "1", 144: "2", 145: "3",
         146: "4", 147: "5", 148: "6", 149: "7",
         150: "8", 151: "9", 141: "."}

# draw_text y is ~18 px below the
# top of the letters (measured on
# the device). Tune if text sits
# too high (raise) or low (lower).
TY = 20
TX = 6

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

# Resource rows: top, height, text offset
RY = 31
RH = 20
RT = 2

def cell(i, sel):
  x = 140 + 92*(i // N)
  y = RY + RH*(i % N)
  box(x, y + 1, 84, RH - 2, SEL if sel else WHITE)
  text(x + TX, y + RT, txt[i] or "0")

def static():
  clear()
  box(0, 0, 320, 15, NAVY)
  text(8, -2, "Endless Legend 2 ROI", WHITE)
  box(0, 15, 320, 15, GREY)
  text(24, 13, "Res")
  text(80, 13, "Wt")
  text(140 + TX, 13, "Cost")
  text(232 + TX, 13, "Gain/t")
  for r in range(N):
    name, col, w = ROWS[r]
    y = RY + RH*r
    box(8, y + 5, 10, 10, col)
    text(24, y + RT, name)
    text(80, y + RT, "x" + str(w))
  set_color(0, 0, 0)
  draw_line(0, 132, 319, 132)
  text(8, 133, "as Prod")
  text(8, 189, "CLEAR: field   DEL: reset all")

def result():
  cost = 0.0
  gain = 0.0
  for r in range(N):
    cost += val(r) * ROWS[r][2]
    gain += val(r + N) * ROWS[r][2]
  box(140, 134, 180, 14, WHITE)
  text(140 + TX, 133, f(cost / W_PROD))
  text(232 + TX, 133, f(gain / W_PROD))
  if gain > 0:
    t = cost / gain
    n = ceil(t - 1e-9)
    box(0, 149, 320, 40, GREEN)
    text(8, 151, "Payback: {} turns".format(n), WHITE)
    text(8, 169, "exact: " + f(t) + " turns", WHITE)
  else:
    box(0, 149, 320, 40, RED)
    text(8, 160, "No yield: no payback", WHITE)

def roi():
  static()
  for i in range(2 * N):
    cell(i, i == 0)
  result()
  i = 0
  fresh = True  # next digit overwrites
  while True:
    k = wait_key()
    j = i
    if k in K_QUIT:
      break
    elif k in K_CLEAR:
      txt[i] = ""
      fresh = False
    elif k in K_DOWN or k in K_ENTER:
      j = (i + 1) % (2 * N)
    elif k in K_UP:
      j = (i - 1) % (2 * N)
    elif k in K_LEFT:
      j = i % N
    elif k in K_RIGHT:
      j = i % N + N
    elif k in K_DEL:
      # Reset all fields, back to the first
      for c in range(2 * N):
        txt[c] = ""
        cell(c, False)
      j = 0
      fresh = True
    elif k in CHARS:
      ch = CHARS[k]
      s = "" if fresh else txt[i]
      fresh = False
      if len(s) < 7 and (ch != "." or "." not in s):
        txt[i] = s + ch
    if j != i:
      cell(i, False)
      i = j
      fresh = True
    cell(i, True)
    result()
  # No show_draw() here: it waits
  # for [clear] and looks frozen.
  clear()

roi()
