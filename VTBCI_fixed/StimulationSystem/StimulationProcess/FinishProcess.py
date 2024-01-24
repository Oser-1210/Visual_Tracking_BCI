from StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from psychopy import core, visual, event
import time


class FinishProcess(BasicStimulationProcess):

    def __init__(self) -> None:
        super().__init__()


    def change(self):

        if self.controller.endBlock:
            self.controller.currentProcess = self.controller.idleProcess
        else:
            self.controller.currentProcess = self.controller.stimulateProcess

    def run(self):
        
        self.controller.currentepochINX += 1

        self._showFeedback()
        if self.controller.currentepochINX == self.controller.epochNUM: 
            self.controller.vltime.append(self.controller.vltime_for_epoch)
            self.controller.targetpos.append(self.controller.targetpos_for_epoch)
            self.controller.velocitys.append(self.controller.velocity_for_epoch[:-1])
            self.controller.endBlock = True
            self.change()
            return
        
        self.change()
        self.viewcontainer.trackPos = [0, 0]
        self.controller.velocitys.append(self.controller.velocity_for_epoch[:-1])
        self.controller.velocity_for_epoch = []
        self.controller.velocity = [0, 0]
        self.controller.velocity_for_epoch.append(self.controller.velocity)
        self.controller.vltime.append(self.controller.vltime_for_epoch)
        self.controller.targetpos.append(self.controller.targetpos_for_epoch)
        self.controller.vltime_for_epoch = []
        self.controller.targetpos_for_epoch = []
        self.viewcontainer.gettargetPos(self.controller.currentepochINX)
        self.viewcontainer.getdistance()
        
        pass

    def _showFeedback(self,):
        
        if self.controller.timeout == 1:
            text = 'Timeout! Press space to continue.' 
            text = visual.TextStim(self.w, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
            text.draw()
            self.w.flip()
            while self.controller.sendEvent == False:
                time.sleep(0.01)
            self.eventController.sendEvent(253)
            event.waitKeys(keyList=['space'])
            self.controller.timeout = 0
            self.eventController.clearEvent()
            time.sleep(0.5)
        else:
            self.viewcontainer.displayFrame.pos = (self.viewcontainer.trackPos[0], self.viewcontainer.trackPos[1])
            self.viewcontainer.displayFrame.draw()
            self.viewcontainer.targetFrame.draw()
            self.w.flip()
            time.sleep(0.5)
            
            text = 'Congratulations!\n\n\nTime cost: %.2f s' % self.controller.trackTimes[-1][0]
            text = visual.TextStim(self.w, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
            text.draw()
            self.w.flip()
            while self.controller.sendEvent == False:
                time.sleep(0.01)
            self.eventController.sendEvent(253)
            event.waitKeys(keyList=['space'])
            self.eventController.clearEvent()
            time.sleep(0.5)

        return
    