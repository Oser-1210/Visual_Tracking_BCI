from viewContainer import viewContainer
from StimulationSystem.StimulationProcess.StimulateProcess import StimulateProcess
from StimulationSystem.StimulationProcess.FinishProcess import FinishProcess
from StimulationSystem.StimulationProcess.IdleProcess import IdleProcess
from psychopy import visual
from psychopy import core
import numpy as np
import math
import os
import copy
from tqdm import tqdm

class StiController:
    def __init__(self):
        # 各个状态
        self.stimulateProcess = None
        self.idleProcess = None
        self.finishProcess = None
        self.currentProcess = None
        
        # 追踪用时
        self.trackTimes = []
        # 显示界面
        self.w = None  
        self.endBlock = False
        # 是否发送trigger
        self.sendEvent = True
        # 当前block的编号
        self.currentepochINX = 0
        # 速度
        self.velocity = [0,0]
        # 保存信息
        self.savepath = None
        self.velocity_for_epoch = []
        self.velocitys = []
        self.vltime_for_epoch = []
        self.vltime = []
        self.targetpos_for_epoch = []
        self.targetpos = []
        # 是否结束
        self.end = False
        # 是否超时
        self.timeout = 0
        self.hit_start = None
        self.hit_end = None
        self.hit_time = 0
        


    def initial(self, config, messenager):

        self.messager = messenager
        self.blockNUM = config.blockNUM 
        self.COM = config.COM
        self.personName = config.personName
        self.prepareFolder()
        
        # 时间
        self.srate = config.refreshRate
        self.timestep = 1/self.srate
        
        viewcontainer = viewContainer(config)
        self.epochNUM = viewcontainer.targetPosition.shape[0]*self.blockNUM
    
        self.loadPics(config, viewcontainer)

        # 开始刺激：刺激时展示cue
        self.stimulateProcess = StimulateProcess()
        self.stimulateProcess.initial(self, viewcontainer, messenager)

        # 结束刺激：展示结果？
        self.finishProcess = FinishProcess()
        self.finishProcess.initial(self, viewcontainer, messenager)

        # Block间的空闲状态
        self.idleProcess = IdleProcess()
        self.idleProcess.initial(self, viewcontainer, messenager)

        self.currentProcess = self.idleProcess

        
        return self

    def loadPics(self, config, viewcontainer):
    
        addSTI = config.addSTI
        self.window_size = config.window_size
        w_width, w_height = config.window_size
        win = visual.Window([w_width, w_height], monitor="testMonitor", units="pix", fullscr=False, waitBlanking=True, color=(0, 0, 0), colorSpace='rgb255', screen=0, allowGUI=True)

        picAdd = os.listdir(addSTI)
        x_resolution, y_resolution = config.resolution
        frameSize = math.sqrt(x_resolution**2+y_resolution**2)
        frameSet = []
        # display frame
        add = config.addSTI + os.sep + 'display_frame.png'
        displayFrame = visual.ImageStim(win, image=add, pos=[0, 0], size=[frameSize, frameSize], units='pix', flipVert=False)

        # stimulation frames
        for picINX in tqdm(range(len(picAdd)-1)):
            add = addSTI + os.sep + '%i.png' % picINX
            frame = visual.ImageStim(win, image=add, pos=[0, 0], size=[frameSize,frameSize], units='pix', flipVert=False)
            frameSet.append(frame)
        # target frame
        add = config.addTG
        targetFrame = visual.ImageStim(win, image=add, pos=[0,0], size=[config.target_size, config.target_size], units='pix', flipVert=False)
        
        self.w = win
        viewcontainer.w = win
        viewcontainer.frameSet = frameSet
        viewcontainer.displayFrame = displayFrame
        viewcontainer.targetFrame = targetFrame

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
        self.savepath = sonAdd
        
        return
    
    def update_velocity(self, result):
        
        self.velocity = result
        self.sendEvent = True
        self.velocity_for_epoch.append(copy.deepcopy(result))
        
        return     
                
        



