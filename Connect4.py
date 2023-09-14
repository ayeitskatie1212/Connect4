class Game:
    def __init__(self, width=7, height=6):
        if width < 0 or height <0:
            raise Exception("That is not a valid size!")
        self.width = width
        self.height = height
        self.reset_game()
        self.max_rounds = width*height + 1

    def print_board(self):
        for i in range(self.height):
            print(self.board[i])

    #returns 0 if the game continues, returns 1 if player 1 won, returns 2 if player 2 won, returns 3 if the game is a tie
    def place_chip(self, col):
        row = self.availableSpots[col]
        if row == -1:
            return 0
        self.availableSpots[col] -= 1   #move up the location that the next chip will be placed
        self.board[row][col] = self.player
        self.round += 1

        # see if there is a winner
        if self.check_winner(row, col):
            winner = self.player
            self.player = 2 if self.player == 1 else 1    #switch the player
            return winner
        
        #see if the game is a tie
        elif self.round == self.max_rounds:
            return 3
        #continue playing
        else:
            self.player = 2 if self.player == 1 else 1    #switch the player
        return 0

    def check_winner(self, row, col):
        # Setting the bounds for the search so it doesn't go out off the board

        # Vertical bounds
        min_row = row - 3 if row-3 > 0 else 0 
        max_row = row + 3 if row + 3 < self.height - 1 else self.height - 1
        # Horizontal bounds
        min_col = col - 3 if col-3 > 0 else 0 
        max_col = col + 3 if col+3 < self.width - 1 else self.width-1
        return self.check_horizontal(row, min_col, max_col) or self.check_vertical(col, max_row, min_row) or self.check_diagonal(row, col, max_row, max_col)

    def check_horizontal(self, row, min_col, max_col):
        whole_row = self.board[row]
        curr = 0
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
        self.availableSpots = [self.height - 1 for _ in range(self.width)] #the row that the next chip will be placed in