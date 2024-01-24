import time
import numpy as np
from StimulationProcess.BasicStimulationProcess import BasicStimulationProcess
from psychopy import visual, core, event
import math


class IdleProcess(BasicStimulationProcess):
    def __init__(self) -> None:
        super().__init__()

    def change(self):

        self.controller.currentProcess = self.controller.prepareProcess

    def run(self):
        # 本节实验结束界面
        self._idleInterface()
        self.eventController.clearEvent()

        time.sleep(1)
        self.change()

    def _idleInterface(self):

        if self.controller.endGame == False:
            text = 'Game begin, press space to continue.'
        else:
            text = 'Game over, score: %d' % self.controller.score
            self.controller.end = True

        text = visual.TextStim(self.w, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
        text.draw()

        self.w.flip()
        event.waitKeys(keyList=['space'])

        pass


