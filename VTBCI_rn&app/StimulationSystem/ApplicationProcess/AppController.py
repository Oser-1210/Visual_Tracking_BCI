import queue
from viewContainer import viewContainer
from StimulationSystem.ApplicationProcess.AppdisplayProcess import AppdisplayProcess
from StimulationSystem.ApplicationProcess.AppinitProcess import AppinitProcess
from psychopy import visual
import copy
import math
import os
from tqdm import tqdm

class AppController:
    def __init__(self):
        # 各个状态
        self.appdisplayProcess = None
        self.appinitProcess = None
        self.currentProcess = None
        
        # 显示界面
        self.w = None  
        # 是否发送trigger
        self.sendEvent = True
        # 速度
        self.velocity = [0,0]
        # 保存信息
        self.savepath = None
        # 是否结束
        self.end = False
        # 位置队列消息
        self.pos = queue.Queue()
        
        


    def initial(self, config, messenager):

        self.messager = messenager
        self.COM = config.COM
        self.personName = config.personName
        self.prepareFolder()
        
        # 时间
        self.srate = config.refreshRate
        self.timestep = 1/self.srate
        
        viewcontainer = viewContainer(config)
        
    
        self.loadPics(config, viewcontainer)

        # 开始刺激：刺激时展示cue
        self.appdisplayProcess = AppdisplayProcess()
        self.appdisplayProcess.initial(self, viewcontainer, messenager)

        # Block间的空闲状态
        self.appinitProcess = AppinitProcess()
        self.appinitProcess.initial(self, viewcontainer, messenager)

        self.currentProcess = self.appinitProcess

        
        return self

    def loadPics(self, config, viewcontainer):
    
        addSTI = config.addSTI
        w_width, w_height = config.window_size
        screen_x, screen_y = config.screen
        posx = int(screen_x/2 + 10)
        posy = int((screen_y-w_height)/2)
        win = visual.Window([w_width, w_height], pos=[posx, posy], monitor="testMonitor", units="pix", fullscr=False, waitBlanking=True, color=(0, 0, 0), colorSpace='rgb255', screen=0, allowGUI=False)

        picAdd = os.listdir(addSTI)
        x_resolution, y_resolution = config.resolution
        frameSize = math.sqrt(x_resolution**2+y_resolution**2)
        frameSet = []

        # stimulation frames
        for picINX in tqdm(range(len(picAdd)-1)):
            add = addSTI + os.sep + '%i.png' % picINX
            frame = visual.ImageStim(win, image=add, pos=[0, 0], size=[frameSize,frameSize], units='pix', flipVert=False)
            frameSet.append(frame)
  
        
        self.w = win
        viewcontainer.w = win
        viewcontainer.frameSet = frameSet

        return self
        
    def run(self):
        
        if self.end == False:
            self.currentProcess.run()
            return True
        else:
            self.w.close()
            return False
        
    def prepareFolder(self):
            
        fatherAdd = 'StimulationSystem/Information'
        sonAdd = os.path.join(fatherAdd, self.personName)
        if not os.path.exists(sonAdd):
            os.makedirs(os.path.join(sonAdd,'info'))
            os.makedirs(os.path.join(sonAdd,'paint'))
        self.savepath = sonAdd
        
        return
    
    def update_velocity(self, result):
        
        self.sendEvent = True
        self.velocity = result

        return     
                
        



