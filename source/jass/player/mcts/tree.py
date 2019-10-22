from jass.player.mcts.node import Node


class Tree:
    def __init__(self) -> None:
        self._root_node = Node()

    def get_root_node(self) -> Node:
        return self._root_node
