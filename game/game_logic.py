import random
import requests

class Game:
    def __init__(self):
        self.board = list(range(1, 21))
        self.player_positions = [0, 0]
        self.player_scores = [0, 0]
        self.current_player = 0
        self.game_over = False

    @staticmethod
    def roll_dice():
        dice_value = random.randint(1, 6)
        print(f"Valor del dado: {dice_value}")
        return dice_value

    def move_player(self, steps):

        new_position = min(self.player_positions[self.current_player] + steps, len(self.board) - 1)
        self.player_positions[self.current_player] = new_position

        return new_position

    def apply_penalty(self):
        penalties = [
            ("Puente: El jugador retrocede tres casillas.", -3),
            ("Resbalón: El jugador retrocede dos casillas.", -2),
            ("Calavera: El jugador vuelve a la casilla 1.", "reset")
        ]
        penalty, movement = random.choice(penalties)


        if movement == "reset":
            self.player_positions[self.current_player] = 0
        else:
            new_position = max(self.player_positions[self.current_player] + movement, 0)
            self.player_positions[self.current_player] = new_position


        return penalty

    def check_answer(self, answer, correct_answer):
        if answer == correct_answer:
            self.player_scores[self.current_player] += 1
            print(f"Jugador {self.current_player + 1} puntaje actualizado: {self.player_scores[self.current_player]}")
            return True
        return False

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def obtener_pregunta(self, dificultad="medium"):
        url = f"https://opentdb.com/api.php?amount=1&type=multiple&difficulty={dificultad}"
        response = requests.get(url)
        data = response.json()

        if data['response_code'] == 0:
            pregunta_data = data['results'][0]

            pregunta_texto = pregunta_data['question']
            opciones = pregunta_data['incorrect_answers'] + [pregunta_data['correct_answer']]
            respuesta_correcta = pregunta_data['correct_answer']

            random.shuffle(opciones)

            return pregunta_texto, opciones, respuesta_correcta
        else:
            print("No se pudo obtener una pregunta.")
            return None, None, None

    def get_winner(self):
        if self.player_scores[0] > self.player_scores[1]:
            return 0
        elif self.player_scores[1] > self.player_scores[0]:
            return 1
        return None