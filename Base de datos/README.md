# Scrabble Database

Este proyecto proporciona una implementación básica de una base de datos en SQLite para gestionar jugadores y juegos del clásico juego de Scrabble. Utiliza una base de datos para almacenar la información de los jugadores, sus puntajes y el estado de las partidas.

## Funcionalidades

- **Crear base de datos y tablas necesarias**: Si no existen, se crean dos tablas:
  - `players`: Almacena la información de los jugadores, como su ID, nombre y puntaje.
  - `games`: Almacena el estado del juego, incluyendo el tablero, el turno actual y el puntaje total.

- **Agregar jugadores**: Puedes agregar nuevos jugadores a la base de datos de Scrabble. Los jugadores se identifican de manera única por su nombre.

- **Actualizar el puntaje de los jugadores**: El puntaje de un jugador se puede actualizar, sumando puntos a su total.

- **Obtener el puntaje de un jugador**: Puedes consultar el puntaje actual de un jugador.

- **Guardar el estado de un juego**: El estado del tablero, el turno actual y el puntaje se pueden guardar después de cada jugada.

## Instalación

1. Clona el repositorio en tu máquina local.
   ```bash
   git clone https://github.com/tu-usuario/scrabble-db.git
import sqlite3
import json

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


![image](https://github.com/user-attachments/assets/dabed2d4-2b58-429b-b315-ff0d26eb502f)

MIT -  LICENSE 
Este `README.md` incluye todos los detalles necesarios sobre cómo funciona el código y cómo se usa. Además, cubre los aspectos de la instalación, el uso y proporciona una pequeña referencia sobre las funciones y la licencia. Puedes pegar este contenido directamente en tu archivo `README.md` en GitHub.
