import tkinter as tk
from tkinter import messagebox
import random

class AlcanzaLaEstrella:
    def __init__(self, root):
        self.root = root
        self.root.title("Alcanza la Estrella")

        # Configuración del tablero y posiciones
        self.tablero = [" "] * 20
        self.posiciones_jugadores = [0, 0]  # Ambos jugadores inician en la primera casilla (posición 0)
        self.puntajes = [0, 0]
        self.turno = 0
        self.dado = 0  # Guardar valor del dado
        self.juego_terminado = False  # Indica si el juego ha terminado

        # Lista de preguntas y respuestas
        self.preguntas = [
            ("¿Qué es H2O?", ["a) Agua", "b) Oxígeno", "c) Hidrógeno"], 0),
            ("¿Cuál es el planeta más cercano al sol?", ["a) Tierra", "b) Mercurio", "c) Venus"], 1),
            ("¿Quién pintó la Mona Lisa?", ["a) Van Gogh", "b) Picasso", "c) Leonardo da Vinci"], 2),
            ("¿Cuántos colores hay en el arcoíris?", ["a) 5", "b) 7", "c) 9"], 1),
            ("¿Cuál es el río más largo del mundo?", ["a) Nilo", "b) Amazonas", "c) Yangtsé"], 1)
        ]
        self.preguntas_disponibles = list(range(len(self.preguntas)))  # Índices de preguntas disponibles

        # Crear interfaz gráfica
        self.crear_interfaz()
        self.actualizar_tablero()  # Reflejar las posiciones iniciales en la interfaz

    def crear_interfaz(self):
        # Crear tablero visual
        self.tablero_frame = tk.Frame(self.root)
        self.tablero_frame.pack(pady=10)

        self.tablero_labels = []
        for i in range(20):
            label = tk.Label(self.tablero_frame, text=f"{i + 1}", borderwidth=1, relief="solid", width=3, height=2)
            label.grid(row=i // 5, column=i % 5)
            self.tablero_labels.append(label)

        # Botón para lanzar dado
        self.lanzar_btn = tk.Button(self.root, text="Lanzar Dado", command=self.lanzar_dado)
        self.lanzar_btn.pack(pady=10)

        # Mostrar puntaje
        self.puntaje_label = tk.Label(self.root, text="Puntajes: Jugador 1 - 0 | Jugador 2 - 0")
        self.puntaje_label.pack()

    def lanzar_dado(self):
        if self.juego_terminado:
            return  # Evitar acciones si el juego ha terminado

        if not self.preguntas_disponibles:
            # Si no quedan preguntas, declarar ganador por puntaje
            self.declarar_ganador_por_puntaje()
            return

        self.dado = random.randint(1, 6)
        jugador = self.turno + 1
        messagebox.showinfo("Dado", f"Jugador {jugador} lanzó un {self.dado}")

        # Actualizar posición del jugador
        self.posiciones_jugadores[self.turno] += self.dado
        if self.posiciones_jugadores[self.turno] >= 20:
            self.posiciones_jugadores[self.turno] = 20  # Mover a la posición 20 al ganar

        # Pregunta de trivia
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        if not self.preguntas_disponibles:
            messagebox.showinfo("Fin de preguntas", "No hay más preguntas disponibles.")
            return

        pregunta_idx = random.choice(self.preguntas_disponibles)  # Seleccionar pregunta al azar sin repetición
        pregunta, opciones, respuesta_correcta = self.preguntas[pregunta_idx]
        self.preguntas_disponibles.remove(pregunta_idx)  # Eliminar pregunta de disponibles para evitar repetición

        self.pregunta_ventana = tk.Toplevel(self.root)
        self.pregunta_ventana.title("Pregunta")

        pregunta_label = tk.Label(self.pregunta_ventana, text=pregunta)
        pregunta_label.pack(pady=10)

        # Crear botones para opciones
        for idx, opcion in enumerate(opciones):
            boton_opcion = tk.Button(self.pregunta_ventana, text=opcion,
                                     command=lambda idx=idx: self.verificar_respuesta(idx, respuesta_correcta))
            boton_opcion.pack(pady=2)

    def verificar_respuesta(self, seleccion, respuesta_correcta):
        self.pregunta_ventana.destroy()

        if seleccion == respuesta_correcta:
            self.puntajes[self.turno] += 1
            messagebox.showinfo("Resultado", "¡Respuesta correcta!")
        else:
            messagebox.showinfo("Resultado", "Respuesta incorrecta.")
            # Aplicar un castigo aleatorio en caso de respuesta incorrecta
            self.aplicar_castigo()

        # Verificar si el jugador ha ganado
        if self.posiciones_jugadores[self.turno] == 20:
            ganador = self.turno + 1
            color_ganador = "red" if self.turno == 0 else "blue"
            self.marcar_tablero_completo(color_ganador)  # Marcar todo el tablero
            messagebox.showinfo("Juego terminado", f"¡Jugador {ganador} ha ganado!")
            self.juego_terminado = True  # Marcar el juego como terminado
            return

        # Actualizar tablero visual y puntajes
        self.actualizar_tablero()

        # Cambiar turno
        self.turno = 1 - self.turno  # Alternar entre 0 y 1
        self.puntaje_label.config(text=f"Puntajes: Jugador 1 - {self.puntajes[0]} | Jugador 2 - {self.puntajes[1]}")

    def aplicar_castigo(self):
        castigos = [
            ("Puente: El jugador retrocede tres casillas.", -3),
            ("Resbalón: El jugador retrocede dos casillas.", -2),
            ("Calavera: El jugador vuelve a la casilla 1.", "reset")
        ]
        castigo, movimiento = random.choice(castigos)

        if movimiento == "reset":
            self.posiciones_jugadores[self.turno] = 0  # Enviar al jugador al inicio
        else:
            # Aplicar el movimiento de retroceso
            self.posiciones_jugadores[self.turno] += movimiento
            if self.posiciones_jugadores[self.turno] < 0:
                self.posiciones_jugadores[self.turno] = 0  # Evitar posiciones negativas

        messagebox.showinfo("Castigo", castigo)

    def actualizar_tablero(self):
        # Restablecer el color de todas las casillas, excepto si el juego ha terminado
        if not self.juego_terminado:
            for i, label in enumerate(self.tablero_labels):
                label.config(text=str(i + 1), bg="SystemButtonFace")

            # Verificar si ambos jugadores están en la misma casilla
            if self.posiciones_jugadores[0] == self.posiciones_jugadores[1] and self.posiciones_jugadores[0] < 20:
                pos = self.posiciones_jugadores[0]
                self.tablero_labels[pos].config(bg="purple", text="1&2")  # Colorear y mostrar ambos jugadores
            else:
                # Colorear posiciones de jugadores individualmente
                for i, pos in enumerate(self.posiciones_jugadores):
                    if pos < 20:
                        self.tablero_labels[pos].config(bg="red" if i == 0 else "blue", text=f"{pos + 1}")

    def marcar_tablero_completo(self, color):
        # Cambia el color de todas las casillas al color del jugador ganador
        for label in self.tablero_labels:
            label.config(bg=color)

    def declarar_ganador_por_puntaje(self):
        # Verificar quién tiene más puntos y declarar ganador
        if self.puntajes[0] > self.puntajes[1]:
            ganador = 1
            color_ganador = "red"
        elif self.puntajes[1] > self.puntajes[0]:
            ganador = 2
            color_ganador = "blue"
        else:
            messagebox.showinfo("Juego terminado", "¡Es un empate!")
            return

        # Marcar el tablero completo con el color del ganador
        self.marcar_tablero_completo(color_ganador)
        messagebox.showinfo("Juego terminado", f"¡Jugador {ganador} ha ganado por tener más respuestas correctas!")
        self.juego_terminado = True  # Marcar el juego como terminado

# Ejecutar la interfaz gráfica
root = tk.Tk()
app = AlcanzaLaEstrella(root)
root.mainloop()