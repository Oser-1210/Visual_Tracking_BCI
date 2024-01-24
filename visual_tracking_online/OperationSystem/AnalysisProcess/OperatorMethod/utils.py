import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

def ensembleData(X,y,idealSub):
    groupData = [X[member] for member in idealSub]
    groupData = np.concatenate([groupData[_] for _ in range(len(groupData))],axis=-1)
    groupData = np.concatenate([groupData[:,:,:,_] for _ in range(groupData.shape[-1])],axis=-1)
    groupData = np.transpose(groupData,(-1,0,1))
    
    groupLabel = [y[member] for member in idealSub]
    groupLabel = np.concatenate([groupLabel[_].flatten() for _ in range(len(groupLabel))])

    return groupData,groupLabel

def changeDataFormat(X,y,window):

    # 窗长统一
    X = np.concatenate([X[_][:, :, :window]
                               for _ in range(len(X))], axis=0)

    y = np.array(y)
    return X,y
    


def ITR(N,P,winBIN):
    
    if   P == 1:
        ITR = math.log2(N)*60/winBIN
    elif P == 0:
        ITR = (math.log2(N)+ 0 +(1-P)*math.log2((1-P)/(N-1)))*60/winBIN
        ITR = 0
    else:
        ITR = (math.log2(N)+P*math.log2(P)+(1-P)*math.log2((1-P)/(N-1)))*60/winBIN

    return ITR


def snsplot(df, savePath):

    sns.set_theme()
    sns.set(font="Verdana")

    f, (ax1,ax2) = plt.subplots(1, 2,sharex=False, figsize=(15, 5))

    sns.lineplot(data=df, x='Epoch', y='score',
                 hue='scheme', style='scheme', ax=ax1, markers=True)
    sns.lineplot(data=df, x='Epoch', y='ITR', hue='scheme',
                 style='scheme', ax=ax2, markers=True)
    ax1.set_title('Accuracy')
    ax2.set_title('ITR')

    plt.savefig(savePath,dpi=600,format='png')
    pass
