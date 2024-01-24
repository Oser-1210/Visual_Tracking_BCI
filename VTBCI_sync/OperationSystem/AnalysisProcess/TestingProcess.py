from AnalysisProcess.BasicAnalysisProcess import BasicAnalysisProcess
import numpy as np
from psychopy import core
import pickle
import os


class TestingProcess(BasicAnalysisProcess):
    def __init__(self):
        self.algorithm = None
        self.cacheData = None
        self.W = None
    
        super().__init__()


    def loadModel(self):

        modelname = os.path.join(self.savepath,'models/model.pickle')
        with open(modelname,"rb") as fp:
            self.algorithm = pickle.load(fp)
        Wname = os.path.join(self.savepath,'models/W.pickle')
        with open(Wname,"rb") as fp:
            self.W = pickle.load(fp)
         
        pass

    def run(self):

        startTime = core.getTime()
        # 同步系统,包含event
        while True:
            self.cacheData, eventId = self.streaming.readFixedData(0, self.winLEN+self.lag)
            if self.cacheData is not None:
                break
            if self.messenager.state.control_state == 'EXIT': return

        # 读取数据
        epoch = self.cacheData
        # 计算结果
        rho = self.getResult(epoch)
        result = np.squeeze(np.dot(rho, self.W))
        result = result.tolist()
        # 汇报结果
        self.controller.report(result)

        endTime = core.getTime()

        # 清空
        self.clear()
        # 模型评价
        self.controller.actualWin = endTime-startTime
        print('Time spend %f s' % self.controller.actualWin)
        self.controller.current_process = self.controller.wait_analysis_process

        return
    




