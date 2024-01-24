import sys
sys.path.append('.')
from CommonSystem.Config import Config
from EventController import EventController
from tqdm import tqdm
from psychopy import event, visual, core
import os
import time

config = Config()

config.addSTI = 'StimulationSystem/pics'
config.addTG = 'StimulationSystem/target/green_tg.png'
config.blockNUM = 6
# 并口号
config.COM = '3100'
eventController = EventController(config.COM)

# blockNUM
blockNUM = config.blockNUM

# get target_pos
step = config.step
x_layout, y_layout = config.layout
x_distance = round((x_layout-1)/8)
y_distance = round((y_layout-1)/8)
target_pos = [[step*x_distance, 0], [step*x_distance, step*y_distance], [0, step*y_distance], [-step*x_distance, step*y_distance],
              [-step*x_distance, 0], [-step*x_distance, -step*y_distance], [0, -step*y_distance], [step*x_distance, -step*y_distance]]

# set the window
w_width, w_height = config.window_size
win = visual.Window([w_width, w_height], monitor="testMonitor", units="pix", fullscr=False, waitBlanking=True, color=(-1,-1,-1), screen=0, allowGUI=True)
picAdd = os.listdir(config.addSTI)
x_resolution, y_resolution = config.resolution
frameSet = []
# display frame
add = config.addSTI + os.sep + 'display_frame.png'
displayFrame = visual.ImageStim(win, image=add, pos=[0, 0], size=[x_resolution, y_resolution], units='pix', flipVert=False)

# stimulation frames
for picINX in tqdm(range(len(picAdd)-1)):
    add = config.addSTI + os.sep + '%i.png' % picINX
    frame = visual.ImageStim(win, image=add, pos=[0, 0], size=[x_resolution, y_resolution], units='pix', flipVert=False)
    frameSet.append(frame)
# target frame
add = config.addTG
targetFrame = visual.ImageStim(win, image=add, pos=[0,0], size=[config.target_size, config.target_size], units='pix', flipVert=False)

# stimulus start
text = 'press space to continue.'
text = visual.TextStim(win, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
text.draw()
win.flip()
event.waitKeys(keyList=['space'])

for i in range(len(target_pos)):
    
    # cue
    displayFrame.draw()
    targetFrame.pos = (target_pos[i][0], target_pos[i][1])
    targetFrame.draw()
    win.flip()
    time.sleep(2)
    
    for j in range(blockNUM):
        
        frameINX = 0
        startTime = core.getTime()
        # one stim loop
        while frameINX < len(frameSet):
            if frameINX == 0:
                eventController.sendEvent(i+1)
            frameSet[frameINX].draw()
            targetFrame.draw()
            win.flip()
            frameINX += 1   
                  
        endTime = core.getTime()
        print("STI ended{}".format(endTime-startTime))
        
        eventController.clearEvent()
        displayFrame.draw()
        targetFrame.draw()
        win.flip()
        time.sleep(0.5)

    
    text = 'press space to continue.'
    text = visual.TextStim(win, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
    text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    
win.close()
core.quit()