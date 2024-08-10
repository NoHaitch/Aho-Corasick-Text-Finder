from trie import Trie, TrieNode

class Search:
    """
    Aho-Corasick Search
    """

    def __init__(self):
        self.reset() 

    def reset(self) -> None:
        """
        Reset the Trie to be empty
        """
        self.trie = Trie()
        

    def add_patterns(self, patterns: list[str]) -> None:
        """
        Add a new pattern to the trie and store them
        """
        for pattern in patterns:
            self.trie.insert(pattern)
        self.trie.build_failure_links()

    def search(self, text: str) -> dict[str, dict[str, int]]:
        """
        Search the text using all the patterns
        """
        current_node: TrieNode = self.trie.root
        results: dict[str, dict[str, int]] = {pattern: {"count": 0, "positions": []} for pattern in self.trie.patterns}
        position: int = 0

        for char in text:
            while current_node is not None and char not in current_node.children:
                current_node = current_node.fail

            if current_node is None:
                current_node = self.trie.root
                position += 1
                continue

            current_node = current_node.children.get(char)
            
            if current_node:
                if current_node.end_of_word:
                    for pattern in current_node.output:
                        results[pattern]["count"] += 1
                        results[pattern]["positions"].append(position)

                temp_node = current_node.fail
                while temp_node is not None:
                    if temp_node.end_of_word:
                        for pattern in temp_node.output:
                            results[pattern]["count"] += 1
                            results[pattern]["positions"].append(position)
                    temp_node = temp_node.fail
            position += 1

        return results
