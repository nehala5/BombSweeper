import tkinter as tk
from random import randint
import random
from PIL import Image, ImageTk

class BlastCelebration:
    def __init__(self, master, winner):
        self.master = master
        self.master.title("Blast Celebration")
        self.canvas = tk.Canvas(master, width=800, height=600, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.particles = []

        # Creating blast particles
        self.create_particles()

        # Displaying winning player message
        self.display_message(f"Player {winner} Won!")

    def create_particles(self):
        for _ in range(400):
            x = randint(400, 420)
            y = randint(300, 320)
            dx = randint(-10, 10)
            dy = randint(-9, 9)
            color = random.choice(["red", "orange", "yellow", "blue", "green"])
            particle = self.canvas.create_oval(x, y, x + 5, y + 5, fill=color)
            self.particles.append((particle, dx, dy))
            self.animate_particle(particle, dx, dy)

    def animate_particle(self, particle, dx, dy):
        self.canvas.move(particle, dx, dy)
        if self.in_canvas(particle):
            self.master.after(50, self.animate_particle, particle, dx, dy)
        else:
            self.canvas.delete(particle)
            if (particle, dx, dy) in self.particles:
                self.particles.remove((particle, dx, dy))

        # Checking if all particles are gone, then closing the window
        if not self.particles:
            self. master.after(1000, self.master.destroy)

    def display_message(self, message):
        label = tk.Label(self.master, text=message, font=("Arial", 24), fg="white", bg="black")
        label.place(relx=0.5, rely=0.5, anchor="center")

    def in_canvas(self, obj):
        x1, y1, x2, y2 = self.canvas.coords(obj)
        return 0 <= x1 <= 800 and 0 <= y1 <= 600

def create_grid(rows: int, cols: int) -> list[list[int]]:
    return [[0 for _ in range(cols)] for _ in range(rows)]

def generate_bombs(rows: int, cols: int):
    grid = create_grid(rows, cols)
    for _ in range(20):
        x = randint(0, rows - 1)
        y = randint(0, cols - 1)
        grid[x][y] = 1
    return grid

def is_valid_move(x: int, y: int, rows: int, cols: int) -> bool:
    return 0 <= x < rows and 0 <= y < cols

def handle_click(x, y):
    global player, grid, buttons, result_label

    if not is_valid_move(x, y, rows, cols) or buttons[x][y]["text"] != " ":
        return
    if grid[x][y] == 1:
        bomb_image = Image.open(r"C:\Users\Administrator\Desktop\bomb.jpeg")
        bomb_image = bomb_image.resize((80, 50))
        bomb_photo = ImageTk.PhotoImage(bomb_image)

        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    buttons[i][j].config(image=bomb_photo, width=30, height=30)
                    buttons[i][j].image = bomb_photo  # Keep a reference

        loser = player
        winner = 3 - player
        result_label.config(text=f"Player {loser} hit a bomb! Player {winner} wins!")

        # Displaying Blast Celebration
        root = tk.Toplevel()
        blast_celebration = BlastCelebration(root, winner)
        return
    if player == 1:
        buttons[x][y].config(text="O", bg="blue")
    else:
        buttons[x][y].config(text="X", bg="red")

    if all(all(cell != 0 for cell in row) for row in grid):
        result_label.config(text="Game Over! It's a draw!")
        root = tk.Toplevel()
        blast_celebration = BlastCelebration(root, player)
        return

    player = 1 if player == 2 else 2
    result_label.config(text=f"Player {player}'s turn")

def start_game():
    welcome_frame.pack_forget()
    setup_gui()

def setup_welcome():
    global welcome_frame
    welcome_frame = tk.Frame(root, bg="#2E8B57")
    welcome_frame.pack(fill=tk.BOTH, expand=True)

    background_image = Image.open(r"C:\Users\Administrator\Desktop\blast.jpeg")

    background_image = background_image.resize((1500, 1500))
    bg_image = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(welcome_frame, image=bg_image)
    background_label.image = bg_image
    background_label.place(relwidth=1, relheight=1)

    welcome_label = tk.Label(welcome_frame, text="Welcome to Bombsweeper!", font=("Arial", 24))
    welcome_label.place(relx=0.5, rely=0.2, anchor="center")

    instructions = """
    Instructions:
    - Click on any cell to reveal its content.
    - If the cell contains a bomb, you lose.
    - If you successfully reveal all safe cells, you win.
    """
    instructions_label = tk.Label(welcome_frame, text=instructions, font=("Arial", 14), justify=tk.LEFT)
    instructions_label.place(relx=0.5, rely=0.4, anchor="center")

    start_button = tk.Button(welcome_frame, text="Start Game", font=("Arial", 16), command=start_game)
    start_button.place(relx=0.5, rely=0.6, anchor="center")

    root.mainloop()

def setup_gui():
    global rows
    global cols
    global grid
    global buttons
    global player
    global result_label

    rows, cols = 15, 15
    grid = generate_bombs(rows, cols)
    player = 1

    root.title("Bombsweeper Game")
    buttons = [[None for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            buttons[i][j] = tk.Button(root, text=" ", width=2, height=1, command=lambda i=i, j=j: handle_click(i, j))
            buttons[i][j].grid(row=i, column=j, sticky="nsew")

    player_color_label = tk.Label(root, text="Player 1: Blue   Player 2: Red", font=("Arial", 12))
    player_color_label.grid(row=rows + 1, columnspan=cols)

    result_label = tk.Label(root, text=f"Player {player}'s turn", font=("Arial", 12))
    result_label.grid(row=rows + 2, columnspan=cols)

    new_game_button = tk.Button(root, text="New Game", font=("Arial", 16), command=new_game)
    new_game_button.grid(row=rows + 3, columnspan=cols, pady=10)

    for i in range(rows):
        root.grid_rowconfigure(i, weight=1)
    for j in range(cols):
        root.grid_columnconfigure(j, weight=1)

    root.grid_rowconfigure(rows, weight=1)
    root.grid_columnconfigure(cols, weight=1)

    root.mainloop()

def new_game():
    global grid
    global buttons
    global player
    global result_label

    for i in range(rows):
        for j in range(cols):
            buttons[i][j].destroy()

    grid = generate_bombs(rows, cols)
    player = 1

    buttons = [[None for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            buttons[i][j] = tk.Button(root, text=" ", width=2, height=1, command=lambda i=i, j=j: handle_click(i, j))
            buttons[i][j].grid(row=i, column=j, sticky="nsew")

    result_label.config(text=f"Player {player}'s turn")

    for i in range(rows):
        root.grid_rowconfigure(i, weight=1)
    for j in range(cols):
        root.grid_columnconfigure(j, weight=1)

    root.grid_rowconfigure(rows, weight=1)
    root.grid_columnconfigure(cols, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("750x800")
    setup_welcome()
