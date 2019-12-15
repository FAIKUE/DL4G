from source.jass.base.const import *
from source.jass.base.player_round import PlayerRound
from source.jass.base.round_factory import get_round_from_player_round
from source.jass.player.fabian_mcts.sampler import Sampler
from source.jass.player.fabian_mcts.node import Node
from source.jass.player.fabian_mcts.UCB import UCB
from source.jass.player.random_player_schieber import RandomPlayerSchieber
import time
from operator import attrgetter


class MCTS:
    @staticmethod
    def monte_carlo_tree_search(rnd: PlayerRound, run_time_seconds=2) -> (Node, int):
        end_time = time.time() + run_time_seconds

        sampled_round = Sampler.sample(rnd)
        root_node = Node()
        root_node.action.player_nr = rnd.player
        root_node.action.round = sampled_round

        simulated_rounds = 0
        while time.time() < end_time:
            promising_node = MCTS._select_promising_node(root_node)
            if promising_node.action.round.nr_cards_in_trick < 4:
                MCTS._expand_node(promising_node, sampled_round)

            node_to_explore = promising_node
            if len(promising_node.childs) > 0:
                node_to_explore = promising_node.get_random_child()

            win_score = MCTS._simulate_round(node_to_explore)
            MCTS._back_propagation(node_to_explore, sampled_round.player, win_score)
            simulated_rounds += 1

        winner = max(root_node.childs, key=attrgetter('action.visit_count'))

        #winner = root_node.get_child_with_max_visit_count()
        print(f"{simulated_rounds} rounds simulated in {run_time_seconds} seconds")
        print(f"winner: {winner.action.card} with visit count {winner.action.visit_count} ({round(winner.action.visit_count/simulated_rounds, 3)}), valid cards: {np.flatnonzero(sampled_round.get_valid_cards())}")
        return winner, simulated_rounds

    @staticmethod
    def _select_promising_node(root_node: Node) -> Node:
        node = root_node
        while len(node.childs) != 0:
            ucb = UCB()
            node = ucb.find_best_node_ucb(node)
        return node

    @staticmethod
    def _expand_node(node: Node, round: PlayerRound):
        valid_cards = np.flatnonzero(round.get_valid_cards())
        for card in valid_cards:
            new_node = Node()
            new_node.parent = node
            new_node.action.round = round
            new_node.action.player_nr = node.action.player_nr
            new_node.action.card = card
            node.add_child(new_node)

    @staticmethod
    def _simulate_round(node: Node) -> float:
        rnd = get_round_from_player_round(node.action.round, node.action.round.hands)
        player = rnd.player
        rnd.action_play_card(node.action.card)
        cards = rnd.nr_played_cards
        random_player = RandomPlayerSchieber()
        while cards < 36:
            player_rnd = PlayerRound()
            player_rnd.set_from_round(rnd)
            card_action = random_player.play_card(player_rnd)
            rnd.action_play_card(card_action)
            cards += 1

        max_points = rnd.points_team_0 + rnd.points_team_1
        my_points = rnd.get_points_for_player(player)
        enemy_points = max_points - my_points

        return (my_points - 0) / (max_points - 0)

    @staticmethod
    def _back_propagation(node: Node, player_nr: int, win_score: float):
        temp_node = node
        while temp_node:
            temp_node.action.increment_visit()
            if temp_node.action.player_nr == player_nr:
                temp_node.action.win_score = win_score
            temp_node = temp_node.parent
