import math
import sys
from jass.player.fabian_mcts.node import Node


class UCB:
    def __init__(self, c=1) -> None:
        self.c = c

    def ucb_value(self, total_visits: int, node_win_count: float, node_visits: int) -> float:
        if node_visits == 0:
            return sys.maxsize
        ucb = (node_win_count / node_visits) + self.c * math.sqrt(math.log(total_visits, math.e) / node_visits)
        return ucb

    def find_best_node_ucb(self, node: Node):
        parent_visits = node.visit_count

        best_child = None
        best_score = -1.0
        for child in node.childs:  # type; State
            score = self.ucb_value(parent_visits, child.win_count, child.visit_count)
            if score > best_score:
                best_child = child
                best_score = score

        if best_child is None:
            print("No best Children Found")

        # print(f" best child: {best_child.card}, best score: {best_score}")
        return best_child
