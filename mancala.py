import numpy as np

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

        # Capture
        if self.board[index] == 1 and index not in [6, 13] and self.board[12 - index] > 0:
            if self.current_player == 0 and 0 <= index <= 5:
                self.board[6] += self.board[index] + self.board[12 - index]
                self.board[index] = self.board[12 - index] = 0
            elif self.current_player == 1 and 7 <= index <= 12:
                self.board[13] += self.board[index] + self.board[12 - index]
                self.board[index] = self.board[12 - index] = 0

        if not ((self.current_player == 0 and index == 6) or (self.current_player == 1 and index == 13)):
            self.current_player = 1 - self.current_player

    def get_valid_moves(self):
        return np.where(self.board[:6] > 0)[0].tolist() if self.current_player == 0 else np.where(self.board[7:13] > 0)[0].tolist()

    def is_game_over(self):
        return np.sum(self.board[:6]) == 0 or np.sum(self.board[7:13]) == 0

    def evaluate(self):
        score_diff = self.board[6] - self.board[13]
        player_bonus = sum(self.board[i] * (i+1) for i in range(6))
        ai_bonus = sum(self.board[i+7] * (6-i) for i in range(6))

        extra_turn_potential = 0
        for i in range(6):
            if self.current_player == 0 and self.board[i] == 6-i:
                extra_turn_potential += 3
            elif self.current_player == 1 and self.board[i+7] == i+1:
                extra_turn_potential -= 3

        capture_potential = 0
        for i in range(6):
            if self.current_player == 0 and self.board[i] == 0 and self.board[12-i] > 0:
                capture_potential += self.board[12-i] * 0.5
            elif self.current_player == 1 and self.board[i+7] == 0 and self.board[5-i] > 0:
                capture_potential -= self.board[5-i] * 0.5

        return score_diff + 0.1 * (player_bonus - ai_bonus) + extra_turn_potential + capture_potential

    def minimax(self, depth, alpha, beta, maximizing):
        if depth == 0 or self.is_game_over():
            return self.evaluate()

        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return self.evaluate()

        if maximizing:
            value = float('-inf')
            for move in valid_moves:
                new_game = Mancala()
                new_game.board = np.copy(self.board)
                new_game.current_player = self.current_player

                prev_player = new_game.current_player
                new_game.move(move)
                next_max = not maximizing
                if new_game.current_player == prev_player:
                    next_max = maximizing

                value = max(value, new_game.minimax(depth-1, alpha, beta, next_max))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for move in valid_moves:
                new_game = Mancala()
                new_game.board = np.copy(self.board)
                new_game.current_player = self.current_player

                prev_player = new_game.current_player
                new_game.move(move)
                next_max = not maximizing
                if new_game.current_player == prev_player:
                    next_max = maximizing

                value = min(value, new_game.minimax(depth-1, alpha, beta, next_max))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def best_move(self):
        best_value = float('-inf')
        best_move = -1
        alpha = float('-inf')
        beta = float('inf')

        for move in self.get_valid_moves():
            new_game = Mancala()
            new_game.board = np.copy(self.board)
            new_game.current_player = self.current_player

            prev_player = new_game.current_player
            new_game.move(move)
            maximizing = False
            if new_game.current_player == prev_player:
                maximizing = True

            value = new_game.minimax(3, alpha, beta, maximizing)
            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, best_value)

        return best_move

    def finalize_game(self):
        self.board[6] += np.sum(self.board[:6])
        self.board[:6] = 0
        self.board[13] += np.sum(self.board[7:13])
        self.board[7:13] = 0
