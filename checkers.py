import sys
import pygame

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Checkers Game")

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TURQUOISE = (64, 224, 208)
blue_img = pygame.image.load('figures/blue.png')
blue_img = pygame.transform.scale(blue_img, (53, 53))
blueking_img = pygame.image.load('figures/blueking.png')
blueking_img = pygame.transform.scale(blueking_img, (53, 53))
red_img = pygame.image.load('figures/red.png')
red_img = pygame.transform.scale(red_img, (53, 53))
redking_img = pygame.image.load('figures/redking.png')
redking_img = pygame.transform.scale(redking_img, (53, 53))
turn = 'red'
lastMove = None

class Square:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = None
        self.piece = None
        self.width = width
        self.tmpColor = None

class Board:
    def __init__(self, width):
        self.board = []
        self.squareWidth = width // 8
        self.pieceCount = 0

        #add squares
        for i in range(8):
            self.board.append([])
            for j in range(8):
                square = Square(i, j, self.squareWidth)
                self.board[i].append(square)
        
        #set colors
        for row in range(8):
            square = 0
            while square < 8:
                currentBox = self.board[row][square]
                if row % 2 == 0 and square % 2 == 0:
                    currentBox.color = RED
                    currentBox.tmpColor = RED
                if row % 2 == 0 and square % 2 == 1:
                    currentBox.color = BLACK
                    currentBox.tmpColor = BLACK
                if row % 2 == 1 and square % 2 == 0:
                    currentBox.color = BLACK
                    currentBox.tmpColor = BLACK
                if row % 2 == 1 and square % 2 == 1:
                    currentBox.color = RED
                    currentBox.tmpColor = RED
                square += 1

        #set pieces
        for row in range(3):
            for square in range(8):
                if self.board[row][square].color == BLACK:
                    self.board[row][square].piece = 'blue'
                    self.pieceCount += 1
        for row in range(5, 8):
            for square in range(8):
                if self.board[row][square].color == BLACK:
                    self.board[row][square].piece = 'red'
                    self.pieceCount += 1

    def draw(self, win):
        win.fill(WHITE)
        for row in self.board:
            for square in row:
                pygame.draw.rect(win, square.color, (square.x, square.y, square.width, square.width))
                if square.piece == 'blue':
                    WIN.blit(blue_img, (square.x + 16, square.y + 16))
                if square.piece == 'red':
                    WIN.blit(red_img, (square.x + 16, square.y + 16))
                if square.piece == 'redking':
                    WIN.blit(redking_img, (square.x + 16, square.y + 16))
                if square.piece == 'blueking':
                    WIN.blit(blueking_img, (square.x + 16, square.y + 16))
        pygame.display.update()

def changeTurn(turn):
    if turn == 'red':
        turn = 'blue'
    elif turn == 'blue':
        turn = 'red'
    return turn

def setLastMoveTake(takePiece):
    global lastMove
    if takePiece != None:
        if takePiece == 'red':
            lastMove = 'bluetake'
        else:
            lastMove = 'redtake'

