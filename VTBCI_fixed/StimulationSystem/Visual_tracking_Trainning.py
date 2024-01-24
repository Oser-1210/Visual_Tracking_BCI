import sys
sys.path.append('.')
from CommonSystem.Config import Config
from EventController import EventController
from tqdm import tqdm
from psychopy import event, visual, core
import os
import time
import math
import numpy as np

config = Config()

config.addSTI = 'StimulationSystem/pics'
config.addTG = 'StimulationSystem/target/green_point_10.png'
# 并口号
config.COM = '3100'
eventController = EventController(config.COM)

# blockNUM
# blockNUM = config.blockNUM
blockNUM = 6
# target size
targetSize = 0.03

# set the window
w_width, w_height = config.window_size
targetSize = int(targetSize*w_height)
win = visual.Window([w_width, w_height], monitor="testMonitor", units="pix", fullscr=False, waitBlanking=True, color=(0, 0, 0), colorSpace='rgb255', screen=0, allowGUI=True)
text = 'STI stage I' 
text = visual.TextStim(win, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
text.draw()
win.flip()

# set target position
radius = int(w_width/6)
targetPosition = np.zeros((32, 2))
for i in range(16):
    angle = i*math.pi/8
    for j in range(2):
        the_radius = radius*(j+1)
        targetPosition[i*2+j, 0] = int(the_radius*math.cos(angle))
        targetPosition[i*2+j, 1] = int(the_radius*math.sin(angle))

picAdd = os.listdir(config.addSTI)
x_resolution, y_resolution = config.resolution
frameSize = math.sqrt(x_resolution**2+y_resolution**2)
frameSet = []
# display frame
add = config.addSTI + os.sep + 'display_frame.png'
displayFrame = visual.ImageStim(win, image=add, pos=[0, 0], size=[frameSize, frameSize], units='pix', flipVert=False)

# stimulation frames
for picINX in tqdm(range(len(picAdd)-1)):
    add = config.addSTI + os.sep + '%i.png' % picINX
    frame = visual.ImageStim(win, image=add, pos=[0, 0], size=[frameSize, frameSize], units='pix', flipVert=False)
    frameSet.append(frame)
# target frame
add = config.addTG
targetFrame = visual.ImageStim(win, image=add, pos=[0,0], size=[targetSize, targetSize], units='pix', flipVert=False)

# stimulus start
text = 'press space to continue.' 
text = visual.TextStim(win, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# STI for TRCA model
pretarget = [1,5,9,13,17,21,25,29]
pretargetPosition = targetPosition[pretarget]
for targetINX in range(len(pretarget)):
    
    targetFrame.pos = (pretargetPosition[targetINX][0], pretargetPosition[targetINX][1])
    
    for blockINX in range(blockNUM):
        # cue
        displayFrame.draw()
        targetFrame.draw()
        win.flip()
        time.sleep(1)
        
        eventController.sendEvent(targetINX+1)
        frameINX = 0
        startTime = core.getTime()
        # one stim loop
        while frameINX < len(frameSet):
            frameSet[frameINX].draw()
            targetFrame.draw()
            win.flip()
            frameINX += 1   
                  
        endTime = core.getTime()
        print("STI ended{}".format(endTime-startTime))
        
        eventController.clearEvent()
        
    text = 'press space to continue.'
    text = visual.TextStim(win, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
    text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# STI for Velocity model
text = 'STI stage II' 
text = visual.TextStim(win, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
text.draw()
win.flip()
time.sleep(5)

for targetINX in range(targetPosition.shape[0]):
    
    # update target position
    targetFrame.pos = (targetPosition[targetINX][0], targetPosition[targetINX][1])
    
    for blockINX in range(blockNUM):
        # cue
        displayFrame.draw()
        targetFrame.draw()
        win.flip()
        time.sleep(1)
        
        eventController.sendEvent(targetINX+1)
        frameINX = 0
        startTime = core.getTime()
        # one stim loop
        while frameINX < len(frameSet):
            frameSet[frameINX].draw()
            targetFrame.draw()
            win.flip()
            frameINX += 1   
                  
        endTime = core.getTime()
        print("STI ended{}".format(endTime-startTime))
        
        eventController.clearEvent()

    text = 'press space to continue.'
    text = visual.TextStim(win, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
    text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
win.close()
core.quit()