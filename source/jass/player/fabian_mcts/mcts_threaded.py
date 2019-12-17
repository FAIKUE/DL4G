from threading import Thread
from jass.player.fabian_mcts.mcts import MCTS
from operator import itemgetter
from jass.player.fabian_mcts import mcts_cythonized
from jass.player.fabian_mcts import mcts_without_cython


class MCTSThreaded:
    def __init__(self, player_rnd, thread_count=10, ucb_c=1):
        self.simulated_rounds = 0
        self.player_rnd = player_rnd
        self.thread_count = thread_count
        self.winners = []
        self.ucb_c = ucb_c

    def run(self):
        threads = []
        for i in range(0, self.thread_count):
            thread = Thread(target=self._call_mcts)
            thread.start()
            threads.append(thread)
        for process in threads:
            process.join()

        result_list = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0,
                       15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0,
                       29: 0, 30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0}
        for card in self.winners:
            result_list[card.card] += card.visit_count

        winner = max(result_list.items(), key=itemgetter(1))

        print(f"winner from all threads: {winner[0]} with visit_count {winner[1]} ({winner[1]/self.simulated_rounds}) after {self.simulated_rounds} rounds of sampling")
        print(f"all options: {result_list}")
        return winner[0]

    def _call_mcts(self):
        #root_node = mcts_without_cython.monte_carlo_tree_search(self.player_rnd, 9, 1)
        root_node = mcts_cythonized.monte_carlo_tree_search(self.player_rnd, 9, self.ucb_c)
        #root_node = MCTS.monte_carlo_tree_search(self.player_rnd)
        self.simulated_rounds += root_node.visit_count
        for card in root_node.childs:
            self.winners.append(card)