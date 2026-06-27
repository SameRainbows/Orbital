import turtle
import math

t = turtle.Turtle()
plt = turtle.Turtle()
k = turtle.Turtle()
t.screen.setup(700,700)

screen = t.screen
objs = []

t.shape("circle")
t.shapesize(2,2)
t.speed(0) # 1:slowest, 3:slow, 5:normal, 10:fast, 0:fastest
t.pu()

objs.append([t, 100, 0, 0])

plt.shape("circle")
plt.color("blue")
plt.shapesize(1,1)
plt.speed(0) # 1:slowest, 3:slow, 5:normal, 10:fast, 0:fastest
plt.pu()
objs.append([plt, 1, 26, -5])
plt.goto(100,100)

plt.pd()

k.shape("circle")
k.color("yellow")
k.shapesize(1,1)
k.speed(0) # 1:slowest, 3:slow, 5:normal, 10:fast, 0:fastest
k.pu()
objs.append([k, 1, 26, -5])
k.goto(-100,140)

G = 1000
def distance(t1, t2): # t1.distance(t2)
    
    return t1.distance(t2)

def force(obj1, obj2): # F = G × (m₁ × m₂) / r²
    force = G * (obj1[1] * obj2[1]) / distance(obj1[0], obj2[0]) ** 2
    return force

def direction(obj1,obj2): # θ = atan2(y₂−y₁, x₂−x₁)
    t1 = obj1[0]
    t2 = obj2[0]
    angle = math.atan2(t2.ycor() - t1.ycor(), t2.xcor() - t1.xcor())
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

        x = body[0].xcor()
        y = body[0].ycor()

        body[0].goto(x + vx, y + vy)

    screen.ontimer(move, t=1)
    """obj1 = objs[0]
    obj2 = objs[1]

    vx = obj2[2]
    vy = obj2[3]

    F = force(obj1, obj2)
    D = direction(obj2, obj1)
    velo_update(objs[1], F, D, obj2[1])

    x = obj2[0].xcor()
    y = obj2[0].ycor()
    
    obj2[0].goto(x + vx, y + vy)
    screen.ontimer(move, t=1)"""




print(objs)

print(force(objs[0], objs[1]))

print(direction(objs[1], objs[0]))

move()

turtle.done()
