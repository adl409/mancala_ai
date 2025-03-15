import numpy as np
import tkinter as tk
from tkinter import messagebox

class Mancala:
    def __init__(self):
        self.board = np.array([4] * 6 + [0] + [4] * 6 + [0])
        self.current_player = 0
    
    def move(self, pit):
        if self.current_player == 1:
            pit += 7
        stones = self.board[pit]
        self.board[pit] = 0
        index = pit

        while stones:
            index = (index + 1) % 14
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