import sys
sys.path.append('.')
import queue
import os
from tkinter import *
from threading import Thread
import time
from CommonSystem.Config import Config
from PIL import Image, ImageTk, ImageGrab

class Vtkinter(Tk):
    
    def __init__(self) -> None:
        
        super().__init__()
        
    def initial_paint(self, comque, config, savepath):
        
        self.comque = comque
        self.color = config.color
        self.pen = config.pen
        self.savepath = savepath
        window_x, window_y = config.window_size
        screen_x, screen_y = config.screen
        x = int(screen_x/2) - window_x - 10
        y = int((screen_y - window_y)/2) 
        self.geometry("%dx%d+%d+%d" % (window_x,  window_y, x, y))
        self.overrideredirect(1)
        self.cv = Canvas(self, bg='white', width=window_x, height=window_y)
        self.cv.pack(side=LEFT, padx=5, pady=5)
        self.center = [int(self.cv.winfo_reqwidth()/2), int(self.cv.winfo_reqheight()/2)]
        self.startpos = [int(self.cv.winfo_reqwidth()/2), int(self.cv.winfo_reqheight()/2)]
        self.endpos = None
        
        self.bind('<<flip>>', self.flip_fnc)
        
        self.stop_flag = False
        self.vtkinterThread = Thread(name='Vtkinter_check', target=self.check_comque)
        
    def flip_fnc(self, event):
        
        line = (self.startpos[0], self.startpos[1], self.endpos[0], self.endpos[1])
        self.startpos[0] = self.endpos[0]
        self.startpos[1] = self.endpos[1]
        self.cv.create_line(line, fill=self.color, width=self.pen)
  
    def check_comque(self):
        
        while True:
            if self.comque.qsize() > 0:
                fque = self.comque.get()
                posx, posy = fque
                self.endpos = [posx+self.center[0], posy+self.center[1]]
                try:
                    self.event_generate('<<flip>>', when='tail')
                except TclError:
                    break
            if self.stop_flag == True:
                print('Exiting Vtkinter!')
                break
            time.sleep(0.1)
            
    def savepaint(self):
        
        self.cv.update()
        x = self.winfo_rootx() + self.cv.winfo_x()
        y = self.winfo_rooty() + self.cv.winfo_y()
        x1 = x + self.cv.winfo_width()
        y1 = y + self.cv.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save(os.path.join(self.savepath,'paint','fig.jpg'))
    
    def initial_map(self, comque, config):
        
        self.comque = comque
        window_x, window_y = config.window_size
        screen_x, screen_y = config.screen
        x = int(screen_x/2) - window_x - 10
        y = int((screen_y - window_y)/2)
        self.geometry("%dx%d+%d+%d" % (window_x,  window_y, x, y))
        self.overrideredirect(1)
        self.addMap = config.addMap
        self.position = [1300, 1700]
        self.multiple = config.multiple
        
        self.cv = Canvas(self, bg='white', width=window_x, height=window_y)
        self.cv.pack(side=LEFT, padx=5, pady=5)
        img = Image.open(self.addMap)
        self.photo = ImageTk.PhotoImage(img)
        self.cv.create_image((self.position[0], self.position[1]), image=self.photo)
        self.cv.pack()
        
        self.bind('<<move_map>>', self.move_map)
        
        self.stop_flag = False
        self.mapThread = Thread(name='map_check', target=self.map_comque)
        
    def move_map(self, event):
        
        self.cv.create_image((self.position[0], self.position[1]), image=self.photo)
        self.cv.pack()
        
    def map_comque(self):
        
        while True:
            if self.comque.qsize() > 0:
                fque = self.comque.get()
                posx, posy = fque
                self.position[0] += -self.multiple*posx
                self.position[1] += -self.multiple*posy
                try:
                    self.event_generate('<<move_map>>', when='tail')
                except TclError:
                    break
            if self.stop_flag == True:
                print('Exiting Map!')
                break
            time.sleep(0.1)
        
           
    def myrun(self):
        
        self.vtkinterThread.start()
        self.mainloop()
        
    def exit(self):
        
        self.vtkinterThread.join()
        self.quit()
    
if __name__ == '__main__':
    
    message = [(10,10), (20,30), (40,50), (10,70), (-30,10)]
    
    config = Config()
    comque = queue.Queue()
    for i in range(len(message)):
        comque.put(message[i])
        
    vtkinter = Vtkinter()
    vtkinter.initial(comque, config)
    vtkinter.myrun()
    vtkinter.stop_flag = True
    vtkinter.exit()
        
        