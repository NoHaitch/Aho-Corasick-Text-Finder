import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from trie import Trie

class TrieVisualizer(tk.Tk):
    """
    Visualize the Aho-Corasick Trie using matplotlib and tkinter
    """

    def __init__(self, trie: Trie):
        super().__init__()
        self.title("Aho-Corasick Trie Visualization")
        self.geometry("800x600")

        self.trie = trie
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.draw_graph()

    def draw_graph(self) -> None:
        """
        Draw graph of Trie 
        """

        graph = self.trie.visualize()
        pos = self._create_tree_layout(graph)

        self.ax.clear()

        # Draw Node 
        nx.draw_networkx_nodes(
            graph, pos, ax=self.ax, node_size=2000, node_color='lightblue', edgecolors='black'
        )

        # Draw label
        nx.draw_networkx_labels(
            graph, pos, ax=self.ax
        )

        # Draw children links
        nx.draw_networkx_edges(
            graph, pos, ax=self.ax,
            edgelist=[(u, v) for u, v, data in graph.edges(data=True) if 'color' not in data],
            arrowstyle='-|>', arrowsize=30, width=3, edge_color='black', connectionstyle='arc3,rad=0'
        )

        # Draw failure links
        nx.draw_networkx_edges(
            graph, pos, ax=self.ax,
            edgelist=[(u, v) for u, v, data in graph.edges(data=True) if data.get('color') == 'purple'],
            style='dashed', edge_color='purple', connectionstyle='arc3,rad=0.5', width=1.5
        )

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(graph, 'label')
        if edge_labels:
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=self.ax)

        self.canvas.draw()


    def _create_tree_layout(self, graph):
        """
        Tree layout manualy using BFS
        """
        
        pos = {}
        visited = set()
        levels = {} 
        level_widths = {} 

        # BFS queue
        queue = [(0, 'root')] 
        x_positions = {}

        # BFS Loop
        while queue:
            level, node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)

            # Set position
            pos[node] = (x_positions.get(node, 0), -level)
            if level not in levels:
                levels[level] = []
            levels[level].append(node)

            # Enqueue children
            children = list(graph.neighbors(node))
            if children:
                if level not in level_widths:
                    level_widths[level] = 2 
                child_width = level_widths[level] / len(children)
                for i, child in enumerate(children):
                    x_pos = x_positions.get(node, 0) + i * child_width - level_widths[level] / 2
                    x_positions[child] = x_pos
                    queue.append((level + 1, child))

        # Adjust positions for nodes at the same level
        for level, nodes in levels.items():
            if len(nodes) > 1:
                layer_width = 2 
                level_widths[level] = layer_width
                for i, node in enumerate(nodes):
                    pos[node] = (i * layer_width - layer_width * (len(nodes) - 1) / 2, pos[node][1])

        return pos
