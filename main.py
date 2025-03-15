import numpy as np
import tkinter as tk
from tkinter import messagebox

class Mancala:
    def __init__(self):
        # gives each player 6 pits and a store
        self.board = np.array([4] * 6 + [0] + [4] * 6 + [0]) 
        # represent player one with 0 and player 2 with 1
        self.current_player = 0 
    
    def move(self, pit):
        #checks player count
        if self.current_player == 1:
            pit += 7
        #takes all stones from selected pit
        stones = self.board[pit]
        #empties the pit
        self.board[pit] = 0
        index = pit

        #Give players stones in counterclockwise order
        while stones:
            #moves the next stone into the next pit and makes sure that the count wraps to 0 to keep in range of pits
            index = (index + 1) % 14
            #skips opponent's store
            if (self.current_player == 0 and index == 13) or (self.current_player == 1 and index == 6):
                continue
            self.board[index] += 1
            stones -= 1

        # Capture opponent's stones if the last stone lands in an empty pit on the player's side
        if self.board[index] == 1 and index != 6 and index != 13 and self.board[12 - index] > 0:
            self.board[6 if self.current_player == 0 else 13] += self.board[index] + self.board[12 - index]
            self.board[index] = self.board[12 - index] = 0  # Empty captured pits

        # Change turn unless last stone landed in the player's store
        if index != 6 and index != 13:
            self.current_player = 1 - self.current_player