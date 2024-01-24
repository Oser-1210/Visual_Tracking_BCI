from abc import ABCMeta, abstractmethod
import os
import numpy as np

class BasicAnalysisProcess:
    def __init__(self) -> None:
        pass


    @abstractmethod
    def initial(self, controller=None, config=None, streaming=None, messenager=None):

        # 3 essentials: controller, config, and data streaming client
        self.controller = controller
        self.config = config
        self.streaming = streaming
        self.messenager = messenager
        self.messenager.exchange_message_operator.controller = self.controller
        
        self.blockNUM = config.blockNUM
        
        # 初始化算法，提供所需参数
        self.winLEN = config.winLEN
        self.srate = config.srate
        self.personName = config.personName
        self.n_band = config.n_band
        self.lag = config.lag
        self.montage = config.classNUM
        self.p = config.p
        
        self.prepareFolder()

    def prepareFolder(self):
        fatherAdd = 'OperationSystem/ResultStored'
        sonAdd = os.path.join(fatherAdd, self.personName)
        if not os.path.exists(sonAdd):
            os.makedirs(os.path.join(sonAdd,'models'))
            os.makedirs(os.path.join(sonAdd,'data'))
            os.makedirs(os.path.join(sonAdd,'test'))
            os.makedirs(os.path.join(sonAdd,'info'))
        self.savepath = sonAdd
        return


    @abstractmethod
    def run(self):

        pass
            
    @abstractmethod
    def clear(self):
        self.cacheData = None
        return
        
    @abstractmethod
    def getResult(self,data):
        result, rho = self.algorithm.predict(data, self.p)
        if rho is None:
            rho = np.zeros((1,8))
        return rho

