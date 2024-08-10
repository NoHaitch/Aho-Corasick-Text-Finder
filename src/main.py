from trie import Trie
from trieVisualizer import TrieVisualizer

if __name__ == "__main__":
    patterns = ["he", "she", "his", "hers"]

    trie = Trie()
    for pattern in patterns:
        trie.insert(pattern)

    trie.build_failure_links()

    app = TrieVisualizer(trie)
    app.mainloop()
