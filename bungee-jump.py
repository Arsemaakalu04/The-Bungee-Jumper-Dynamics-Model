web vpython 3.2
from vpython import *
from random import random

# ----------------------------- Scene Setup -----------------------------
-------------------- Stars and Moon -----------------------------

ground = box(pos=vector(0,0,0), size=vector(60,1,60), color=vector(0.5,0.35,0.2))
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
ush
jumper.pos = top_edge + vector(0.5, 0, 0)
v = vector(1.5, 0, 0) 

# ----------------------------- Bungee Cord -----------------------------
cord = cylinder(pos=top_edge, axis=jumper.pos - top_edge, radius=0.1, color=color.cyan)


# Trackers
max_stretch = 0
max_g_force = 0
lowest_y = jumper.pos.y
lowest_reached = False

# Labels
live_info = label(pos=vector(-25,32,-10), height=14, box=False, color=color.white)
phase_info = label(pos=vector(25,32,-10), height=14, box=False, color=color.yellow)
fixed_info = label(pos=vector(0,-5,0), height=14, box=False, color=color.cyan)
record_info = label(pos=vector(40, 32, 10), box=False, height=15, color=color.yellow)

# ----------------------------- Simulation Loop -----------------------------
running = True

while True:
    rate(100)
    if not running: continue
    
    t += dt

    # Physics Calculations
    r_vec = jumper.pos - top_edge
    distance = mag(r_vec)

    # Forces
    Fg = m * g
    Fspring = vector(0,0,0)


    Fdrag = -b * v
    Fnet = Fg + Fspring + Fdrag

    if distance < L0:
        phase = " Stage 1 Free fall"
    elif v.y < 0:
        phase = " Stage 2 Cord streching"
    else:
        phase = " Stage 3 Rebound and oscillation"

    )
    record_info.text = "MAX G: " + round(max_g_force, 2) + "\nMAX STRETCH: " + round(max_stretch, 1) + "m"

   
