import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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

        # tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # matplotlib navigation
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create button frame
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        # Create buttons
        self.show_success_button = tk.Button(button_frame, text="Show Successful Links", command=self.show_successful, height=2, width=20)
        self.hide_success_button = tk.Button(button_frame, text="Hide Successful Links", command=self.hide_successful, height=2, width=20)
        self.show_failure_button = tk.Button(button_frame, text="Show Failure Links", command=self.show_failure, height=2, width=20)
        self.hide_failure_button = tk.Button(button_frame, text="Hide Failure Links", command=self.hide_failure, height=2, width=20)
        self.show_normal_button = tk.Button(button_frame, text="Show Normal Links", command=self.show_normal, height=2, width=20)
        self.hide_normal_button = tk.Button(button_frame, text="Hide Normal Links", command=self.hide_normal, height=2, width=20)

        # Arrange buttons in grid
        self.show_success_button.grid(row=0, column=0, padx=5)
        self.hide_success_button.grid(row=0, column=1, padx=5)
        self.show_failure_button.grid(row=0, column=2, padx=5)
        self.hide_failure_button.grid(row=0, column=3, padx=5)
        self.show_normal_button.grid(row=0, column=4, padx=5)
        self.hide_normal_button.grid(row=0, column=5, padx=5)

        # Center the buttons
        button_frame.update_idletasks()
        total_width = sum(btn.winfo_width() for btn in button_frame.winfo_children()) + 5 * (len(button_frame.winfo_children()) - 1)
        button_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        button_frame.update()
        button_frame_width = button_frame.winfo_width()
        for i in range(len(button_frame.winfo_children())):
            button_frame.grid_columnconfigure(i, weight=1)

        self.show_successful_links = True
        self.show_failure_links = True
        self.show_normal_links = True

        self.draw_graph()

    def draw_graph(self) -> None:
        """
        Draw graph of Trie 
        """

        graph = self.trie.visualize()
        pos = self._create_tree_layout(graph)

        self.ax.clear()

        # Draw Nodes 
        nx.draw_networkx_nodes(
            graph, pos, ax=self.ax, node_size=1500, node_color='lightcoral', edgecolors='black'
        )

        # Draw Node Labels 
        nx.draw_networkx_labels(
            graph, pos, ax=self.ax, font_size=10, font_color='black'
        )

        # Draw children links 
        if self.show_normal_links:
            nx.draw_networkx_edges(
                graph, pos, ax=self.ax,
                edgelist=[(u, v) for u, v, data in graph.edges(data=True) if data.get('color') == 'black'],
                arrowstyle='->', arrowsize=50, width=2, edge_color='black', connectionstyle='arc3,rad=0'
            )

        # Draw successful links
        if self.show_successful_links:
            nx.draw_networkx_edges(
                graph, pos, ax=self.ax,
                edgelist=[(u, v) for u, v, data in graph.edges(data=True) if data.get('color') == 'green'],
                arrowstyle='->', edge_color='green', connectionstyle='arc3,rad=0.1', width=2, arrowsize=40
            )

        # Draw failure links
        if self.show_failure_links:
            nx.draw_networkx_edges(
                graph, pos, ax=self.ax,
                edgelist=[(u, v) for u, v, data in graph.edges(data=True) if data.get('color') == 'blue'],
                arrowstyle='->', edge_color='blue', connectionstyle='arc3,rad=0.05', width=1, arrowsize=40
            )

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(graph, 'label')
        if edge_labels:
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=self.ax, font_size=10)

        self.canvas.draw()

    def _create_tree_layout(self, graph):
        """
        Tree layout manually using BFS
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

            # Set height position
            pos[node] = (x_positions.get(node, 0), -level * 20)
            if level not in levels:
                levels[level] = []
            levels[level].append(node)

            # Enqueue children
            children = list(graph.neighbors(node))
            if children:
                if level not in level_widths:
                    level_widths[level] = 80
                child_width = level_widths[level] / len(children)
                for i, child in enumerate(children):
                    x_pos = x_positions.get(node, 0) + i * child_width - level_widths[level] / 2
                    x_positions[child] = x_pos
                    queue.append((level + 1, child))

        # Adjust positions for nodes at the same level
        for level, nodes in levels.items():
            layer_width = 20 
            level_widths[level] = layer_width
            for i, node in enumerate(nodes):
                pos[node] = (i * layer_width - layer_width * (len(nodes) - 1) / 2, pos[node][1])

        return pos

    def show_successful(self):
        self.show_successful_links = True
        self.draw_graph()

    def hide_successful(self):
        self.show_successful_links = False
        self.draw_graph()

    def show_failure(self):
        self.show_failure_links = True
        self.draw_graph()

    def hide_failure(self):
        self.show_failure_links = False
        self.draw_graph()

    def show_normal(self):
        self.show_normal_links = True
        self.draw_graph()

    def hide_normal(self):
        self.show_normal_links = False
        self.draw_graph()

    def on_close(self):
        """
        Handle the window close event
        """
        self.destroy()
        plt.close(self.fig)
