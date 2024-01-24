from AnalysisProcess.BasicAnalysisProcess import BasicAnalysisProcess
import numpy as np
from psychopy import core
import pickle
import os


class TestingProcess(BasicAnalysisProcess):
    def __init__(self):
        self.algorithm = None
        self.state = None
        self.cacheData = None
        self.deposit = [] #数据
        self.record = [] #标签
        self.epochNUM = 0
        self.correctepoch = 0

        super().__init__()


    def loadModel(self):

        modelname = os.path.join(self.savepath,'models/model.pickle')
        with open(modelname,"rb") as fp:
            self.algorithm = pickle.load(fp)
        pass

    def run(self):

        startTime = core.getTime()
        window_time = 0
        # 同步系统,包含event
        while True:
            window_time += self.stepLEN
            if window_time > self.winLEN: 
                window_time = self.winLEN
            
            while True:
                self.cacheData, eventId = self.streaming.readFixedData(0, window_time+self.lag)
                if self.cacheData is not None:
                    break
                if self.messenager.state.control_state == 'EXIT': return
            
            # 读取数据
            epoch = self.cacheData
            # 计算结果
            result = self.getResult(epoch)
            if result is not None: 
                self.streaming.eventExist = False
                break
            elif window_time == self.winLEN:
                result = 0
                self.streaming.eventExist = False
                break
                
        self.deposit.append(epoch)
        self.record.append(eventId)
        self.epochNUM += 1
        
        if result == eventId:
            self.correctepoch += 1
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
    
    def save(self):
        
        data = dict(
            X=self.deposit,
            y=self.record
        )
        with open(os.path.join(self.savepath, 'test/raw.pickle'), "wb+") as fp:
            pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
    
    def report(self):
        
        acc = (self.correctepoch/self.epochNUM)*100
        print('%d blocks, %d epoches, Accuracy %.2f' % (self.blockNUM, self.epochNUM, acc))



