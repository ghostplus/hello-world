#initial code was taken from the Internet (move_keyboard.py)

import pygame
import pid_class as pid
import numpy as np

level1 = 100.0;
level2 = 200.0;
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
 
def draw_stick_figure(screen, x, y):
    # Head
    pygame.draw.ellipse(screen, BLACK, [1 + x, y, 10, 10], 0)
 
##    # Legs
##    pygame.draw.line(screen, BLACK, [5 + x, 17 + y], [10 + x, 27 + y], 2)
##    pygame.draw.line(screen, BLACK, [5 + x, 17 + y], [x, 27 + y], 2)
## 
##    # Body
##    pygame.draw.line(screen, RED, [5 + x, 17 + y], [5 + x, 7 + y], 2)
## 
##    # Arms
##    pygame.draw.line(screen, RED, [5 + x, 7 + y], [9 + x, 17 + y], 2)
##    pygame.draw.line(screen, RED, [5 + x, 7 + y], [1 + x, 17 + y], 2)

def draw_osbt(screen, a):
    pygame.draw.line(screen, BLACK, a[0], a[1], 2)

# Setup
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [700, 700]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0)
 

hold_mode = False 
hold_distance = 2.0

class pid_hold:
    
    def __init__(self, gain):
        self.north = pid.PID(gain)
        self.south = pid.PID(gain)
        self.east = pid.PID(gain)
        self.west = pid.PID(gain)

    def setPoints(self, sps):
        self.north.setPoint(sps[0])
        self.south.setPoint(sps[1])
        self.east.setPoint(sps[2])
        self.west.setPoint(sps[3])

    def update(self, pvs):
        return self.north.update(pvs[0]), self.south.update(pvs[1]), self.east.update(pvs[2]), self.west.update(pvs[3])               

pid_hold = pid_hold(1.0)
 
# Speed in pixels per frame
x_speed = 0
y_speed = 0
 
# Initial position
x_coord = 75
y_coord = 75

# Obstacles
a = [[0,50], [1000, 50]]
b = [[0,500], [1000, 500]]
#b = [[0,200], [1000, 200]]

c = [[10,0], [10, 700]]
d = [[500,0], [500, 700]]
#d = [[200,0], [200, 700]]

p = pid.PID(3.0, 0.4, 1.2)
p.setPoint(1.0)

r = pid.PID(3.0, 0.4, 1.2)
r.setPoint(1.0)

# -------- Main Program Loop -----------
while not done:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            # User pressed down on a key
 
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3 
            elif event.key == pygame.K_BACKSPACE:
                hold_mode = True
                once_set = True

        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT:
                x_speed = 0
            elif event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP:
                y_speed = 0
            elif event.key == pygame.K_DOWN:
                y_speed = 0
            elif event.key == pygame.K_BACKSPACE:
                hold_mode = False

    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
 
    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

    #ultrasonic
    north_o = abs(y_coord - a[0][1]) + np.random.uniform(0, 10)
    south_o = abs(y_coord - b[0][1]) + np.random.uniform(0, 10)
    print "North: " + str(north_o) + " South: " + str(south_o)

    west_o = abs(x_coord - c[0][0]) + np.random.uniform(0, 10)
    east_o = abs(x_coord - d[0][0]) + np.random.uniform(0, 10)
    print "West: " + str(west_o) + " East: " + str(east_o)    

    north = north_o
    south = south_o
    west = west_o
    east = east_o

    if (north_o == 0) and (south_o == 0):
        north = 1
        south = 1

    if (north_o > level1):
        north = level1
    if (south_o > level1):
        south = level1

    if (north - south) != 0:
        value = p.update(north / south)

    if (west == 0) and (east == 0):
        west = 1
        east = 1

    if (west > level1):
        west = level1
    if (east > level1):
        east = level1

    if (west - east) != 0:
        value2 = r.update(west / east)

    if (value > 1):
        p.setIntegrator(0)
        value = 1
    if (value2 > 1):
        r.setIntegrator(0)
        value2 = 1
    if (value < -1):
        p.setIntegrator(0)
        value = -1
    if (value2 < -1):
        r.setIntegrator(0)
        value2 = -1
        

    print value, value2
 
    # Move the object according to the speed vector.
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed
 
    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

    if (north - south) != 0:
        y_speed = -3 * value
        y_speed = 3 * value

    if (west - east) != 0:
        x_speed = -3 * value2
        x_speed = 3 * value2    
                
    if hold_mode == True:
        #x_speed = 0
        #y_speed = 0  
        #set once setpoints
        if once_set:
            pid_hold.setPoints([north_o, south_o, east_o, west_o])
            once_set = False
            
        act = pid_hold.update([north_o, south_o, east_o, west_o])
        
        if north_o > south_o:
            y_speed = act[0] / 100
        else:
            y_speed = -act[1] / 100
            
        if east_o > west_o:
            x_speed = -act[2] / 100
        else:
            x_speed = act[3] /100   
              
        print act
        
    #add noise 
    x_speed += np.random.uniform(-0.1, 0.1) 
    y_speed += np.random.uniform(-0.1, 0.1)     
     
        
        
 
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
 
    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
 
    draw_stick_figure(screen, x_coord, y_coord)
    draw_osbt(screen, a)
    draw_osbt(screen, b)
    draw_osbt(screen, c)
    draw_osbt(screen, d)
 
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 20 frames per second
    clock.tick(60)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
