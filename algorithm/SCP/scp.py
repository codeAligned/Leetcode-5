import pulp
import random

class SCP(object):
    def __init__(self):
        super(SCP, self).__init__()
        self.X = []
        self.F = []
        self.data_generator(100)
        
    def data_generator(self, N):
        self.X = range(N)
        self.S0 = random.sample(self.X, 20)
        
        U = set(self.S0)
        F = [self.S0]
        i = 1
        while len(set(self.X) - set(U)) > 20:
            F.append([])
            n = random.randint(1, 20)
            x = random.randint(1, n)
            for j in range(0, i-1):
                U = U | set(F[j])
            
            remind_items = set(self.X) - U
            F[i].extend(random.sample(remind_items, x))
            F[i].extend(random.sample(U, n-x))
            i += 1
        F.append([])
        remind = list(set(self.X) - U)
        F[i].extend(remind)
        
        
        cur_size = len(F)
        remind_size = len(self.X) - cur_size
        
        for item in range(0, remind_size):
            n = random.randint(0, int(N/2))
            sample = random.sample(self.X, n)
            F.append(sample)
        
        self.F = F
        self.X = set(self.X)
        
    def greedy(self):
        F = self.F
        U = self.X
        C = []
        state = [0]*len(F)
        intersetion = {}
        index = -1
        while len(U) != 0:
            
            for i in range(0, len(F)):
                if state[i] == -1:
                    intersetion[i] = -1
                    continue
                intersetion[i] = len(set(F[i]) & U)
            
            for item in intersetion:
                if intersetion[item] == max(intersetion.values()):
                    index = item
                    break
           
            U = U - set(F[index])
            C.append(F[index])
            state[index] = -1
        
        return C
    
    def LP(self):
        C = []
        F = self.F
        sub_sets = []
        for i in range(0, len(F)):
            sub_sets.append('Sub{}'.format(i + 1))
        
        subject = []
        for i in range(0, len(self.X)):
            st = [-1] * len(F)
            for j in range(0, len(F)):
                if i in F[j]:
                    st[j] = 1
                else:
                    st[j] = 0
            subject.append(st)

        scp_model = pulp.LpProblem('SCP', pulp.LpMinimize)
        x = pulp.LpVariable.dict('x_%s', sub_sets, lowBound=0, upBound=1)
        cost = dict(zip(sub_sets, [1] * len(F)))
    
        scp_model += sum(cost[i] * x[i] for i in sub_sets)
        # parameters
        parameters = []
        for i in range(0, len(subject)):
            pars = dict(zip(sub_sets, subject[i]))
            parameters.append(pars)
    
        for item in range(0, len(parameters)):
            scp_model += sum([parameters[item][i] * x[i] for i in sub_sets]) >= 1.0
    
        scp_model.solve()
    
        lp_result = [x[item].value() for item in sub_sets]
        print(lp_result)
        f = max([sum(item) for item in subject])
        print(f)
        if f == 0:
            f = 0.0001
    
        for i in range(0, len(lp_result)):
            if lp_result[i] > 1.0 / f:
                C.append(F[i])
    
        return C
    
    
if __name__ == '__main__':
    S = SCP()
    g = S.greedy()
    ROUND = S.LP()
    print (ROUND)