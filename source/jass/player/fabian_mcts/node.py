import numpy as np
from source.jass.player.fabian_mcts.action import Action


class Node:
    def __init__(self) -> None:
        self.parent = None
        self.action = Action()
        self.childs = []  # Node

    def get_random_child(self) -> 'Node':
        return np.random.choice(self.childs)

    def add_child(self, node: 'Node'):
        self.childs.append(node)

    def get_child_with_max_score(self) -> 'Node':
        best_child = self.childs[0]
        for child in self.childs:
            if child.action.win_score > best_child.action.win_score:
                best_child = child
        return best_child

    def get_child_with_max_visit_count(self) -> 'Node':
        best_child = self.childs[0]
        for child in self.childs:
            if child.action.visit_count > best_child.action.visit_count:
                best_child = child
        return best_child
