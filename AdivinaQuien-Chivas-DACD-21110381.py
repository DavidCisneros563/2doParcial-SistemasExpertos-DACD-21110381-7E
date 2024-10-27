import json
import os

class Jugador:
    def __init__(self, nombre, atributos):
        # Inicializa un jugador con un nombre y un conjunto de atributos
        self.nombre = nombre
        self.atributos = atributos

    def __str__(self):
        # Devuelve el nombre del jugador para facilitar la visualización
        return self.nombre


class JuegoAdivinaQuien:
    def __init__(self):
        # Inicializa la lista de jugadores con sus atributos
        self.jugadores = [
            Jugador("Guadalajara", {"es portero": True, "tiene barba": False}),
            Jugador("Chicote", {"es portero": False, "tiene barba": True}),
            Jugador("Córdoba", {"es portero": False, "tiene barba": False}),
            Jugador("Ponce", {"es portero": False, "tiene barba": True}),
            # Agrega más jugadores según sea necesario
        ]
        # Carga las preguntas desde un archivo JSON
        self.preguntas = self.cargar_preguntas()

    def cargar_preguntas(self):
        # Carga las preguntas de un archivo JSON, o devuelve preguntas por defecto
        if os.path.exists("preguntas.json"):
            with open("preguntas.json", "r") as f:
                data = json.load(f)
            return data.get("preguntas", ["es portero", "tiene barba"])
        else:
            return ["es portero", "tiene barba"]

    def guardar_preguntas(self):
        # Guarda las preguntas actuales en un archivo JSON
        data = {"preguntas": self.preguntas}
        with open("preguntas.json", "w") as f:
            json.dump(data, f)

    def hacer_pregunta(self, jugador, pregunta):
        # Devuelve la respuesta del jugador a la pregunta (True o False)
        return jugador.atributos.get(pregunta, False)

    def adivinar_jugador(self):
        # Crea una copia de la lista de jugadores para filtrar
        posibles_jugadores = self.jugadores[:]
        
        # Mientras haya más de un jugador posible
        while len(posibles_jugadores) > 1:
            # Muestra las preguntas disponibles
            print(f"Preguntas disponibles: {', '.join(self.preguntas)}")
            # Solicita al usuario que elija una pregunta o que cree una nueva
            pregunta = input("¿Qué pregunta quieres hacer? (o escribe 'nuevo' para crear una nueva pregunta): ").strip().lower()
            
            # Si el usuario quiere crear una nueva pregunta
            if pregunta == 'nuevo':
                nueva_pregunta = input("Escribe la nueva pregunta: ").strip().lower()
                respuesta_correcta = input("¿Cuál es la respuesta para cada jugador? (s/n): ").strip().lower()
                
                # Agrega la nueva pregunta y su respuesta para todos los jugadores
                self.preguntas.append(nueva_pregunta)
                for jugador in self.jugadores:
                    jugador.atributos[nueva_pregunta] = (respuesta_correcta == 's')
                
                # Guarda las preguntas actualizadas
                self.guardar_preguntas()
                continue  # Vuelve al inicio del ciclo para hacer otra pregunta

            # Verifica si la pregunta es válida
            if pregunta not in self.preguntas:
                print("Pregunta no válida. Por favor elige una pregunta existente.")
                continue
            
            # Pregunta al usuario y almacena la respuesta
            respuesta = input(f"¿El jugador {pregunta}? (s/n): ").strip().lower()
            
            # Filtra los jugadores basándose en la respuesta
            if respuesta == 's':
                # Mantiene solo los jugadores que cumplen con la pregunta
                posibles_jugadores = [j for j in posibles_jugadores if self.hacer_pregunta(j, pregunta)]
            else:
                # Mantiene solo los jugadores que no cumplen con la pregunta
                posibles_jugadores = [j for j in posibles_jugadores if not self.hacer_pregunta(j, pregunta)]

            # Muestra los jugadores restantes
            print(f"Jugadores restantes: {[str(j) for j in posibles_jugadores]}")
        
        # Si hay un solo jugador posible, se adivina
        if len(posibles_jugadores) == 1:
            print(f"¡Adiviné! El jugador es {posibles_jugadores[0]}.")
        else:
            print("No pude adivinar el jugador.")

    def jugar(self):
        # Mensaje de bienvenida y comienzo del juego
        print("Bienvenido al juego 'Adivina Quién' con jugadores de Chivas.")
        self.adivinar_jugador()


if __name__ == "__main__":
    # Crea una instancia del juego y comienza a jugar
    juego = JuegoAdivinaQuien()
    juego.jugar()