import sqlite3

# Conectar a la base de datos o crearla si no existe
conn = sqlite3.connect('futbol_game.db')
cursor = conn.cursor()

# Crear la tabla para almacenar las respuestas
cursor.execute('''CREATE TABLE IF NOT EXISTS respuestas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pregunta TEXT,
                    respuesta TEXT)''')

# Crear la tabla para los jugadores y sus características
cursor.execute('''CREATE TABLE IF NOT EXISTS jugadores (
                    nombre TEXT PRIMARY KEY,
                    nacionalidad TEXT,
                    posicion TEXT,
                    club TEXT,
                    habilidades TEXT)''')

# Función para agregar jugadores iniciales en la base de datos si no existen
def agregar_jugadores_iniciales():
    jugadores_iniciales = {
        "Lionel Messi": {"nacionalidad": "Argentina", "posicion": "Delantero", "club": "Inter Miami", "habilidades": "Regate, Tiros libres"},
        "Cristiano Ronaldo": {"nacionalidad": "Portugal", "posicion": "Delantero", "club": "Al Nassr", "habilidades": "Velocidad, Tiros de cabeza"},
        "Neymar Jr.": {"nacionalidad": "Brasil", "posicion": "Delantero", "club": "Al Hilal", "habilidades": "Regate, Tiros precisos"},
        "Kylian Mbappé": {"nacionalidad": "Francia", "posicion": "Delantero", "club": "Paris Saint-Germain", "habilidades": "Velocidad, Dribbling"},
        "Kevin De Bruyne": {"nacionalidad": "Bélgica", "posicion": "Centrocampista", "club": "Manchester City", "habilidades": "Pases, Tiros lejanos"},
        "Virgil van Dijk": {"nacionalidad": "Países Bajos", "posicion": "Defensa", "club": "Liverpool", "habilidades": "Cabeza, Marcaje"},
    }

    for nombre, caracteristicas in jugadores_iniciales.items():
        cursor.execute('''INSERT OR IGNORE INTO jugadores (nombre, nacionalidad, posicion, club, habilidades)
                          VALUES (?, ?, ?, ?, ?)''',
                       (nombre, caracteristicas['nacionalidad'], caracteristicas['posicion'], caracteristicas['club'], caracteristicas['habilidades']))
    conn.commit()

# Función para hacer preguntas al usuario
def hacer_pregunta(pregunta):
    respuesta = input(pregunta + " (sí/no): ").lower()
    while respuesta not in ['sí', 'no']:
        respuesta = input("Por favor responde 'sí' o 'no': ").lower()
    
    # Guardar la respuesta en la base de datos
    cursor.execute("INSERT INTO respuestas (pregunta, respuesta) VALUES (?, ?)", (pregunta, respuesta))
    conn.commit()
    
    return respuesta == 'sí'

# Función para agregar un nuevo jugador a la base de datos
def agregar_jugador():
    nombre = input("¿Cuál era el jugador correcto?: ").capitalize()
    if cursor.execute("SELECT * FROM jugadores WHERE nombre = ?", (nombre,)).fetchone():
        print("Este jugador ya está registrado.")
        return

    nacionalidad = input(f"¿Cuál es la nacionalidad de {nombre}?: ")
    posicion = input(f"¿Cuál es la posición de {nombre}?: ")
    club = input(f"¿Cuál es el club de {nombre}?: ")
    habilidades = input(f"¿Cuáles son las habilidades de {nombre}?: ")
    
    cursor.execute('''INSERT INTO jugadores (nombre, nacionalidad, posicion, club, habilidades)
                      VALUES (?, ?, ?, ?, ?)''', (nombre, nacionalidad, posicion, club, habilidades))
    conn.commit()
    print(f"{nombre} ha sido agregado a la base de datos.")

# Encadenamiento hacia adelante con recuperación desde la base de datos
def encadenamiento_adelante():
    cursor.execute("SELECT * FROM jugadores")
    jugadores = cursor.fetchall()
    
    posibles = {j[0]: {"nacionalidad": j[1], "posicion": j[2], "club": j[3], "habilidades": j[4]} for j in jugadores}

    # Aplicar reglas según las respuestas
    if hacer_pregunta("¿El jugador es argentino?"):
        posibles = {k: v for k, v in posibles.items() if v["nacionalidad"] == "Argentina"}
    elif hacer_pregunta("¿El jugador es portugués?"):
        posibles = {k: v for k, v in posibles.items() if v["nacionalidad"] == "Portugal"}

    if hacer_pregunta("¿Juega como delantero?"):
        posibles = {k: v for k, v in posibles.items() if v["posicion"] == "Delantero"}
    elif hacer_pregunta("¿Juega como defensa?"):
        posibles = {k: v for k, v in posibles.items() if v["posicion"] == "Defensa"}

    # Si quedan más de un jugador, preguntar sobre el club
    if len(posibles) > 1:
        print("Todavía quedan varios jugadores posibles. Vamos a hacer más preguntas.")
        clubes_posibles = list(set(v["club"] for v in posibles.values()))  # Obtener clubes distintos de los jugadores restantes
        
        # Hacer preguntas sobre los clubes solo si hay más de un club posible
        for club in clubes_posibles:
            if hacer_pregunta(f"¿El jugador juega en {club}?"):
                posibles = {k: v for k, v in posibles.items() if v["club"] == club}
                break
    
    # Mostrar resultado si queda solo uno
    if len(posibles) == 1:
        jugador_adivinado = list(posibles.keys())[0]
        print(f"¿Tu jugador es {jugador_adivinado}?")
        if hacer_pregunta("¿Es correcto?"):
            print("¡He adivinado correctamente!")
        else:
            print("Vaya, no lo adiviné.")
            agregar_jugador()
    elif len(posibles) > 1:
        print(f"Algo salió mal, todavía hay varios jugadores: {', '.join(posibles.keys())}")
    else:
        print("No se pudo determinar el jugador.")
        agregar_jugador()

# Lógica del juego
def juego():
    print("¡Bienvenido al juego de Adivina Quién, versión futbolística!")
    agregar_jugadores_iniciales()  # Asegurar que los jugadores iniciales estén cargados en la base de datos
    encadenamiento_adelante()
    
# Ejecutar el juego
juego()

# Cerrar la conexión a la base de datos al final
conn.close()