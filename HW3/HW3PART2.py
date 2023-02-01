class Sodo:
    def __init__(self, dim, fileDir):
        self.dim = dim
        self.expandedNodes = 0
        with open(fileDir) as f:
            content = f.readlines()
            self.board = [list(x.strip()) for x in content]
        self.rv = self.getRemainingValues()

    def getDomain(self, row, col):
        RVCell = [str(i) for i in range(1, self.dim + 1)]
        for i in range(self.dim):
            if self.board[row][i] != '0':
                if self.board[row][i] in RVCell:
                    RVCell.remove(self.board[row][i])
        for i in range(self.dim):
            if self.board[i][col] != '0':
                if self.board[i][col] in RVCell:
                    RVCell.remove(self.board[i][col])
        boxRow = row - row % 3
        boxCol = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.board[boxRow + i][boxCol + j] != 0:
                    if self.board[boxRow + i][boxCol + j] in RVCell:
                        RVCell.remove(self.board[boxRow + i][boxCol + j])
        return RVCell

    def getRemainingValues(self):
        RV = []
        for row in range(self.dim):
            for col in range(self.dim):
                if self.board[row][col] != '0':
                    RV.append(['x'])
                else:
                    RV.append(self.getDomain(row, col))
        return RV
    def getNextLocation(self):
        list=[]
        for i in range(0,self.dim):
            for j in range(0,self.dim):
                if self.board[i][j] =='0':
                    list.append((i,j))
        if len(list)==0:
            return (-1,-1)
        min =len(self.rv[list[0][0]*self.dim+list[0][1]])
        res=list[0]
        for e in list:
            temp=len(self.rv[e[0]*self.dim+e[1]])
            if(temp<min):
                min =temp
                res=e
        return res
    def solveCspBackTracking(self):
        location = self.getNextLocation()
        b=True
        if location[0] == -1:
            return True
        else:
            self.expandedNodes += 1
            for choice in  self.rv[location[0]*self.dim + location[1]] :
                    self.board[location[0]][location[1]] = str(choice)
                    self.rv=self.getRemainingValues()
                    if self.solveCspBackTracking():
                        return True
                    self.board[location[0]][location[1]] = '0'
        return False
s= Sodo(9,"filedir.txt")
s.solveCspBackTracking()
for i in range(0,9):
    for j in range(0,9):
        print(s.board[i][j],end=" ")
    print()