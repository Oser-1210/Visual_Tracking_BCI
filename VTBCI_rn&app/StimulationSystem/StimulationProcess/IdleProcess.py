import time
import numpy as np
from StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from psychopy import visual, core, event
import math
import os
import pickle


class IdleProcess(BasicStimulationProcess):
    def __init__(self) -> None:
        super().__init__()

    def change(self):

        self.controller.currentProcess = self.controller.stimulateProcess

    def run(self):
        # 本节实验结束界面
        self._idleInterface()
        self.eventController.clearEvent()

        time.sleep(1)
        
        self.change()

    def _idleInterface(self):

        if self.controller.currentBlockINX == 0:
            self.controller.velocity_for_epoch.append(self.controller.velocity)
            text = 'Game begin, press space to continue.'
        else:
            Fitts, score = self.getScore()
            text = 'Game over, Fitts score: %.2f \n\n\n           Accuracy: %.2f' % (Fitts, score*100)
            self.controller.end = True
            self.saveinfo()

        text = visual.TextStim(self.w, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
        text.draw()

        self.w.flip()
        event.waitKeys(keyList=['space'])

        pass

    def getScore(self,):
        
        trackTimes = self.controller.trackTimes
        distances = self.viewcontainer.distance
 
        Fitts = []
        score = 0
        for i in range(len(trackTimes)):
            distance = distances[i].real
            time = trackTimes[i][0]
            ifout = trackTimes[i][1]
            # Fitts.append(math.log2(distance+1)/time)
            if ifout == 0:
                score += 1
                Fitts.append(math.log2(distance/self.viewcontainer.targetSize+1/2)/time)
        Fitts = np.mean(Fitts)
        score = score/len(trackTimes)
        return Fitts, score
    
    def saveinfo(self):
        
        info = dict(distances=self.viewcontainer.distance,
                    trackTimes=self.controller.trackTimes,
                    velocitys=self.controller.velocitys,
                    vltime=self.controller.vltime,
                    targetPosition=self.viewcontainer.targetPosition)
        
        with open(os.path.join(self.controller.savepath,'info/info.pickle'),'wb+') as fp:
            pickle.dump(info, fp, protocol=pickle.HIGHEST_PROTOCOL)

