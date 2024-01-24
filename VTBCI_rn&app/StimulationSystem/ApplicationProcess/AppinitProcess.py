import time
from ApplicationProcess.BasicAppProcess import BasicAppProcess
from psychopy import visual, core, event


class AppinitProcess(BasicAppProcess):
    def __init__(self) -> None:
        super().__init__()

    def change(self):

        self.controller.currentProcess = self.controller.appdisplayProcess

    def run(self):
        # 本节实验结束界面
        self._idleInterface()
        self.eventController.clearEvent()

        time.sleep(1)
        
        self.change()

    def _idleInterface(self):

    
        text = 'To begin, press space.'
        text = visual.TextStim(self.w, pos=[0, 0], text=text, color=(255, 255, 255), colorSpace='rgb255')
        text.draw()

        self.w.flip()
        event.waitKeys(keyList=['space'])

        pass


