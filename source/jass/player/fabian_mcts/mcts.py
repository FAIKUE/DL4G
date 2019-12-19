from jass.base.const import *
from jass.base.player_round import PlayerRound
from jass.base.round_factory import get_round_from_player_round
from jass.player.fabian_mcts.sampler import Sampler
from jass.player.fabian_mcts.node import Node
from jass.player.fabian_mcts.UCB import UCB
from jass.player.random_player_schieber import RandomPlayerSchieber
import time
import copy


class MCTS:
    @staticmethod
    def monte_carlo_tree_search(rnd: PlayerRound, run_time_seconds=9) -> (Node, int):
        end_time = time.time() + run_time_seconds

        sampled_round = Sampler.sample(rnd)
        root_node = Node()
        root_node.player_nr = rnd.player
        root_node.round = sampled_round
        simulated_rounds = 0

        while time.time() < end_time:
            promising_node, depth = MCTS._select_promising_node(root_node)
            valid_cards = np.flatnonzero(promising_node.round.get_valid_cards())

            for card in valid_cards:
                win, played_round = MCTS._simulate_round(sampled_round, card, (((depth + sampled_round.player) % 2) == 0))
                new_node = Node()
                new_node.parent = promising_node
                new_node.round = played_round
                new_node.player_nr = ((promising_node.player_nr + 1) % 4)
                new_node.card = card
                promising_node.add_child(new_node)
                MCTS._back_propagation(new_node, win)
            simulated_rounds += 1

        return root_node

    @staticmethod
    def _select_promising_node(root_node: Node) -> (Node, int):
        node = root_node
        depth = 0
        while len(node.childs) != 0:
            ucb = UCB()
            node = ucb.find_best_node_ucb(node)
            depth += 1
        return node, depth

    @staticmethod
    def _expand_node(node: Node, round: PlayerRound):
        valid_cards = np.flatnonzero(round.get_valid_cards())
        for card in valid_cards:
            new_node = Node()
            new_node.parent = node
            new_node.round = round
            new_node.player_nr = node.player_nr
            new_node.card = card
            node.add_child(new_node)

    @staticmethod
    def _simulate_round(round: PlayerRound, card, my_play) -> (bool, PlayerRound):
        rnd = get_round_from_player_round(round, round.hands)
        player = rnd.player
        rnd.action_play_card(card)
        played_round = copy.deepcopy(rnd)
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

        win = (my_points > enemy_points and my_play) or (enemy_points > my_points and not my_play)
        return win, played_round

    @staticmethod
    def _back_propagation(node: Node, win: bool):
        temp_node = node
        while temp_node:
            temp_node.increment_visit()
            if win:
                temp_node.win_count += 1
            else:
                temp_node.lose_count += 1
            temp_node = temp_node.parent
