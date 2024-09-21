# this is a mini project to explore the tkinter library
import tkinter as tk
import random
import colors as c

gridSize = 400
cellSize = 100
cellPadding = 5
gridCount = 4

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")

        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=3, width=gridSize, height=gridSize)
        self.main_grid.grid(pady=(80, 0)) # horizontal padding within the grid
        self.make_GUI()
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    def make_GUI(self):
        # making the base empty grid
        self.cells = []
        for i in range(gridCount):
            row = []
            for j in range(gridCount):
                cell_frame = tk.Frame(self.main_grid, bg=c.EMPTY_CELL_COLOR, width=cellSize, height=cellSize)
                cell_frame.grid(row=i, column=j, padx=cellPadding, pady=cellPadding)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # score header
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=40, anchor="center") # CSS style for positioning etc
        tk.Label(score_frame, text="Score", font=c.SCORE_LABEL_FONT).grid(row=0)


        # initialise 0 score count/value
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    def start_game(self):
        self.matrix = [[0] * gridCount for _ in range(gridCount)]

        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")

        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)

        # potential optimisation to avoid code repetition
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")

        self.score = 0


    # Matrix Manipulation Functions
    def stack(self):
        new_matrix = [[0] * gridCount for _ in range(gridCount)]
        for i in range(gridCount):
            fillPosition = 0
            for j in range(gridCount):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fillPosition] = self.matrix[i][j]
                    fillPosition += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(gridCount):
            for j in range(gridCount - 1):
                # we can only combine if they are the same number
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        for i in range(gridCount):
            self.matrix[i] = self.matrix[i][::-1]

    def transpose(self):
        # self.matrix = list(zip(*self.matrix))
        # can't use this as tuple
        new_matrix = [[0] * gridCount for _ in range(gridCount)]
        for i in range(gridCount):
            for j in range(gridCount):
                self.matrix[i][j] = new_matrix[j][i]
        self.matrix = new_matrix


    # Adding 2 or 4 randomly
    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col]  = random.choice([2, 4])

    def update_GUI(self):
        for i in range(gridCount):
            for j in range(gridCount):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(bg=c.CELL_COLORS[cell_value], fg=c.CELL_NUMBER_COLORS[cell_value], font=c.CELL_NUMBER_FONTS[cell_value], text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    # Arrow Key Instructions
    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    # Checking if vertical or horizontal movement exists
    def horizontal_move_exists(self):
        for i in range(gridCount):
            for j in range(gridCount - 1):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False

    def vertical_move_exists(self):
        for i in range(gridCount - 1):
            for j in range(gridCount):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False

    # Check if game is over
    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="You win!",
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="Game over!",
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()

def main():
    Game()

if __name__ == "__main__":
    main()

