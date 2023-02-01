from random import randrange
import random

class NQueens:
    def __init__(self, N):
        self.N = N

    def initial(self):
        ''' Returns a random initial state '''
        return tuple(randrange(self.N) for i in range(self.N))
    def amount(self,state):
        sum=0
        for x in range(self.N):
            for y in range(x+1,self.N):
                diffx=abs(x-y)
                diffy=abs(state[x]-state[y])
                if((state[x]==state[y]) or (diffx==diffy)):
                    sum+=1
        return sum
    
    def goal_test(self, state):
        
        if self.amount(state)>0:
            return False
        return True

    def value(self, state):
        ''' Returns the value of a state. The higher the value, the closest to a goal state '''
        return ((self.N*self.N)-self.amount(state))
    
    def safevalue(self,y,l):
        l.remove(y)
        return l
    
    def neighbors(self, state):
        ''' Returns all possible neighbors (next states) of a state '''
        l=[]
        temp=[]
        res=[]
        for i in range(self.N):
            temp.append(i)
        for i in range(self.N):
            l.append(temp)
            l[i]=self.safevalue(state[i],l[i])
            temp.append(state[i])
            for j in range(self.N-1):
                s=list(state)
                s[i]=l[i][j]
                res.append(tuple(s))
        return res