from collections import deque
from Utility import Node
from Algorithm import Algorithm

# site manba:
# https://github.com/NinaM31/Snake-ai

class BFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)
    def initial(self):
        self.frontier = deque([])
        self.explored_set = []
        self.path = []
    def exist(self, node):
        if node in self.explored_set:
            return True
        return False
    
    def run_algorithm(self, snake):
        startandgoal = self.get_initstate_and_goalstate(snake)
        self.initial()
        self.frontier.append(startandgoal[0])
        while True:
            if len(self.frontier) <= 0:
                break
            expandNode = self.frontier.popleft()  
            childrens = self.get_neighbors(expandNode)
            
            if not expandNode in self.explored_set :
                self.explored_set.append(expandNode)
            for child in childrens:
                if self.outside_boundary(child) and not  child in self.explored_set:
                    self.explored_set.append(child)
                    continue  
                if self.inside_body(snake, child)  :
                    self.explored_set.append(child)
                    continue 
                if self.inside_body(snake, child) and self.outside_boundary(child):
                    continue
                if child not in self.frontier :
                    if not self.exist(child):
                        self.explored_set.append(child)  
                        self.frontier.append(child)
                        child.parent = expandNode  
                        if child.x==startandgoal[1].x and child.y==startandgoal[1].y:
                            return self.get_path(child)
        return None