class hw3:
    def __init__(self, dim, fileDir):
        self.dim = dim
        self.expandedNodes = 0
        with open(fileDir) as f:
            content = f.readlines()
            self.board = [list(x.strip()) for x in content]
        
    def solveSimpleBackTracking(self):

        location = self.getNextLocation()

        if location[0] == -1:

            return True

        else:

            self.expandedNodes += 1
            for choice in range(1, self.dim + 1):
                if self.isSafe(location[0], location[1], choice):
                    self.board[location[0]][location[1]] = str(choice)
                    if self.solveSimpleBackTracking():
                        return True
                    self.board[location[0]][location[1]] = '0'
        return False

    def isSafe(self, x, y, choice):
        bx = True
        by = True
        for i in range(0, self.dim):
            if self.board[i][y]  == str(choice):
                return False
        for j in range(0, self.dim):
            if self.board[x][j]  == str(choice):
                return False
        square_x = x - x % 3
        square_y = y - y % 3
        for i in range(3):
            for j in range(3):
                if self.board[square_x+i][square_y+j] == str(choice):
                    return False
        return True
    def getNextLocation(self):
        
        for i in range(0,self.dim):
            for j in range(0,self.dim):
                if self.board[i][j] =='0':
                    return (i,j)
        return (-1,-1)
s= hw3(9,"filedir.txt")
s.solveSimpleBackTracking()
for i in range(0,9):
    for j in range(0,9):
        print(s.board[i][j],end=" ")
    print()