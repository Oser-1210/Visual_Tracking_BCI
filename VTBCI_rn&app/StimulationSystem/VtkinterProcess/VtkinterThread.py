from VtkinterProcess.Vtkinter import Vtkinter
import threading

class VtkinterThread(threading.Thread):
    
    def __init__(self, config=None, stimulator=None, threadName='Vtkinter', app='paint'):
        
        threading.Thread.__init__(self)
        self.name = threadName
        self.config = config
        self.comque = stimulator.pos
        self.app = app
        self.savepath = stimulator.savepath
        
        
    def run(self):
        
        self.vtkinter = Vtkinter()
        if self.app == 'paint':
            self.vtkinter.initial_paint(config=self.config, comque=self.comque, savepath=self.savepath)
            self.vtkinter.vtkinterThread.start()
            self.vtkinter.mainloop()
        elif self.app == 'map':
            self.vtkinter.initial_map(config=self.config, comque=self.comque)
            self.vtkinter.mapThread.start()
            self.vtkinter.mainloop()
        
    def stop(self):
        
        self.vtkinter.stop_flag = True
        if self.app == 'paint':
            self.vtkinter.savepaint()
            self.vtkinter.vtkinterThread.join()
        elif self.app == 'map':
            self.vtkinter.mapThread.join()
        self.vtkinter.quit()
        
        