import math
from StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from psychopy import visual


class PrepareProcess(BasicStimulationProcess):
    def __init__(self) -> None:

        super().__init__()

    def change(self):

        self.controller.currentProcess = self.controller.stimulateProcess

    def run(self):

        # 更新刺激位置坐标
        self.viewcontainer.targetFrame.pos = (self.viewcontainer.targetPos[0], self.viewcontainer.targetPos[1])
        for i in range(len(self.viewcontainer.frameSet)):
            self.viewcontainer.frameSet[i].pos = (self.viewcontainer.trackPos[0], self.viewcontainer.trackPos[1])

        
        # 当前状态交给stimulate
        self.change()
        

        