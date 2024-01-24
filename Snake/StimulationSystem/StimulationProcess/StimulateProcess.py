import time 
from StimulationSystem.StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from psychopy import core, event
import datetime


class StimulateProcess(BasicStimulationProcess):
    def __init__(self) -> None:
        super().__init__()

    def change(self, result):
        
        self.controller.currentProcess = self.controller.finishProcess
        self.controller.currentResult = result

    def run(self):
        
        
        message = 'STRD'
        self.messenager.send_exchange_message(message)
        
        while_INX = 0
        escape_key = 0
        while self.controller.currentProcess is self and escape_key == 0:
            
            frameINX = 0
            # 发送trigger
            while frameINX < len(self.viewcontainer.frameSet) and escape_key == 0:
                
                
                if frameINX == 0 and while_INX == 0:
                    self.eventController.sendEvent(1)
                
                self.viewcontainer.frameSet[frameINX].draw()
                self.viewcontainer.targetFrame.draw()
                if len(self.viewcontainer.snakeFrame) > 0:
                    for frame in self.viewcontainer.snakeFrame:
                        frame.draw()
                self.w.flip()
                
                frameINX += 1
                keys = event.getKeys(keyList=['escape'])
                if 'escape' in keys: 
                    self.controller.end = True
                    time.sleep(2)
                    escape_key = 1

            while_INX += 1

        self.eventController.clearEvent()

