import pandas as pd
import numpy as np
class State_Action_table:
    def __init__(self,actions):
        self.actions=actions
        self.n_actions=len(actions)
        self.__table=pd.DataFrame(columns=actions,dtype=float)
        self.__rand_seed=1
        #np.random.seed(self.__rand_seed)

    def check_state(self,s):
        s=tuple(s)
        if s not in self.__table.index:
            self.__table=self.__table.append(other=pd.Series(data=[0]*self.n_actions,index=self.__table.columns,name=s))
    def choose_best_action(self,s0):
        self.check_state(s0)
        action_group=self.__table.loc[[s0],:]#tuple不加[]会出现错误，解释器无法识别是元组是统一一个参数还是多个参数
        best_action_group=action_group.loc[:,action_group.iloc[0]==np.max(action_group.values)].columns#
        if len(best_action_group)==0:
            print(s0)
            self.show_data()
        bestaction=np.random.choice(best_action_group)
        return bestaction
    def choose_only_one_best_action(self,s0):#正式运行时使用
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


