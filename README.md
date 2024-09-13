# A Connect Four Game with Negamax AI
This is a Python program that allows users to play Connect Four game against an AI agent that uses aa Negamax algorithm. I built this in September 2022.
## Requirements
Python 3.x  
numpy  
scipy  
## Usage
Clone the repository.
Open a terminal and navigate to the directory containing the repository.
Run the command ```python ConnectFour.py``` to start the game.
The game will begin and you will be prompted to select a column to drop your piece. Enter the number of the column and press enter.
The AI will then make its move and the game will continue until one player wins or the game is a draw.
To exit the game, press Ctrl+C.
## The Algorithm
The AI agent in this program uses the Negamax algorithm to determine the best move to make at each turn. The algorithm searches the game tree to a certain depth, and evaluates each leaf node using a heuristic function. The heuristic function used in this program uses 2D kernels for diagonal, vertical and horizontal lines, to detect any matching sequences of 1s or 2s in the game grid. It assigns a score proportional to the length of the matching sequences, and also gives a large positive score if there is a winning sequence of 1s, and a large negative score if there is a winning sequence of 2s. The algorithm then returns the move with the highest evaluated score.
