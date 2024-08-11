import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from search import Search
from trie import Trie
import json

class AhoCorasickApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aho-Corasick Pattern Search")
        self.center_window(800, 600)
        self.create_widgets()
        self.search = Search()
        self.results_window = None

        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Aho-Corasick Pattern Search", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=(20, 20))

        # Text input
        text_label = tk.Label(self, text="Enter Text:", font=("Helvetica", 12), anchor='center')
        text_label.pack(anchor='center', padx=20)
        self.text_input = tk.Text(self, height=5, width=40, font=("Arial", 12), bg="#f0f0f0", padx=10, pady=10, borderwidth=2, relief="groove")
        self.text_input.tag_configure("center", justify='center')
        self.text_input.pack(padx=20, pady=(0, 10))
        self.set_placeholder(self.text_input, "Lorem ipsum dolor sit amet, consectetur adipiscing elit...")

        # Pattern input
        pattern_label = tk.Label(self, text="Enter Patterns separated with a comma:\n(case sensitive)", font=("Helvetica", 12), anchor='center')
        pattern_label.pack(anchor='center', padx=20)
        self.pattern_input = tk.Text(self, height=5, width=40, font=("Arial", 12), bg="#f0f0f0", padx=10, pady=10, borderwidth=2, relief="groove")
        self.pattern_input.tag_configure("center", justify='center')
        self.pattern_input.pack(padx=20, pady=(0, 20))
        self.set_placeholder(self.pattern_input, "pattern1, pattern2, pattern3, ...")

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        search_button = tk.Button(button_frame, text="Search", font=("Helvetica", 12), command=self.aho_corasick_search)
        search_button.pack(side=tk.LEFT, padx=(0, 10))

        visualize_button = tk.Button(button_frame, text="Visualize Pattern", font=("Helvetica", 12), command=self.visualize_patterns)
        visualize_button.pack(side=tk.LEFT, padx=(0, 10))

        json_button = tk.Button(button_frame, text="Input using JSON", font=("Helvetica", 12), command=self.input_using_json)
        json_button.pack(side=tk.LEFT)

    def set_placeholder(self, text_widget, placeholder):
        # Insert placeholder text
        text_widget.insert("1.0", placeholder)
        text_widget.config(fg="gray")
        text_widget.bind("<FocusIn>", lambda event: self.on_focus_in(event, text_widget, placeholder))
        text_widget.bind("<FocusOut>", lambda event: self.on_focus_out(event, text_widget, placeholder))

    def on_focus_in(self, event, text_widget, placeholder):
        if text_widget.get("1.0", "end-1c") == placeholder:
            text_widget.delete("1.0", "end")
            text_widget.config(fg="black")

    def on_focus_out(self, event, text_widget, placeholder):
        if not text_widget.get("1.0", "end-1c"):
            text_widget.insert("1.0", placeholder)
            text_widget.config(fg="gray")

    def aho_corasick_search(self):
        self.search.reset()

        # Retrieve and process inputs
        text = self.text_input.get("1.0", tk.END).strip()
        if not text or text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit...":
            messagebox.showwarning("Input Error", "Text input cannot be empty.")
            return

        rawpattern = self.pattern_input.get("1.0", tk.END).strip()
        if not rawpattern or rawpattern == "pattern1, pattern2, pattern3, ...":
            messagebox.showwarning("Input Error", "Pattern input cannot be empty.")
            return

        patterns = rawpattern.split(',')
        self.search.add_patterns([p.strip() for p in patterns if p.strip()])
        results = self.search.search(text)
        sorted_results = sorted(results.items(), key=lambda item: item[1]['count'], reverse=True)

        # Create a new window to display the results
        if self.results_window is not None:
            self.results_window.destroy()

        self.results_window = tk.Toplevel(self)
        self.results_window.title("Search Results")
        self.results_window.geometry("800x600")
        self.results_window.configure(padx=20, pady=20)

        # Title for results window
        results_title_label = tk.Label(self.results_window, text="Result", font=("Helvetica", 16, "bold"))
        results_title_label.pack(pady=(10, 20))

        # Frame for results
        results_frame = tk.Frame(self.results_window)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Results for occurrences and positions
        results_text = tk.Text(results_frame, height=10, width=50, font=("Arial", 12), bg="#f0f0f0", padx=10, pady=10, borderwidth=2, relief="groove")
        results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for results
        results_scroll = tk.Scrollbar(results_frame, command=results_text.yview)
        results_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        results_text.config(yscrollcommand=results_scroll.set)

        # Insert results
        if not sorted_results:
            results_text.insert(tk.END, "No occurrence found\n")
        else:
            results_text.insert(tk.END, "Pattern Occurrences and Positions:\n\n")
            for pattern, data in sorted_results:
                results_text.insert(tk.END, f"Pattern: {pattern}\n")
                results_text.insert(tk.END, f"Count: {data['count']}\n")
                if data['count'] != 0:
                    results_text.insert(tk.END, f"Positions: {data['positions']}\n\n")
                else:
                    results_text.insert(tk.END, "\n")

        # Highlight patterns
        highlighted_text = tk.Text(self.results_window, height=15, width=80, font=("Arial", 12), bg="#ffffff", padx=10, pady=10, borderwidth=2, relief="groove")
        highlighted_text.pack(pady=(10, 0), fill=tk.BOTH, expand=True)

        # Insert text and highlight patterns
        highlighted_text.insert(tk.END, text)
        for pattern in results.keys():
            start_idx = '1.0'
            while True:
                start_idx = highlighted_text.search(pattern, start_idx, tk.END)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(pattern)}c"
                highlighted_text.tag_add(pattern, start_idx, end_idx)
                highlighted_text.tag_configure(pattern, background="yellow", foreground="black")
                start_idx = end_idx

    def visualize_patterns(self):
        self.search.reset()

        rawpattern = self.pattern_input.get("1.0", tk.END).strip()
        if not rawpattern or rawpattern == "pattern1, pattern2, pattern3, ...":
            messagebox.showwarning("Input Error", "Pattern input cannot be empty.")
            return
        patterns = rawpattern.split(',')
        
        self.search.add_patterns([p.strip() for p in patterns if p.strip()])
        visualizer = TrieVisualizer(self.search.trie)
        visualizer.grab_set()

    def input_using_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            text = data.get("text", "").strip()
            patterns = data.get("patterns", [])
            
            if isinstance(patterns, str):
                patterns = patterns.split(',')
            
            if not text or not patterns:
                raise ValueError("Text or patterns are missing in the JSON data.")

            # Update the input fields
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", text)
            self.text_input.config(fg="black")
            
            self.pattern_input.delete("1.0", tk.END)
            self.pattern_input.insert("1.0", ", ".join(patterns))
            self.pattern_input.config(fg="black")

        except (json.JSONDecodeError, ValueError) as e:
            messagebox.showerror("JSON Error", f"Invalid JSON data: {e}")

    def on_closing(self):
        if self.results_window is not None:
            self.results_window.destroy()
        self.destroy()

class TrieVisualizer(tk.Toplevel):
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

    def on_closing(self):
        self.destroy()
        plt.close(self.fig)

if __name__ == "__main__":
    app = AhoCorasickApp()
    app.mainloop()
