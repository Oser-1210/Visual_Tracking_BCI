import datetime


class StimulationState:
    def __init__(self):
        
        self.status = None
        self.result_id = None

class stimulationOperator:
    def __init__(self):
        self.messenager = None
        self.state = StimulationState()
        self.events = ['CTOK',
                       'DCOK',
                       'TROK',
                       'PROK',
                       'TNOK',
                       'PNOK',
                       'CAOK',
                       'STSN',
                       'RSLT',
                       'CUE',
                       'FreeSpelling']

    def do_CTOK(self,event):
        self.state.status = 'CTOK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('CTOK', self.state.status))

    def do_DCOK(self, event):
        self.state.status = 'DCOK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('DCOK', self.state.status))

    def do_TROK(self, event):
        self.state.status = 'TROK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('TROK', self.state.status))

    def do_PROK(self, event):
        self.state.status = 'PROK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('PROK', self.state.status))

    def do_TNOK(self, event):
        self.state.status = 'TNOK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('TNOK', self.state.status))

    def do_PNOK(self, event):
        self.state.status = 'PNOK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('PNOK', self.state.status))


    def do_CAOK(self, event):
        self.state.status = 'CAOK'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('CAOK', self.state.status))

    def do_STSN(self, event):
        self.state.status = 'STSN'
        message = event.message
        print('接收消息{0}，设置监视器状态{1}\n'.format('STSN', self.state.status))

    def do_CUE(self,event):
        self.state.cue_state = 'CUE'
        print('接收消息{0}，设置监视器状态{1}\n'.format('STSN', self.state.status))

    def do_RSLT(self, event):
        
        message = event.message
        message_result = message['result']
        
        self.controller.currentProcess.change(message_result)
        
        

    def add_listener(self, event_manager):
        event_manager.AddEventListener('CTOK', self.do_CTOK)
        event_manager.AddEventListener('DCOK', self.do_DCOK)
        event_manager.AddEventListener('TROK', self.do_TROK)
        event_manager.AddEventListener('PROK', self.do_PROK)
        event_manager.AddEventListener('TNOK', self.do_TNOK)
        event_manager.AddEventListener('PNOK', self.do_PNOK)
        event_manager.AddEventListener('CAOK', self.do_CAOK)
        event_manager.AddEventListener('STSN', self.do_STSN)
        event_manager.AddEventListener('RSLT', self.do_RSLT)
        event_manager.AddEventListener('CUE', self.do_CUE)


    def remove_listener(self, event_manager):
        event_manager.RemoveEventListener('CTOK', self.do_CTOK)
        event_manager.RemoveEventListener('DCOK', self.do_DCOK)
        event_manager.RemoveEventListener('TROK', self.do_TROK)
        event_manager.RemoveEventListener('PROK', self.do_PROK)
        event_manager.RemoveEventListener('TNOK', self.do_TNOK)
        event_manager.RemoveEventListener('PNOK', self.do_PNOK)
        event_manager.RemoveEventListener('CAOK', self.do_CAOK)
        event_manager.RemoveEventListener('STSN', self.do_STSN)
        event_manager.RemoveEventListener('RSLT', self.do_RSLT)
        event_manager.RemoveEventListener('CUE', self.do_CUE)
