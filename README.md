# Airplanes
##### A game about destroying the computer-controlled opponent's planes
---
The game can be run either in console mode or in GUI mode, by running `ConsoleUI.py` or `PyGameUI.py`, respectively.

#### Rules
---
At the beginning of the game, each player places two planes on their 8x8 board, without overlaps. In order to place your planes in console mode, follow the on-screen instructions. In the GUI, placing planes is done by hovering over your board (the left one) and scrolling to rotate the plane. Clicking will set the desired position and rotation.
After placing the planes (which the computer opponent does randomly), you take turns guessing where the other player's planes are (by clicking on the squares in the right board in GUI mode, or by entering coordinates in console) and trying to destroy them. A plane is destroyed and revealed if its' head is hit. The player who manages to destroy the other one's planes wins.

#### Implementation details
---
- The computer-controlled opponent uses information obtained at each miss in order to compute the number of possibilities (min. 0, max. 4) for a plane's head to be in a square of the board; choices then become picking a random square from the ones with the same number of directions a plane could be in while having the head in that square.
- The GUI is implemented using PyGame.
