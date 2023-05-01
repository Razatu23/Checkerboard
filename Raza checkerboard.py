import pygame #Uses pygame to run checkers
import time 

redwins=0 #Allows for accumulation for number of game wins
bluewins=0


numgames=int(input("How many games? ")) #finds out how many games to run
colors= input("How would you like to play? eccentric or classic? ") #finds what theme player wants
if colors == "eccentric": #color scheme 1
    blue = (95, 158, 160)
    red = (240, 128, 128)
    pink = (255, 110, 180)
    indigo = (75, 0, 130)
elif colors == "classic": #color scheme 2
    blue = (255, 0, 0)
    red = (0, 0, 0)
    pink = (50, 50, 50)
    indigo = (0, 0, 255)
else:
    print("invalid") #quits program for invalid answers
    quit()

Doge = pygame.transform.scale(pygame.image.load("dogebread.png"), (44, 25)) #image to distinguish king

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        if game.winner() != None:
            print(game.winner())
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ends the game
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: #selects a piece where mouse clicks
                pos = pygame.mouse.get_pos()
                row, col = mouse_location(pos)
                game.select(row, col)
        game.update()

class Board:
    def __init__(self):
        z=ROWS/2
        z=int(z)
        x=z*amount
        x=int(x)
        self.board = []
        self.blue_left = self.red_left = x #how many pieces that have to be killed on one side for a winner
        self.blue_kings = self.red_kings = 0
        self.create_board()
    def squares(self, win):
        win.fill(pink) #background
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, blue, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) #draws the checkerboard
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == ROWS - 1 or row == 0: #Piece becomes a king at opposite end of board
            piece.make_king()
            if piece.color == red:
                self.red_kings += 1
            else:
                self.blue_kings += 1
    def get_piece(self, row, col):
        return self.board[row][col]
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < amount:
                        self.board[row].append(Piece(row, col, red))
                    elif row > ROWS - amount - 1:
                        self.board[row].append(Piece(row, col, blue))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    def draw(self, win):
            self.squares(win)
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board[row][col]
                    if piece != 0:
                        piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == blue:
                    self.blue_left -= 1
                else:
                    self.red_left -= 1
    def winner(self):
        global redwins
        global bluewins
        if self.blue_left <= 0: #returns the number of wins at end of game and who won last game
            whitewins=redwins+1
            whitewins=str(redwins)
            pinkwins=str(bluewins)
            if colors == "eccentric":
                print("red has " + redwins +" wins and blue has " + bluewins + " wins")
                whitewins = int(redwins)
                pinkwins = int(bluewins)
                return ("red wins!")
            elif colors == "classic":
                print("black has " + redwins + " wins and red has " + bluewins + " wins")
                whitewins = int(redwins)
                pinkwins = int(bluewins)
                return("Black wins!")
        elif self.red_left <= 0:
            bluewins=bluewins+1
            redwins = str(redwins)
            bluewins = str(bluewins)
            if colors == "eccentric":
                print("white has " + redwins + " wins and pink has " + bluewins + " wins")
                whitewins = int(redwins)
                pinkwins = int(bluewins)
                return ("blue wins!")
            elif colors == "classic":
                print("black has " + redwins + " wins and red has " + bluewins + " wins")
                whitewins = int(redwins)
                pinkwins = int(bluewins)
                return("Red wins!")
        else:
            pass

    def moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == blue or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == red or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = blue
        self.valid_moves = {}
    def winner(self):
        return self.board.winner()
    def reset(self):
        self._init()
    def select(self, row, col):
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.moves(piece)
            return True
        return False
    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, indigo,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == blue:
            self.turn = red
        else:
            self.turn = blue

class Piece:
    PADDING = 10
    OUTLINE = 0
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    def make_king(self):
        self.king = True
    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, blue, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(Doge, (self.x - Doge.get_width() // 2, self.y - Doge.get_height() // 2))
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
    def rep(self):
        return str(self.color)

FPS = 60 #sets fps
WIN = pygame.display.set_mode((800, 800)) #screen size
pygame.display.set_caption("Checkers") #name of window

def mouse_location(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

for i in range(numgames):
    ROWS= int(input("how many rows in your game?")) #asks how big of a board to make
    COLS= ROWS
    SQUARE_SIZE = 800//ROWS #how big the squares will be

    amount=int(input("how many rows for pieces per side?")) #asks how many of rows to load
    while amount >= ROWS/2:
        amount = int(input("how many rows for pieces per side?")) #asks again if original answer doesn't work
    main()
