import json
import os

class Akinator:
    def __init__(self, data_file='data.json'):
        # Inicializa el juego y carga los datos desde un archivo JSON
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        # Carga las preguntas y respuestas desde el archivo JSON
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)  # Carga los datos existentes
        else:
            # Si no existe el archivo, inicializa una nueva estructura
            self.data = {
                "questions": [],  # Lista de preguntas
                "answers": {}     # Diccionario de respuestas
            }

    def save_data(self):
        # Guarda las preguntas y respuestas en el archivo JSON
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file, indent=4)  # Guarda los datos en formato JSON

    def ask_question(self, question):
        # Pregunta al usuario y devuelve una respuesta booleana
        answer = input(question + " (sí/no): ").strip().lower()  # Pide una respuesta
        return answer == "sí"  # Devuelve True si la respuesta es "sí"

    def play(self):
        # Inicia el juego e intenta adivinar al personaje
        if self.guess_player():
            print("¡He adivinado tu personaje!")  # Si adivina correctamente
        else:
            print("No pude adivinar. ¿Quién era?")
            new_character = input("Introduce el nombre del personaje: ").strip()  # Pide el nombre del personaje
            new_question = input("Introduce una pregunta que distinga a este personaje: ").strip()  # Pide una nueva pregunta
            # Pregunta si la respuesta es "sí" o "no" para la nueva pregunta
            correct_answer = self.ask_question(f"¿La respuesta para {new_character} es 'sí' o 'no' para esta pregunta: {new_question}?")

            # Agrega la nueva pregunta y respuesta a los datos
            self.data["questions"].append(new_question)  # Añade la nueva pregunta
            self.data["answers"][new_question] = {
                "yes": new_character,  # Personaje para respuesta "sí"
                "no": "Chicharito Hernández"  # Personaje para respuesta "no"
            }

            self.save_data()  # Guarda los datos actualizados
            print(f"He aprendido algo nuevo: {new_question} -> {'sí' if correct_answer else 'no'} es {new_character}")

    def guess_player(self):
        # Realiza la lógica para adivinar el personaje
        for question in self.data["questions"]:
            # Para cada pregunta almacenada, pregunta al usuario
            if self.ask_question(question):
                # Si la respuesta es "sí", verifica si es Chicharito
                if question in self.data["answers"]:
                    character = self.data["answers"][question]["yes"]
                    if character == "Chicharito Hernández":
                        return True  # Adivinó correctamente
            else:
                # Si la respuesta es "no", verifica la respuesta correspondiente
                if question in self.data["answers"]:
                    character = self.data["answers"][question]["no"]
                    if character == "Chicharito Hernández":
                        return False  # No adivinó

        return False  # Si no se puede adivinar, devuelve False

if __name__ == "__main__":
    game = Akinator()  # Crea una instancia del juego
    print("¡Bienvenido al juego de adivinar al futbolista!")  # Mensaje de bienvenida
    game.play()  # Inicia el juego