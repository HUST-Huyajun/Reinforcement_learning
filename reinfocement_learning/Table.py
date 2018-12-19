import pandas as pd
import numpy as np
class State_Action_table:
    def __init__(self,actions):
        self.actions=actions
        self.n_actions=len(actions)
        self.__table=pd.DataFrame(columns=self.actions,dtype=float)
        self.__rand_seed=1
        #np.random.seed(self.__rand_seed)

    def check_state(self,s):#相当于动态初始化
        s=tuple(s)
        if s not in self.__table.index:
            self.__table=self.__table.append(other=pd.Series(data=[0]*self.n_actions,index=self.__table.columns,name=s))
    
    def count_s_a(self,state,action):
        self.check_state(state)
        self.__table.loc[[state],[action]]=self.__table.loc[[state],[action]]+1


    def choose_best_action(self,s0):
        self.check_state(s0)
        action_group=self.__table.loc[[s0],:]#tuple不加[]会出现错误，解释器无法识别是元组是统一一个参数还是多个参数
        best_action_group=action_group.loc[:,action_group.iloc[0]==np.max(action_group.values)].columns#
        if len(best_action_group)==0:
            print(s0)
            self.show_data()
        bestaction=np.random.choice(best_action_group)
        return bestaction
    def choose_best_action(self,s0,actions):
        action_group=self.__table.loc[[s0],actions]#tuple不加[]会出现错误，解释器无法识别是元组是统一一个参数还是多个参数
        best_action_group=action_group.loc[:,action_group.iloc[0]==np.max(action_group.values)].columns#
        if len(best_action_group)==0:
            print("best_action_group==0 s0=")
            print(s0)
            self.show_data()
        a=[val for val in best_action_group if val in actions]#求交集防止刚开始训练时候都是0出界
        bestaction=np.random.choice(a)
        return bestaction

    def choose_only_one_best_action(self,s0):#训练后run时使用
        self.check_state(s0)
        action_group=self.__table.loc[[s0],:]#tuple不加[]会出现错误，解释器无法识别是元组是统一一个参数还是多个参数
        best_action_group=action_group.loc[:,action_group.iloc[0]==np.max(action_group.values)].columns#
        if len(best_action_group)==1:
            bestaction=best_action_group[0]
        else:
            bestaction='None'
        return bestaction
    def modify_table(self,s,action,value):
        self.check_state(s)
        self.__table.loc[[s],[action]]=value
    def read_table(self,s,action):
        self.check_state(s)
        return self.__table.loc[[s],[action]].values[0][0]
    def max_state_value(self,s):
        self.check_state(s)
        action_group=self.__table.loc[[s],:]
        return np.max(action_group.values)
    def show_data(self):
        print(self.__table)
    def clear(self):
        self.__table.loc[:,:]=0.0
class tuple_table():#用来记录状态转移表
    def __init__(self,actions):
        self.actions=actions
        self.n_actions=len(actions)
        self.__table=pd.DataFrame(columns=self.actions,dtype=float)
        self.__rand_seed=1
        #np.random.seed(self.__rand_seed)

    def check_state(self,s):#相当于动态初始化
        s=tuple(s)
        if s not in self.__table.index:
            self.__table=self.__table.append(other=pd.Series(data=[0]*self.n_actions,index=self.__table.columns,name=s))
    
    def modify_table(self,s,action,value):#value 是 tuple
        self.check_state(s)
        x=value[0]
        y=value[1]
        self.__table.loc[[s],[action]]=str(x)+','+str(y)
    def read_table(self,s,action):
        self.check_state(s)
        value=self.__table.loc[[s],[action]].values[0][0]
        if value==0:
            return 'None'
        else:
            [x,y]=value.split(',')
            x=int(x.split('.')[0])#考虑到float型输入
            y=int(y.split('.')[0])
            return tuple([x,y])
    def show_data(self):
        print(self.__table)
if __name__=='__main__':
    table=State_Action_table(['up','down','left','right'])
    for i in range(5):
        for j in range(5):
            s=(i,j)
            print(type(s))
            table.check_state(s)
    table.show_data()
    s=(0,1)
    table.modify_table(s,'left',1)
    for i in range(20):
        print(table.choose_best_action(s))


