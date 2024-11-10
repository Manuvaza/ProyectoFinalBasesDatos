# ProyectoFinalBasesDatos
Scrabble Educativo es un juego de palabras interactivo en Python con interfaz Tkinter y base de datos en SQLite. Permite construir palabras en categorías específicas como animales y deportes, fomentando el aprendizaje de vocabulario. Ideal para estudiantes y educadores que buscan una herramienta divertida y educativa.
AlphaLearn
## Características

- **Interfaz gráfica**: Utiliza Tkinter para una experiencia visual amigable y fácil de usar.
- **Categorías de palabras**: Las palabras deben pertenecer a una categoría específica (por ejemplo, "animales", "deportes").
- **Base de datos SQLite**: Registra información de jugadores y estados de juego.
- **Sistema de puntuación**: Basado en el valor de cada letra, similar a Scrabble clásico.
- **Modo multijugador**: Permite agregar múltiples jugadores en una misma partida.

## Instrucciones de Instalación

1. **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/scrabble-educativo.git
    ```
2. **Instalar dependencias**:
    - Asegúrate de tener Python 3.6+ instalado.
    - Instala las bibliotecas necesarias con:
      ```bash
      pip install -r requirements.txt
      ```
3. **Ejecutar el juego**:
    ```bash
    python scrabble_educativo.py
    ```
## Uso

1. Al iniciar el programa, se abrirá una pantalla de bienvenida.
2. Selecciona "Play" para iniciar una partida o "Instructions" para ver las reglas.
3. Ingresa la cantidad de jugadores y sus nombres.
4. El juego asignará una categoría de palabras (por ejemplo, "animales").
5. En cada turno, ingresa una palabra válida en la categoría, así como su posición y dirección en el tablero.
6. La partida finalizará después de un número determinado de turnos, y se anunciará el jugador con el puntaje más alto.

## Dependencias

- **Python** 3.6+
- **nltk**: Para la generación y verificación de palabras según la categoría.
- **sqlite3**: Para la administración de datos del juego y jugadores.
- **tkinter**: Interfaz gráfica de usuario.
- **PIL (Pillow)**: Para la gestión de imágenes (opcional, si incluyes un logo).

## Personalización

Puedes modificar las categorías y el sistema de puntuación, así como el límite de turnos en `scrabble_educativo.py`. También puedes agregar más validaciones o ajustar la interfaz para mejorar la experiencia de usuario.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request con tus sugerencias y mejoras.

## Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.
