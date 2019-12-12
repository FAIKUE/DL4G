import math
import sys
from jass.player.mcts.node import Node
import logging
import random

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('MyLogger')


class UCB:
    def __init__(self, c=1) -> None:
        self._c = c

    def ucb_value(self, total_visits: int, node_win_score: float, node_visit: int) -> float:
        if node_visit == 0:
            return sys.maxsize

        return (node_win_score / node_visit) + self._c * math.sqrt(math.log(total_visits, math.e) / node_visit)

    def find_best_node_ucb(self, node: Node):
        parentVisit = node.getAction().getVisitCount()

        bestchildren = []
        bestScore = 0.0
        for c in node.getChilds():  # type; State
            score = self.ucb_value(parentVisit, c.getAction().getWinScore(), c.getAction().getVisitCount())
            if score == bestScore:
                bestchildren.append(c)

            if score > bestScore:
                bestchildren = [c]
                bestScore = score

        if len(bestchildren) == 0:
            logger.warning("No best Children Found")

        return random.choice(bestchildren)
