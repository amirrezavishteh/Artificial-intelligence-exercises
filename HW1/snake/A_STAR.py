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
    # def distmanhantan(self,sanke,mannhantan):
    #     start,goal=self.get_initstate_and_goalstate()
    #     childrens = self.get_neighbors(expandNode)

    def run_algorithm(self, snake):
        if len(self.path)==0:
            self.initial()
            start,goal=self.get_initstate_and_goalstate(snake)
            for n in range(NO_OF_CELLS):
                for m in range(NO_OF_CELLS):
                    self.grid[n][m].parent=None
                    self.grid[n][m].f=0
                    self.grid[n][m].g=0
                    self.grid[n][m].h=self.manhattan_distance(self.grid[n][m],goal)
            childrens = self.get_neighbors(start)
            for child in childrens:
                self.frontier.append(child)
                self.frontier.sort(key=lambda child : child.f,reverse=True)
                self.grid[child.x][child.y].g=1
                self.grid[child.x][child.y].f=self.grid[child.x][child.y].g + self.grid[child.x][child.y].h
            while len(self.frontier)>0 :
                current=self.frontier.pop()
                if current.equal(goal):
                    break
                if current not in self.explored_set:
                    self.explored_set.append(current)
                childrensf = self.get_neighbors(current)
                for c in childrensf:
                    if self.inside_body(snake, c) or self.outside_boundary(c) or c in self.explored_set:
                        continue
                    else:
                        c.parent = current
                        c.g=current.g+1
                        c.f=c.g + c.h
                        self.frontier.append(c)
                    self.frontier.sort(key=lambda c : c.f,reverse=True)
            masir= self.get_path(self.grid[goal.x][goal.y])
            if masir.parent != None:
                return masir
        else:
            return self.path.pop()
        return None