import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    # Método constructor de la clase Grafo
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    # Método para la obtención de los nodos conectados al nodo v
    def get_neighbors(self, v):
        return self.adjacency_list[v]

    # Método que asigna la función heurística a cada nodo
    def h(self, n):
        H = {
            'Ara': 366,
            'Buc': 0,
            'Cra': 160,
            'Dob': 242,
            'Efo': 161,
            'Fag': 178,
            'Giu': 77,
            'Hir': 151,
            'Ias': 226,
            'Lug': 244,
            'Meh': 241,
            'Nea': 234,
            'Ora': 380,
            'Pit': 98,
            'Rim': 193,
            'Sib': 253,
            'Tim': 329,
            'Urz': 80,
            'Vas': 199,
            'Zer': 374,
        }
        return H[n]
    
    # Método para el despliegue de los nodos y su costo en la terminal
    def print_node_and_cost(self, start_node, n, parents, costg, costh):
        reconst_path = []

        while parents[n] != n:
            reconst_path.append(n)
            n = parents[n]
        reconst_path.append(start_node)
        reconst_path.reverse()

        cost = costh + costg
        print(f"{costg}+{costh} = {cost} {reconst_path}")

    def a_star_algorithm(self, start_node, stop_node):
        # La lista abierta es la de los nodos que han sido visitados, pero sus vecinos
        # aún deben ser inspeccionados
        open_list = set([start_node])
        # La lista cerrada está conformada por los nodos visitados y con vecinos que
        # ya han sido inspeccionados
        closed_list = set([])

        # g es la variable acumuladora que contiene el valor de las distancias desde
        # el nodo inicial hacia todos los nodos visitados, su valor por defecto es +infinito
        g = {}
        g[start_node] = 0

        # parents contiene todas las relaciones entre los nodos del mapa
        parents = {}
        parents[start_node] = start_node

        # La variable nivel muestra la profundidad en el grafo
        nivel = 0
        nv_change = True

        # Este ciclo efectúa la búsqueda mientras haya nodos por investigar
        while len(open_list) > 0:
            n = None

            # Encuentra el nodo con el menor costo y se selecciona para expandir
            for v in open_list:
                if n == None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v
                    if nv_change:
                        print(" *** Nivel *** ", nivel)
                        nv_change = False
                    self.print_node_and_cost(start_node, n, parents, g[n], self.h(n))
                    if len(closed_list)>0:
                        print("Nodos expandidos: {}\n".format(closed_list))
                    else:
                        print("Nodos expandidos: {'---'}\n")

            # Si el nodo n es ninguno, quiere decir que no hay más nodos por expandir
            if n == None:
                print('No se encontró el camino')
                return None

            # Si el nodo n es el nodo meta, se reconstruye la trayectoria desde el nodo inicial
            if n == stop_node:
                final_cost = g[n] + self.h(n)
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)
                reconst_path.reverse()

                print("************* ENCONTRADO ************")
                print('Trayectoria: {}'.format(reconst_path))
                print('Costo: {}[km]'.format(final_cost))
                graficar_subgrafo(self.adjacency_list, reconst_path)
                return reconst_path

            # Se obtienen todos los nodos vecinos y su peso del nodo actual 
            for (m, weight) in self.get_neighbors(n):
                # Si el nodo actual no se encuentra en la lista abierta, se añade
                # y se agrega como padre de m
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # En caso de que ya se encuentre en la lista abierta, se revisa cual 
                # trayectoria es más corta y se selecciona. En
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # Si todos los nodos vecinos de n fueron inspeccionados,
            # se remueve n de la lista abierta actual y se añade a la lista cerrada
            open_list.remove(n)
            closed_list.add(n)
            # Se incrementa el nivel de profundidad
            nivel = nivel+1
            nv_change = True

        # En caso de no haber encontrado el nodo meta, se termina la búsqueda
        print('Trayectoria no encontrada')
        return None
    
def graficar_subgrafo(adjacency_list, nodes_to_plot):
    # Crear un objeto grafo de NetworkX
    G = nx.Graph()

    # Filtrar el diccionario adjacency_list para obtener solo los nodos y conexiones que deseamos graficar
    filtered_adjacency_list = {node: connections for node, connections in adjacency_list.items() if node in nodes_to_plot}

    # Agregar nodos y aristas al grafo
    for node, connections in filtered_adjacency_list.items():
        G.add_node(node)
        for neighbor, weight in connections:
            if neighbor in nodes_to_plot:
                G.add_edge(node, neighbor, weight=weight)

    # Dibujar el subgrafo
    pos = nx.spring_layout(G)  # Layout para la visualización
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

def main():
    adjacency_list = {
        'Ara': [('Sib', 140), ('Tim', 118), ('Zer', 75)],
        'Buc': [('Fag', 211), ('Giu', 90), ('Pit', 101), ('Urz', 85)],
        'Cra': [('Dob', 120), ('Pit', 138), ('Rim', 146)],
        'Dob': [('Cra', 120), ('Meh', 75)],
        'Efo': [('Hir', 86)],
        'Fag': [('Buc', 211), ('Sib', 99)],
        'Giu': [('Buc', 90)],
        'Hir': [('Efo', 86), ('Urz', 98)],
        'Ias': [('Nea', 87), ('Vas', 92)],
        'Lug': [('Meh', 70), ('Tim', 111)],
        'Meh': [('Dob', 75), ('Lug', 70)],
        'Nea': [('Ias', 87)],
        'Ora': [('Sib', 151), ('Zer', 71)],
        'Pit': [('Buc', 101), ('Cra', 138), ('Rim', 97)],
        'Rim': [('Cra', 146), ('Pit', 97), ('Sib', 80)],
        'Sib': [('Ara', 140), ('Fag', 99), ('Ora', 151), ('Rim', 80)],
        'Tim': [('Ara', 118), ('Lug', 111)],
        'Urz': [('Buc', 85), ('Hir', 98), ('Vas', 142)],
        'Vas': [('Ias', 92), ('Urz', 142)],
        'Zer': [('Ara', 75), ('Ora', 71)],
    }

    # Seleccionar la ciudad de orígen
    start_node_input = input("Ingrese la ciudad de inicio:    ")
    while(start_node_input != 'Ara' and
    start_node_input != 'Buc' and
    start_node_input != 'Cra' and
    start_node_input != 'Dob' and
    start_node_input != 'Efo' and
    start_node_input != 'Fag' and
    start_node_input != 'Giu' and
    start_node_input != 'Hir' and
    start_node_input != 'Ias' and
    start_node_input != 'Lug' and
    start_node_input != 'Meh' and
    start_node_input != 'Nea' and
    start_node_input != 'Ora' and
    start_node_input != 'Pit' and
    start_node_input != 'Rim' and
    start_node_input != 'Sib' and
    start_node_input != 'Tim' and
    start_node_input != 'Urz' and
    start_node_input != 'Vas' and
    start_node_input != 'Zer'):
        start_node_input = input("Ciudad no existente.\nIntroduzca una ciudad válida:    ")

    start_node = start_node_input
    goal_node = 'Buc'
    graph1 = Graph(adjacency_list)
    graph1.a_star_algorithm(start_node, goal_node)

if __name__ == "__main__":
    print("************** INICIO ***************")
    main()
    print("*************** FINAL ***************")