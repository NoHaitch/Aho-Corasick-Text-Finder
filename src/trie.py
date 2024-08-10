from collections import deque
import networkx as nx


class TrieNode:
    """
    Trie Node, parameter: name (default: None)
    """

    def __init__(self, name=None):
        self.children: dict[str, TrieNode] = {}
        self.end_of_word: bool = False
        self.fail: TrieNode = None
        self.output: str = []
        self.name: str = name


class Trie:
    """
    Trie data structure for Aho-Corasick algorithm
    """

    def __init__(self):
        self.root = TrieNode(name="root")

    def insert(self, word: str) -> None:
        """Add a word to the Trie"""
        current_node = self.root
        for i, char in enumerate(word):
            node_name = f"{word[:i+1]}"
            if char not in current_node.children:
                current_node.children[char] = TrieNode(name=node_name)
            current_node = current_node.children[char]
        current_node.end_of_word = True
        current_node.output.append(word)

    def build_failure_links(self) -> None:
        """
        Build Aho-Corasick failure links
        """
        queue = deque()
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        while queue:
            current_node = queue.popleft()
            for char, child_node in current_node.children.items():
                queue.append(child_node)
                fail_node = current_node.fail

                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail

                if fail_node is None:
                    child_node.fail = self.root
                else:
                    child_node.fail = fail_node.children[char]
                    child_node.output.extend(child_node.fail.output)

    def visualize(self) -> nx.Graph:
        """
        Create a newtworkx graph for the trie. Used by matplotlib to visualize the trie
        """
        graph = nx.DiGraph()

        def add_edges(node, parent_name):
            for char, child_node in node.children.items():
                if parent_name == "root":
                    child_name = f"{char}"
                else:
                    child_name = f"{parent_name}{char}"
                graph.add_node(child_name, label=char)
                graph.add_edge(parent_name, child_name)
                add_edges(child_node, child_name)

        graph.add_node("root", label="root")
        add_edges(self.root, "root")

        def add_failure_links(node, name):
            for char, child_node in node.children.items():
                child_name = f"{name}{char}"
                if "root" in child_name:
                    child_name = child_name[4:]

                if child_node.fail:
                    fail_name = child_node.fail.name
                    if fail_name and fail_name != name:
                        graph.add_edge(
                            child_name, fail_name, color="purple", style="dashed"
                        )
                add_failure_links(child_node, child_name)

        add_failure_links(self.root, "root")

        return graph

    def print_trie(self) -> None:
        """
        Print Trie for Debugging
        """

        def print_node(node, prefix):
            end_marker = " *" if node.end_of_word else ""
            fail_marker = f" (fail: {node.fail.name})" if node.fail else ""
            print(f"{node.name}: {node.output}{end_marker}{fail_marker}")

            for char, child in node.children.items():
                print_node(child, prefix + char)

        print_node(self.root, "")
