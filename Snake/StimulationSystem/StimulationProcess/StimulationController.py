import queue
from viewContainer import viewContainer
from StimulationSystem.StimulationProcess.PrePareProcess import PrepareProcess
from StimulationSystem.StimulationProcess.StimulateProcess import StimulateProcess
from StimulationSystem.StimulationProcess.FinishProcess import FinishProcess
from StimulationSystem.StimulationProcess.IdleProcess import IdleProcess
from psychopy import visual
from psychopy import core
import os
from tqdm import tqdm
import datetime

class StimulationController:
    def __init__(self):
        # 各个状态
        self.initialProcess = None
        self.prepareProcess = None
        self.stimulateProcess = None
        self.idleProcess = None
        self.finishProcess = None
        self.currentProcess = None
        
        # 显示界面
        self.w = None

        self.endGame = False
        # 当前epoch的结果（由operation返回）
        self.currentResult = None
        # 是否结束
        self.end = False
        # 分数
        self.score = 0
        


    def initial(self, config, messenager):

        self.messager = messenager
        self.COM = config.COM
        
        viewcontainer = viewContainer(config)
        
    
        self.loadPics(config, viewcontainer)
        
        # 准备阶段：展示cue，展示上次结果
        self.prepareProcess = PrepareProcess()
        self.prepareProcess.initial(self, viewcontainer, messenager)

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
        w_width, w_height = config.window_size
        win = visual.Window([w_width, w_height], monitor="testMonitor", units="pix", fullscr=False, waitBlanking=True, color=(0, 0, 0), colorSpace='rgb255', screen=0, allowGUI=True)

        picAdd = os.listdir(addSTI)
        x_resolution, y_resolution = config.resolution
        frameSet = []
        # display frame
        add = config.addSTI + os.sep + 'display_frame.png'
        displayFrame = visual.ImageStim(win, image=add, pos=[0, 0], size=[x_resolution, y_resolution], units='pix', flipVert=False)

        # stimulation frames
        for picINX in tqdm(range(len(picAdd)-1)):
            add = addSTI + os.sep + '%i.png' % picINX
            frame = visual.ImageStim(win, image=add, pos=[0, 0], size=[x_resolution, y_resolution], units='pix', flipVert=False)
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
            print('\n开始进入{0}呈现阶段，执行时间{1}\n'.format(self.__class__.__name__, datetime.datetime.now()))
            self.currentProcess.run()
            return True
        else:
            self.w.close()
            return False



