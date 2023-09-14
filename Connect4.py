class Game:
    DEFAULT_WIDTH = 7
    DEFAULT_HEIGHT = 6

    def __init__(self, width=0, height=0):
        if width < 0 or height <0:
            raise Exception("That is not a valid size!")
        self.width = Game.DEFAULT_WIDTH if width==0 else width
        self.height = Game.DEFAULT_HEIGHT if height==0 else height
        self.player = 1
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.availableSpots = [self.height-1 for _ in range(self.width)]
        self.round = 1
        self.max_rounds = width*height

    def print_board(self):
        for i in range(self.height):
            print(self.board[i])

    def place_chip(self, col):
        row = self.availableSpots[col]
        if row == -1:
            raise Exception("The board is already filled in that column!")
        self.availableSpots[col] -= 1       #move up the location that the next chip will be placed
        self.board[row][col] = self.player
        self.round += 1
        if self.check_winner(row, col):
            print(self.player, " has won the game!")
            self.print_board()
            self.reset_game()
        elif self.round == self.max_rounds:
            print("The game was a tie!")
            self.reset_game()
        else:
            print(self.player, "has now taken their turn. The board now looks like:")
            self.print_board()
            self.player = 2 if self.player == 1 else 1    #switch the player

    def check_winner(self, row, col):
        min_row = row - 3 if row-3 > 0 else 0 #up and down
        max_row = row + 3 if row + 3 < self.height - 1 else self.height - 1
        min_col = col - 3 if col-3 > 0 else 0 #left to right
        max_col = col + 3 if col+3 < self.width - 1 else self.width-1
        return self.check_horizontal(row, min_col, max_col) or self.check_vertical(col, max_row, min_row) or self.check_diagonal(row, col, max_row, max_col)

    def check_horizontal(self, row, min_col, max_col):
        whole_row = self.board[row]
        curr = 0
        print(row)
        print(min_col, max_col)
        for i in range(min_col, max_col + 1):
            if whole_row[i] == self.player:
                curr += 1
                if curr == 4:
                    return True
            else:
                curr = 0
        return False

    def check_vertical(self, col, max_row, min_row):
        curr = 0
        for i in range(min_row, max_row + 1):
            if self.board[i][col] == self.player:
                curr += 1
                if curr == 4:
                    return True
            else:
                curr = 0
        return False

    def check_diagonal(self, row, col, max_row, max_col):
        curr_pos = 0 #initializing the current number of a player's chips in a row for the positive and negative slope
        curr_neg = 0
        for i in range(-3, 4):
            curr_row_pos = row - i #for the positive slope diagonals
            curr_col_pos = col + i
            curr_row_neg = row + i #for the negative slope diagonals
            curr_col_neg = col + i
            if 0 <= curr_row_pos <= max_row and 0 <= curr_col_pos <= max_col:
                if self.board[curr_row_pos][curr_col_pos] == self.player:
                    curr_pos += 1
                    if curr_pos >= 4:
                        return True
                else:
                    curr_pos = 0
            if 0 <= curr_row_neg <= max_row and 0 <= curr_col_neg <= max_col:
                if self.board[curr_row_neg][curr_col_neg] == self.player:
                    curr_neg += 1
                    if curr_neg >= 4:
                        return True
                else:
                    curr_neg = 0
        return False

    def reset_game(self):
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.player = 1
        self.round = 1
        self.availableSpots = [self.height - 1 for _ in range(self.width)]
        print("The game has been reset. It is now Player 1's turn.")


testGame = Game()
#print(testGame.board[0])
testGame.place_chip(0)
testGame.place_chip(0)
testGame.place_chip(6)
testGame.place_chip(0)
testGame.place_chip(0)
testGame.place_chip(0)
testGame.place_chip(1)
testGame.place_chip(2)
testGame.place_chip(1)
testGame.place_chip(2)
testGame.place_chip(2)
testGame.place_chip(3)
testGame.place_chip(3)
testGame.place_chip(4)
testGame.place_chip(3)
testGame.place_chip(6)
testGame.place_chip(1)
testGame.place_chip(2)
testGame.place_chip(1)
testGame.place_chip(2)
testGame.place_chip(1)
