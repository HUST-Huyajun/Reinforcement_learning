
import Table 
import numpy as np
import Environment_Maze
import time
class Q_learning():
    def __init__(self,epsilon_greedy=0.9,reward_delay=0.9,learning_rate=0.1,train_times=10):
        self.epsilon=epsilon_greedy
        self.gamma=reward_delay
        self.alpha=learning_rate
        self.n=train_times
        self.Env=Environment_Maze.env_maz()
        self.actions=self.Env.actions
        self.Q_table=Table.State_Action_table(self.actions)

    def epsilon_choose_action(self,s0):
        self.Q_table.check_state(s0)
        if np.random.uniform(0,1)<self.epsilon:#利用
            action=self.Q_table.choose_best_action(s0)
        else:#探索
            action=np.random.choice(self.actions)
        return action
    def run_choose_action(self,s0):
        self.Q_table.check_state(s0)
        return self.Q_table.choose_only_one_best_action(s0)
    def run(self):
        s0=self.Env.reset()
        s1=(-1,-1)
        done=False
        while True:
            action=self.run_choose_action(s0)#算法自动选择
            if(self.Env.is_move_legal(action)):#判断合法性
                done,s1,reward=self.Env.do_move(s0,action)#在环境中动作
                s0=s1
                if done:
                    break
            else:
                break
        return self.Env.judge_state(s0)
    def learning(self,s0,action,s1,reward):
        self.Q_table.check_state(s0)
        self.Q_table.check_state(s1)
        target=reward+self.Q_table.max_state_value(s1)*self.gamma#Q-learning更新核心公式 与SARSA不同之处
        oldvalue=self.Q_table.read_table(s0,action)
        new_value=oldvalue+(target-oldvalue)*self.alpha
        self.Q_table.modify_table(s0,action,new_value)

    def training(self):
        for i in range(self.n):#n次完整训练
            s0=self.Env.reset()
            s1=(-1,-1)
            done=False
            while True:
                action=self.epsilon_choose_action(s0)#算法自动选择
                if(self.Env.is_move_legal(action)):#判断合法性
                    done,s1,reward=self.Env.do_move(s0,action)#环境交互
                    self.learning(s0,action,s1,reward)#从环境反馈学习
                    if done:
                        break
                    s0=s1
            print('iteration=',i)
            self.Q_table.show_data()
            if self.run()=='apple':
                break
            else:
                print('this move to '+self.run())
        #self.Env.mainloop()

if __name__=='__main__':
    a=Q_learning(train_times=100)
    a.training()
    #time.sleep(5)
    a.run()
    a.Env.mainloop()

           
