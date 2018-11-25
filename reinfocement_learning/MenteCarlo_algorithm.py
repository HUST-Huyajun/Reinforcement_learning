#epsilon-greedy and value iteration 
import RL_struct
import Table
class MenteCarlo(RL_struct.RL_struct):
    def __init__(self, epsilon_greedy = 0.9, reward_delay = 0.9, learning_rate = 0.5, train_times = 10):
        super().__init__(epsilon_greedy, reward_delay, learning_rate, train_times)
        self.sampling_times=Table.State_Action_table(self.actions)
    def learning(self,s0,action0,target):#速度优化可以开表记录总和和次数
        self.sampling_times.count_s_a(s0,action0)
        oldvalue=self.Q_table.read_table(s0,action0)
        n_times=self.sampling_times.read_table(s0,action0)
        new_value=(oldvalue*(n_times-1)+target)/n_times
        self.Q_table.modify_table(s0,action0,new_value)
    def caculate_target(self,s0,action0):
        s1,reward=self.Env.do_move(s0,action0)#环境交互
        if(self.Env.Whether_to_end(s1)):
            target=reward
        else:
            action1=self.epsilon_choose_action(s1)
            target=reward+self.gamma*self.caculate_target(s1,action1)
        
        self.learning(s0,action0,target)
        return target
    def training(self):
        for i in range(self.n):#n次完整训练
            s0=self.Env.reset()
            action0=self.epsilon_choose_action(s0)
            target=self.caculate_target(s0,action0)
            self.learning(s0,action0,target)
            
            print('iteration=',i)
            self.Q_table.show_data()

if __name__=='__main__':
    a=MenteCarlo(train_times=1000)
    
    a.training()
    #time.sleep(5)
    a.run()
    a.Env.mainloop()
            
