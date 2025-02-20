from datetime import datetime  # Importa para manejar fechas y horas.

class BSTNode:
    """
    Nodo del árbol binario de búsqueda que almacena la placa y la posición del coche.
    """
    def __init__(self, placa, parking_spot):
        self.placa = placa  # Placa del vehículo.
        self.parking_spot = parking_spot  # Posición del aparcamiento.
        self.left = None  # Hijo izquierdo.
        self.right = None  # Hijo derecho.


class BinarySearchTree:
    """
    Árbol binario de búsqueda para almacenar y buscar vehículos.
    """
    def __init__(self):
        self.root = None  # Raíz del árbol.

    def insert(self, placa, parking_spot):
        """
        Inserta un nodo en el árbol.
        """
        def _insert(node, placa, parking_spot):
            if not node:  # Si el nodo es vacío, crea uno nuevo.
                return BSTNode(placa, parking_spot)
            if placa < node.placa:  # Si la placa es menor, ve a la izquierda.
                node.left = _insert(node.left, placa, parking_spot)
            elif placa > node.placa:  # Si la placa es mayor, ve a la derecha.
                node.right = _insert(node.right, placa, parking_spot)
            return node

        self.root = _insert(self.root, placa, parking_spot)

    def search(self, placa):
        """
        Busca un nodo por placa en el árbol.
        """
        def _search(node, placa):
            if not node or node.placa == placa:  # Si el nodo es vacío o coincide, retorna.
                return node
            if placa < node.placa:  # Si la placa es menor, busca a la izquierda.
                return _search(node.left, placa)
            return _search(node.right, placa)  # Si es mayor, busca a la derecha.

        return _search(self.root, placa)

    def delete(self, placa):
        """
        Elimina un nodo del árbol por placa.
        """
        def _delete(node, placa):
            if not node:  # Si el nodo es vacío, retorna.
                return node
            if placa < node.placa:  # Si la placa es menor, busca a la izquierda.
                node.left = _delete(node.left, placa)
            elif placa > node.placa:  # Si la placa es mayor, busca a la derecha.
                node.right = _delete(node.right, placa)
            else:  # Nodo encontrado.
                if not node.left:  # Si no tiene hijo izquierdo, retorna el derecho.
                    return node.right
                elif not node.right:  # Si no tiene hijo derecho, retorna el izquierdo.
                    return node.left
                temp = self._min_value_node(node.right)  # Busca el mínimo en el subárbol derecho.
                node.placa, node.parking_spot = temp.placa, temp.parking_spot  # Reemplaza datos.
                node.right = _delete(node.right, temp.placa)  # Elimina el duplicado.
            return node

        self.root = _delete(self.root, placa)

    def _min_value_node(self, node):
        """
        Encuentra el nodo con el valor mínimo en un subárbol.
        """
        current = node
        while current.left:  # Busca el hijo más a la izquierda.
            current = current.left
        return current


class ParkingState:
    """
    Estado del aparcamiento: gestiona las posiciones ocupadas y las horas de entrada.
    """
    def __init__(self):
        self.parking_status = {f"P{i}": None for i in range(1, 10)}  # Estado de cada posición.
        self.entry_times = {f"P{i}": None for i in range(1, 10)}  # Hora de entrada de cada posición.
