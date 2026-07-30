import turtle
import math
import tkinter
import random
import time
import ctypes


__ = turtle.Turtle()
screen = __.screen

__.speed(0)
__.color('white')
__.pensize(1.3)
__.pu()
__.hideturtle()
gd = turtle.Turtle()
gd.speed(0)
gd.color('#222222')
gd.hideturtle()

screen.tracer(0)

screen.update()
print("Press, drag and release to shoot Orbitals. \n Use WASD to move, \n Your mouse wheel to zoom in and out. \n Press G to increase gravity \n Press R to reset \n Use arrow up to increase spawn mass of Orbitals and arrow down to decrease.")
screen.tracer(0)
screen.setup(700,700)
screen.title('Orbital')

root = screen.getcanvas().winfo_toplevel()
root.update()
HWND = ctypes.windll.user32.GetForegroundWindow()
ctypes.windll.dwmapi.DwmSetWindowAttribute(HWND, 20, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int))

screen.bgcolor('black')
colors = ['orange', '#FFE44D', 'blue', 'light blue', 'white']
objs = []
G = 30

spawn_mass = 100
spawn_size = spawn_mass / 10

camera_x = 0
camera_y = 0

zoom = 1

class Particle:
    def __init__(self, mass, vx, vy, x, y, old_x, old_y, radius, color):
        # store parameters on the instance

        self.turt = turtle.Turtle()
        self.turt.speed(0)
        self.mass = mass
        self.vx = vx
        self.vy = vy
        self.x = x
        self.y = y
        self.old_x = old_x
        self.old_y = old_y
        self.radius = radius
        if color == None:
            self.color = random.choice(colors)
        else:
            self.color = color


        # optional: register the instance in an external list
        

        # initialize turtle appearance / position

        objs.append(self)
        
        self.turt.pu()
        self.turt.shape('circle')
        self.turt.color(self.color)
        self.turt.shapesize(self.radius / 10, self.radius / 10)
        self.turt.goto(x, y)
 
Particle(3000, 0, 0, 0, 0, 0, 0, 30, '#FFE44D')




def distance(obj1,obj2):
    return math.sqrt(((obj2.x ) - (obj1.x )) ** 2 + ((obj2.y ) - (obj1.y )) **2)

def force(obj1, obj2):
    return G * ((obj1.mass * obj2.mass) / (distance(obj1, obj2) ** 2))

def angle(obj1, obj2):
    return math.atan2(obj2.y - obj1.y, obj2.x - obj1.x)

def velo_update(obj, force, angle, mass):
    vx = obj.vx
    vy = obj.vy
    Fx = force * math.cos(angle)
    Fy = force * math.sin(angle)
    ax = Fx / mass
    ay = Fy / mass
    vx += ax
    vy += ay
    obj.vx = vx
    obj.vy = vy
    return 

def merge(obj1, obj2):
    global objs # (obj1 mass * vx plus obj2 mass * vx) divided by total mass\
    new_m = obj1.mass + obj2.mass # mass of the merged object
    biggest = max(obj1.mass, obj2.mass)
    if biggest == obj1.mass:
        biggest = obj1
    else:
        biggest = obj2
    new_vx = (obj1.mass * obj1.vx + obj2.mass * obj2.vx) / (obj1.mass + obj2.mass)
    new_vy = (obj1.mass * obj1.vy + obj2.mass * obj2.vy) / (obj1.mass + obj2.mass)
    obj1.turt.hideturtle()
    obj2.turt.hideturtle()
    Particle(new_m, new_vx, new_vy, obj1.x, obj1.y, obj1.x, obj1.y, math.sqrt((obj1.radius ** 2) + obj2.radius ** 2), biggest.color)
    objs.remove(obj1)
    objs.remove(obj2)

def passed_through(obj1, obj2):
    if obj1.x == obj1.old_x and obj1.y == obj1.old_y:
        return False

    x_percent = (obj2.x - obj1.old_x) / (obj1.x - obj1.old_x)
    y_percent = (obj2.y - obj1.old_y) / (obj1.y - obj1.old_y)
    if x_percent == y_percent and x_percent <= 1.0 and x_percent >= 0.0 and y_percent <= 1.0 and y_percent >= 0.0:
        return True
    else:
        return False

def merge_collisions():
    merged = False
    for body in objs:
        if merged == True:
            break
        for other in objs:
            if other == body:
                continue
            else:
                if distance(body, other) < body.radius + other.radius or passed_through(body, other):
                    merge(body, other)
                    merged = True
                    break

