from StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from psychopy import core, visual, event
import time


class FinishProcess(BasicStimulationProcess):

    def __init__(self) -> None:
        super().__init__()


    def change(self):

        if self.controller.endGame:
            self.controller.currentProcess = self.controller.idleProcess
        else:
            self.controller.currentProcess = self.controller.prepareProcess

    def run(self):
        
        # 更新trackPos
        pos = self.update_pos()
        if abs(pos[0]-0) + abs(pos[1]-0) == 0: 
            self.change()
            return
        newbody = [self.viewcontainer.trackPos[0], self.viewcontainer.trackPos[1]]
        self.viewcontainer.trackPos[0] += pos[0]
        self.viewcontainer.trackPos[1] += pos[1]
        
        self.viewcontainer.snakebody.insert(0, newbody)
        frame = visual.Rect(self.w, units='pix', pos=[newbody[0],newbody[1]], width=self.viewcontainer.cubSize, height=self.viewcontainer.cubSize, fillColor=(1,1,-1), opacity=0.5)
        self.viewcontainer.snakeFrame.insert(0, frame)
        # 检测是否追踪到目标块
        hit_TG = self.hit_target()
        if hit_TG:
            self.controller.score += 1
            self.viewcontainer.getTGPos()
        else:
            self.viewcontainer.snakeFrame.pop()
            self.viewcontainer.snakebody.pop()
        hit_myself = self.hit_myself()
        if hit_myself:
            self.feedback()
            self.controller.endGame = True
     
        self.change()

        pass
    
    
    def feedback(self):
        
        self.viewcontainer.displayFrame.pos = (self.viewcontainer.trackPos[0], self.viewcontainer.trackPos[1])
        self.viewcontainer.displayFrame.draw()
        if len(self.viewcontainer.snakeFrame) > 0:
            for frame in self.viewcontainer.snakeFrame:
                frame.draw() 
        self.w.flip()
        time.sleep(0.3)
        
        return

    def update_pos(self,):
        
        step = self.viewcontainer.step
        result = self.controller.currentResult

        if result == 1: pos = [step, 0]
        elif result == 3: pos = [0, step]
        elif result == 5: pos = [-step, 0]
        elif result == 7: pos = [0, -step]
        else: pos = [0, 0]
        
        return pos
    
    def hit_myself(self):
        if self.viewcontainer.trackPos[0] < -self.viewcontainer.boundary[0] or self.viewcontainer.trackPos[0] > self.viewcontainer.boundary[0] or self.viewcontainer.trackPos[1] > self.viewcontainer.boundary[1] or self.viewcontainer.trackPos[1] < -self.viewcontainer.boundary[1]:
            return True
        if len(self.viewcontainer.snakebody) == 0: return False
        for snake in self.viewcontainer.snakebody:
            if abs(self.viewcontainer.trackPos[0]-snake[0]) + abs(self.viewcontainer.trackPos[1]-snake[1]) == 0:
                return True
        return False
        
    
    def hit_target(self,):
        
        if abs(self.viewcontainer.trackPos[0]-self.viewcontainer.targetPos[0]) + abs(self.viewcontainer.trackPos[1]-self.viewcontainer.targetPos[1]) == 0:
            return True
        else: return False