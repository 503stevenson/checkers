import pygame

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Checkers Game")

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TURQUOISE = (64, 224, 208)
blue_img = pygame.image.load('figures/blue.png')
blue_img = pygame.transform.scale(blue_img, (65, 65))
red_img = pygame.image.load('figures/red.png')
red_img = pygame.transform.scale(red_img, (65, 65))

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
        for row in range(5, 8):
            for square in range(8):
                if self.board[row][square].color == BLACK:
                    self.board[row][square].piece = 'red'

    def draw(self, win):
        win.fill(WHITE)
        for row in self.board:
            for square in row:
                pygame.draw.rect(win, square.color, (square.x, square.y, square.width, square.width))
                if square.piece == 'blue':
                    WIN.blit(blue_img, (square.x + 16, square.y + 16))
                if square.piece == 'red':
                    WIN.blit(red_img, (square.x + 16, square.y + 16))
        pygame.display.update()

def getClickedPos(pos, width):
    gap = width // 8
    x, y = pos
    row = y // gap
    col = x // gap
    return row, col

def main():
    run = True
    board = Board(WIDTH)
    turn = 'red'
    selected = None

    while run:
        board.draw(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #left click screen
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, WIDTH)
                square = board.board[row][col]

                if square.piece != None and turn in square.piece:
                    if selected != None:
                        selected.color = selected.tmpColor
                    square.color = TURQUOISE
                    selected = square

main()