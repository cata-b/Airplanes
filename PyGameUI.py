from HistoryBoard import HistoryBoard
from AirplaneBoard import AirplaneBoard
from ComputerStrategic import ComputerStrategic
from DirectionsHelper import *
import pygame
import sys
pygame.init()

class UIGameBoard():
    def __init__(self, EmptySquare: str, PlaneSquare: str, HitSquare: str, MissSquare: str, PlanePreview: str, width: int, height: int, x: int, y: int, square_spacing: int, underlying_board, event_list):
        self._sqwidth = width // 8
        self._sqheight = height // 8
        self._emptysq = pygame.transform.scale(pygame.image.load(EmptySquare), (self._sqwidth - square_spacing, self._sqheight - square_spacing))
        self._planesq = pygame.transform.scale(pygame.image.load(PlaneSquare), (self._sqwidth - square_spacing, self._sqheight - square_spacing))
        self._hitsq = pygame.transform.scale(pygame.image.load(HitSquare), (self._sqwidth - square_spacing, self._sqheight - square_spacing))
        self._misssq = pygame.transform.scale(pygame.image.load(MissSquare), (self._sqwidth - square_spacing, self._sqheight - square_spacing))
        self._sqspacing = square_spacing
        self._x = x
        self._y = y
        self._data = underlying_board
        self.board = AirplaneBoard()
        self._plane_prev = pygame.transform.scale(pygame.image.load(PlanePreview), (self._sqwidth * 5 - square_spacing, self._sqheight * 4 - square_spacing))
        self._plane_prev_square = None
        self._plane_prev_dir = None
        self.planes_no = 0
        self.events = event_list
        self._heads = []

    def place_planes(self, display):
        _body_maker = AirplaneBoard()
        for event in self.events:
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if mx >= self._x and mx < self._x + self._sqwidth * 8 and my >= self._y and my < self._y + self._sqheight * 8:
                    self._plane_prev_square = ((my - self._y) // self._sqheight + 1, (mx - self._x) // self._sqwidth + 1)
                    if self._plane_prev_dir == None:
                        self._plane_prev_dir = up()
                else:
                    self._plane_prev_square = None
                    continue
                break
            elif self._plane_prev_square != None and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # scroll up
                    dl = dirlist()
                    self._plane_prev_dir = dl[(dl.index(self._plane_prev_dir) + 1) % len(dl)]
                elif event.button == 5: # scroll down
                    dl = dirlist()
                    self._plane_prev_dir = dl[(dl.index(self._plane_prev_dir) - 1) % len(dl)]
                elif event.button == 1: # left click
                    if self.planes_no == 2:
                            raise PermissionError("Only placing 2 planes is allowed")
                    if self._plane_prev_square != None and self._plane_prev_dir != None:
                        try:
                            self.board.place_plane(self._plane_prev_square, self._plane_prev_dir)
                        except PermissionError:
                            continue
                        except ValueError:
                            continue
                        self.planes_no += 1
                        self._data.copy_from_airplane_board(self.board)

                            

        if self._plane_prev_square != None and self._plane_prev_dir != None:
            if self._data[self._plane_prev_square] != "":
                return
            
            angle = 0
            rlcd = (-3, -1)
            if self._plane_prev_dir == left():
                angle = 90
                rlcd = (-1, -3)
            elif self._plane_prev_dir == down():
                angle = 180
                rlcd = (-3, -4)
            elif self._plane_prev_dir == right():
                angle = 270
                rlcd = (-4, -3)

            prev = pygame.transform.rotate(self._plane_prev, angle)
            display.blit(prev, pygame.Rect(self._x + (self._plane_prev_square[1] + rlcd[0]) * self._sqwidth, self._y + (self._plane_prev_square[0] + rlcd[1]) * self._sqheight, prev.get_width(), prev.get_height()))

    def get_choice(self):
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
                mx, my = pygame.mouse.get_pos()
                if mx >= self._x and mx < self._x + self._sqwidth * 8 and my >= self._y and my < self._y + self._sqheight * 8:
                    square = ((my - self._y) // self._sqheight + 1, (mx - self._x) // self._sqwidth + 1)
                    if self._data[square] != "":
                        return None
                    return square

    def Draw(self, display):
        x = 1
        for X in range(self._x, self._x + self._sqwidth * 7 + 1, self._sqwidth):
            y = 1
            for Y in range(self._y, self._y + self._sqheight * 7 + 1, self._sqheight):
                if self._data[y, x] == "": 
                    display.blit(self._emptysq, pygame.Rect(X, Y, self._sqwidth, self._sqheight))
                elif self._data[y, x] == "H":
                    display.blit(self._hitsq, pygame.Rect(X, Y, self._sqwidth, self._sqheight))
                elif self._data[y, x] == "P":
                    display.blit(self._planesq, pygame.Rect(X, Y, self._sqwidth, self._sqheight))
                elif self._data[y, x] == "M":
                    display.blit(self._misssq, pygame.Rect(X, Y, self._sqwidth, self._sqheight))
                y += 1
            x += 1
    
class Button():
    def __init__(self, normal, hover, x, y, width, height, function):
        self.events = []
        self._normal = normal
        self._hover = hover
        self._function = function
        self._x, self._y, self._width, self._height = x, y, width, height

    def Draw(self, display):
        mx, my = pygame.mouse.get_pos()
        if mx >= self._x and mx <= self._x + self._width and my >= self._y and my <= self._y + self._height:
            display.blit(self._hover, pygame.Rect(self._x, self._y, self._width, self._height))
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
                    self._function()
                    return
        else:
            display.blit(self._normal, pygame.Rect(self._x, self._y, self._width, self._height))

class PygameUI():

    def __init__(self, game_to_screen_ratio, aspect_ratio, menu_width_to_game_width):
        self._events = []
        self._display_info = pygame.display.Info()
        self._game_to_screen_ratio = game_to_screen_ratio
        self._aspect_ratio = aspect_ratio
        self._menu_width_to_game_width = menu_width_to_game_width

        self._width = int(self._display_info.current_w * self._game_to_screen_ratio)
        self._height = int(self._width / self._aspect_ratio)

        self._gbWidth = self._gbHeight = self._width // 2 - int(self._menu_width_to_game_width * self._width)

        self._computer = ComputerStrategic()
        self._computer.place_planes()
        
        self._player_board = UIGameBoard("Assets/BoardEmptySquare.png", "Assets/BoardPlaneSquare.png", "Assets/BoardHitSquare.png", "Assets/BoardMissSquare.png", "Assets/PlanePreview.png", self._gbWidth, self._gbHeight, 0, (self._height - self._gbHeight) // 2, 3, HistoryBoard(), self._events)
        self._map_board = UIGameBoard("Assets/BoardEmptySquare.png", "Assets/BoardPlaneSquare.png", "Assets/BoardHitSquare.png", "Assets/BoardMissSquare.png", "Assets/PlanePreview.png", self._gbWidth, self._gbHeight, self._width - self._gbWidth, (self._height - self._gbHeight) // 2, 3, HistoryBoard(), self._events)

        button_width = int(self._menu_width_to_game_width * self._width)
        base_btn = pygame.image.load("Assets/Buttons/BaseButton.png")
        button_height = int(button_width / base_btn.get_width() * base_btn.get_height())
        btn_x = (self._width - button_width) // 2

        self._start_btn = Button(pygame.transform.scale(pygame.image.load("Assets/Buttons/PlayButton.png"), [button_width, button_height]), \
                                 pygame.transform.scale(pygame.image.load("Assets/Buttons/PlayButtonHover.png"), [button_width, button_height]),\
                                 btn_x, int(self._height / 3) - button_height, button_width, button_height, self._start_btn_click)
        self._reset_btn = Button(pygame.transform.scale(pygame.image.load("Assets/Buttons/ResetButton.png"), [button_width, button_height]), \
                                 pygame.transform.scale(pygame.image.load("Assets/Buttons/ResetButtonHover.png"), [button_width, button_height]),\
                                 btn_x, int(self._height / 3 - button_height) * 2, button_width, button_height, self._reset_btn_click)
        self._quit_btn = Button(pygame.transform.scale(pygame.image.load("Assets/Buttons/QuitButton.png"), [button_width, button_height]), \
                                 pygame.transform.scale(pygame.image.load("Assets/Buttons/QuitButtonHover.png"), [button_width, button_height]),\
                                 btn_x, int(self._height / 3 - button_height) * 3, button_width, button_height, self._quit_btn_click)

        self._state = -1
        self._computer_plane_no = 2
        self._player_plane_no = 2

    def _start_btn_click(self):
        self._state = 0

    def _reset_btn_click(self):
        self._computer = ComputerStrategic()
        self._computer.place_planes()
        
        self._player_board = UIGameBoard("Assets/BoardEmptySquare.png", "Assets/BoardPlaneSquare.png", "Assets/BoardHitSquare.png", "Assets/BoardMissSquare.png", "Assets/PlanePreview.png", self._gbWidth, self._gbHeight, 0, (self._height - self._gbHeight) // 2, 3, HistoryBoard(), self._events)
        self._map_board = UIGameBoard("Assets/BoardEmptySquare.png", "Assets/BoardPlaneSquare.png", "Assets/BoardHitSquare.png", "Assets/BoardMissSquare.png", "Assets/PlanePreview.png", self._gbWidth, self._gbHeight, self._width - self._gbWidth, (self._height - self._gbHeight) // 2, 3, HistoryBoard(), self._events)

        self._state = -1
        self._computer_plane_no = 2
        self._player_plane_no = 2


    def _quit_btn_click(self):
        sys.exit()

    def Start(self):
        screen = pygame.display.set_mode((self._width, self._height))
        self._events = []
        while True:
            self._events = list(pygame.event.get())
            self._player_board.events = self._events
            self._map_board.events = self._events
            self._start_btn.events = self._reset_btn.events = self._quit_btn.events = self._events
            for event in self._events:
                if event.type == pygame.QUIT: sys.exit()

            screen.fill([207, 243, 250])
            self._player_board.Draw(screen)
            if self._state == -1: # main menu
                self._start_btn.Draw(screen)
                self._reset_btn.Draw(screen)
                self._quit_btn.Draw(screen)
            if self._state == 0: # player choosing planes
                if self._player_board.planes_no < 2:
                    self._player_board.place_planes(screen)
                else:
                    self._state += 1
                self._reset_btn.Draw(screen)
                self._quit_btn.Draw(screen)
            elif self._state == 1: # player choosing hit
                player_choice = self._map_board.get_choice()
                if player_choice != None:
                    computer_response = self._computer[player_choice]
                    if computer_response == 0:
                        self._map_board._data.mark_miss(player_choice)
                        self._state = 2
                    elif computer_response == 1:
                        self._map_board._data.mark_hit(player_choice)
                        self._state = 2
                    else:
                        plane = self._computer.get_plane(player_choice)
                        self._map_board._data.mark_hit(player_choice)
                        for sq in plane:
                            self._map_board._data.mark_hit(sq)
                        self._computer_plane_no -= 1
                        if self._computer_plane_no == 0:
                            self._state = 3
                        else:
                            self._state = 2
                self._reset_btn.Draw(screen)
                self._quit_btn.Draw(screen)
            elif self._state == 2: # computer choosing hit
                computer_choice = self._computer.get_choice()
                player_response = self._player_board.board[computer_choice]
                if player_response == 0:
                    self._player_board._data.mark_miss(computer_choice)
                    self._computer.was_miss(computer_choice)
                    self._state = 1
                elif player_response == 1:
                    self._player_board._data.mark_hit(computer_choice)
                    self._computer.was_hit(computer_choice)
                    self._state = 1
                else:
                    plane = self._player_board.board.get_plane(computer_choice)
                    self._player_board._data.mark_hit(computer_choice)
                    for sq in plane:
                        self._player_board._data.mark_hit(sq)
                    self._computer.was_head(computer_choice, plane)
                    self._player_plane_no -= 1
                    if self._player_plane_no == 0:
                        self._state = 4
                    else:
                        self._state = 1
            elif self._state == 3:
                self._reset_btn.Draw(screen)
                self._quit_btn.Draw(screen)
            elif self._state == 4:
                self._reset_btn.Draw(screen)
                self._quit_btn.Draw(screen)
            self._map_board.Draw(screen)
            pygame.display.flip()

ui = PygameUI(0.6, 18.5 / 9, 1 / 10)
ui.Start()