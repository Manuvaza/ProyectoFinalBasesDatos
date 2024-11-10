import os
import sys  # Asegúrate de importar sys aquí
from PIL import Image, ImageTk
import sqlite3
import random
import nltk
import json
import tkinter as tk
from tkinter import messagebox, simpledialog, font
from nltk.corpus import words, wordnet

# Descargar los datos de nltk al ejecutar el programa por primera vez
nltk.download('words')
nltk.download('wordnet')

# (Código de base de datos y funciones adicionales permanecen igual)

# Función para mostrar instrucciones del juego
def show_instructions():
    messagebox.showinfo(
            "Instructions\n\n",
            "1. Objective: Place words on the board that fit the assigned category (e.g., 'Animals' or 'Sports').\n\n"
            "2. How to Play:\n"
            "   - Enter a word, then specify the row, column, and direction (horizontal or vertical).\n"
            "   - Only words that match the category will be accepted.\n\n"
            "3. Scoring: Each letter has a point value. Your score is the sum of points for all letters in your words.\n\n"
            "4. Winning: The game ends after a set number of turns. The player with the highest score wins!\n\n"
            "5.Tips: \n"
            "Use high-value letters like 'Q' and 'Z' strategically to maximize your score.\n\n"
            "Plan your moves carefully to avoid blocking yourself or other players from making valuable words.\n"
            "6.Values per letter: \n\n"
            "1 point: A, E, I, L, N, O, R, S, T, U\n"
            "2 points: D, G\n"
            "3 points: B, C, M, P\n"
            "4 points: F, H, V, W, Y\n"
            "5 points: K\n"
            "8 points: J, X\n"
            "10 points: Q, Z\n\n"
            "Good luck, and have fun!"
        )


# Clase de la pantalla de bienvenida
class WelcomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrabble Game - Welcome")
        
        # Configurar el logo
        logo_path = os.path.join(sys._MEIPASS, "Logo.png") if hasattr(sys, "_MEIPASS") else "Logo.png"
        self.logo_image = Image.open(logo_path)
        self.logo_image = self.logo_image.resize((150, 150), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = tk.Label(self.root, image=self.logo_photo)
        self.logo_label.pack(pady=20)

        # Título de bienvenida
        title_font = font.Font(size=16, weight="bold")
        self.title_label = tk.Label(self.root, text="Welcome to Educational Scrabble", font=title_font)
        self.title_label.pack(pady=10)

        # Botón para Jugar
        self.play_button = tk.Button(self.root, text="Play", command=self.start_game, width=20, height=2, bg="#4CAF50", fg="white")
        self.play_button.pack(pady=5)

        # Botón para mostrar Instrucciones
        self.instructions_button = tk.Button(self.root, text="Instructions", command=show_instructions, width=20, height=2, bg="#2196F3", fg="white")
        self.instructions_button.pack(pady=5)


        # Botón para Salir
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit, width=20, height=2, bg="#f44336", fg="white")
        self.exit_button.pack(pady=5)

    def start_game(self):
        self.root.destroy()  # Cierra la pantalla de bienvenida
        app = ScrabbleApp()  # Inicia la aplicación del juego


