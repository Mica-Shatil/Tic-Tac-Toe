import numpy as np
import pygame
import pyautogui
from pygame.locals import *

X_TURN = True
O_TURN = False
XX = 1
OO = 2
BLACK = (0,0,0)
BLUE = (0, 160, 210)
WHITE = (255, 255, 255)
pygame.font.init()

class Board:

    font_game = pygame.font.Font('freesansbold.ttf', 100)
    font_turn = pygame.font.Font('freesansbold.ttf', 30)

    def __init__ (self, players):
        self.num_player = players
        self.board = np.zeros([3, 3], dtype='int16')
        self.turn = X_TURN
        self.screen_width = 360
        self.screen_height = 400
        self.top = 40
        self.board_height = 360
        self.end_game = False

        # initialize window
        self.game_screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.x_text = Board.font_turn.render('Xs Turn', 1, BLACK)
        self.o_text = Board.font_turn.render('Os Turn', 1, BLACK)
        pygame.display.set_caption("Tic-Tac-Toe")
        self.game_screen.fill(BLUE)
        pygame.display.update()

    # redraws game window
    def update_window(self):
        self.game_screen.fill(BLUE)
        dist = self.screen_width / 3

        # writes which player's turn it is
        if self.turn == XX or self.num_player == 1:
            self.game_screen.blit(self.x_text, (127, 5))
        else:
            self.game_screen.blit(self.o_text, (127, 5))
        
        # draws grid
        for i in range(3):
            pygame.draw.lines(self.game_screen, BLACK, False, [(i * dist, self.top), (i * dist, self.screen_height)], 5)
            pygame.draw.lines(self.game_screen, BLACK, False, [(0, i * dist + self.top), (self.screen_width, i * dist + self.top)], 5)

        # fills tiles
        for i in range(0, self.board.shape[0]):
            for j in range(0, self.board.shape[1]):
                if self.board[i, j] == XX:
                    text = Board.font_game.render("X", 1, BLACK)
                    self.game_screen.blit(text, (j * dist + 25, i * dist + 12 + self.top))
                if self.board[i, j] == OO:
                    text = Board.font_game.render("O", 1, BLACK)
                    self.game_screen.blit(text, (j * dist + 25, i * dist + 12 + self.top))

        pygame.display.update()

    # retrns XX or OO if x or o has won respectively, true if the board is full, and false if the game is not over
    def completed(self):
        board_full = True

        # checks for winner
        for i in range(0, self.board.shape[0]):
            if self.board[i, 0] == self.board[i, 1] == self.board[i, 2] == XX or self.board[0, i] == self.board[1, i] == self.board[2, i] == XX:
                return XX
            elif self.board[i, 0] == self.board[i, 1] == self.board[i, 2] == OO or self.board[0, i] == self.board[1, i] == self.board[2, i] == OO:
                return OO
        if self.board[1, 1] == XX and ((self.board[0, 0] == XX and self.board[2, 2] == XX) or (self.board[0, 2] == XX and self.board[2, 0] == XX)):
            return XX
        elif self.board[1, 1] == OO and ((self.board[0, 0] == OO and self.board[2, 2] == OO) or (self.board[0, 2] == OO and self.board[2, 0] == OO)):
            return OO

        # checks if board is full
        for i in range(0, self.board.shape[0]):
            for j in range(0, self.board.shape[1]):
                if self.board[i, j] == 0:
                    board_full = False
                    break
                elif i == 2 and j == 2:
                    return 3
            if board_full == False:
                break
    
        return False

    # Gets and updates board with a player's move
    def player_turn(self):
        if self.turn == X_TURN:
            made_move = False
            while (not made_move) and self.end_game == False:
                for event in pygame.event.get():
                    if event.type == QUIT: # endgame
                        self.end_game = True
                    if event.type == MOUSEBUTTONDOWN: # mouse press
                        pos = pygame.mouse.get_pos()
                        if pos[0] < self.screen_width and self.top < pos[1] < self.screen_height:
                            gap = int(self.screen_width / 3)
                            x = pos[0] // gap
                            y = (pos[1] - self.top) // gap
                            if (self.board[y, x] == 0):
                                self.board[y, x] = 1
                                self.update_window()
                                made_move = True
                                self.turn = ~self.turn
        else:
            made_move = False
            while (not made_move) and self.end_game == False:
                for event in pygame.event.get():
                    if event.type == QUIT: # endgame
                        self.end_game = True
                    if event.type == MOUSEBUTTONDOWN: # mouse press
                        pos = pygame.mouse.get_pos()
                        if pos[0] < self.screen_width and self.top < pos[1] < self.screen_height:
                            gap = self.screen_width // 3
                            x = pos[0] // gap
                            y = (pos[1] - self.top) // gap
                            if (self.board[y, x] == 0):
                                self.board[y, x] = OO
                                self.update_window()
                                made_move = True
                                self.turn = ~self.turn

    # Completes and updates board with bots move
    def bot_turn(self):
        # looks for o's immidiate opportunity to win
        for i in range(0, self.board.shape[0]):
            if (self.board[i, 0] == self.board[i, 1] == OO) and self.board[i, 2] == 0:
                self.board[i, 2] = OO
                self.turn = ~self.turn
                return
            elif (self.board[i, 1] == self.board[i, 2] == OO) and self.board[i, 0] == 0:
                self.board[i, 0] = OO
                self.turn = ~self.turn
                return
            elif (self.board[i, 0] == self.board[i, 2] == OO) and self.board[i, 1] == 0:
                self.board[i, 1] = OO
                self.turn = ~self.turn
                return
            elif (self.board[0, i] == self.board[1, i] == OO) and self.board[2, i] == 0:
                self.board[2, i] = OO
                self.turn = ~self.turn
                return
            elif (self.board[1, i] == self.board[2, i] == OO) and self.board[0, i] == 0:
                self.board[0, i] = OO
                self.turn = ~self.turn
                return
            elif (self.board[0, i] == self.board[2, i] == OO) and self.board[1, i] == 0:
                self.board[1, i] = OO
                self.turn = ~self.turn
                return
        if self.board[1, 1] == OO:
            if self.board[0, 0] == OO and self.board[2, 2] == 0:
                self.board[2, 2] = OO
                self.turn = ~self.turn
                return
            elif self.board[0, 2] == OO and self.board[2, 0] == 0:
                self.board[2, 0] = OO
                self.turn = ~self.turn
                return
            elif self.board[2, 0] == OO and self.board[0, 2] == 0:
                self.board[0, 2] = OO
                self.turn = ~self.turn
                return
            elif self.board[2, 2] == OO and self.board[0, 0] == 0:
                self.board[0, 0] = OO
                self.turn = ~self.turn
                return
        if self.board[0, 0] == self.board[2, 2] == OO and self.board[1, 1] == 0:
            self.board[1, 1] = OO
            self.turn = ~self.turn
            return
        elif self.board[0, 2] == self.board[2, 0] == OO and self.board[1, 1] == 0:
            self.board[1, 1] = OO
            self.turn = ~self.turn
            return
            
        # looks for x's opportunity to win (to block)
        for i in range(0, self.board.shape[0]):
            if (self.board[i, 0] == self.board[i, 1] == XX) and self.board[i, 2] == 0:
                self.board[i, 2] = OO
                self.turn = ~self.turn
                return
            elif (self.board[i, 1] == self.board[i, 2] == XX) and self.board[i, 0] == 0:
                self.board[i, 0] = OO
                self.turn = ~self.turn
                return
            elif (self.board[i, 0] == self.board[i, 2] == XX) and self.board[i, 1] == 0:
                self.board[i, 1] = OO
                self.turn = ~self.turn
                return
            elif (self.board[0, i] == self.board[1, i] == XX) and self.board[2, i] == 0:
                self.board[2, i] = OO
                self.turn = ~self.turn
                return
            elif (self.board[1, i] == self.board[2, i] == XX) and self.board[0, i] == 0:
                self.board[0, i] = OO
                self.turn = ~self.turn
                return
            elif (self.board[0, i] == self.board[2, i] == XX) and self.board[1, i] == 0:
                self.board[1, i] = OO
                self.turn = ~self.turn
                return
        if self.board[1, 1] == XX:
            if self.board[0, 0] == XX and self.board[2, 2] == 0:
                self.board[2, 2] = OO
                self.turn = ~self.turn
                return
            elif self.board[0, 2] == XX and self.board[2, 0] == 0:
                self.board[2, 0] = OO
                self.turn = ~self.turn
                return
            elif self.board[2, 0] == XX and self.board[0, 2] == 0:
                self.board[0, 2] = OO
                self.turn = ~self.turn
                return
            elif self.board[2, 2] == XX and self.board[0, 0] == 0:
                self.board[0, 0] = OO
                self.turn = ~self.turn
                return
        if self.board[0, 0] == self.board[2, 2] == XX and self.board[1, 1] == 0:
            self.board[1, 1] = OO
            self.turn = ~self.turn
            return
        elif self.board[0, 2] == self.board[2, 0] == XX and self.board[1, 1] == 0:
            self.board[1, 1] = OO
            self.turn = ~self.turn
            return
        
        # Randomizes position if no immidiate win/loss is present
        while True:
            open_spaces = np.argwhere(self.board == 0)
            maximum = (open_spaces.size / 2) - 1
            index = np.random.randint(0, maximum)
            if self.board[open_spaces[index][0], open_spaces[index][1]] == 0:
                self.board[open_spaces[index][0], open_spaces[index][1]] = OO
                self.turn = ~self.turn
                break
    
