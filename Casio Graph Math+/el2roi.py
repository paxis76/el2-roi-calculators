# Endless Legend 2 ROI (Casio Graph Math+)
# arrows move, EXE next field, digits type,
# DEL empties the field, x10^x resets all,
# AC quits.
from casioplot import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (225, 225, 225)
NAVY = (30, 40, 90)
GREEN = (0, 130, 60)
RED = (190, 30, 30)
SEL = (255, 225, 90)

# key codes (from the manual's key diagram)
DIG = {91: "0", 81: "1", 82: "2", 83: "3", 71: "4",
       72: "5", 73: "6", 61: "7", 62: "8", 63: "9",
       92: "."}
K_UP, K_DN, K_LT, K_RT = 14, 34, 23, 25
K_OK, K_EXE, K_DEL, K_RST = 24, 95, 64, 93

# name, color, weight in Dust
ROWS = (("Prod", (200, 110, 30), 3.0),
        ("Food", (90, 170, 60), 2.0),
        ("Dust", (220, 180, 0), 1.0),
        ("Sci", (40, 120, 220), 6.0),
        ("Infl", (150, 80, 180), 2.5))
N = 5
txt = [""] * (2 * N)
CX = (170, 280)   # left x of Cost / Gain cells
CWID = 96
RY, RH = 35, 18
BOXY, BOXH = 145, 35
shown = ["", "", "", "", None]  # texts on screen, box color


def rect(x, y, w, h, c):
  for j in range(y, y + h):
    for i in range(x, x + w):
      set_pixel(i, j, c)


def f(v):
  return "{:.1f}".format(v)


def val(i):
  s = txt[i]
  if s == "" or s == ".":
    return 0.0
  return float(s)


def cell(i, sel, fill=True):
  x = CX[i // N]
  y = RY + RH * (i % N)
  if fill:
    rect(x, y, CWID - 4, RH - 1, SEL if sel else WHITE)
  draw_string(x + 4, y + 1, txt[i] or "0", BLACK, "medium")


def static():
  clear_screen()
  rect(0, 0, 384, 16, NAVY)
  draw_string(6, 1, "Endless Legend 2 ROI", WHITE, "medium")
  rect(0, 17, 384, 16, GREY)
  draw_string(26, 18, "Res", BLACK, "medium")
  draw_string(100, 18, "Wt", BLACK, "medium")
  draw_string(CX[0] + 4, 18, "Cost", BLACK, "medium")
  draw_string(CX[1] + 4, 18, "Gain/t", BLACK, "medium")
  for r in range(N):
    name, col, w = ROWS[r]
    y = RY + RH * r
    rect(8, y + 4, 10, 10, col)
    draw_string(26, y + 1, name, BLACK, "medium")
    draw_string(100, y + 1, "x" + str(w), BLACK, "medium")
  rect(0, RY + RH * N + 1, 384, 1, BLACK)
  draw_string(8, 128, "as Prod", BLACK, "medium")
  draw_string(6, 182, "DEL:field   x10^x:reset all   EXE:next",
              BLACK, "small")


def result():
  cost = 0.0
  gain = 0.0
  for r in range(N):
    cost += val(r) * ROWS[r][2]
    gain += val(r + N) * ROWS[r][2]
  col = GREEN if gain > 0 else RED
  if gain > 0:
    t = cost / gain
    n = int(t)
    if n < t - 1e-9:
      n += 1
    l1 = "Payback: {} turns".format(n)
    l2 = "exact: " + f(t) + " turns"
  else:
    l1 = "No yield: no payback"
    l2 = ""
  new = [f(cost / 3), f(gain / 3), l1, l2]
  pos = [(CX[0] + 4, 128), (CX[1] + 4, 128), (8, BOXY + 2),
         (8, BOXY + 18)]
  if col != shown[4]:
    # box color changed: refill box, forget old box texts
    rect(0, BOXY, 384, BOXH, col)
    shown[2] = ""
    shown[3] = ""
    shown[4] = col
  for q in range(4):
    if new[q] != shown[q]:
      bg = WHITE if q < 2 else col
      fg = BLACK if q < 2 else WHITE
      x, y = pos[q]
      # erase old text by drawing it in the background color
      draw_string(x, y, shown[q], bg, "medium")
      draw_string(x, y, new[q], fg, "medium")
      shown[q] = new[q]


static()
for i in range(2 * N):
  cell(i, i == 0)
result()
show_screen()

i = 0
fresh = True  # next digit overwrites
last = 0
while True:
  k = getkey()
  if k == 0 or k == last:
    last = k
    continue
  last = k
  j = i
  chg = False
  fill = True
  if k in (K_DN, K_OK, K_EXE):
    j = (i + 1) % (2 * N)
  elif k == K_UP:
    j = (i - 1) % (2 * N)
  elif k == K_LT:
    j = i % N
  elif k == K_RT:
    j = i % N + N
  elif k == K_RST:
    for c in range(2 * N):
      txt[c] = ""
      cell(c, False)
    j = 0
    fresh = True
    chg = True
  elif k == K_DEL:
    txt[i] = ""
    fresh = False
    chg = True
  elif k in DIG:
    ch = DIG[k]
    s = "" if fresh else txt[i]
    # appending: old text is a prefix, no need to clear the cell
    fill = fresh or s == ""
    fresh = False
    if len(s) < 7 and (ch != "." or "." not in s):
      txt[i] = s + ch
    chg = True
  if j != i:
    cell(i, False)
    i = j
    fresh = True
    fill = True
  cell(i, True, fill)
  if chg:
    result()
  show_screen()
