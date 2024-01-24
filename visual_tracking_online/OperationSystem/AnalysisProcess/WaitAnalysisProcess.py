# from os import wait
from OperationSystem.AnalysisProcess.BasicAnalysisProcess import BasicAnalysisProcess
import time


class WaitAnalysisProcess(BasicAnalysisProcess):

    def run(self):


        while (self.messenager.state.current_detect_state != 'STRD') and (self.messenager.state.control_state != 'EXIT'):
            time.sleep(0.1)
            
        self.controller.current_process = self.controller.testing_process

