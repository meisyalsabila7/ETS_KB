from copy import deepcopy
from sys import exit
import sys
import pygame
import time
import random
pygame.init()

def generate():
    if args != '':
        puzzleArr = []
        for i in range(0,81,9):
            row = []
            for j in range(1,10):
                row.append(int(args[i+j-1]))
            puzzleArr.append(row)
        notSolved = deepcopy(puzzleArr)
        if solve(puzzleArr):
            return notSolved
        else:
            print("puzle not solvable exiting...")
            exit()
    else :    
        while True:  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            board = [[0 for i in range(9)] for j in range(9)]

            for i in range(9):
                for j in range(9):
                    if random.randint(1, 10) >= 5:
                        board[i][j] = random.randint(1, 9) 
                        if valid(board, (i, j), board[i][j]):
                            continue
                        else:
                            board[i][j] = 0
            partialBoard = deepcopy(board)  
            if solve(board):
                print(board)
                return partialBoard

def puzzle():
    sudoku = input("insert sudoku puzzle \n")

    puzzleArr = []
    for i in range(0,81,9):
        row = []
        for j in range(1,10):
            row.append(int(sudoku[i+j-1]))
        puzzleArr.append(row)
    return puzzleArr

class Board:
    def __init__(self, window):
        self.board = generate()
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        self.tiles = [[Tile(self.board[i][j], window, i * 60, j * 60) for j in range(9)] for i in range(9)]
        self.window = window

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                if j % 3 == 0 and j != 0:  
                    pygame.draw.line(self.window, (0, 0, 0), (j // 3 * 180, 0), (j // 3 * 180, 540), 4)

                if i % 3 == 0 and i != 0: 
                    pygame.draw.line(self.window, (0, 0, 0), (0, i // 3 * 180), (540, i // 3 * 180), 4)

                self.tiles[i][j].draw((0, 0, 0), 1)

                if self.tiles[i][j].value != 0:  
                    self.tiles[i][j].display(self.tiles[i][j].value, (21 + j * 60, 16 + i * 60), (0, 0, 0))  

        pygame.draw.line(self.window, (0, 0, 0), (0, (i + 1) // 3 * 180), (540, (i + 1) // 3 * 180), 4)

    def deselect(self, tile):
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j] != tile:
                    self.tiles[i][j].selected = False

    def redraw(self, keys, wrong, time):
        self.window.fill((255, 255, 255))
        self.draw_board()
        for i in range(9):
            for j in range(9):
                if self.tiles[j][i].selected: 
                    self.tiles[j][i].draw((50, 205, 50), 4)
                elif self.tiles[i][j].correct:

                    self.tiles[j][i].draw((34, 139, 34), 4)
                elif self.tiles[i][j].incorrect:

                    self.tiles[j][i].draw((255, 0, 0), 4)

        if len(keys) != 0:  
            for value in keys:
                self.tiles[value[0]][value[1]].display(keys[value], (21
                        + value[0] * 60, 16 + value[1] * 60), (128,
                        128, 128))

        if wrong > 0:
            font = pygame.font.SysFont('Bauhaus 93', 30) 
            text = font.render('X', True, (255, 0, 0))
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont('Bahnschrift', 40)  
            text = font.render(str(wrong), True, (0, 0, 0))
            self.window.blit(text, (32, 542))

        font = pygame.font.SysFont('Bahnschrift', 40)  
        text = font.render(str(time), True, (0, 0, 0))
        self.window.blit(text, (388, 542))
        pygame.display.flip()

    def visualSolve(self, wrong, time):
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                exit()

        empty = find_empty(self.board)
        if not empty:
            return True

        for nums in range(9):
            if valid(self.board, (empty[0], empty[1]), nums + 1):
                self.board[empty[0]][empty[1]] = nums + 1
                self.tiles[empty[0]][empty[1]].value = nums + 1
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(63)  
                self.redraw({}, wrong, time)

                if self.visualSolve(wrong, time):
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)
                self.redraw({}, wrong, time)

    def hint(self, keys):
        while True: 
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.board[i][j] == 0:  
                if (j, i) in keys:
                    del keys[(j, i)]
                self.board[i][j] = self.solvedBoard[i][j]
                self.tiles[i][j].value = self.solvedBoard[i][j]
                return True
            elif self.board == self.solvedBoard:
                return False

class Tile:
    def __init__(self, value, window, x1, y1):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60)  
        self.selected = False
        self.correct = False
        self.incorrect = False

    def draw(self, color, thickness):
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(self, value, position, color):
        font = pygame.font.SysFont('lato', 45)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    def clicked(self, mousePos):
        if self.rect.collidepoint(mousePos):
            self.selected = True
        return self.selected
    
def find_empty(board):
    '''Finds an empty cell and returns its position as a tuple'''

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)

def valid(board, pos, num):
    '''Whether a number is valid in that cell, returns a bool'''
    for i in range(9):
        if board[i][pos[1]] == num and (i, pos[1]) != pos:  # make sure it isn't the same number we're checking for by comparing coords
            return False

    for j in range(9):
        if board[pos[0]][j] == num and (pos[0], j) != pos:  # Same row but not same number
            return False

    start_i = pos[0] - pos[0] % 3  # ex. 5-5%3 = 3 and thats where the grid starts
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):  # adds i and j as needed to go from start of grid to where we need to be
            if board[start_i + i][start_j + j] == num and (start_i + i,
                    start_j + j) != pos:
                return False
    return True

def solve(board):
    '''Solves the Sudoku board via the backtracking algorithm'''
    empty = find_empty(board)
    if not empty:  # no empty spots are left so the board is solved
        return True

    for nums in range(9):
        if valid(board, empty, nums + 1):
            board[empty[0]][empty[1]] = nums + 1

            if solve(board):  # recursive step
                return True
            board[empty[0]][empty[1]] = 0  # this number is wrong so we set it back to 0
    return False

def main():
    screen = pygame.display.set_mode((540, 590))
    screen.fill((255, 255, 255))
    pygame.display.set_caption('Sudoku Solver with DFS Solution')
    icon = pygame.image.load('assets/thumbnail.png')
    pygame.display.set_icon(icon)
    pygame.display.flip()

    wrong = 0
    board = Board(screen)
    selected = (-1, -1)  
    keyDict = {}
    running = True
    startTime = time.time()
    
    while running:
        elapsed = time.time() - startTime
        passedTime = time.strftime('%H:%M:%S', time.gmtime(elapsed))

        if board.board == board.solvedBoard:  
            for i in range(9):
                for j in range(9):
                    board.tiles[i][j].selected = False
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()  
            elif event.type == pygame.MOUSEBUTTONUP:

                mousePos = pygame.mouse.get_pos()
                for i in range(9):
                    for j in range(9):
                        if board.tiles[i][j].clicked(mousePos):
                            selected = (i, j)
                            board.deselect(board.tiles[i][j])  
            elif event.type == pygame.KEYDOWN:

                if board.board[selected[1]][selected[0]] == 0 \
                    and selected != (-1, -1):
                    if event.key == pygame.K_1:
                        keyDict[selected] = 1

                    if event.key == pygame.K_2:
                        keyDict[selected] = 2

                    if event.key == pygame.K_3:
                        keyDict[selected] = 3

                    if event.key == pygame.K_4:
                        keyDict[selected] = 4

                    if event.key == pygame.K_5:
                        keyDict[selected] = 5

                    if event.key == pygame.K_6:
                        keyDict[selected] = 6

                    if event.key == pygame.K_7:
                        keyDict[selected] = 7

                    if event.key == pygame.K_8:
                        keyDict[selected] = 8

                    if event.key == pygame.K_9:
                        keyDict[selected] = 9
                    elif event.key == pygame.K_BACKSPACE or event.key \
                        == pygame.K_DELETE:

                        if selected in keyDict:
                            board.tiles[selected[1]][selected[0]].value = \
                                0
                            del keyDict[selected]
                    elif event.key == pygame.K_RETURN:

                        if selected in keyDict:
                            if keyDict[selected] \
                                != board.solvedBoard[selected[1]][selected[0]]:  
                                wrong += 1
                                board.tiles[selected[1]][selected[0]].value = \
                                    0
                                del keyDict[selected]
                                break

                            board.tiles[selected[1]][selected[0]].value = \
                                keyDict[selected]  
                            board.board[selected[1]][selected[0]] = \
                                keyDict[selected] 
                            del keyDict[selected]

                if event.key == pygame.K_h:
                    board.hint(keyDict)

                if event.key == pygame.K_SPACE:
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].selected = False
                    keyDict = {}  
                    board.visualSolve(wrong, passedTime)
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].correct = False
                            board.tiles[i][j].incorrect = False 
                    running = False

        board.redraw(keyDict, wrong, passedTime)
    while True:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

args = ''
if len(sys.argv) > 1:
    args = sys.argv[1]

main()
pygame.quit()
