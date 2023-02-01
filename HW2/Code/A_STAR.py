from Algorithm import Algorithm
from Constants import NO_OF_CELLS 
from Utility import Node

class A_STAR(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)
    def initial(self):
        self.frontier = []
        self.explored_set = []
        self.path = []
    
    def run_algorithm(self, snake):
        if len(self.path)==0:
            self.initial()
            start,goal=self.get_initstate_and_goalstate(snake)
            start = self.grid[start.x][start.y]
            goal = self.grid[goal.x][goal.y]
            domain=NO_OF_CELLS
            for n in range(domain):
                for m in range(domain):
                    self.grid[n][m].h=self.manhattan_distance(self.grid[n][m],goal)
                    self.grid[n][m].parent=None
            childrens = self.get_neighbors(start)
            self.frontier.append(start)
            while len(self.frontier)>0 :
                current=self.frontier.pop()
                if current.equal(goal):
                    res=self.get_path(self.grid[current.x][current.y])
                    return res
                if current not in self.explored_set:
                    self.explored_set.append(current)
                childrenscurrent = self.get_neighbors(current)
                for c in childrenscurrent:
                    if  self.inside_body(snake, c) or  self.outside_boundary(c)  :
                        continue
                    if c  not in self.explored_set:
                        c.parent = current
                        c.g=current.g+1
                        c.f=c.g + c.h
                        self.frontier.append(c)
                    self.frontier=sorted(self.frontier , key=lambda c : c.f , reverse=True)
            
        elif len(self.path)>0 or len(self.path)<0:
            return self.path.pop()
        return None
    