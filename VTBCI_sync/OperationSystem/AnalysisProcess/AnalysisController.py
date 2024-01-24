from OperationSystem.AnalysisProcess.TestingProcess import TestingProcess
from OperationSystem.AnalysisProcess.WaitAnalysisProcess import WaitAnalysisProcess
import json

class AnalysisController:
    def __init__(self):
        self.current_process = None
        self.algorithm = None
        self.actualWin = None

    def initial(self, config, streaming, messenger):

        self.messenger = messenger
        # 个人数据
        self.data = dict(
            X = [],# data
            y = [], # label
        )

        # 测试阶段
        self.testing_process = TestingProcess()
        self.testing_process.initial(self, config, streaming, messenger)
        self.testing_process.loadModel()

        # 等待下一次处理
        self.wait_analysis_process = WaitAnalysisProcess()
        self.wait_analysis_process.initial(self, config, streaming, messenger)

        self.current_process = self.wait_analysis_process

        return self

    def report(self, result):
        data = json.dumps(result)
        message = 'RSLT:'+ data
        self.messenger.send_exchange_message(message)


    def run(self):
        # algorithm需要在各个状态之间传递
        self.current_process.run()
        



