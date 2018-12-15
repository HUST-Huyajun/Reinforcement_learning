import RL_struct
class Q_learning(RL_struct.RL_struct):
    def __init__(self,epsilon_greedy=0.9,reward_delay=0.9,learning_rate=0.5,train_times=10):
        super().__init__(epsilon_greedy, reward_delay, learning_rate, train_times)

    def learning(self,s0,action0,s1,action1,reward):
        self.Q_table.check_state(s0)
        self.Q_table.check_state(s1)
        if self.Env.Whether_to_end(s1) or action1=='None':
            target=reward
        else:
            target=reward+self.Q_table.max_state_value(s1)*self.gamma#Q-learning更新核心公式 与SARSA不同之处
        oldvalue=self.Q_table.read_table(s0,action0)
        new_value=oldvalue+(target-oldvalue)*self.alpha
        self.Q_table.modify_table(s0,action0,new_value)

    def training(self):
        for i in range(self.n):#n次完整训练
            s0=(-1,-1)
            s1=self.Env.reset()
            action0='None'
            action1=self.epsilon_choose_action(s1)
            while True:
                s0=s1
                action0=action1
                s1,reward=self.Env.do_move(s0,action0)#环境交互
                action1=self.epsilon_choose_action(s1)
                self.learning(s0,action0,s1,action1,reward)#从环境反馈学习
                if self.Env.Whether_to_end(s1):
                    break

            print('iteration=',i)
            self.Q_table.show_data()
            print('this move to '+self.run(),'\n')
            # if self.run()=='apple':
            #     break
            # else:
            #     print('this move to '+self.run())
        #self.Env.mainloop()

if __name__=='__main__':
    a=Q_learning(train_times=10000,learning_rate=0.1,epsilon_greedy=0.01)
    
    a.training()
    #time.sleep(5)
    a.run()
    a.Env.mainloop()

           
