
import numpy as np
import sys
import random
import time
if sys.version_info.major==2:
    import Tkinter as tk
else:
    import tkinter as tk
#迷宫大小参数
pixel=60
length=7
width=7
#美观参数
searcher_beauty_bias=10
#环境设置参数
hell=np.array([[3,1],[2,2],[5,4],[5,7],[7,3],[4,6]])#x为从左到右第几个，y为从上到下第几个
apple=np.array([[3,2]])
#动作延时参数
time_interval=200#ms
#奖赏设置
reward_dict={'hell':-1,'apple':1,'nothing':0}

class env_maz(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.action=['up','down','left','right']
        self.n_action=len(self.action)
        self.title('Find apple')
        self.max_length=length*pixel
        self.max_width=width*pixel
        self.geometry('{0}x{1}'.format((length)*pixel,(width+1)*pixel))

        self.state_text = tk.StringVar()
        self.state_Label=tk.Label(self,textvariable=self.state_text)
        self.state_Label.pack(side='bottom')

        self.action_text = tk.StringVar()
        self.action_Label=tk.Label(self,textvariable=self.action_text)
        self.action_Label.pack()
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
        _b=searcher_beauty_bias
        self.searcher=self.canvas.create_oval(x1+_b,y1+_b,x2-_b,y2-_b,fill='yellow')
        self.canvas.pack()
    def reset(self):
        self.update()
        time.sleep(1)
        self.canvas.delete(self.searcher)
        x1,y1,x2,y2=0,0,pixel,pixel
        _b=searcher_beauty_bias
        self.searcher=self.canvas.create_oval(x1+_b,y1+_b,x2-_b,y2-_b,fill='yellow')
        self.update()
        
    def is_move_legal(self,action):
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
            self.action_text.set('no->'+action+'<-action!')
            return
        x=self.canvas.coords(self.searcher)[0]+deltax
        y=self.canvas.coords(self.searcher)[1]+deltay
        if (x>=0)&(x<=self.max_length-pixel)&(y>=0)&(y<=self.max_width-pixel):
            return True
        else:
            return False

    def move(self,action):
        time.sleep(time_interval/1000)

        deltax=0
        deltay=0
        if action=='up':
            deltay=-pixel
            self.action_text.set('up')
        elif action=='down':
            deltay=+pixel
            self.action_text.set('down')
        elif action=='left':
            deltax=-pixel
            self.action_text.set('left')
        elif action=='right':
            deltax=+pixel
            self.action_text.set('right')
        else:
            print("no this move!\n")
            self.action_text.set('no->'+action+'<-action!')
            raise RuntimeError('no this move!')
            return -1
        x=self.canvas.coords(self.searcher)[0]+deltax-searcher_beauty_bias
        y=self.canvas.coords(self.searcher)[1]+deltay-searcher_beauty_bias
        #print("search",self.canvas.coords(self.searcher),'\n')
        if (x>=0)&(x<=self.max_length-pixel)&(y>=0)&(y<=self.max_width-pixel):
            self.canvas.move(self.searcher,deltax,deltay)
            self.update()
            for coord in hell:
                if ([x/pixel+1,y/pixel+1]==coord).all():
                    print("get to hell\n")
                    self.state_text.set('get to hell')
                    done=True
                    s=coord
                    return done,s,reward_dict['hell']#到地狱了
            for coord in apple:
                if ([x/pixel+1,y/pixel+1]==coord).all():
                    print("find the apple\n")
                    self.state_text.set('find the apple')
                    done=True
                    s=coord
                    return done,s,reward_dict['apple']#找到苹果了
            self.state_text.set('')
            done=False
            s=coord
            return done,s,reward_dict['nothing']
        else:
            print("This action will move out of the boundary!\n")
            self.state_text.set('This action will move out of the boundary!')
            raise RuntimeError('testError_This action will move out of the boundary!')
            return -1


if __name__=='__main__':
    a=env_maz()
    for i in range(100):
        a.reset()
        done=False
        while True:
            action=a.action[random.randint(0,3)]
            #action='down'
            if(a.is_move_legal(action)):
                
                done,s,reward=a.move(action)
                if done:
                    break
        
    #a.after(500,a.move('down'))
    #a.after(500,a.move('left'))
    #a.mainloop()
