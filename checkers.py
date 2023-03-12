import pygame

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Square:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = col * 8
        self.y = row * 8
        self.color = None
        self.piece = None
        self.width = width

def setColors(board):
    for row in range(8):
        square = 0
        while square < 8:
            if row % 2 == 0 and square % 2 == 0:
                board[row][square].color = RED
            if row % 2 == 0 and square % 2 == 1:
                board[row][square].color = BLACK
            if row % 2 == 1 and square % 2 == 0:
                board[row][square].color = BLACK
            if row % 2 == 1 and square % 2 == 1:
                board[row][square].color = RED
            square += 1

def makeBoard(width):
    board = []
    gap = width // 8
    for i in range(8):
        board.append([])
        for j in range(8):
            square = Square(i, j, gap)
            board[i].append(square)
    setColors(board)
    return board

def draw(win, board):
    win.fill(WHITE)
    for row in board:
        for square in row:
            pygame.draw.rect(win, square.color, (square.x, square.y, square.width, square.width))
    pygame.display.update()

def main():
    run = True
    while run:
        board = makeBoard(WIDTH)
        draw(WIN, board)

main()