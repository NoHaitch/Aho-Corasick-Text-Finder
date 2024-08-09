import networkx as nx


class TrieNode:
    """
    A Node in a Trie data structure.
    """
    
    def __init__(self):
        """
        Initializes a TrieNode with no children and not marked as the end of a word.
        """
        self.children: dict[str, 'TrieNode'] = {}
        self.end_of_word: bool = False


class Trie:
    """
    Represents a Trie data structure.
    """

    def __init__(self):
        """
        Initializes a Trie with an empty node.
        """
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        """
        Add a word into the Trie.
        """
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.end_of_word = True