def update():
    global objs
    global camera_x
    global camera_y

    merge_collisions()

    for body in objs:
        for other in objs:
            
            if body == other:
                continue
            else:
                F = force(body, other)
                A = angle(body, other)
                velo_update(body, F, A, body.mass)


        body.old_x = body.x
        body.old_y = body.y
        for i in range(5):    
            body.x += body.vx / 5
            body.y += body.vy / 5
            merge_collisions()

        body.turt.goto((body.x - camera_x) * zoom, (body.y - camera_y) * zoom)
        body.turt.shapesize((body.radius / 10) * zoom, (body.radius / 10) * zoom)
    merge_collisions()

    gd.clear()
    
    sw = screen.window_width()
    sh = screen.window_height()
    spacing = 80  # universe units between grid lines

    # visible universe range (left edge to right edge)
    left = camera_x - (sw / 2) / zoom
    right = camera_x + (sw / 2) / zoom

    # find the first grid line at or past the left edge
    first_line = int(left // spacing) * spacing

    gd.pensize(1)

    for gx in range(first_line, int(right) + spacing, spacing):
        screen_x = (gx - camera_x) * zoom
        gd.pu()
        gd.goto(screen_x, sh / 2)
        gd.pd()
        gd.goto(screen_x, -sh / 2)
    
    # visible universe range (left edge to right edge)
    up = camera_y - (sh / 2) / zoom
    down = camera_y + (sh / 2) / zoom

    # find the first grid line at or past the left edge
    first_line = int(up // spacing) * spacing

    gd.pensize(1)

    for gx in range(first_line, int(down) + spacing, spacing):
        screen_y = (gx - camera_y) * zoom
        gd.pu()
        gd.goto(-sw / 2, screen_y)
        gd.pd()
        gd.goto(sw / 2, screen_y)

    if keys['w'] == True:
        camera_y += 15 / zoom
    if keys['a'] == True:
        camera_x -= 15 / zoom
    if keys['s'] == True:
        camera_y -= 15/ zoom
    if keys['d'] == True:
        camera_x += 15 / zoom
    screen.update()
    screen.ontimer(update, t=30)

state = None
press_x = None
press_y = None
def sling(event):

    global state
    global press_x
    global press_y
    
    swhh = screen.window_height() / 2
    swwh = screen.window_width() / 2
    if state == None:
        press_x = (event.x  - swwh) / zoom + camera_x
        press_y = (swhh - event.y) / zoom  + camera_y
        state = press_x, press_y
    else:
        release_x = (event.x - swwh) / zoom + camera_x
        release_y = (swhh - event.y) / zoom + camera_y
        state = None
        vx = (press_x - release_x) * 0.2
        vy = (press_y - release_y) * 0.2
        __.clear()
        Particle(spawn_mass, vx, vy, press_x, press_y, press_x, press_y, spawn_size, None) 


    return

def aim(event):
    swhh = screen.window_height() / 2
    swwh = screen.window_width() / 2
    __.clear()
    __.pu()
    __.goto((press_x - camera_x) * zoom, (press_y  - camera_y) * zoom)
    __.pd()
    __.goto((event.x - swwh) , (swhh - event.y) )
    screen.update()

keys = {'w': False, 'a': False, 's': False, 'd': False}

def w():
    keys['w'] = True
def a():
    keys['a'] = True
def s():
    keys['s'] = True
def d():
    keys['d'] = True

def w_r():
    keys['w'] = False
def a_r():
    keys['a'] = False
def s_r():
    keys['s'] = False
def d_r():
    keys['d'] = False

def mass_up(event):
    global spawn_mass
    global spawn_size
    if spawn_mass + 10 < 1000:
        spawn_mass += 10
        spawn_size = spawn_mass / 10

def mass_down(event):
    global spawn_mass
    global spawn_size
    if spawn_mass - 10 > 0:
        spawn_mass -= 10
        spawn_size = spawn_mass / 10

def reset():
    for i in range(len(objs)):
        objs[i].turt.hideturtle()

    objs.clear()
    global camera_x
    global camera_y
    global G
    global zoom
    camera_x = 0
    camera_y = 0
    zoom = 1
    G = 10
    Particle(3000,0,0,0,0,0,0,30, None)

def g_up():
    global G
    G += 10

def zoom_fun(event):
    global zoom
    if event.delta < 0:
        zoom /= 1.1
    elif event.delta > 0:
        zoom *= 1.1
    if zoom < 0.1:
        zoom = 0.1
    if zoom > 4.1:
        zoom = 4.1

canvas = screen.getcanvas()

canvas.bind("<MouseWheel>", zoom_fun)
canvas.bind('<ButtonPress-1>', sling)
canvas.bind('<ButtonRelease-1>', sling)
canvas.bind('<B1-Motion>', aim)
canvas.bind('<Up>', mass_up)
canvas.bind('<Down>', mass_down)

screen.onkeypress(w, 'w')
screen.onkeypress(a, 'a')
screen.onkeypress(s, 's')
screen.onkeypress(d, 'd')

screen.onkeyrelease(w_r, 'w')
screen.onkeyrelease(a_r, 'a')
screen.onkeyrelease(s_r, 's')
screen.onkeyrelease(d_r, 'd')

screen.onkeypress(reset, 'r')
screen.onkeypress(g_up, 'g')

screen.listen()
update()
turtle.done()