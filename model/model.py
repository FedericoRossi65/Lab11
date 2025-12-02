import networkx as nx
from database.dao import DAO
from model.rifugio import Rifugio


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._nodes = None
        self._rifugi = {}
        for r in DAO.get_rifugio():
            self._rifugi[r.id] = r

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        self.G.clear()
        self._nodes = set()

        all_connessioni = DAO.get_connesione()

        for t in all_connessioni:
            if t.anno <= year:
                r1 = t.r1
                r2 = t.r2


                self.G.add_node(r1, obj=self._rifugi[r1])
                self.G.add_node(r2, obj=self._rifugi[r2])

                self.G.add_edge(r1, r2)

                self.G[r1][r2]["nome"] = f"{self._rifugi[r1].nome} --> {self._rifugi[r2].nome}"

                self._nodes.add(r1)
                self._nodes.add(r2)

        return self.G


    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        return [self._rifugi[rid] for rid in self._nodes]


    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        r_raggiungibili = []
        node = node.id
        for r in nx.neighbors(self.G, node):
            r_raggiungibili.append(r)
        return len(r_raggiungibili)
    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        componenti_connese = list(nx.connected_components(self.G))
        return len(componenti_connese)

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a

        """
        start = start.id
        # BFS
        bfs_tree = nx.bfs_tree(self.G, start)
        nodi_bfs = []
        for nodo in bfs_tree.nodes():
            if nodo != start:
                nodi_bfs.append(nodo)




        # DFS
        dfs_tree = nx.dfs_tree(self.G, start)
        nodi_dfs = []
        for nodo in dfs_tree.nodes():
            if nodo != start:
                nodi_dfs.append(nodo)
        lista_rifugi = []
        for nodo_id in nodi_bfs:
            rifugio = self._rifugi[nodo_id]
            lista_rifugi.append(rifugio)
        return lista_rifugi

