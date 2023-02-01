from NQueens import NQueens

def hill_climbing(problem:NQueens,state):
    ''' Returns a state as the solution of the problem '''
    Neighbors=problem.neighbors(state)
    max=problem.value(state)
    start=max
    best=state
    for ne in  Neighbors:
        temp=problem.value(ne)
        if max<=temp:
            max=temp
            best=ne
    
    return best

def hill_climbing_random_restart(problem:NQueens, limit = 10):
    state = problem.initial()
    cnt = 0
    while problem.goal_test(state) == False and cnt < limit:
        state = hill_climbing(problem,state)
        
        cnt += 1
    return state
