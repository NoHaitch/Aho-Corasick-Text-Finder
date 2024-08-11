import tkinter as tk
from tkinter import messagebox
from search import Search
from trieVisualizer import TrieVisualizer 

class AhoCorasickApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aho-Corasick Pattern Search")
        self.center_window(800, 600) 
        self.create_widgets()
        self.search = Search()
        self.results_window = None

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
        
        # Search and Visualize buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        search_button = tk.Button(button_frame, text="Search", font=("Helvetica", 12), command=self.aho_corasick_search)
        search_button.pack(side=tk.LEFT, padx=(0, 10)) 

        visualize_button = tk.Button(button_frame, text="Visualize Pattern", font=("Helvetica", 12), command=self.visualize_patterns)
        visualize_button.pack(side=tk.LEFT)

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
                if(data['count'] != 0):
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
        visualizer.mainloop() 

    def on_closing(self):
        if self.results_window is not None:
            self.results_window.destroy()
        self.destroy()

if __name__ == "__main__":
    # Run the app
    app = AhoCorasickApp()
    app.mainloop()
