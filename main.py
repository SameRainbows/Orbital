import turtle
import math

t = turtle.Turtle() 
t.screen.setup(700,700)
screen = t.screen
objs = []

cam_x = 0
cam_y = 0


t.shape("circle")
t.shapesize(4,4)
t.speed(0) # 1:slowest, 3:slow, 5:normal, 10:fast, 0:fastest
t.pu()

objs.append([t, 100, 0, 0, 0, 0])



G = 1000
def distance(obj1, obj2): # r = √((x₂−x₁)² + (y₂−y₁)²)
    
    return math.sqrt((obj2[4]-obj1[4]) ** 2 + (obj2[5] - obj1[5]) ** 2)

def force(obj1, obj2): # F = G × (m₁ × m₂) / r²
    force = G * (obj1[1] * obj2[1]) / distance(obj1,obj2) ** 2
    return force

def direction(obj1,obj2): # θ = atan2(y₂−y₁, x₂−x₁)
    angle = math.atan2(obj2[5] - obj1[5] , obj2[4]- obj1[4])
    return angle

def velo_update(obj, force, angle, mass):    # Fx = F × cos(θ),  Fy = F × sin(θ)
    global vx
    global vy
    
    Fx = force * math.cos(angle)
    Fy = force * math.sin(angle)
    ax = Fx / mass
    ay = Fy / mass
    obj[2] += ax
    obj[3] += ay
    return 

def move():
    global objs
    for body in objs:
        for other in objs:
            if other == body:
                continue
            else:
                F = force(body, other)
                D = direction(body, other)
                velo_update(body, F, D, body[1])
        vx = body[2]
        vy = body[3]

        x = body[4]
        y = body[5]
        body[4] += vx
        body[5] += vy
        body[0].goto(body[4] - cam_x, body[5] - cam_y)
        
    screen.ontimer(move, t=1)
    

canvas = screen.getcanvas()
press_x = None
press_y = None


sling_state = None
def sling(event):
    global sling_state
    global press_x
    global press_y
    scww = canvas.winfo_width() / 2
    scwh = canvas.winfo_height() / 2

    if sling_state == None:
        press_x = (event.x - scww) + cam_x
        press_y = (scwh - event.y) + cam_y
        sling_state = press_x, press_y
    else:
        release_x = (event.x - scww) + cam_x
        release_y = (scwh - event.y) + cam_y
        sling_state = None
        vx = press_x - release_x
        vy = press_y - release_y
        new_body = turtle.Turtle()
        new_body.shapesize(1,1)
        new_body.color("orange")
        new_body.shape('circle')
        new_body.speed(0)
        new_body.penup()
        new_body.goto(press_x - cam_x, press_y - cam_y)
        objs.append([new_body, 1, vx, vy, press_x, press_y])
        
def w():
    global cam_y
    cam_y += 10
def a():
    global cam_x
    cam_x -= 10
def s():
    global cam_y
    cam_y -= 10
def d():
    global cam_x
    cam_x += 10
    

canvas.bind("<ButtonPress-1>", sling)
canvas.bind("<ButtonRelease-1>", sling)

screen.onkeypress(w, "w")
screen.onkeypress(a, "a")
screen.onkeypress(s, "s")
screen.onkeypress(d, "d")

screen.listen()


move()

turtle.done()
