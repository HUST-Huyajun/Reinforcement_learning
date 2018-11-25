import RL_struct
import Table
class MenteCarlo(RL_struct.RL_struct):
    def __init__(self, epsilon_greedy = 0.9, reward_delay = 0.9, learning_rate = 0.5, train_times = 10):
        sampling_tims=Table.State_Action_table()
        super().__init__(epsilon_greedy, reward_delay, learning_rate, train_times)
    def learning(self,s0,action0,target):#速度优化可以开表记录总和和次数
        oldvalue=self.Q_table.read_table(s0,action0)
        n_times=self.sampling_times.read_table(s0,action0)
        new_value=(oldvalues*(n_times-1)+target)/n_times
        self.Q_table.modify_table(s0,action0,new_value)
    def train(self):
        for i in range(self.n):#n次完整训练
            s0=self.Env.reset()
            action0=self.epsilon_choose_action(s0)
            sampling_tims.count_s_a(s0,action0)
            target=self.next_step(s0,action0)
            self.learning(s0,action0,target)

            
