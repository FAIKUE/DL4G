import math
import sys
from source.jass.player.fabian_mcts.node import Node


class UCB:
    def __init__(self, c=2) -> None:
        self.c = c

    def ucb_value(self, total_visits: int, node_win_score: float, node_visits: int) -> float:
        if node_visits == 0:
            return sys.maxsize
        ucb = (node_win_score / node_visits) + self.c * math.sqrt(math.log(total_visits, math.e) / node_visits)
        return ucb

    def find_best_node_ucb(self, node: Node):
        parent_visits = node.action.visit_count

        best_child = None
        best_score = 0.0
        for child in node.childs:  # type; State
            score = self.ucb_value(parent_visits, child.action.win_score, child.action.visit_count)
            if score >= best_score:
                best_child = child
                best_score = score

        if best_child is None:
            print("No best Children Found")

        # print(f" best child: {best_child.action.card}, best score: {best_score}")
        return best_child
