import sys
sys.path.append('.')

import time
from StimulationSystem.VtkinterProcess.VtkinterThread import VtkinterThread
from CommonSystem.Config import Config
from StimulationSystem.stimulationOperator import stimulationOperator
from StimulationSystem.ApplicationProcess.AppController import AppController 
from CommonSystem.MessageReceiver.ExchangeMessageManagement import ExchangeMessageManagement

# ----
config = Config()
config.displayINFO()
config.addSTI = 'StimulationSystem/pics'
# 并口号
config.COM = '3100'
config.stiLEN = 1
config.personName = 'Oser'
app = 'paint'


stimulationOperator = stimulationOperator()

messenager = ExchangeMessageManagement('server',stimulationOperator,config)
messenager.start()


stimulationOperator.messenager = messenager


application = AppController().initial(config,messenager)
vtkinter = VtkinterThread(config=config, stimulator=application, app=app)
vtkinter.start()
# stimulation准备好后给op发消息
message = 'STON'
messenager.send_exchange_message(message)

while messenager.state.status != 'TNOK':
    time.sleep(0.1)

stimFlag = True
while stimFlag:
    stimFlag = application.run()

message = 'EXIT'
messenager.send_exchange_message(message)

time.sleep(2)
messenager.stop()
vtkinter.stop()
