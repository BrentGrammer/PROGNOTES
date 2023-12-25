import random
c="" # corner 
p="" # point

def turtle_setup(canv_width, canv_height):
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
    t.speed(0) #0 is the fastest speed, 10 is fast, 6 is normal, slow is 3, and 1 is slowest
    t.color("black")#can change the color of the dots here 
    #uncomment the below line and the last line if you do NOT want to watch the triangle being drawn 
    screen.tracer(0, 0) 
    
    return t

def midpoint(a, b):
    """ Return the midpoint between points a = (ax, ay) and b = (bx, by) """
    ax, ay = a
    bx, by = b
    mx = (ax + bx) / 2
    my = (ay + by) / 2
    return mx, my

def randopoint():
    """generates a random point given the window size specified in the system arguments"""
    xcoord= random.randint(0, canv_width) # rand x between 0 and 500
    ycoord= random.randint(0, canv_height) # rand y between 0 and 500
    randopoint = (xcoord, ycoord)
    return randopoint

def randocorner():
    """produces the coordinates of one of the three corners
    that has been determined by the window size from the system arguments"""
    randocorner=random.choice(corners)
    c = randocorner
    return c

if __name__ == "__main__":
    import turtle
    
    """uncomment the following 2 lines if you want to set canvas size from command line arguments"""
    #canv_width = int(sys.argv[1])
    #canv_height = int(sys.argv[2])
    
    """ if using command line arguments (above) comment out the following two lines, 
       otherwise you can use them to set the canvas size """
    canv_width = 500
    canv_height = 500
    
    t = turtle_setup(canv_width,canv_height)
    
    #establishes corners
    middlex= (canv_width/2) # i.e. 250
    topCorner= (middlex, canv_height) # (250, 500) middle top point
    bottomLeftCorner= (0,0)
    bottomRightCorner= (canv_width, 0) # (500, 0) 
    corners= [topCorner, bottomLeftCorner, bottomRightCorner]
    
    p= randopoint() #random starting point in the window - this is run once at the start of the game
    c= randocorner() #random corner of the triangle - recomputed on each loop in the game
    m= midpoint(p,c) #midpoint between point p and a random corner of the triangle 
    
    t.up()
   #use the below line to set the number of iterations, higher number = more dots and longer running time
    for i in range (100000):
        c=randocorner()
        m=midpoint(p,c)
        t.goto(m)
        
        if i > 5:
            # draw a point at the midpoint calculated for the current iteration
            t.pendown()
            t.dot(2) #can change the size of the dots here 
            t.penup()
        p=m
        
    turtle.update() # faster rendering - don't watch game
    turtle.Screen().exitonclick()