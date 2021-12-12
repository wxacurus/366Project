import copy

def checkInput(initial):
    #assuming 3x3 grid
    concat = concatBoard(initial.board)
    if len(concat) == 9:
        for num in range(9):
            if num not in concat:
                return False
        return True
    else:
        return False

def checkSolveable(initial, goal):
    #assuming 3x3 proper grid
    inversions = 0
    board = concatBoard(initial.board)
    for index in range(len(board)):
        for num in range(index + 1, len(board)):
            if board[index] > board[num] and board[num] != 0:
                inversions += 1
    if inversions % 2 == 0:
        return True
    else:
        return False

def concatBoard(board):
    returnList = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            returnList.append(board[row][col])
    return returnList

def heuristicCalculation(initial, goal):
    total = 0
    goalConcat = concatBoard(goal.board)
    boardConcat = concatBoard(initial.board)
  
    #Manhattan first
    for row in range(3):
        for col in range(3):
            if initial.board[row][col] != 0:
                idx = goalConcat.index(initial.board[row][col])
                total += abs(row - (idx // 3)) + abs(col - (idx % 3))
                
    #linear conflicts
    potential = [1, 2, 3, 4, 5, 6, 7, 8]
    while potential != []:
        num = potential.pop()
        try:
            if initial.board[num//3].index(num) >= 0:
                conflict = boardConcat.index(num)
                if conflict in potential:
                    potential.remove(conflict)
                    total += 2
            elif initial.board[0][num%3] == num or initial.board[1][num%3] == num or initial.board[2][num%3] == num:
                if concat.index(num) != num:
                    conflict = boardConcat.index(num)
                    if conflict in potential:
                        potential.remove(conflict)
                        total += 2
        except:
            continue
    return total

def isGoal(initial, goal):
    if initial == goal:
        return True
    return False

def IDAStar(initial, goal):
    initial.h = heuristicCalculation(initial, goal)
    initial.f = initial.g + initial.h
    limit = initial.f
    var = 0
    while (str(var).isdigit()==True):
        var, cont, optimal, board = limitDFS(initial, goal, limit)
        if cont:
            limit = var
        else:
            return var, board
        if optimal > 100:
            return ("non-optimal, ended early"), board
    return var, board

def findMoves(initial):
    board = concatBoard(initial.board)
    blank = board.index(0)
    ret = []
    if blank % 3 == 1:
        first = []
        second = []
        first.append(blank//3)
        first.append(0)
        second.append(blank//3)
        second.append(2)
        ret.append(first)
        ret.append(second)
    else:
        first = []
        first.append(blank//3)
        first.append(1)
        ret.append(first)
        
    if blank//3 == 1:
        first = []
        second = []
        first.append(0)
        first.append(blank%3)
        second.append(2)
        second.append(blank%3)
        ret.append(first)
        ret.append(second)
    else:
        first = []
        first.append(1)
        first.append(blank%3)
        ret.append(first)
    return ret
        
def limitDFS(initial, goal, limit):
    done = False
    miniumum = 9999999
    number_expanded = 0
    openList = []
    path = []
    openList.append(initial)
    while not done:
        initial.h = heuristicCalculation(initial, goal)
        initial.f = initial.g + initial.h

        if initial.f <= limit:
            if isGoal(initial.board, goal.board):
                return number_expanded, False, 0, initial.board
            else: 
                neighbors = findMoves(initial)
                for move in neighbors:
                    newBoard = copy.deepcopy(initial)
                    newBoard.makeMove(move)
                    newBoard.g = initial.g + 1
                    if newBoard not in openList:
                        openList.append(newBoard)
        else:
            if (initial.f < miniumum) or miniumum == None:
                miniumum = initial.f       
        try:
            initial = openList.pop()
        except:
            done = True        
        number_expanded += 1       
    return miniumum, True, initial.f, initial.board

class Board():
    def __init__(self, board, g, h, f):
        self.board = board
        self.g = g
        self.h = h
        self.f = f
        
    def __eq__(self, other):
        return self.board == other.board
    
    def makeMove(self, move):
        zRow = 0
        zCol = 0
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == 0:
                    zRow = row
                    zCol = col
                    break
        temp = self.board[move[0]][move[1]]
        self.board[move[0]][move[1]] = 0
        self.board[zRow][zCol] = temp

if __name__ == "__main__":  
    initial = Board([[0, 3, 1],[2, 4, 5],[6, 7, 8]], 0, 0, 0)
    goal = Board([[0, 1, 2],[3, 4, 5],[6, 7, 8]], 0, 0, 0)
    
    properInput = checkInput(initial)
    if not properInput:
        print("Bad input, please try again.")
    else:
        possible = checkSolveable(initial, goal)
        if not possible:
            print("Impossible solution")
        else:
            numIterations, finalBoard = IDAStar(initial, goal)
            print("Number of scenarios visited:", numIterations)
            print("Final Board:", finalBoard)
