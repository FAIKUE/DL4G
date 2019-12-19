import numpy as np


class Node:
    def __init__(self) -> None:
        self.parent = None
        self.childs = []  # Node
        self.player_nr = 0
        self.win_score = 0.0
        self.win_count = 0
        self.lose_count = 0
        self.visit_count = 0
        self.round = None
        self.card = None

    def increment_visit(self):
        self.visit_count += 1

    def get_random_child(self) -> 'Node':
        return np.random.choice(self.childs)

    def add_child(self, node: 'Node'):
        self.childs.append(node)

    def get_child_with_max_score(self) -> 'Node':
        best_child = self.childs[0]
        for child in self.childs:
            if child.win_score > best_child.win_score:
                best_child = child
        return best_child

    def get_child_with_max_visit_count(self) -> 'Node':
        best_child = self.childs[0]
        for child in self.childs:
            if child.visit_count > best_child.visit_count:
                best_child = child
        return best_child

    def get_child_cards(self):
        child_cards = []
        for child in self.childs:
            child_cards.append(child.card)
        return child_cards

