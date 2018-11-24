
import Table 
import numpy as np
import Environment_Maze
import time
class RL_struct():
    def __init__(self,epsilon_greedy=0.9,reward_delay=0.9,learning_rate=0.5,train_times=10):
        self.epsilon=epsilon_greedy
        self.gamma=reward_delay
        self.alpha=learning_rate
        self.n=train_times
        self.Env=Environment_Maze.env_maz()
        self.actions=self.Env.actions
        self.Q_table=Table.State_Action_table(self.actions)

    def epsilon_choose_action(self,s0):
        if self.Env.Whether_to_end(s0):
            return 'None'
        self.Q_table.check_state(s0)
        while True:
            if np.random.uniform(0,1)<self.epsilon:#利用
                action=self.Q_table.choose_best_action(s0)
            else:#探索
                action=np.random.choice(self.actions)
            if self.Env.is_move_legal(action):#判断合法性(是否越界)
                break
        return action
    def run_choose_action(self,s0):
        self.Q_table.check_state(s0)
        action=self.Q_table.choose_only_one_best_action(s0)
        if self.Env.is_move_legal(action):
            return action
        else:
            return 'None'
    def run(self):
        s0=(-1,-1)
        s1=self.Env.reset()
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
    

