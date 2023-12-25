import random
import time

from numba import jit


random_corner="" # corner 
random_start="" # point

def turtle_setup(canv_width, canv_height, draw_speed, watch_game=False):
    """ Set up the canvas and a turtle for creating dots. Return a turtle
        object in hidden state with its pen up. The canvas has size canv_width
        by canv_height, with a coordinate system where (0,0) is in the bottom
        left corner, and automatic re-drawing of the canvas is disabled so that
        turtle.update() must be called to update the drawing.
    """
    t = turtle.Turtle()
    screen = t.getscreen()
    screen.setup(canv_width, canv_height)
    screen.setworldcoordinates(0, 0, canv_width, canv_height)
    
    t.hideturtle()
    t.speed(draw_speed) #0 is the fastest speed, 10 is fast, 6 is normal, slow is 3, and 1 is slowest
    t.color("black")#can change the color of the dots here 
   
    if not watch_game:
        screen.tracer(0, 0) 
    
    return t

@jit(nopython=True)
def midpoint(a, b):
    """ Return the midpoint between points a = (ax, ay) and b = (bx, by) """
    ax, ay = a
    bx, by = b
    mx = (ax + bx) / 2
    my = (ay + by) / 2
    return mx, my

@jit(nopython=True)
def randopoint():
    """generates a random point given the window size specified in the system arguments"""
    xcoord= random.randint(0, canv_width) # rand x between 0 and 500
    ycoord= random.randint(0, canv_height) # rand y between 0 and 500
    randopoint = (xcoord, ycoord)
    return randopoint


def randocorner():
    """produces the coordinates of one of the three corners
    that has been determined by the window size from the system arguments"""
    randocorner=random.choice(corners) # corners defined in upper scope: top left and right corners of the grid
    c = randocorner
    return c

if __name__ == "__main__":
    import sys
    import turtle

    if len(sys.argv) > 1:
        watch_game = sys.argv[1]
    else:
        watch_game = ''
    watch_game = watch_game == 'watch'
    
    """ if using command line arguments (above) comment out the following two lines, 
       otherwise you can use them to set the canvas size """
    canv_width = 500
    canv_height = 500
    draw_speed = 1 # 1-10 1 is slowest, 10 fast, 0 is fastest
    
    t = turtle_setup(
        canv_width,
        canv_height,
        draw_speed, 
        watch_game
    )
    
    #establishes corners
    middlex= (canv_width/2) # i.e. 250
    topCorner= (middlex, canv_height) # (250, 500) middle top point
    bottomLeftCorner= (0,0)
    bottomRightCorner= (canv_width, 0) # (500, 0) 
    corners= [topCorner, bottomLeftCorner, bottomRightCorner]

    starttime = time.monotonic()
    
    random_start = randopoint() #random starting point in the window - recomputed on each iteration
    random_corner = randocorner() #random corner of the triangle - uses corners created above for bound
    halfway = midpoint(random_start,random_corner) #midpoint between point p and a random corner of the triangle 
    
    t.up()
    dot_size = 10

    iterations = 4 # default is 10000
    #use the below line to set the number of iterations, higher number = more dots and longer running time
    for i in range (iterations):
        random_corner=randocorner()
        print('p: ',random_start)
        halfway=midpoint(random_start,random_corner)
        t.goto(halfway)
        
        # if i > 5:
        # draw a point at the midpoint calculated for the current iteration
        t.pendown()
        t.dot(dot_size) #can change the size of the dots here 
        t.penup()

        random_start=halfway # update the random starting point to be halfway between the last start point and new random corner selected (for direction)
    
    endtime = time.monotonic()

    print(f'TIME TAKEN: {endtime-starttime}')

    if not watch_game:
        turtle.update() # faster rendering - don't watch game

    turtle.Screen().exitonclick()