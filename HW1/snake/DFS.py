from Utility import Node
from Algorithm import Algorithm

# site manba:
# https://github.com/NinaM31/Snake-ai

class DFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def initial(self):
        self.frontier = []
        self.explored_set = []
        self.path = []
    def run_algorithm(self, snake):
        
        if len(self.path) == 0:
            self.initial()
            startandgoal = self.get_initstate_and_goalstate(snake)
            self.frontier.append(startandgoal[0])
            return self.DFS(snake, startandgoal[1], startandgoal[0])
        else:
            Nodeforexpand = self.path.pop()
            if self.inside_body(snake, Nodeforexpand):
                self.path = [] 
            return Nodeforexpand
    
    def exist(self, node):
        if node in self.explored_set:
            return True
        return False

    def DFS(self, snake, goal, start):
        if self.exist(start):
                return None
        if start.x==goal.x and start.y==goal.y:
            return self.get_path(start)
        childrens = self.get_neighbors(start)  
        if not self.exist(start):
            self.explored_set.append(start)
        
        for child in childrens:
            if self.inside_body(snake, child) != True:
                if self.outside_boundary(child) != True :
                    if self.exist(child) != True:
                        child.parent = start  
                        path = self.DFS(snake, goal, child)  
                        if path != None:
                            return path  
        return None

    