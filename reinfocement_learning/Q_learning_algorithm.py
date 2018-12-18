import RL_struct as RLst
class Q_learning(RLst.RL_tabu):
    def __init__(self,epsilon_greedy=0.9,reward_delay=0.9,learning_rate=0.5,train_times=10,tabu_step=0):
        super().__init__(epsilon_greedy, reward_delay, learning_rate, train_times,tabu_step)

    def learning(self,s0,action0,s1,action1,reward):#已经从s0执行action0到s1,选择好了action1
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

            self.tabu_table.clear()#采样结束，清空禁忌信息
            self.time=1

            action0='None'
            action1=self.epsilon_choose_action(s1)
            while True:
                s1,action1=self.roll_back(s1,action1)#看是否踏入了禁忌区踏入了就重新选 s1,action1是马上要进行的动作
                s0=s1
                action0=action1

                print('do move',s0,action0)
                s1,reward=self.Env.do_move(s0,action0)#环境交互

                action1=self.epsilon_choose_action(s1)#Q-learning里可有可无

                self.learning(s0,action0,s1,action1,reward)#从环境反馈学习
                self.set_tabu(s0,action0,s1,action1)#设置禁忌
                if self.Env.Whether_to_end(s1):
                    break

            print('iteration=',i)
            #self.Q_table.show_data()
            #self.tabu_table.show_data()
            #self.spredict_table.show_data()
            #place=self.run()
            #print('this move to '+place,'\n')
            #if place=='apple':
            #    break
            # else:
            #     print('this move to '+self.run())
        #self.Env.mainloop()

if __name__=='__main__':
    a=Q_learning(train_times=100,learning_rate=0.1,epsilon_greedy=0,tabu_step=10)
    
    a.training()
    #time.sleep(5)
    a.run()
    a.Env.mainloop()

           
