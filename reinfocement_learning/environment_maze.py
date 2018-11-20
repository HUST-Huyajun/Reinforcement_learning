
import numpy as np
import sys
import time
import random
if sys.version_info.major==2:
    import Tkinter as tk
else:
    import tkinter as tk

pixel=40
length=5
width=4
hell=np.array([[3,1],[2,2]])
apple=np.array([[3,2]])

class env_maz(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.action=['up','down','left','right']
        self.n_action=len(self.action)
        self.title('Find apple')
        self.max_length=length*pixel
        self.max_width=width*pixel
        self.geometry('{0}x{1}'.format(length*pixel,width*pixel))
        self.__create_graph()

    def __create_graph(self):
        self.canvas=tk.Canvas(self,bg='white',height=width*pixel,width=length*pixel)
        for i in range(0,pixel*length,pixel):
            x1,y1,x2,y2=i,0,i,self.max_width
            self.canvas.create_line(x1,y1,x2,y2)
        for i in range(0,pixel*width,pixel):
            x1,y1,x2,y2=0,i,self.max_length,i
            self.canvas.create_line(x1,y1,x2,y2)
        for onehell in hell:
            x1,y1,x2,y2=(onehell[0]-1)*pixel,(onehell[1]-1)*pixel,onehell[0]*pixel,onehell[1]*pixel
            self.canvas.create_rectangle(x1,y1,x2,y2,fill='black')
        for oneapple in apple:
            x1,y1,x2,y2=(oneapple[0]-1)*pixel,(oneapple[1]-1)*pixel,oneapple[0]*pixel,oneapple[1]*pixel
            self.canvas.create_rectangle(x1,y1,x2,y2,fill='red')
        x1,y1,x2,y2=0,0,pixel,pixel
        self.searcher=self.canvas.create_oval(x1,y1,x2,y2,fill='yellow')
        self.canvas.pack()
    def move(self,action):
        deltax=0
        deltay=0
        if action=='up':
            deltay=-pixel
        elif action=='down':
            deltay=+pixel
        elif action=='left':
            deltax=-pixel
        elif action=='right':
            deltax=+pixel
        else:
            print("no this move!\n")
            return
        x=self.canvas.coords(self.searcher)[0]+deltax
        y=self.canvas.coords(self.searcher)[1]+deltay
        if (x>=0)&(x<=self.max_length-pixel)&(y>=0)&(y<=self.max_width-pixel):
            self.update()
            self.canvas.move(self.searcher,deltax,deltay)
        else:
            print("move out of edge!\n")
            return


if __name__=='__main__':
    a=env_maz()
    #a.mainloop()
    for i in range(100):
        a.after(500,a.move(a.action[random.randint(0,3)]))
    #a.after(500,a.move('down'))
    #a.after(500,a.move('left'))
    a.mainloop()
