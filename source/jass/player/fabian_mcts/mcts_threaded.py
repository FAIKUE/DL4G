from threading import Thread
from jass.player.fabian_mcts.mcts import MCTS
from operator import attrgetter

class MCTSThreaded:
    def __init__(self, player_rnd, thread_count=4):
        self.player_rnd = player_rnd
        self.thread_count = thread_count
        self.winners = []

    def run(self):
        threads = []
        for i in range(0, self.thread_count):
            thread = Thread(target=self._call_mcts)
            thread.start()
            threads.append(thread)

        # We now pause execution on the main thread by 'joining' all of our started threads.
        # This ensures that each has finished processing the urls.

        for process in threads:
            process.join()

        simulated_rounds = 0
        best_winner = None
        best_score = 0
        for winner in self.winners:
            score = winner[0].action.visit_count / winner[1]
            simulated_rounds += winner[1]
            if score > best_score:
                best_score = score
                best_winner = winner

        print(f"winner from all threads: {best_winner[0].action.card} after {simulated_rounds} rounds of sampling")
        return best_winner[0].action.card

    def _call_mcts(self):
        self.winners.append(MCTS.monte_carlo_tree_search(self.player_rnd))