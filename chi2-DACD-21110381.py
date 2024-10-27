import json
import os

class Jugador:
    def __init__(self, nombre, caracteristicas):
        self.nombre = nombre
        self.caracteristicas = caracteristicas

    def tiene_caracteristica(self, caracteristica):
        return caracteristica in self.caracteristicas

class Pregunta:
    def __init__(self, texto, siguiente=None):
        self.texto = texto  # Texto de la pregunta
        self.siguiente = siguiente  # Pregunta siguiente si la respuesta es "no"

class Akinator:
    def __init__(self):
        self.jugadores = self.cargar_jugadores()  # Cargar jugadores desde el archivo JSON
        self.preguntas = self.generar_preguntas()  # Generar la lista de preguntas

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
        with open('jug2.json', 'w') as f:
            data = [{'nombre': j.nombre, 'caracteristicas': j.caracteristicas} for j in self.jugadores]
            json.dump(data, f)

    def generar_preguntas(self):
        # Define una lista de preguntas con encadenamiento
        return [
            Pregunta("¿El jugador es delantero?", Pregunta("¿El jugador es argentino?")),
            Pregunta("¿El jugador juega en Europa?", Pregunta("¿El jugador juega en la Premier League?")),
            Pregunta("¿El jugador es conocido por su velocidad?", Pregunta("¿El jugador es de Brasil?")),
            Pregunta("¿El jugador ha ganado el Balón de Oro?", Pregunta("¿El jugador juega en el PSG?")),
        ]

    def preguntar(self, pregunta):
        respuesta = input(pregunta.texto + " (sí/no): ").strip().lower()
        if respuesta == "si":
            return True
        else:
            return self.preguntar(pregunta.siguiente) if pregunta.siguiente else False

    def adivinar_jugador(self):
        posibles_jugadores = self.jugadores

        for pregunta in self.preguntas:
            if self.preguntar(pregunta):
                # Filtrar los jugadores basados en las características
                posibles_jugadores = [j for j in posibles_jugadores if j.tiene_caracteristica(pregunta.texto.lower().replace("¿El jugador es ", "").replace("?", "").strip())]
            if len(posibles_jugadores) <= 1:
                break

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
            if self.preguntar(Pregunta(f"¿El jugador es {jugador.nombre}?")):
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