# Game loop
def game_cycle(num_players):
    game = Board(num_players)
    game.update_window()
    
    if num_players == 2:
        game_over = False
        while game_over == False and game.end_game == False:
            game.player_turn()
            game.update_window()
            game_over = game.completed()
    elif num_players == 1:
        game_over = False
        while game_over == False and game.end_game == False:
            if game.turn == X_TURN:
                game.player_turn()
                game.update_window()
                game_over = game.completed()
            else:
                game.bot_turn()
                game.update_window()
                game_over = game.completed()
            
    if game_over == XX:
        del game
        end_process('X Wins')
    elif game_over == OO:
        del game
        end_process('O Wins')
    elif game_over == 3:
        del game
        end_process('  Draw')

# Start process (1 or 2 player selection)
def start_process():
    screen_width = 360
    screen_height = 360

    font_start = pygame.font.Font('freesansbold.ttf', 40)
    font_welcome = pygame.font.Font('freesansbold.ttf', 25)

    # initialize window
    start_screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tic-Tac-Toe")
    start_screen.fill(BLUE)

    b1_top = 50
    b1_height = 50
    b_left = 20
    b_width = 300
    b2_top = 200
    b2_height = 50
    pygame.draw.rect(start_screen, BLACK, (b_left, b1_top, b_width, b1_height))
    pygame.draw.rect(start_screen, BLACK, (b_left, b2_top, b_width, b2_height))

    # writes headers
    box1_text = font_start.render("Single Player", 1, WHITE)
    start_screen.blit(box1_text, (b_left + 18, b1_top + 5))
    box2_text = font_start.render("Double Player", 1, WHITE)
    start_screen.blit(box2_text, (b_left + 12, b2_top + 5))
    welcome_text = font_welcome.render("Select Your Game Mode!", 1, BLACK)
    start_screen.blit(welcome_text, (20, 135))

    pygame.display.update()
    end_game = False
    num_players = 0
    while num_players == 0 and end_game == False:
        for event in pygame.event.get():
            if event.type == QUIT: # endgame
                end_game = True
            if event.type == MOUSEBUTTONDOWN: # mouse press
                pos = pygame.mouse.get_pos()
                if b_left <= pos[0] <= (b_left + b_width):
                    if b1_top <= pos[1] <= (b1_top + b1_height):
                        num_players = 1
                    elif b2_top <= pos[1] <= (b2_top + b2_height):
                        num_players = 2

    if end_game != True:
        game_cycle(num_players)

# End of game process (ask to play again)
def end_process(winner):
    screen_width = 360
    screen_height = 360

    font_start = pygame.font.Font('freesansbold.ttf', 40)

    # initialize window
    start_screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tic-Tac-Toe")
    start_screen.fill(BLUE)

    b_left = 20
    b_width = 320
    b_top = 200
    b_height = 50
    pygame.draw.rect(start_screen, BLACK, (b_left, b_top, b_width, b_height))

    # writes headers
    winner_text = font_start.render(winner + "!", 1, BLACK)
    start_screen.blit(winner_text, (b_left + 90, 75))
    box_text = font_start.render("Play Again", 1, BLUE)
    start_screen.blit(box_text, (b_left + 65, b_top + 5))

    pygame.display.update()
    end_game = False
    play_again = False
    while play_again == False and end_game == False:
        for event in pygame.event.get():
            if event.type == QUIT: # endgame
                end_game = True
            if event.type == MOUSEBUTTONDOWN: # mouse press
                pos = pygame.mouse.get_pos()
                if b_left <= pos[0] <= (b_left + b_width):
                    if b_top <= pos[1] <= (b_top + b_height):
                        play_again = True
    
    if end_game != True:
        start_process()

def main():
    start_process()

main()
pygame.quit()