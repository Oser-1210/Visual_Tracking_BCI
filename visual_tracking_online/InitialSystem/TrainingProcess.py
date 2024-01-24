import os
import pickle
import numpy as np
from tqdm import tqdm
import seaborn as sns
import scipy.io as scio
import pandas as pd
import random
import matplotlib.pyplot as plt


class TrainingProcess():

    def __init__(self, config, dataStreaming) -> None:

        self.personName = config.personName
        # 默认保存在Operation里
        self.fatherAdd = 'OperationSystem/ResultStored'
        self.prepareFolder()
        self.streaming = dataStreaming

        self.config = config

        self.srate = config.srate
        self.winLEN = config.winLEN
        self.lag = config.lag
        self.n_band=config.n_band
        self.p = config.p

        T = int(self.srate*(self.winLEN+self.lag))

        self.epochNUM = int(config.classNUM * config.blockNUM)
        self.classNUM = config.classNUM
        self.epochINX = 0
        self.chnNUM = config.chnNUM

        self.data = dict(
            X=np.zeros((self.epochNUM,self.chnNUM,T)),
            y=np.zeros(self.epochNUM)
        )

        self.streaming.start()
        self.pbar = tqdm(total=self.epochNUM, desc="Progress")
        self.endFlag = False

        pass


    def prepareFolder(self):
        
        fatherAdd = self.fatherAdd
        sonAdd = os.path.join(fatherAdd,self.personName)
        if not os.path.exists(sonAdd):
            os.makedirs(os.path.join(sonAdd, 'models'))
            os.makedirs(os.path.join(sonAdd, 'data'))
            os.makedirs(os.path.join(sonAdd,'test'))
        self.savepath = sonAdd
        
        return


    def collectData(self):

        while True:
            epoch, event = self.streaming.readFixedData(0, self.winLEN+self.lag)
            if epoch is not None:
                self.streaming.eventExist = False
                break

        self.data['X'][self.epochINX] = epoch
        self.data['y'][self.epochINX] = event

        self.epochINX += 1
        self.pbar.update(1)

        if (self.epochINX) >= self.epochNUM:
            self.saveData()
            self.endFlag = True
            self.pbar.close()
            self.streaming.disconnect()


    def saveData(self):

        with open(os.path.join(self.savepath, 'data/raw.pickle'), "wb+") as fp:
            pickle.dump(self.data, fp, protocol=pickle.HIGHEST_PROTOCOL)


    def trainModel(self):

        from OperationSystem.AnalysisProcess.OperatorMethod.spatialFilter import TDCA
        # load data
        with open(self.savepath+os.sep+'data/raw.pickle', "rb") as fp:
            data = pickle.load(fp)

        X, y = data['X'], data['y']

        model = TDCA(winLEN=self.winLEN, lag=self.lag, srate=self.srate, montage=self.classNUM, n_band=self.n_band)
        model.fit(X, y)
        with open(os.path.join(self.savepath, 'models/model.pickle'), "wb+") as fp:
                pickle.dump(model, fp, protocol=pickle.HIGHEST_PROTOCOL)

        return
