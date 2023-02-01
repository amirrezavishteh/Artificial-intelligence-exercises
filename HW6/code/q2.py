from random import choice
import os
import random
import math
import copy
player, opponent = 'X', 'O'
iteration_numbers = 1000
# link ha:
# https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
# https://vgarciasc.github.io/mcts-viz/

class linkboard:
    def __init__(self, board):

        self.board = board
        self.childrens = []
        self.parent = None
        self.value = 0
        self.visit = 0
        self.ucb = 0

    def calculateucb(self):
        if (self.visit == 0):
            self.ucb = float('inf')
        else:
            if self.parent == None:
                self.ucb = self.value/self.visit
            else:
                self.ucb = self.value/self.visit + math.sqrt(2*math.log(self.parent.visit)/self.visit)

    def set_score(self, value):
        self.value = value

    def set_parent(self, parent):
        self.parent = parent

    def set_children(self, children):
        self.childrens.append(children)

    def get_children(self):
        return self.childrens

    def get_parent(self):
        return self.parent

    def get_board(self):
        return self.board
# turn =0->player='X' , 1->'O'


def make_childrens(emptyhomes, link, total, turn):
    childrens = []
    board = link.get_board()
    for i in emptyhomes:
        newboard = copy.deepcopy(board)
        newboard[i[0]][i[1]] = player if turn == 0 else opponent
        c = linkboard(newboard)
        c.set_parent(link)
        link.set_children(c)
        childrens.append(c)
        total.append(c)
    return childrens


def get_emptyhomes(board):
    emptyhomes = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                emptyhomes.append([i, j])
    return emptyhomes


def get_score(board):
    score = 50
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2] and not board[row][0] == '_'):
            if board[row][0] == board[row][1] and board[row][1] == board[row][2]== player:
                score = -70
            else:
                score = 48
    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col] and not board[0][col] == '_'):
            if board[0][col] == board[1][col] and board[1][col] == board[2][col]== player:
                score = -54
            else:
                score = 50
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and not board[0][0] == '_'):
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]== player:
            score = -55
        else:
            score = 55
    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and not board[0][2] == '_'):
        if board[0][2] == board[1][1] and board[1][1] == board[2][0] == player:
            score = -40
        else:
            score = 66
    return score

    


def selection(link):
    if len(link.childrens )==0:
        return link
    else:
        maxucb = 0
        for i in link.get_children():
            i.calculateucb()
            if i.ucb >= maxucb:
                maxucb = i.ucb
                link = i
        return selection(link)




# def expansion(link, total, turn):
#     emptyhomes = get_emptyhomes(link.get_board())
#     childrens = make_childrens(emptyhomes, link, total, turn)
#     # return random.choice(childrens)
#     return pick(link,childrens)
def expansion(link, turn):
    emptyhomes = get_emptyhomes(link.get_board())
    childrens = []
    for i in emptyhomes:
        newboard = copy.deepcopy(link.get_board())
        newboard[i[0]][i[1]] = player if turn == 0 else opponent
        c = linkboard(newboard)
        c.set_parent(link)
        link.set_children(c)
        c.calculateucb()
        childrens.append(c)
    return selection(link)

def simulation(link, turn):
    board = copy.deepcopy(link.get_board())
    emptyhomes = get_emptyhomes(board)
    while emptyhomes != [] and isMovesLeft(link.get_board()) and not checkWin(board) :
        home = random.choice(emptyhomes)
        board[home[0]][home[1]] = player if turn == 0 else opponent
        emptyhomes.remove(home)
        turn = 1-turn
    return get_score(board)


def backpropagation(link, score):
    link.visit += 1
    link.value += score
    if link.get_parent() != None:
        backpropagation(link.get_parent(), score)


def update(link):
    link.calculateucb()
    if link.get_children() != None:
        for e in link.get_children():
            update(e)
# def get_best_move(total):

#     max=0
#     if len(total)==1:
#         return total[0]
#     for i in total:
#         # i.calculateucb()
#         if max<i.value:
#             max=i.value
#             link=i
#     return link


def findbesthome(bestmove, firstboard):
    for i in range(3):
        for j in range(3):
            if (bestmove[i][j] != firstboard[i][j]):
                return [i, j]


def findBestMove(board):
    first = linkboard(board)
    total = []
    total.append(first)
    turn = 1
    for i in range(iteration_numbers):
        link = selection(first)
        if isMovesLeft(link.get_board()) and not checkWin(first.get_board()) :
            link=expansion(link,turn)
            
        
        # link=get_best_move(total)
        

        # link = expansion(link, turn)

        score = simulation(link, turn)

        backpropagation(link, score)
    best=0
    for i in first.get_children():
        temp=i.ucb
        if temp>= best:
            best=temp
            link=i
    
    return findbesthome(link.get_board(), board)


def possibleselection(link, total, turn):
    emptyhomes = findempty(board)
    childrens = make_childrens(emptyhomes, link, total, turn)
    return childrens


def findempty(board):
    res = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                res.append((i, j))
    return res





def findRandom(board):
    empty_spots = [i*3+j for i in range(3)
                   for j in range(3) if board[i][j] == "_"]
    idx = choice(empty_spots)
    return [int(idx/3), idx % 3]


def isMovesLeft(board):
    return ('_' in board[0] or '_' in board[1] or '_' in board[2])


def checkWin(board):
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2] and not board[row][0] == '_'):
            return True
    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col] and not board[0][col] == '_'):
            return True

    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and not board[0][0] == '_'):
        return True

    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and not board[0][2] == '_'):
        return True

    return False


def printBoard(board):
    os.system('cls||clear')
    print("\n Player : X , Agent: O \n")
    for i in range(3):
        print(" ", end=" ")
        for j in range(3):
            if (board[i][j] == '_'):
                print(f"[{i*3+j+1}]", end=" ")
            else:
                print(f" {board[i][j]} ", end=" ")

        print()
    print()


if __name__ == "__main__":
    board = [
            ['_', '_', '_'],
            ['_', '_', '_'],
            ['_', '_', '_']
    ]

    turn = 0

    while isMovesLeft(board) and not checkWin(board):
        if (turn == 0):
            printBoard(board)
            print(" Select Your Move :", end=" ")
            tmp = int(input())-1
            userMove = [int(tmp/3),  tmp % 3]
            while ((userMove[0] < 0 or userMove[0] > 2) or (userMove[1] < 0 or userMove[1] > 2) or board[userMove[0]][userMove[1]] != "_"):
                print('\n \x1b[0;33;91m' + ' Invalid move ' + '\x1b[0m \n')
                print("Select Your Move :", end=" ")
                tmp = int(input())-1
                userMove = [int(tmp/3),  tmp % 3]
            board[userMove[0]][userMove[1]] = player
            print("Player Move:")
            printBoard(board)
            turn = 1
        else:

            bestMove = findBestMove(board)
            board[bestMove[0]][bestMove[1]] = opponent
            print("Agent Move:")
            printBoard(board)
            turn = 0

    if (checkWin(board)):
        if (turn == 1):
            print('\n \x1b[6;30;42m' + ' Player Wins! ' + '\x1b[0m')

        else:
            print('\n \x1b[6;30;42m' + ' Agent Wins! ' + '\x1b[0m')
    else:
        print('\n \x1b[0;33;96m' + ' Draw! ' + '\x1b[0m')

    input('\n Press Enter to Exit... \n')
