class Player():
    def __init__(self, marker):
        self.marker = marker # this is the symbol the player is playing with
        self.score = 0

class Game():
    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.player1 = Player('X')
        self.player2= Player('O')

    def display_board(self):
        print("  1   2   3")
        print(f"1 {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]}")
        print("  --------")
        print(f"2 {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]}")
        print("  --------")
        print(f"3 {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]}")

    def player_input(self, player):
        while True:
            row = int(input(f"Player {player.marker}, enter the row number (1 - 3): "))
            col = int(input(f"Player {player.marker}, enter the column number (1 - 3): "))
            if self.board[row-1][col-1] == " ":
                self.board[row-1][col-1] = player.marker
                break
            print(f"The space in row {row} and the column {col} is either invalid or has already been filled.")

    def check_win(self):
        for row in self.board:
            if row[0] == row[1] and row[1] == row[2] and " " not in row:
                return True

        for column in list(zip(*self.board)):
            if column[0] == column[1] and column[1] == column[2] and " " not in column:
                return True

        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return True

        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board [2][0] and self.board[0][2] != " ":
            return True

        for row in self.board:
            for col in row:
                if col == ' ':
                    return False

        # if it fails all other cases we return Tie as it means fully filled and no openings
        return "Tie"

def print_result(game, result):
    if result == "win":
        print(f"Player {game.current_player.marker} wins!")
        game.current_player.score += 1
    elif result == "tie":
        print("It's a tie!")

    print(f"Player X: {game.player1.score} | Player O: {game.player2.score}")

def reset_board(game):
    game.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

def ask_to_continue():
    response = input("Do you want to keep on playing? (y/n)").lower()
    return response != 'n'

def main():
    game = Game()
    game.current_player = game.player1
    while True:
        game.display_board()
        game.player_input(game.current_player)
        if game.check_win():
            print_result(game, "win")
            reset_board(game)

            if not ask_to_continue():
                break

        elif game.check_win() == "Tie":
            print_result(game, "tie")
            reset_board(game)

            if not ask_to_continue():
                break

        # we need to switch players every turn
        game.current_player = game.player2 if game.current_player == game.player1 else game.player1

if __name__ == "__main__":
    main()
    # mylist = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    # print(mylist)
    # print(list(zip(*mylist)))