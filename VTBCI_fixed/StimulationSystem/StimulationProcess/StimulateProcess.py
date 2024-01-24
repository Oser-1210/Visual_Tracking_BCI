import time 
from StimulationSystem.StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from psychopy import core, event
import math
import copy


class StimulateProcess(BasicStimulationProcess):
    def __init__(self) -> None:
        super().__init__()

    def change(self):
        
        self.controller.currentProcess = self.controller.finishProcess


    def run(self):
        
        escape_key = 0
        if_hit = False
        # cue
        self.viewcontainer.targetFrame.pos = (self.viewcontainer.targetPos[0], self.viewcontainer.targetPos[1])
        self.viewcontainer.displayFrame.pos = (0,0)
        self.viewcontainer.displayFrame.draw()
        self.viewcontainer.targetFrame.draw()
        self.w.flip()
        time.sleep(1)
        
        track_start_time = core.getTime()
        while if_hit == False and escape_key == 0 and self.controller.timeout == 0:
            
            frameINX = 0
            frameLen = len(self.viewcontainer.frameSet)
            VFEstart = None
        
            # 发送trigger
            if self.controller.sendEvent == True: 
                message = 'STRD'
                self.messenager.send_exchange_message(message)
                VFEstart = core.getTime()
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
                
                # 绘图
                self.viewcontainer.frameSet[frameINX].pos = (self.viewcontainer.trackPos[0], self.viewcontainer.trackPos[1])
                self.viewcontainer.frameSet[frameINX].draw()
                self.viewcontainer.targetFrame.draw()
                self.w.flip()
                
                if_hit = self.check_hit()
                if if_hit: 
                    if self.controller.hit_start == None:
                        self.controller.hit_start = core.getTime()
                    else:
                        self.controller.hit_end = core.getTime()
                        if self.controller.hit_end - self.controller.hit_start >= self.controller.hit_time:
                            break
                else:
                    self.controller.hit_start = None       
                
                track_current_time = core.getTime()
                if track_current_time - track_start_time > 15:
                    self.controller.timeout = 1
                    self.controller.hit_start = None
                    break
                
                frameINX += 1
                frameINX = frameINX % len(self.viewcontainer.frameSet)
                keys = event.getKeys(keyList=['escape'])
                if 'escape' in keys: 
                    self.controller.end = True
                    time.sleep(2)
                    escape_key = 1
                    break

            self.eventController.clearEvent()
            VFEend = core.getTime()
            if VFEstart is not None:
                self.controller.vltime_for_epoch.append(VFEend-VFEstart)
            the_targetpos = copy.deepcopy(self.viewcontainer.trackPos)
            self.controller.targetpos_for_epoch.append(the_targetpos)
        track_end_time = core.getTime()
        track_time = track_end_time - track_start_time  - self.controller.hit_time
        self.controller.trackTimes.append([track_time, self.controller.timeout])
        self.change()
        
    def check_hit(self):
        
        raduis = math.sqrt((self.viewcontainer.trackPos[0]-self.viewcontainer.targetPos[0])**2+(self.viewcontainer.trackPos[1]-self.viewcontainer.targetPos[1])**2)
        if raduis <= self.viewcontainer.targetSize/2:
            return True
        else: return False