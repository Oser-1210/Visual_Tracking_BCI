import datetime


class OperationState:
    def __init__(self):

        self.receiver_state = 'INIT'

        self.control_state = 'INIT'

        self.current_detect_state = 'INIT'


class operationOperator:

    def __init__(self):
        self.messenager = None
        self.streaming = None
        self.state = OperationState()
        self.events = ['CTNS', #connectToNeuroScan
                       'DCNS', #disconnectToNeuroScan;
                       'STAR', #startReceivedData
                       'STOP', #stopReceivedData
                       'CLRT', #ClearResultOperation
                       'STON', #StartOperation
                       'SPON', #StopOperation
                       'CSAL', #CloseAllOperation
                       'STRD', #StartRealTimeDetection
                       'CUE',  #开始下一次刺激
                       'EXIT'] #Exit Program

    def do_CTNS(self, event):
        self.streaming.connect()
        self.state.receiver_state = 'CTNS'
        message = 'CTOK'
        self.messenager.send_exchange_message(message)
        print('成功连接到NeuroScan服务器')


    def do_DCNS(self, event):
        self.streaming.disconnect()
        self.state.receiver_state = 'DCNS'
        #message = ToStimulationSendingExchangeMessage.DisconnectToNeuroScanOK
        print('中断到NeuroScan服务器连接')
        #self.messenager.sendExchangeMessage(message)
        #print('发送消息{}\n'.format(message.chId))
    def do_STAR(self, event):
        # self.streaming.start_receive_data()
        self.state.receiver_state = 'STAR'
        message = 'TROK'
        self.messenager.send_exchange_message(message)
        print('开始从NeuroScan服务器接收数据')
        #print('发送消息{}\n'.format(message.chId))


    def do_STOP(self, event):
        self.streaming.stop_receive_data()
        #message = ToStimulationSendingExchangeMessage.StopReceiveOK
        self.state.receiver_state = 'STOP'
        print('停止从NeuroScan服务器接收数据')
        #self.messenager.sendExchangeMessage(message)
        #print('发送消息{}\n'.format(message.chId))

    def do_STON(self, event):
        self.state.control_state = 'STON'
        print('设置为开始数据处理状态')
        message = 'TNOK'
        self.messenager.send_exchange_message(message)
        #print('发送消息{}\n'.format(message.chId))

    def do_SPON(self, event):
        #message = ToStimulationSendingExchangeMessage.StopOperationOK
        self.state.control_state = 'SPON'
        print('设置为停止数据处理状态')
        #self.messenager.sendExchangeMessage(message)
        #print('发送消息{}\n'.format(message.chId))

    def do_CSAL(self, event):
        #message = ToStimulationSendingExchangeMessage.CloseAllOperationOK
        self.state.control_state = 'CSAL'
        print('设置为停止所有操作状态')
        #self.messenager.sendExchangeMessage(message)
        #print('发送消息{}\n'.format(message.chId))



    def do_EXIT(self, event):
        self.state.control_state = 'EXIT'
        print('处理程序准备退出')

    def do_STRD(self, event):
        self.state.current_detect_state = 'STRD'
        print('\n准备进入实时处理模式,%s'%datetime.datetime.now())

    def add_listener(self, event_manager):
        event_manager.AddEventListener('CTNS', self.do_CTNS)
        event_manager.AddEventListener('DCNS', self.do_DCNS)
        event_manager.AddEventListener('STAR', self.do_STAR)
        event_manager.AddEventListener('STOP', self.do_STOP)
        event_manager.AddEventListener('STON', self.do_STON)
        event_manager.AddEventListener('SPON', self.do_SPON)
        event_manager.AddEventListener('CSAL', self.do_CSAL)
        event_manager.AddEventListener('STRD', self.do_STRD)
        event_manager.AddEventListener('EXIT', self.do_EXIT)

    def remove_listener(self, event_manager):
        event_manager.RemoveEventListener('CTNS', self.do_CTNS)
        event_manager.RemoveEventListener('DCNS', self.do_DCNS)
        event_manager.RemoveEventListener('STAR', self.do_STAR)
        event_manager.RemoveEventListener('STOP', self.do_STOP)
        event_manager.RemoveEventListener('STON', self.do_STON)
        event_manager.RemoveEventListener('SPON', self.do_SPON)
        event_manager.RemoveEventListener('CSAL', self.do_CSAL)
        event_manager.RemoveEventListener('STRD', self.do_STRD)
        event_manager.RemoveEventListener('EXIT', self.do_EXIT)
