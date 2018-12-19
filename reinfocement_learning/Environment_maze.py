import numpy as np
import sys
import random
import time
if sys.version_info.major==2:
    import Tkinter as tk
else:
    import tkinter as tk

#迷宫大小参数
pixel=30
length=9
width=9
#美观参数
searcher_beauty_bias=5
#动作延时参数
time_interval=0#ms,每移动一次延时
terminal_interval=0#ms，每次抽样延时
#奖赏设置
reward_dict={'hell':-1,'apple':100,'normal':0}
#terminal设置
terminal_place={'hell':True,'apple':True,'normal':False}
def set_hell():
    #hell=np.array([[2,1],[3,1],[4,2],[2,3],[2,4],[2,5],[3,4],[2,6]])#x为从左到右第几个，y为从上到下第几个
    hell=np.array([[1,2]])
    path=list()
    path.append((1,1))
    x=2
    y=1
    status=0#0:right  1:down   2:left  3:up
    apple1=(0,0)
    while( (x,y) not in path):
        path.append((x,y))
        apple1=(x,y)
        if status==0:
            x+=1
            if x>length or (x+1,y) in path:
                x-=1
                y+=1
                status=1
        elif status==1:
            y+=1
            if y>width or (x,y+1) in path:
                y-=1
                x-=1
                status=2
        elif status==2:
            x-=1
            if x<=0 or (x-1,y) in path:
                x+=1
                y-=1
                status=3
        elif status==3:
            y-=1
            if y<=0 or (x,y-1) in path:
                y+=1
                x+=1
                status=0
    #print(path)
    for x in range(1,length):
        for y in range(1,width):
            if (x,y) not in path and (x,y) != (1,2):
                site=np.array([x,y])
                hell=np.row_stack((hell,[site]))
    #print(hell)
    apple=np.array([[apple1[0],apple1[1]]])
    #apple=np.array([])
    return hell,apple
#环境设置参数
hell,apple=set_hell()
#hell=np.array([[2,1],[3,1],[4,2],[2,3],[2,4],[2,5],[3,4],[2,6]])
#apple=np.array([[int(length/2),int(width/2)+1]])
#apple=np.array([[0,0]])
        



class ActionError(ValueError):
    def __init__(self,message):
        ValueError.__init__(self)
        self.message=message
class env_maz(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = 'Tk', useTk = 1, sync = 0, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.actions=['up','down','left','right']
        self.n_action=len(self.actions)
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
        if terminal_interval>0:
            time.sleep(terminal_interval/1000)
        self.canvas.delete(self.searcher)
        x1,y1,x2,y2=0,0,pixel,pixel
        _b=searcher_beauty_bias
        self.searcher=self.canvas.create_oval(x1+_b,y1+_b,x2-_b,y2-_b,fill='yellow')
        self.update()
        s0=(1,1)
        return s0#初始状态
        
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
        if action not in self.actions:
            return False
            
        x=self.canvas.coords(self.searcher)[0]+deltax-searcher_beauty_bias
        y=self.canvas.coords(self.searcher)[1]+deltay-searcher_beauty_bias
        if (x>=0)&(x<=self.max_length-pixel)&(y>=0)&(y<=self.max_width-pixel):
            return True
        else:
            return False
    def where_state(self,s1): #判断状态在哪
        s1=list(s1)
        for coord in hell:
            if (s1==coord).all():
                return 'hell'#到地狱了
        for coord in apple:
            if (s1==coord).all():
                return 'apple'#找到苹果了
        return 'normal'
    def Whether_to_end(self,s1): #判断是否为terminal
        done=terminal_place[self.where_state(s1)]
        return done

    def do_move(self,s0,action):#叫状态转移更好
        if time_interval>0:
            time.sleep(time_interval/1000)
        s0=list(s0)
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
            print(action)
            raise ActionError('No this action!')
        x=self.canvas.coords(self.searcher)[0]+deltax-searcher_beauty_bias
        y=self.canvas.coords(self.searcher)[1]+deltay-searcher_beauty_bias
        #print("search",self.canvas.coords(self.searcher),'\n')
        if (x>=0)&(x<=self.max_length-pixel)&(y>=0)&(y<=self.max_width-pixel):
            self.canvas.move(self.searcher,deltax,deltay)
            self.update()
            s1=[x/pixel+1,y/pixel+1]#
            where=self.where_state(s1)

            if where=='hell':
                self.state_text.set('get to hell')
            elif where=='apple':
                self.state_text.set('find the apple')
            elif where=='normal':
                self.state_text.set('')
            else:
                raise ValueError('not define->'+where+'<-this place')
            reward=reward_dict[where]
            return tuple(s1),reward#在普通板块
        else:
            raise ActionError('This action will move out of the boundary!')
    def do_back(self,s0,action0,s1):#这里为了方便还是用了对称信息，其实只要是模拟环境逻辑上完全可以做到model-free情况下的回滚
        if action0=='left':
            action0_oppose='right'
        elif action0=='right':
            action0_oppose='left'
        elif action0=='up':
            action0_oppose='down'
        elif action0=='down':
            action0_oppose='up'
        self.do_move(s1,action0_oppose)


if __name__=='__main__':
    a=env_maz()
    for i in range(10):
        s0=a.reset()
        done=False
        s=s0
        while True:
            action=a.actions[0]
            action='down'
            if(a.is_move_legal(action)):
                
                s1,reward=a.do_move(s,action)
                s=s1
                if a.Whether_to_end(s):
                    break
    a.mainloop()
    
