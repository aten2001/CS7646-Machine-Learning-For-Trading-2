"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):
        self.num_actions=num_actions
        self.num_states=num_states
        self.alpha=alpha
        self.gamma=gamma
        self.rar=rar
        self.radr=radr
        self.dyna=dyna
        self.verbose=verbose
        self.s = 0
        self.a = 0
        self.s_=0
        self.s_a=dict()
        self._s=set()
        self.Q=dict()
        self.R=dict()
        self.C=dict()
        self.C_num=dict()
        self.C_num[self.s,self.a,self.s_]=0
        self.T=dict()
        self.Tc=dict()
        self.Tc[self.s,self.a,self.s_]=0.00001
        actions=[0,1,2,3]
        self.actions=dict()
        self.inv_actions=dict()
        for s in range(num_states):
            self.Q[s]=[]
            self.R[s]=[]
            for i,a in enumerate(actions):
                self.actions[a]=i
                self.inv_actions[i]=a
                self.Q[s].append(rand.random())
                self.R[s].append(0.0)
        for s in range(num_states):
            for a in actions:
                self.C_num[s,a]=0
                for s_ in range(num_states):
                    self.C[s,a,s_]=0
                    self.Tc[s,a,s_]=0.00001

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        q=[]
        for a in self.Q[s]:
            if a==max(self.Q[s]):
                q.append(0.8+0.2/len(self.Q[s]))
            else:
                q.append(0.2/len(self.Q[s]))
        index=np.argmax(q)
        r=rand.random()
        if self.rar>r:
            action=rand.randint(0, self.num_actions-1)
        else:
            action=self.inv_actions[index]
        self.a=action
        self.rar=self.radr*self.rar
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        if self.dyna==0:
            if r==1:
                self.Q[self.s][self.actions[self.a]]+=self.alpha*(r-self.Q[self.s][self.actions[self.a]])
            if r==-1:
                self.Q[self.s][self.actions[self.a]]+=self.alpha*(r+self.gamma*max(self.Q[s_prime])-self.Q[self.s][self.actions[self.a]])
            self.s = s_prime
            q=[]
            for a in self.Q[s_prime]:
                if a==max(self.Q[s_prime]):
                    q.append(0.8+0.2/len(self.Q[s_prime]))
                else:
                    q.append(0.2/len(self.Q[s_prime]))
            index=np.argmax(q)
            r=rand.random()
            if self.rar>r:
                action=rand.randint(0, self.num_actions-1)
            else:
                action=self.inv_actions[index]
            self.a = action
            self.rar=self.radr*self.rar
            if self.verbose: print "s =", s_prime,"a =",action,"r =",r
            return action

        elif self.dyna>0:

            if r==1:
                self.Q[self.s][self.actions[self.a]]+=self.alpha*(r-self.Q[self.s][self.actions[self.a]])
            if r==-1:
                self.Q[self.s][self.actions[self.a]]+=self.alpha*(r+self.gamma*max(self.Q[s_prime])-self.Q[self.s][self.actions[self.a]])
            q=[]
            for a in self.Q[s_prime]:
                if a==max(self.Q[s_prime]):
                    q.append(0.8+0.2/len(self.Q[s_prime]))
                else:
                    q.append(0.2/len(self.Q[s_prime]))
            index=np.argmax(q)
            rd=rand.random()
            if self.rar>rd:
                action=rand.randint(0, self.num_actions-1)
            else:
                action=self.inv_actions[index]
            self.rar=self.radr*self.rar


            dynalpha=0.2
            self.s_ = s_prime
            self.C[self.s,self.a,self.s_]+=1
            self.C_num[self.s,self.a]+=1
            if (self.s,self.a) not in self.T.keys():
                self.T[self.s,self.a]=[]
                self.T[self.s,self.a].append(self.s_)
            else:
                self.T[self.s,self.a].append(self.s_)
            self.Tc[self.s,self.a,self.s_]=self.C[self.s,self.a,self.s_]/self.C_num[self.s,self.a]
            self.R[self.s][self.actions[self.a]]=dynalpha*r+(1-dynalpha)*self.R[self.s][self.actions[self.a]]

            self._s.add(self.s)

            if self.s not in self.s_a.keys():
                self.s_a[self.s]=set()
                self.s_a[self.s].add(self.a)
            else:
                self.s_a[self.s].add(self.a)
            for i in range(0,self.dyna):
                state_dyna=np.random.choice(tuple(self._s))
                action_dyna=np.random.choice(tuple(self.s_a[state_dyna]))

                s_T=[]
                s_random=self.T[state_dyna,action_dyna]
                for i in s_random:
                    s_T.append(self.Tc[state_dyna,action_dyna,i])

                prime_dyna=np.random.choice(tuple(s_random))

                r_dyna=self.R[state_dyna][self.actions[action_dyna]]
                self.Q[state_dyna][self.actions[action_dyna]]+=self.alpha*(r_dyna+self.gamma*max(self.Q[prime_dyna])-self.Q[state_dyna][self.actions[action_dyna]])
            self.a = action
            self.s=s_prime
            return action
        else:
            print 'error'

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
