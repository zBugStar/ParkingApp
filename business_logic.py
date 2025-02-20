import re  # Expresiones regulares para validar placas.
import heapq  # Cola de prioridad para Dijkstra.
from datetime import datetime
from data_layer import BinarySearchTree, ParkingState


class ParkingGraph:
    """
    Representa el grafo del aparcamiento y sus conexiones.
    """
    def __init__(self):
        self.graph = {}  # Diccionario que almacena el grafo.
        self.entries = ["E1"]  # Lista de entradas al aparcamiento.
        self.parking_spots = [f"P{i}" for i in range(1, 10)]  # Lista de posiciones de aparcamiento.
        self.initialize_graph()

    def initialize_graph(self):
        """
        Inicializa las conexiones del grafo entre nodos.
        """
        for spot in self.parking_spots + self.entries:
            self.graph[spot] = []

        # Conexiones entre nodos con sus respectivos pesos (distancias).
        connections = {
            "E1": [("P1", 1)],
            "P1": [("P2", 1), ("P4", 1)],
            "P2": [("P3", 1), ("P5", 1)],
            "P3": [("P6", 1)],
            "P4": [("P5", 1), ("P7", 1)],
            "P5": [("P6", 1), ("P8", 1)],
            "P6": [("P9", 1)],
            "P7": [("P8", 1)],
            "P8": [("P9", 1)],
        }
        for node, edges in connections.items():
            for edge, weight in edges:
                self.graph[node].append((edge, weight))  # Conexión de `node` a `edge`.
                self.graph[edge].append((node, weight))  # Conexión inversa para bidireccionalidad.

    def shortest_path(self, start, end):
        """
        Calcula el camino más corto entre dos nodos usando Dijkstra.
        """
        if start not in self.graph or end not in self.graph:  # Verifica que los nodos existan.
            return [], float('inf')
        heap = [(0, start)]  # Inicializa la cola de prioridad.
        distances = {node: float('inf') for node in self.graph}  # Distancias iniciales infinitas.
        distances[start] = 0  # Distancia al nodo inicial es 0.
        prev = {node: None for node in self.graph}  # Rastrear los nodos previos.

        while heap:
            current_dist, current_node = heapq.heappop(heap)  # Extrae el nodo con menor distancia.
            if current_node == end:  # Si llegamos al destino, terminamos.
                break
            for neighbor, weight in self.graph[current_node]:  # Recorre vecinos.
                distance = current_dist + weight  # Calcula nueva distancia.
                if distance < distances[neighbor]:  # Si es más corto, actualiza.
                    distances[neighbor] = distance
                    prev[neighbor] = current_node
                    heapq.heappush(heap, (distance, neighbor))  # Agrega a la cola.

        # Reconstruir el camino desde `end` a `start`.
        path, current = [], end
        while prev[current]:
            path.insert(0, current)  # Inserta al inicio para invertir el orden.
            current = prev[current]
        if path:
            path.insert(0, start)
        return path, distances[end]


class ParkingLogic:
    """
    Lógica principal del aparcamiento, conecta los datos y el grafo.
    """
    def __init__(self):
        self.bst = BinarySearchTree()  # Árbol binario para buscar vehículos.
        self.parking_state = ParkingState()  # Estado del aparcamiento.
        self.graph = ParkingGraph()  # Grafo para calcular rutas.

    def add_car(self, placa, parking_spot):
        """
        Agrega un coche al aparcamiento.
        """
        if not re.match(r"^[A-Z]{3}[0-9]{3}$", placa):  # Valida el formato de la placa.
            return "Placa inválida. Formato: XXX123."
        if self.parking_state.parking_status[parking_spot] is not None:  # Verifica si la posición está ocupada.
            return "El aparcamiento ya está ocupado."
        self.bst.insert(placa, parking_spot)  # Inserta en el árbol.
        self.parking_state.parking_status[parking_spot] = placa  # Actualiza el estado.
        self.parking_state.entry_times[parking_spot] = datetime.now()  # Registra la hora.
        return f"Coche con placa {placa} aparcado en {parking_spot}."

    def search_car(self, placa):
        """
        Busca un coche en el aparcamiento y retorna su información.
        """
        node = self.bst.search(placa)  # Busca el nodo en el árbol.
        if not node:  # Si no existe, retorna error.
            return None, None, None, "Placa no encontrada."
        path, distance = self.graph.shortest_path("E1", node.parking_spot)  # Calcula el camino más corto.
        entry_time = self.parking_state.entry_times[node.parking_spot]  # Obtiene la hora de entrada.
        return path, distance, entry_time, f"Placa encontrada en {node.parking_spot}."

    def delete_car(self, placa):
        """
        Elimina un coche del aparcamiento.
        """
        node = self.bst.search(placa)  # Busca el nodo.
        if not node:  # Si no existe, retorna error.
            return "Placa no encontrada."
        self.bst.delete(placa)  # Elimina del árbol.
        self.parking_state.parking_status[node.parking_spot] = None  # Libera la posición.
        self.parking_state.entry_times[node.parking_spot] = None  # Borra la hora de entrada.
        return f"Placa {placa} eliminada del sistema."
