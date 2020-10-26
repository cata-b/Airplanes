from HistoryBoard import HistoryBoard
from AirplaneBoard import AirplaneBoard
from ComputerStrategic import ComputerStrategic
from DirectionsHelper import *
import re
class ConsoleUI:
    def __init__(self):
        self._computer = ComputerStrategic()
        self._computer.place_planes()
        self._computer_history = HistoryBoard()

        self._player_board = AirplaneBoard()
        self._player_history = HistoryBoard()

    def _reset(self):
        self._computer = ComputerStrategic()
        self._computer.place_planes()
        self._computer_history = HistoryBoard()

        self._player_board = AirplaneBoard()
        self._player_history = HistoryBoard()
        self.pick_planes()

    def pick_planes(self):
        picked_planes = 0
        while picked_planes < 2:
            print("Pick plane no. " + str(picked_planes + 1))
            data = input("Write the coordinates of the head of the plane and its direction e.g. \"4, E, up\": ").strip().lower()
            match = re.fullmatch("([1-8], *[a-h]), +(up|down|left|right)", data)
            if match != None:
                coords_raw = match.groups()[0].replace(" ", "").split(",")
                coords = (int(coords_raw[0]), ord(coords_raw[1]) - ord("a") + 1)
                dir = eval(match.groups()[1] + "()")
                try:
                    self._player_board.place_plane(coords, dir)
                except Exception as e:
                    print(str(e))
                    continue
                picked_planes += 1
                print("Now your board looks like: \n" + str(self._player_board))
            else:
                print("Didn't understand that, mind repeating?\n")

    def get_player_choice(self):
        data = input("Enter your coordinates (e.g. 4, E): ").strip().lower()
        match = re.fullmatch("([1-8], *[a-h])", data)
        coords_raw = match.groups()[0].replace(" ", "").split(",")
        return (int(coords_raw[0]), ord(coords_raw[1]) - ord("a") + 1)

    def play_game(self):
        print(" Welcome to Planes. Every player has an 8x8 board, 1 to 8, A to H, and places 2 planes on it. Your goal is to guess where they are and destroy the other player's planes.")
        print("First, we need to place your planes on the board.\n" + str(self._player_board))
        self.pick_planes()
        self._computer_history.copy_from_airplane_board(self._player_board)
        computer_planes = 2
        player_planes = 2
        player_turn = True
        while player_planes * computer_planes > 0:
            if player_turn:
                print("It's your turn. Here are your tries so far (H - hit, M - miss): \n" + str(self._player_history))
                player_choice = self.get_player_choice()
                computer_response = self._computer[player_choice]
                if computer_response == 0:
                        print("It was a miss.")
                        self._player_history.mark_miss(player_choice)
                elif computer_response == 1:
                    print("It was a hit.")
                    self._player_history.mark_hit(player_choice)
                else:
                    print("You managed to destroy an enemy plane. All its parts are now visible to you.")
                    plane = self._computer.get_plane(player_choice)
                    self._player_history.mark_hit(player_choice)
                    for sq in plane:
                        self._player_history.mark_hit(sq)
                    computer_planes -= 1
            else:
                print("It's computer's turn.")
                computer_choice = self._computer.get_choice()
                print("Computer chose (%s, %s)." % (computer_choice[0], chr(ord("A") + computer_choice[1] - 1)))
                player_response = self._player_board[computer_choice]
                if player_response == 0:
                        print("It was a miss.")
                        self._computer_history.mark_miss(computer_choice)
                        self._computer.was_miss(computer_choice)
                elif player_response == 1:
                    print("It was a hit.")
                    self._computer_history.mark_hit(computer_choice)
                    self._computer.was_hit(computer_choice)
                else:
                    print("Computer managed to destroy your plane. All its parts are now visible to it.")
                    plane = self._player_board.get_plane(computer_choice)
                    self._computer_history.mark_hit(computer_choice)
                    for sq in plane:
                        self._computer_history.mark_hit(sq)
                    player_planes -= 1
                    self._computer.was_head(computer_choice, plane)
                print("These are the computer's tries so far (H - hit, M - miss, P - undiscovered plane part):\n" + str(self._computer_history))
            player_turn = not player_turn
        if player_turn:
            print("You lost. Through great wisdom, probability science and luck, the computer won.")
        else:
            print("You won, and so, beat the master in Planes.")
UI = ConsoleUI()
UI.play_game()