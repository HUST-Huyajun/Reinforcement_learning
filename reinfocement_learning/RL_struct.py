
import Table 
import numpy as np
import Environment_Maze
import time
class RL_base():
    def __init__(self,epsilon_greedy=0.9,reward_delay=0.9,learning_rate=0.5,train_times=10,tabu_step=0):
        self.epsilon=epsilon_greedy
        self.gamma=reward_delay
        self.alpha=learning_rate#只对Sarsa 和Q-learning有意义
        self.n=train_times
        self.Env=Environment_Maze.env_maz()
        self.actions=self.Env.actions
        self.Q_table=Table.State_Action_table(self.actions)

    def reset(self):
        s1=self.Env.reset()
        return s1
    def epsilon_choose_action(self,s0):#epsilon-greedy
        if self.Env.Whether_to_end(s0):
            return 'None'
        self.Q_table.check_state(s0)
        legal_actions=list()
        for action in self.actions:
            if self.Env.is_move_legal(action):#判断合法性(是否越界)
                legal_actions.append(action)
        if len(legal_actions)==0:
            return 'None'
        else:
            if np.random.uniform(0,1)<self.epsilon:#利用
                action=self.Q_table.choose_best_action(s0,legal_actions)
            else:#探索
                action=np.random.choice(legal_actions)
            return action
    def run_choose_action(self,s0):
        self.Q_table.check_state(s0)
        action=self.Q_table.choose_only_one_best_action(s0)
        if self.Env.is_move_legal(action):
            return action
        else:
            return 'None'
    def set_tabu(self,s0,action0,s1,action1):#为了上下结构完整只需要调整RL_struct即可调整是否禁忌
        return
    def run(self):
        s0=(-1,-1)
        s1=self.reset()
        action0='None'
        action1=self.run_choose_action(s1)
        while True:
            s0=s1
            action0=action1
            if action0=='None':
                break
            s1,_=self.Env.do_move(s0,action0)#环境交互
            action1=self.run_choose_action(s1)
            if self.Env.Whether_to_end(s1) or action1=='None':
                break
        return self.Env.where_state(s1)
    def roll_back(self,s0,action0):#如果踏入禁忌区域就回滚 base就是啥也不做
        return s0,action0

class RL_tabu(RL_base):#每一次抽样中禁忌
    def __init__(self, epsilon_greedy = 0.9, reward_delay = 0.9, learning_rate = 0.5, train_times = 10,tabu_step=10):
        super().__init__(epsilon_greedy, reward_delay, learning_rate, train_times,tabu_step)
        self.tabu_table=Table.State_Action_table(['tabu_value'])
        self.time=1
        self.tabu_step=tabu_step

        self.spredict_table=Table.tuple_table(self.actions)
    def reset(self):
        self.tabu_table.clear()#采样结束，清空禁忌信息
        self.time=1
        s1=self.Env.reset()
        return s1

            
    def whether_tabu(self,s0,action):
        s1=self.spredict_table.read_table(s0,action)
        if s1=='None':#还没有状态转移信息
            return False
        else:
            if self.tabu_table.read_table(s1,'tabu_value')<self.time:
                return False
            else:
                return True

    def epsilon_choose_action(self, s0):
        if self.Env.Whether_to_end(s0):
            return 'None'
        self.Q_table.check_state(s0)
        self.tabu_table.check_state(s0)
        legal_actions=list()
        for action in self.actions:
            if self.Env.is_move_legal(action):
                if self.whether_tabu(s0,action)==False:#判断合法性(是否越界)和是否禁忌
                    legal_actions.append(action)
                else:
                    print(s0,action)
        if len(legal_actions)==0:
            print("no legal_action in tabu pattern")
            self.tabu_table.show_data()
            print('choose',s0,self.time)
            return 'None'
        else:
            if np.random.uniform(0,1)<self.epsilon:#利用 (0,epsilon)利用
                action=self.Q_table.choose_best_action(s0,legal_actions)
            else:#探索
                action=np.random.choice(legal_actions)
            return action
    def set_tabu(self,s0,action0,s1,action1):#每次学习结束后设置禁忌,学习状态转移
        self.spredict_table.modify_table(s0,action0,s1)

        self.tabu_table.modify_table(s0,'tabu_value',self.time+self.tabu_step)
        self.time+=1

    def roll_back(self,s0,action0):#如果踏入禁忌区域就回滚
        s1=self.spredict_table.read_table(s0,action0)
        if s1=='None':#如果没有记录不知道状态转移信息
            s1,_=self.Env.do_move(s0,action0)#环境交互
            self.spredict_table.modify_table(s0,action0,s1)
            if self.whether_tabu(s0,action0):
                #self.tabu_table.show_data()
                print('do move',s0,action0)
                print('comeback',s1,s0)
                self.Env.do_back(s0,action0,s1)#回滚
                action0=self.epsilon_choose_action(s0)
                return s0,action0
            else:
                self.Env.do_back(s0,action0,s1)#回滚//消除本次试探的影响，其实可以对后面的move优化
                return s0,action0
        else:
            if self.whether_tabu(s0,action0):
                action0=self.epsilon_choose_action(s0)
                return s0,action0
            else:
                return s0,action0

        


