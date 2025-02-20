import tkinter as tk  # Biblioteca para crear la interfaz gráfica.
from tkinter import messagebox, ttk  # Widgets adicionales y mensajes emergentes.
from business_logic import ParkingLogic  # Lógica del sistema.

class ParkingApp:
    """
    Interfaz gráfica del sistema de aparcamiento.
    """
    def __init__(self, root):
        self.root = root  # Ventana principal.
        self.root.title("Sistema de Aparcamiento")  # Título de la ventana.
        self.logic = ParkingLogic()  # Instancia de la lógica del sistema.
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")  # Canvas para dibujar el aparcamiento.
        self.canvas.pack()  # Muestra el canvas.

        # Posiciones de los nodos en el canvas.
        self.positions = {
            "E1": (50, 50),
            "P1": (150, 150), "P2": (300, 150), "P3": (450, 150),
            "P4": (150, 300), "P5": (300, 300), "P6": (450, 300),
            "P7": (150, 450), "P8": (300, 450), "P9": (450, 450),
        }

        self.draw_graph_connections()  # Dibuja las conexiones del grafo.
        self.draw_parking()  # Dibuja los nodos del aparcamiento.
        self.draw_legend()  # Dibuja la leyenda del sistema.

        # Widgets para interactuar con el sistema.
        tk.Label(root, text="Placa (XXX123):").pack()  # Etiqueta para introducir la placa.
        self.placa_entry = tk.Entry(root)  # Entrada de texto para la placa.
        self.placa_entry.pack()  # Muestra la entrada.

        tk.Label(root, text="Seleccione Aparcamiento:").pack()  # Etiqueta para seleccionar un aparcamiento.
        self.parking_selector = ttk.Combobox(root, values=self.get_available_parking_spots())  # ComboBox con los aparcamientos disponibles.
        self.parking_selector.pack()  # Muestra el ComboBox.

        # Botones para agregar, buscar y eliminar coches.
        tk.Button(root, text="Agregar", command=self.add_car).pack()  # Botón para agregar un coche.
        tk.Button(root, text="Buscar", command=self.search_car).pack()  # Botón para buscar un coche.
        tk.Button(root, text="Eliminar", command=self.delete_car).pack()  # Botón para eliminar un coche.

    def draw_graph_connections(self):
        """
        Dibuja las conexiones del grafo como líneas en el canvas.
        """
        for node, edges in self.logic.graph.graph.items():  # Recorre cada nodo y sus conexiones.
            x1, y1 = self.positions[node]  # Coordenadas del nodo actual.
            for neighbor, _ in edges:  # Recorre los nodos vecinos.
                x2, y2 = self.positions[neighbor]  # Coordenadas del nodo vecino.
                self.canvas.create_line(x1, y1, x2, y2, fill="gray", tags="connection")  # Dibuja una línea entre los nodos.

    def draw_parking(self):
        """
        Dibuja los nodos del aparcamiento (entradas y posiciones).
        """
        for node, pos in self.positions.items():  # Recorre cada nodo y su posición.
            x, y = pos  # Coordenadas del nodo.
            color = "green" if node == "E1" else "blue"  # Entrada en verde, aparcamientos en azul.
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, tags=f"circle_{node}")  # Dibuja un círculo para el nodo.
            self.canvas.create_text(x, y, text=node, fill="white", tags=f"text_{node}")  # Dibuja el texto del nodo.

    def draw_legend(self):
        """
        Dibuja una leyenda en el canvas para explicar los colores y elementos.
        """
        legend_x, legend_y = 600, 50  # Posición inicial de la leyenda.
        legend_items = [
            ("green", "Entrada"),
            ("blue", "Aparcamiento disponible"),
            ("orange", "Aparcamiento ocupado"),
            ("gray", "Conexión entre nodos"),
        ]
        for color, label in legend_items:  # Recorre los elementos de la leyenda.
            self.canvas.create_rectangle(legend_x, legend_y, legend_x + 20, legend_y + 20, fill=color)  # Dibuja un rectángulo con el color correspondiente.
            self.canvas.create_text(legend_x + 50, legend_y + 10, text=label, anchor="w")  # Dibuja el texto descriptivo.
            legend_y += 30  # Incrementa la posición vertical.

    def get_available_parking_spots(self):
        """
        Obtiene una lista de aparcamientos disponibles.
        """
        return [spot for spot, car in self.logic.parking_state.parking_status.items() if car is None]  # Retorna los nodos no ocupados.

    def update_parking_selector(self):
        """
        Actualiza los valores del ComboBox de aparcamientos disponibles.
        """
        self.parking_selector['values'] = self.get_available_parking_spots()  # Actualiza las opciones disponibles.

    def add_car(self):
        """
        Agrega un coche al sistema basado en los datos introducidos.
        """
        placa = self.placa_entry.get()  # Obtiene la placa del usuario.
        selected_spot = self.parking_selector.get()  # Obtiene la posición seleccionada.
        message = self.logic.add_car(placa, selected_spot)  # Llama a la lógica para agregar el coche.
        self.update_parking_selector()  # Actualiza los aparcamientos disponibles.
        self.update_parking_colors()  # Actualiza los colores de los nodos.
        messagebox.showinfo("Resultado", message)  # Muestra el resultado en un mensaje emergente.

    def search_car(self):
        """
        Busca un coche en el sistema y muestra su información.
        """
        placa = self.placa_entry.get()  # Obtiene la placa del usuario.
        result = self.logic.search_car(placa)  # Busca el coche en la lógica.
        if result[0]:  # Si se encuentra el coche.
            path, distance, entry_time, message = result  # Desempaqueta la información del coche.
            self.draw_path(path)  # Dibuja el camino más corto hacia el coche.
            self.show_vehicle_position(placa, path[-1], entry_time, distance)  # Muestra la ventana emergente con la información.
        else:
            messagebox.showerror("Error", result[3])  # Muestra un mensaje de error si no se encuentra.

    def show_vehicle_position(self, placa, position, entry_time, distance):
        """
        Muestra una ventana emergente con la información del coche.
        """
        popup = tk.Toplevel(self.root)  # Crea una nueva ventana.
        popup.title("Posición del Vehículo")  # Título de la ventana.
        popup.geometry("300x200")  # Tamaño de la ventana.
        popup.resizable(False, False)  # Deshabilita el cambio de tamaño.

        # Información del coche.
        tk.Label(popup, text=f"Placa: {placa}", font=("Arial", 14)).pack(pady=5)  # Muestra la placa.
        tk.Label(popup, text=f"Posición: {position}", font=("Arial", 14)).pack(pady=5)  # Muestra la posición.
        if entry_time:  # Si existe hora de entrada.
            tk.Label(popup, text=f"Hora de entrada: {entry_time.strftime('%H:%M:%S')}", font=("Arial", 14)).pack(pady=5)  # Muestra la hora de entrada.
        tk.Label(popup, text=f"Distancia: {distance} unidades", font=("Arial", 14)).pack(pady=5)  # Muestra la distancia desde la entrada.

        tk.Button(popup, text="Cerrar", command=popup.destroy).pack(pady=10)  # Botón para cerrar la ventana.

    def delete_car(self):
        """
        Elimina un coche del sistema.
        """
        placa = self.placa_entry.get()  # Obtiene la placa del usuario.
        message = self.logic.delete_car(placa)  # Llama a la lógica para eliminar el coche.
        self.update_parking_selector()  # Actualiza los aparcamientos disponibles.
        self.update_parking_colors()  # Actualiza los colores de los nodos.
        messagebox.showinfo("Resultado", message)  # Muestra el resultado en un mensaje emergente.

    def update_parking_colors(self):
        """
        Actualiza los colores de los nodos según su estado.
        """
        for spot, car in self.logic.parking_state.parking_status.items():  # Recorre cada nodo y su estado.
            color = "orange" if car else "blue"  # Naranja si está ocupado, azul si está libre.
            self.canvas.itemconfig(f"circle_{spot}", fill=color)  # Actualiza el color del nodo.

    def draw_path(self, path):
        """
        Dibuja el camino más corto en el canvas.
        """
        self.canvas.delete("path")  # Elimina caminos anteriores.
        for i in range(len(path) - 1):  # Recorre cada par de nodos en el camino.
            x1, y1 = self.positions[path[i]]  # Coordenadas del nodo actual.
            x2, y2 = self.positions[path[i + 1]]  # Coordenadas del siguiente nodo.
            self.canvas.create_line(x1, y1, x2, y2, fill="yellow", width=3, tags="path")  # Dibuja una línea amarilla entre los nodos.
