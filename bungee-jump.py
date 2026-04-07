web vpython 3.2 
from vpython import *
from random import random

# ----------------------------- Scene Setup -----------------------------
scene.title = "Bungee Jump Simulation"
scene.width = 1000
scene.height = 600
scene.background = color.black
scene.range = 35
scene.center = vector(0,15,0)
scene.userspin = True
scene.userzoom = True
scene.userpan = True

# ----------------------------- Stars and Moon -----------------------------
for i in range(100):
    sphere(
        pos=vector(random()*200-100, random()*80+10, random()*200-100),
        radius=0.3,
        color=color.white,
        emissive=True
    )
moon = sphere(pos=vector(80,80,-50), radius=7, color=color.gray(0.9), emissive=True)

# ----------------------------- Ground and Building -----------------------------
ground = box(pos=vector(0,0,0), size=vector(60,1,60), color=vector(0.5,0.35,0.2))  # brownish
building = box(pos=vector(-10,15,0), size=vector(4,30,4), color=color.gray(0.5))
top_edge = vector(-8,30,0)

# ----------------------------- Jumper -----------------------------
head = sphere(pos=vector(0,0,0), radius=0.4, color=color.yellow)
body = cylinder(pos=vector(0,0,0), axis=vector(0,-1.2,0), radius=0.2, color=color.red)
arm_left = cylinder(pos=vector(0,-0.2,0), axis=vector(0.8,0.8,0), radius=0.07, color=color.red)
arm_right = cylinder(pos=vector(0,-0.2,0), axis=vector(-0.8,0.8,0), radius=0.07, color=color.red)
leg1 = cylinder(pos=vector(0,-1.2,0), axis=vector(0.2,-0.8,0), radius=0.07, color=color.red)
leg2 = cylinder(pos=vector(0,-1.2,0), axis=vector(-0.2,-0.8,0), radius=0.07, color=color.red)
jumper = compound([head, body, arm_left, arm_right, leg1, leg2])

# ----------------------------- Initial Position -----------------------------
jumper.pos = top_edge  # starts at anchor point
v = vector(0,0,0)      # initially at rest

# ----------------------------- Bungee Cord -----------------------------
cord = cylinder(pos=top_edge, axis=jumper.pos - top_edge, radius=0.15, color=color.cyan)

# ----------------------------- Physics Constants -----------------------------
g = vector(0,-9.8,0)
m = 70
k = 120
L0 = 10
b = 1.8
dt = 0.01
t = 0

# ----------------------------- Trackers -----------------------------
max_stretch = 0
max_g_force = 0
lowest_y = jumper.pos.y
lowest_reached = False

# ----------------------------- HUD Labels -----------------------------
live_info = label(pos=vector(-25,32,-10), height=14, box=False, color=color.white)
phase_info = label(pos=vector(25,32,-10), height=14, box=False, color=color.yellow)
fixed_info = label(pos=vector(0,-25,0), height=14, box=False, color=color.cyan)

# ----------------------------- Controls -----------------------------
running = True
def toggle_run(b):
    global running
    running = not running
    b.text = "Pause" if running else "Resume"

def restart():
    global jumper, v, t, max_stretch, max_g_force, lowest_y, lowest_reached
    jumper.pos = top_edge
    v = vector(0,0,0)
    t = 0
    max_stretch = 0
    max_g_force = 0
    lowest_y = jumper.pos.y
    lowest_reached = False
    live_info.text = ""
    phase_info.text = ""
    fixed_info.text = ""

scene.append_to_caption("\n")
button(text="Pause", bind=toggle_run)
button(text="Restart", bind=restart)
scene.append_to_caption("\n\n")

# ----------------------------- Simulation Loop -----------------------------
while True:
    rate(100)
    if not running:
        continue
    t += dt

    scene.center = jumper.pos  # camera follows jumper

    r_vec = jumper.pos - top_edge
    distance = mag(r_vec)

    # ---------------- Phase Detection ----------------
    if distance < L0:
        phase = "Phase 1: Free Fall"
    elif v.y < 0:
        phase = "Phase 2: Cord Stretching"
    else:
        phase = "Phase 3: Rebound / Oscillation"
    # ---------------- Forces ----------------
Fg = m * g
Fspring = vector(0,0,0)
stretch = 0

if distance > L0:
    stretch = distance - L0
    Fspring = -k * stretch * norm(r_vec)
    if stretch > max_stretch:
        max_stretch = stretch

Fdrag = -b * v
Fnet = Fg + Fspring + Fdrag

# ---------------- Motion Update ----------------
a = Fnet / m
v = v + a * dt
jumper.pos = jumper.pos + v * dt
current_g = mag(a)/9.8

if current_g > max_g_force:
    max_g_force = current_g

# Track lowest point
if jumper.pos.y < lowest_y:
    lowest_y = jumper.pos.y
if not lowest_reached and v.y > 0:
    lowest_reached = True

cord.axis = jumper.pos - top_edge

# ---------------- Stop Oscillation ----------------
# If speed and stretch are small, stop
if abs(v.y) < 0.05 and abs(distance - L0) < 0.05 and lowest_reached:
    v = vector(0,0,0)
    jumper.pos = jumper.pos  # Keep jumper at rest

# ---------------- Update HUD ----------------
live_info.text = (
    "Time: " + str(round(t,2)) + " s\n"
    + "Current Stretch: " + str(round(stretch,2)) + " m\n"
    + "Current G-Force: " + str(round(current_g,2)) + " g"
)

if lowest_reached:
    fixed_info.text = (
        "Max Stretch: " + str(round(max_stretch,2)) + " m\n"
        + "Max G-Force: " + str(round(max_g_force,2)) + " g\n"
        + "Lowest Point: " + str(round(lowest_y,2)) + " m"
    ) 
