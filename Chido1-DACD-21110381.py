import json
import os

class Jugador:
    def __init__(self, nombre, caracteristicas):
        self.nombre = nombre
        self.caracteristicas = caracteristicas

    def tiene_caracteristica(self, caracteristica):
        return caracteristica in self.caracteristicas

class Akinator:
    def __init__(self):
        self.jugadores = self.cargar_jugadores()  # Carga los jugadores desde un archivo JSON
        self.preguntas = self.generar_preguntas()  # Genera una lista de preguntas

    def cargar_jugadores(self):
        if os.path.exists('jugadores.json'):
            with open('jugadores.json', 'r') as f:
                data = json.load(f)
                return [Jugador(j['nombre'], j['caracteristicas']) for j in data]
        else:
            return [
                Jugador("Lionel Messi", ["argentina", "delantero", "barcelona"]),
                Jugador("Cristiano Ronaldo", ["portugal", "delantero", "real madrid"]),
                Jugador("Neymar", ["brasil", "delantero", "psg"]),
                Jugador("Kylian Mbappé", ["francia", "delantero", "psg"]),
                Jugador("Kevin De Bruyne", ["bélgica", "centrocampista", "manchester city"])
            ]

    def guardar_jugadores(self):
        with open('jug.json', 'w') as f:
            data = [{'nombre': j.nombre, 'caracteristicas': j.caracteristicas} for j in self.jugadores]
            json.dump(data, f)

    def generar_preguntas(self):
        # Genera un conjunto de preguntas basadas en características de los jugadores
        return [
            "¿El jugador es argentino?",
            "¿El jugador juega como delantero?",
            "¿El jugador juega en el PSG?",
            "¿El jugador juega en Barcelona?",
            "¿El jugador juega en el Real Madrid?",
            "¿El jugador es centrocampista?"
        ]

    def preguntar(self, pregunta):
        respuesta = input(pregunta + " (sí/no): ").strip().lower()
        return respuesta == "sí"

    def adivinar_jugador(self):
        posibles_jugadores = self.jugadores  # Lista de jugadores posibles

        for pregunta in self.preguntas:  # Recorre cada pregunta
            if len(posibles_jugadores) <= 1:  # Si ya hay un solo jugador posible
                break  # Termina las preguntas

            # Realiza la pregunta y filtra según la respuesta
            if self.preguntar(pregunta):
                posibles_jugadores = [j for j in posibles_jugadores if j.tiene_caracteristica(pregunta.split(" ")[-1].lower())]
            else:
                posibles_jugadores = [j for j in posibles_jugadores if not j.tiene_caracteristica(pregunta.split(" ")[-1].lower())]

        # Si queda un solo jugador posible, lo adivina
        if len(posibles_jugadores) == 1:
            print(f"¡He adivinado! El jugador es {posibles_jugadores[0].nombre}.")
        else:
            print("No puedo adivinar el jugador.")
            self.aprender(posibles_jugadores)

    def aprender(self, posibles_jugadores):
        nuevo_jugador = input("¿Cuál es el nombre del jugador? ")
        nueva_caracteristica = input("¿Cuál es una característica que lo describe? (ej. 'argentina', 'delantero', etc.): ")
        self.jugadores.append(Jugador(nuevo_jugador, [nueva_caracteristica]))

        for jugador in posibles_jugadores:
            if self.preguntar(f"¿El jugador es {jugador.nombre}?"):
                jugador.caracteristicas.append(nueva_caracteristica)
                break

        self.guardar_jugadores()

    def jugar(self):
        print("¡Bienvenido al juego Akinator de futbolistas!")
        while True:
            self.adivinar_jugador()
            continuar = input("¿Quieres jugar de nuevo? (sí/no): ").strip().lower()
            if continuar != "sí":
                print("¡Gracias por jugar!")
                break

if __name__ == "__main__":
    akinator = Akinator()
    akinator.jugar()