def validateMove(board, selected, square):
    global lastMove
    if selected.piece == 'red':
        #regular move
        if square.row == selected.row - 1 and (square.col == selected.col + 1 or square.col == selected.col - 1):
            lastMove = None
            return True
        #takes right
        elif square.row == selected.row - 2 and square.col == selected.col + 2 and 'blue' in board.board[selected.row - 1][selected.col + 1].piece:
            board.board[selected.row - 1][selected.col + 1].piece = None
            lastMove = 'redtake'
            return 'take'
        #takes left
        elif square.row == selected.row - 2 and square.col == selected.col - 2 and 'blue' in board.board[selected.row - 1][selected.col - 1].piece:
            board.board[selected.row - 1][selected.col - 1].piece = None
            lastMove = 'redtake'
            return 'take'
    elif selected.piece == 'blue':
        #regular move
        if square.row == selected.row + 1 and (square.col == selected.col + 1 or square.col == selected.col - 1):
            lastMove = None
            return True
        #takes right
        elif square.row == selected.row + 2 and square.col == selected.col + 2 and 'red' in board.board[selected.row + 1][selected.col + 1].piece:
            board.board[selected.row + 1][selected.col + 1].piece = None
            lastMove = 'bluetake'
            return 'take'
        #takes left
        elif square.row == selected.row + 2 and square.col == selected.col - 2 and 'red' in board.board[selected.row + 1][selected.col - 1].piece:
            board.board[selected.row + 1][selected.col - 1].piece = None
            lastMove = 'bluetake'
            return 'take'

    elif selected.piece in ['redking', 'blueking']:
        #regular move
        if (square.row == selected.row + 1 or square.row == selected.row - 1) and (square.col == selected.col + 1 or square.col == selected.col - 1) and square.piece == None:
            lastMove = None
            return True
        #takes
        if selected.piece == 'redking':
            takePiece = 'blue'
        elif selected.piece == 'blueking':
            takePiece = 'red'
        #takes downleft
        if square.row == selected.row + 2 and square.col == selected.col - 2 and takePiece in board.board[selected.row + 1][selected.col - 1].piece:
            board.board[selected.row + 1][selected.col - 1].piece = None
            setLastMoveTake(takePiece)
            return 'take'
        #takes downright
        if square.row == selected.row + 2 and square.col == selected.col + 2 and takePiece in board.board[selected.row + 1][selected.col + 1].piece:
            board.board[selected.row + 1][selected.col + 1].piece = None
            setLastMoveTake(takePiece)
            return 'take'
        #takes upleft
        if square.row == selected.row - 2 and square.col == selected.col - 2 and takePiece in board.board[selected.row - 1][selected.col - 1].piece:
            board.board[selected.row - 1][selected.col - 1].piece = None
            setLastMoveTake(takePiece)
            return 'take'
        #takes upright
        if square.row == selected.row - 2 and square.col == selected.col + 2 and takePiece in board.board[selected.row - 1][selected.col + 1].piece:
            board.board[selected.row - 1][selected.col + 1].piece = None
            setLastMoveTake(takePiece)
            return 'take'
    return False

def getClickedPos(pos, width):
    gap = width // 8
    x, y = pos
    row = y // gap
    col = x // gap
    return row, col

def checkForKing(square):
    if square.row == 7 and square.piece == 'blue':
        square.piece = 'blueking'
    elif square.row == 0 and square.piece == 'red':
        square.piece = 'redking'

def checkWin(board):
    blue = 0
    red = 0
    for row in board.board:
        for square in row:
            if square.piece != None and 'red' in square.piece:
                red += 1
            if square.piece != None and 'blue' in square.piece:
                blue += 1
    if blue == 0:
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        redWin = my_font.render('Red Wins!', False, (0, 0, 0))
        WIN.blit(redWin, (40,40))
    if red == 0:
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        blueWin = my_font.render('Blue Wins!', False, (0, 0, 0))
        WIN.blit(blueWin, (40,40))

def handleClick(board, selected, square, mid_take):
    global turn
    if square == selected:
        return selected
    if mid_take:
        if selected != None and square.piece == None:
            if validateMove(board, selected, square) == 'take':
                square.piece = selected.piece
                selected.piece = None
                selected.color = selected.tmpColor
                square.color = TURQUOISE
                checkForKing(square)
                checkWin(board)
                return square
        return selected
    else:
        #the user who's turn it is has selected one of their pieces
        if square.piece != None and turn in square.piece:
            #the user who's turn it is has changed their piece selection
            if selected != None and selected.piece != None and turn in selected.piece:
                selected.color = selected.tmpColor
                square.color = TURQUOISE
                selected = square
            #the user is making an initial piece selection
            elif selected == None:
                square.color = TURQUOISE
                selected = square
            return selected
        #the user has already selected their piece and is making a move
        elif selected != None and square.piece == None:
            response = validateMove(board, selected, square)
            if response == True:
                square.piece = selected.piece
                selected.piece = None
                selected.color = selected.tmpColor
                checkForKing(square)
                turn = changeTurn(turn)
                return None
            elif response == 'take':
                square.piece = selected.piece
                selected.piece = None
                selected.color = selected.tmpColor
                square.color = TURQUOISE
                checkForKing(square)
                checkWin(board)
                return square
        return selected

def main():
    run = True
    board = Board(WIDTH)
    selected = None
    mid_take = False
    global turn
    global lastMove

    while run:
        board.draw(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    sys.exit()
            if pygame.mouse.get_pressed()[2]:
                if mid_take:
                    selected.color = selected.tmpColor
                    selected = None
                    turn = changeTurn(turn)
                    mid_take = False

            #left click screen
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, WIDTH)
                square = board.board[row][col]
                selected = handleClick(board, selected, square, mid_take)
                if selected == square and lastMove == turn + 'take':
                    mid_take = True

main()