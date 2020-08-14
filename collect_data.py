import pygame
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
import numpy as np

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

starting_value = 1

while True:
    file_name = 'training_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along',starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)

        break
    
# -------- Main Program Loop -----------


def main(file_name,starting_value):
    file_name = file_name
    counter = 0
    starting_value = starting_value
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
        
    #last_time = time.time()
    paused = False

    print('STARTING!!!')
    while (True):
        if counter == 25:
            pygame.quit()
            break
        #
        # EVENT PROCESSING STEP
        #
        # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION
        screen.fill(WHITE)
        textPrint.reset()
        for event in pygame.event.get(): # User did something.
            if event.type == pygame.QUIT: # If user clicked close.
                #done = True # Flag that we are done so we exit this loop.
                break
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")
        if not paused:
            joystick_count = pygame.joystick.get_count()
            gta_screen = grab_screen(region=(0,40,800,640))
            #last_time = time.time()
            gta_screen = cv2.resize(gta_screen, (160,120)) #maybe resize to smaller image
            gta_screen = cv2.cvtColor(gta_screen, cv2.COLOR_BGR2GRAY)

            textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
            textPrint.indent()
            
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        
            textPrint.tprint(screen, "Joystick {}".format(0))
            textPrint.indent()
        
            name = joystick.get_name()
            textPrint.tprint(screen, "Joystick name: {}".format(name))
        
            axes = joystick.get_numaxes()
            textPrint.tprint(screen, "Number of axes: {}".format(axes))
            textPrint.indent()
        
            axis_0 = joystick.get_axis(0)#steering
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(0, axis_0))
    
            #axis_1 = joystick.get_axis(1)
            #textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(0, axis_1))
        
            #axis_2 = joystick.get_axis(2)#brake
            #textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(0, axis_2))
    
            axis_3 = joystick.get_axis(3)#throttle
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(0, axis_3))
    
            #axis_4 = joystick.get_axis(4)
            #textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(0, axis_4))
    
            #axis_5 = joystick.get_axis(5)
            #textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(0, axis_5))
        #
            output = [axis_0, axis_3] #[steering, throttle]
            training_data.append([gta_screen,output])
            if len(training_data) % 100 == 0:
                print(len(training_data))

            if len(training_data) == 4000:
                np.save(file_name,training_data)
                print('ALL DONE SAVED')
                counter = counter +1
                training_data = []
                starting_value += 1
                file_name = 'training_data-{}.npy'.format(starting_value)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        #
    
        # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
    
        # Limit to 20 frames per second.
            clock.tick(20)
            
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
    pygame.quit()


main(file_name, starting_value)
