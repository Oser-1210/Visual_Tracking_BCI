import time 
from ApplicationProcess.BasicAppProcess import BasicAppProcess
from psychopy import core, event


class AppdisplayProcess(BasicAppProcess):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        
        escape_key = 0
        while escape_key == 0:
            
            frameINX = 0
            frameLen = len(self.viewcontainer.frameSet)
        
            # 发送trigger
            if self.controller.sendEvent == True:
                message = 'STRD'
                self.messenager.send_exchange_message(message)
                self.eventController.sendEvent(1)
                self.controller.sendEvent = False

            while self.controller.sendEvent == False:
                
                # 位移
                self.viewcontainer.trackPos[0] += int(self.controller.timestep*self.controller.velocity[0])
                self.viewcontainer.trackPos[1] += int(self.controller.timestep*self.controller.velocity[1])
                # 速度衰减
                if frameINX % 10 == 9:
                    self.controller.velocity[0] = self.controller.velocity[0]*(frameLen-frameINX)/(frameLen+1)
                    self.controller.velocity[1] = self.controller.velocity[1]*(frameLen-frameINX)/(frameLen+1)
                    self.controller.pos.put((self.viewcontainer.trackPos[0], -self.viewcontainer.trackPos[1]))
                
                # 绘图
                self.viewcontainer.frameSet[frameINX].pos = (self.viewcontainer.trackPos[0], self.viewcontainer.trackPos[1])
                self.viewcontainer.frameSet[frameINX].draw()
                self.w.flip()
        
                frameINX += 1
                frameINX = frameINX % len(self.viewcontainer.frameSet)
                keys = event.getKeys(keyList=['escape'])
                if 'escape' in keys: 
                    self.controller.end = True
                    time.sleep(2)
                    escape_key = 1
                    break

            self.eventController.clearEvent()
        self.controller.end = True
        