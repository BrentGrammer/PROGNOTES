### Barnsley Fern
# good explanation of functions: https://www.youtube.com/watch?v=xoXe0AljUMA
# https://www.algorithm-archive.org/contents/barnsley/barnsley.html

import turtle
import random

watch_game = False

t = turtle.Turtle()
screen = t.getscreen()
if not watch_game:
    screen.tracer(0, 0)

t.speed(0)
t.color('green')
t.pensize(3)
t.penup()

x = 0
y = 0
iters = 5000
for n in range(iters):
    t.goto(65*x,37*y-252)
    t.pendown()
    t.circle(1) # draw a point
    t.penup()

    r = random.random()
    r = r*100
    xn = x
    yn = y
    if r < 1: # probability of 1%
        x = 0
        y = 0.16 * yn # moves points to single line
    elif r < 86: # 85% probability - moves points up and to the right
        x = 0.85 * xn + 0.04 * yn
        y = -0.04 * xn + 0.85 * yn + 1.6 #
    elif r < 93: # rotates points to the left of fern
        x = 0.20 * xn - 0.26 * yn
        y = 0.23 * xn + 0.22 * yn + 1.6
    else: # flips points to rotate to the right side of fern
        x = -0.15 * xn + 0.28 * yn
        y = 0.26 * xn + 0.24 * yn + 0.44

if not watch_game:
    turtle.update() # faster rendering - don't watch game

turtle.Screen().exitonclick()

    
    
