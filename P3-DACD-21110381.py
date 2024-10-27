import json
import os

# Clase que representa a un jugador de fútbol.
class Jugador:
    def __init__(self, nombre, caracteristicas):
        self.nombre = nombre  # Nombre del jugador
        self.caracteristicas = caracteristicas  # Lista de características del jugador

    # Método para verificar si el jugador tiene una característica específica
    def tiene_caracteristica(self, caracteristica):
        return caracteristica in self.caracteristicas

# Clase principal que maneja el juego Akinator
class Akinator:
    def __init__(self):
        self.jugadores = self.cargar_jugadores()  # Carga los jugadores desde un archivo JSON

    # Carga la lista de jugadores desde un archivo JSON si existe
    def cargar_jugadores(self):
        if os.path.exists('jugadores.json'):  # Verifica si el archivo existe
            with open('jugadores.json', 'r') as f:  # Abre el archivo en modo lectura
                data = json.load(f)  # Carga los datos del archivo
                return [Jugador(j['nombre'], j['caracteristicas']) for j in data]  # Crea una lista de objetos Jugador
        else:
            # Si no existe el archivo, se inicializan jugadores predeterminados
            return [
                Jugador("Lionel Messi", ["argentina", "delantero", "barcelona"]),
                Jugador("Cristiano Ronaldo", ["portugal", "delantero", "real madrid"]),
                Jugador("Neymar", ["brasil", "delantero", "psg"]),
                Jugador("Kylian Mbappé", ["francia", "delantero", "psg"]),
                Jugador("Kevin De Bruyne", ["bélgica", "centrocampista", "manchester city"])
            ]

    # Guarda la lista actualizada de jugadores en un archivo JSON
    def guardar_jugadores(self):
        with open('jugadores.json', 'w') as f:  # Abre el archivo en modo escritura
            data = [{'nombre': j.nombre, 'caracteristicas': j.caracteristicas} for j in self.jugadores]  # Prepara los datos
            json.dump(data, f)  # Guarda los datos en el archivo

    # Pregunta al usuario una pregunta y devuelve True si la respuesta es "sí"
    def preguntar(self, pregunta):
        respuesta = input(pregunta + " (sí/no): ").strip().lower()  # Pide la respuesta al usuario
        return respuesta == "sí"  # Devuelve True si la respuesta es "sí"

    # Método que intenta adivinar el jugador
    def adivinar_jugador(self):
        posibles_jugadores = self.jugadores  # Lista de jugadores posibles

        # Mientras haya más de un jugador posible
        while len(posibles_jugadores) > 1:
            caracteristica = input("Introduce una característica (ej. 'argentina', 'delantero', 'barcelona'): ")
            # Pregunta si el jugador tiene la característica
            if self.preguntar(f"¿El jugador es {caracteristica}?"):
                posibles_jugadores = [j for j in posibles_jugadores if j.tiene_caracteristica(caracteristica)]  # Filtra los jugadores que tienen la característica
            else:
                posibles_jugadores = [j for j in posibles_jugadores if not j.tiene_caracteristica(caracteristica)]  # Filtra los que no la tienen

        # Si queda un solo jugador posible, lo adivina
        if len(posibles_jugadores) == 1:
            print(f"¡He adivinado! El jugador es {posibles_jugadores[0].nombre}.")
        else:
            print("No puedo adivinar el jugador.")
            self.aprender(posibles_jugadores)  # Si no puede adivinar, aprende del nuevo jugador

    # Método para aprender un nuevo jugador y sus características
    def aprender(self, posibles_jugadores):
        nuevo_jugador = input("¿Cuál es el nombre del jugador? ")  # Pide el nombre del jugador no adivinado
        nueva_caracteristica = input("¿Cuál es una característica que lo describe? (ej. 'argentina', 'delantero', etc.): ")  # Pide una característica
        self.jugadores.append(Jugador(nuevo_jugador, [nueva_caracteristica]))  # Agrega el nuevo jugador a la lista

        # Pregunta si uno de los posibles jugadores era el correcto
        for jugador in posibles_jugadores:
            if self.preguntar(f"¿El jugador es {jugador.nombre}?"):
                jugador.caracteristicas.append(nueva_caracteristica)  # Agrega la nueva característica al jugador existente
                break

        self.guardar_jugadores()  # Guarda la lista actualizada de jugadores

    # Método para iniciar el juego
    def jugar(self):
        print("¡Bienvenido al juego Akinator de futbolistas!")
        while True:
            self.adivinar_jugador()  # Intenta adivinar el jugador
            continuar = input("¿Quieres jugar de nuevo? (sí/no): ").strip().lower()  # Pregunta si quiere jugar de nuevo
            if continuar != "sí":
                print("¡Gracias por jugar!")  # Mensaje de despedida
                break

# Punto de entrada del programa
if __name__ == "__main__":
    akinator = Akinator()  # Crea una instancia de Akinator
    akinator.jugar()  # Inicia el juego