# Conectar o crear la base de datos y las tablas necesarias
def create_database():
    connection = sqlite3.connect('Scrabble.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            score INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            board_state TEXT,
            current_turn INTEGER,
            score INTEGER DEFAULT 0,
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
    ''')
    connection.commit()
    connection.close()

create_database()

# Funciones de base de datos

def add_player(name):
    with sqlite3.connect('Scrabble.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO players (name) VALUES (?)", (name,))
        conn.commit()

def get_player_id(name):
    with sqlite3.connect('Scrabble.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT player_id FROM players WHERE name = ?", (name,))
        result = cursor.fetchone()
    return result[0] if result else None

def update_score(player_id, points):
    with sqlite3.connect('Scrabble.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE players SET score = score + ? WHERE player_id = ?", (points, player_id))
        conn.commit()

def get_score(player_id):
    with sqlite3.connect('Scrabble.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT score FROM players WHERE player_id = ?", (player_id,))
        result = cursor.fetchone()
    return result[0] if result else 0

def save_game_state(player_id, board_state, current_turn):
    board_state_json = json.dumps(board_state)
    with sqlite3.connect('Scrabble.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO games (player_id, board_state, current_turn, score) VALUES (?, ?, ?, ?)",
                       (player_id, board_state_json, current_turn, get_score(player_id)))
        conn.commit()

# Definir los valores de cada letra en el juego de Scrabble
letter_values = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 
    'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 
    'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 
    'Y': 4, 'Z': 10
}

# Función para calcular el puntaje de una palabra
def calculate_score(word):
    return sum(letter_values.get(letter.upper(), 0) for letter in word)

# Generar listas de palabras para cada categoría usando hipónimos en WordNet
def generate_category_words():
    categories = {
        "clothes": [],
        "fruits": [],
        "sports": [],
        "animals": []
    }
    
    # Definir las palabras clave de WordNet para cada categoría
    category_keywords = {
        "clothes": "clothing",
        "fruits": "fruit",
        "sports": "sport",
        "animals": "animal"
    }
    
    # Rellenar cada lista de la categoría
    for category, keyword in category_keywords.items():
        synsets = wordnet.synsets(keyword)
        words = set()
        for synset in synsets:
            words.update([lemma.name() for hyponym in synset.closure(lambda s: s.hyponyms()) for lemma in hyponym.lemmas()])
        categories[category] = list(words)
    
    return categories

# Llamar a la función para crear las listas de palabras para cada categoría
category_words = generate_category_words()

# Función para validar si una palabra pertenece a una categoría específica
def validate_word(word, category):
    return word.lower() in category_words.get(category, [])

# Clase principal del juego
class ScrabbleApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Scrabble Game")
        # Detectar cuando se intenta cerrar la ventana
        self.window.protocol("WM_DELETE_WINDOW", self.end_game)

        bold_font = font.Font(weight="bold", size=14)
        label_font = font.Font(size=12)
        cell_font = font.Font(size=10)
        
        # Etiqueta para mostrar la categoría
        self.category_label = tk.Label(self.window, text="", font=bold_font, fg="#333", bg="#f0e5d8")
        self.category_label.pack(pady=(10, 5))

        self.board_frame = tk.Frame(self.window, bg="#8fa3bf", padx=10, pady=10)
        self.board_frame.pack()

        self.players_frame = tk.Frame(self.window, bg="#f0e5d8", pady=10)
        self.players_frame.pack(fill="x")

        # Frame contenedor centrado
        self.center_frame = tk.Frame(self.window, pady=20)
        self.center_frame.pack(anchor="center", expand=True)

        # Centrar el input_frame en el centro_frame
        self.input_frame = tk.Frame(self.center_frame, bg="#f7f7f7", pady=10, padx=10)
        self.input_frame.pack(anchor="center")

        self.board = [[" " for _ in range(15)] for _ in range(15)]
        self.tiles = [[None for _ in range(15)] for _ in range(15)]
        self.players = []
        self.current_player_index = 0
        self.max_turns = 20
        self.current_turn_count = 0
        self.game_category = None  # Almacena la categoría para todo el juego

        self.setup_board(cell_font)
        self.setup_input_area(label_font)
        self.start_game()

    def setup_board(self, cell_font):
        for col in range(15):
            label = tk.Label(self.board_frame, text=str(col), width=4, height=2, borderwidth=1, relief="solid", bg="#d3d3d3")
            label.grid(row=0, column=col + 1, padx=1, pady=1)

        for row in range(15):
            label = tk.Label(self.board_frame, text=str(row), width=4, height=2, borderwidth=1, relief="solid", bg="#d3d3d3")
            label.grid(row=row + 1, column=0, padx=1, pady=1)
            for col in range(15):
                cell_color = "#ffffff" if (row + col) % 2 == 0 else "#d9d9d9"
                cell = tk.Label(self.board_frame, text=" ", width=4, height=2, borderwidth=1, relief="solid", bg=cell_color, font=cell_font)
                cell.grid(row=row + 1, column=col + 1, padx=1, pady=1)
                self.tiles[row][col] = cell

    def setup_input_area(self, label_font):
        # Centrar todos los elementos dentro del input_frame
        tk.Label(self.input_frame, text="Word:", font=label_font, bg="#f7f7f7").grid(row=0, column=0, padx=(10, 5), sticky="e")
        self.word_entry = tk.Entry(self.input_frame, font=label_font)
        self.word_entry.grid(row=0, column=1, padx=(5, 10))

        tk.Label(self.input_frame, text="Row:", font=label_font, bg="#f7f7f7").grid(row=1, column=0, padx=(10, 5), sticky="e")
        self.row_entry = tk.Entry(self.input_frame, font=label_font)
        self.row_entry.grid(row=1, column=1, padx=(5, 10))

        tk.Label(self.input_frame, text="Column:", font=label_font, bg="#f7f7f7").grid(row=2, column=0, padx=(10, 5), sticky="e")
        self.col_entry = tk.Entry(self.input_frame, font=label_font)
        self.col_entry.grid(row=2, column=1, padx=(5, 10))

        tk.Label(self.input_frame, text="Direction (h/v):", font=label_font, bg="#f7f7f7").grid(row=3, column=0, padx=(10, 5), sticky="e")
        self.direction_entry = tk.Entry(self.input_frame, font=label_font)
        self.direction_entry.grid(row=3, column=1, padx=(5, 10))

        # Ajustar el botón "Submit" con un estilo moderno
        self.submit_button = tk.Button(self.input_frame, text="Submit", command=self.submit_turn, font=label_font, bg="#4CAF50", fg="white", relief="raised")
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    def clear_inputs(self):
        self.word_entry.delete(0, tk.END)
        self.row_entry.delete(0, tk.END)
        self.col_entry.delete(0, tk.END)
        self.direction_entry.delete(0, tk.END)

    def start_game(self):
        self.game_category = select_random_category()
        self.category_label.config(text=f"Category: {self.game_category.capitalize()}")
        messagebox.showinfo("Game Category", f"The category for this game is: {self.game_category.capitalize()}")
        
        num_players = simpledialog.askinteger("Players", "How many players are playing?", parent=self.window)
        for i in range(num_players):
            name = simpledialog.askstring("Player Name", f"Enter Player {i+1} Name:", parent=self.window)
            add_player(name)
            player_id = get_player_id(name)
            self.players.append((name, player_id))
        self.update_scoreboard()
        self.next_turn()

    def update_scoreboard(self):
        for widget in self.players_frame.winfo_children():
            widget.destroy()
        for i, (name, player_id) in enumerate(self.players):
            score = get_score(player_id)
            label = tk.Label(self.players_frame, text=f"{name}: {score} pts", bg="#f0e5d8", fg="#333")
            label.pack()

    def next_turn(self):
        if self.current_turn_count >= self.max_turns:
            self.end_game()
            return

        self.current_turn_count += 1
        name, player_id = self.players[self.current_player_index]
        messagebox.showinfo("Turn", f"{name}'s turn")
        self.clear_inputs()

    def submit_turn(self):
        name, player_id = self.players[self.current_player_index]
        word = self.word_entry.get().strip().upper()
        row = int(self.row_entry.get().strip())
        col = int(self.col_entry.get().strip())
        direction = self.direction_entry.get().strip().lower()
        direction = 'horizontal' if direction == 'h' else 'vertical'
        
        if validate_word(word, self.game_category):
            if self.place_word(word, row, col, direction):
                points = calculate_score(word)
                update_score(player_id, points)
                self.update_scoreboard()
                messagebox.showinfo("Score", f"{name} scored {points} points with '{word}'!")
                
                # Cambiar al siguiente jugador
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
                self.next_turn()
            else:
                messagebox.showwarning("Error", "The word does not fit on the board.")
        else:
            messagebox.showwarning("Error", f"Invalid word. It must be related to {self.game_category}.")

    def place_word(self, word, row, col, direction):
        if direction == 'horizontal':
            if col + len(word) > 15:
                return False
            for i in range(len(word)):
                if self.board[row][col + i] != " " and self.board[row][col + i] != word[i]:
                    return False
            for i in range(len(word)):
                self.tiles[row][col + i].config(text=word[i])
                self.board[row][col + i] = word[i]
        elif direction == 'vertical':
            if row + len(word) > 15:
                return False
            for i in range(len(word)):
                if self.board[row + i][col] != " " and self.board[row + i][col] != word[i]:
                    return False
            for i in range(len(word)):
                self.tiles[row + i][col].config(text=word[i])
                self.board[row + i][col] = word[i]
        return True

    def end_game(self):
        # Crear el mensaje con los puntajes de cada jugador
        scores_message = "Game Over!\n\nFinal Scores:\n"
        max_score = 0
        winner = ""
        
        for name, player_id in self.players:
            score = get_score(player_id)
            scores_message += f"{name}: {score} points\n"
            if score > max_score:
                max_score = score
                winner = name

        # Agregar el nombre del ganador al mensaje
        scores_message += f"\nWinner: {winner} with {max_score} points!"

        # Mostrar el mensaje final con los puntajes y el ganador
        messagebox.showinfo("End of Game", scores_message)
        
        # Cerrar la ventana del juego
        self.window.destroy()

# Función para seleccionar una categoría al azar
def select_random_category():
    return random.choice(list(category_words.keys()))



# Ejecución principal
if __name__ == "__main__":
    root = tk.Tk()
    welcome_screen = WelcomeScreen(root)
    root.mainloop()
