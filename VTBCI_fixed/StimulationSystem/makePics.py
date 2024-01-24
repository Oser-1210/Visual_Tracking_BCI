import sys
sys.path.append('.')

from CommonSystem.Config import Config
from UICreator.UIFactory import UIFactory

config = Config()
config.stiLEN=1

factory = UIFactory(config)
frames = factory.getFrames()
factory.saveFrames(frames)

