from email.mime import application
from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QGridLayout, QMessageBox, QInputDialog,QApplication
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer
from mancala import Mancala

class MancalaGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mancala with AI")
        self.game = Mancala()
        self.buttons = []
        self.ai_thinking = False
        self.init_ui()
        self.choose_starting_player()

    def init_ui(self):
        layout = QGridLayout(self)

        self.turn_label = QLabel("Your Turn")
        self.turn_label.setAlignment(Qt.AlignCenter)
        self.turn_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.turn_label, 0, 3, 1, 3)

        for i in range(6):
            btn = QPushButton(str(self.game.board[7 + i]))
            btn.setEnabled(False)
            layout.addWidget(btn, 1, i + 1)
            self.buttons.append(btn)

        for i in range(6):
            btn = QPushButton(str(self.game.board[i]))
            btn.clicked.connect(lambda _, x=i: self.player_move(x))
            layout.addWidget(btn, 3, i + 1)
            self.buttons.append(btn)

        self.store_p2 = QLabel(f"AI: {self.game.board[13]}")
        self.store_p2.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.store_p2, 2, 0)

        self.store_p1 = QLabel(f"You: {self.game.board[6]}")
        self.store_p1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.store_p1, 2, 7)

    def choose_starting_player(self):
        choice, ok = QInputDialog.getItem(
            self, "Choose Starting Player", "Who goes first?",
            ["You", "AI"], editable=False
        )
        if ok and choice == "AI":
            self.game.current_player = 1
            self.update_board()
            QTimer.singleShot(1000, self.ai_move)
        else:
            self.game.current_player = 0
            self.update_board()

    def update_board(self):
        for i in range(6):
            self.buttons[i].setText(str(self.game.board[7 + i]))
            self.buttons[i + 6].setText(str(self.game.board[i]))
        self.store_p1.setText(f"You: {self.game.board[6]}")
        self.store_p2.setText(f"AI: {self.game.board[13]}")

        if self.game.current_player == 0:
            self.turn_label.setText("Your Turn")
            self.turn_label.setStyleSheet("color: green")
        else:
            self.turn_label.setText("AI's Turn")
            self.turn_label.setStyleSheet("color: red")

    def player_move(self, pit):
        if self.game.current_player != 0 or self.ai_thinking:
            return

        valid_moves = self.game.get_valid_moves()
        if not valid_moves:
            self.game.current_player = 1
            self.update_board()
            QTimer.singleShot(1000, self.ai_move)
            return

        if pit not in valid_moves:
            return

        previous_player = self.game.current_player
        self.game.move(pit)
        self.update_board()

        if self.game.is_game_over():
            self.end_game()
        elif self.game.current_player == 1:
            QTimer.singleShot(1000, self.ai_move)

    def ai_move(self):
        if self.ai_thinking:
            return
            
        self.ai_thinking = True
        self.update_board()
        
        valid_moves = self.game.get_valid_moves()
        if not valid_moves:
            self.game.current_player = 0
            self.update_board()
            self.ai_thinking = False
            if self.game.is_game_over():
                self.end_game()
            return

        QTimer.singleShot(300, self._execute_ai_move)
        
    def _execute_ai_move(self):
        move = self.game.best_move()
        if move != -1:
            self.game.move(move)
            self.update_board()
            
            if self.game.is_game_over():
                self.ai_thinking = False
                self.end_game()
            elif self.game.current_player == 1:
                self.ai_thinking = False
                QTimer.singleShot(500, self.ai_move)
            else:
                self.ai_thinking = False
        else:
            self.game.current_player = 0
            self.update_board()
            self.ai_thinking = False

    def end_game(self):
        self.game.finalize_game()
        self.update_board()
        result = self.game.evaluate()
        
        if result > 0:
            msg = f"You win! Final score: You {self.game.board[6]} - AI {self.game.board[13]}"
        elif result < 0:
            msg = f"AI wins! Final score: You {self.game.board[6]} - AI {self.game.board[13]}"
        else:
            msg = f"It's a tie! Final score: {self.game.board[6]} each"
            
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.buttonClicked.connect(lambda _: QApplication.quit())
        msg_box.exec()
