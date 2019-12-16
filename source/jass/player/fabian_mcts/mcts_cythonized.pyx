import math
import random
import sys

from jass.base.const import *
from jass.base.player_round import PlayerRound
from jass.base.player_round_cheating import PlayerRoundCheating
from jass.base.round_factory import get_round_from_player_round
from jass.player.fabian_mcts.node import Node
from jass.player.random_player_schieber import RandomPlayerSchieber
import time
from operator import attrgetter


class MctsCythonized:
    @staticmethod
    def monte_carlo_tree_search(rnd: PlayerRound, run_time_seconds=9) -> (Node, int):
        end_time = time.time() + run_time_seconds

        sampled_round = MctsCythonized._sample(rnd)
        root_node = Node()
        root_node.action.player_nr = rnd.player
        root_node.action.round = sampled_round

        simulated_rounds = 0
        while time.time() < end_time:
            promising_node = MctsCythonized._select_promising_node(root_node)
            if promising_node.action.round.nr_cards_in_trick < 4:
                MctsCythonized._expand_node(promising_node, sampled_round)

            node_to_explore = promising_node
            if len(promising_node.childs) > 0:
                node_to_explore = promising_node.get_random_child()

            win_score = MctsCythonized._simulate_round(node_to_explore)
            MctsCythonized._back_propagation(node_to_explore, sampled_round.player, win_score)
            simulated_rounds += 1

        winner = max(root_node.childs, key=attrgetter('action.visit_count'))

        #winner = root_node.get_child_with_max_visit_count()
        print(f"{simulated_rounds} rounds simulated in {run_time_seconds} seconds")
        print(f"winner: {winner.action.card} with visit count {winner.action.visit_count} ({round(winner.action.visit_count/simulated_rounds, 3)}), valid cards: {np.flatnonzero(sampled_round.get_valid_cards())}")
        return root_node

    @staticmethod
    def _select_promising_node(root_node: Node) -> Node:
        node = root_node
        while len(node.childs) != 0:
            node = MctsCythonized._find_best_node_ucb(node)
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

        return my_points > enemy_points

    @staticmethod
    def _back_propagation(node: Node, player_nr: int, win: bool):
        temp_node = node
        while temp_node:
            temp_node.action.increment_visit()
            if temp_node.action.player_nr == player_nr:
                if win:
                    temp_node.action.win_count += 1
                else:
                    temp_node.action.lose_count += 1
            temp_node = temp_node.parent

    @staticmethod
    def _sample(rnd: PlayerRound) -> PlayerRoundCheating:
        sampled_cards = np.ones(36, int)
        np.ma.masked_where(rnd.hand == 1, sampled_cards).filled(0)
        hands = np.zeros(shape=[4, 36], dtype=np.int)

        # give the own player the correct hand and the other players sampled hands
        for i in range(0, 4):
            if i == rnd.player:
                hands[i] = rnd.hand
            else:
                new_hands, sampled_cards = MctsCythonized.__get_hands(sampled_cards)
                hands[i] = new_hands

        return get_round_from_player_round(rnd, hands)

    @staticmethod
    def __get_hands(sampled_cards: np.array):
        one_hand = np.zeros(shape=36, dtype=int)
        for i in range(0, 9):
            card = random.choice(np.flatnonzero(sampled_cards))
            sampled_cards[card] = 0
            one_hand[card] = 1

        return one_hand, sampled_cards

    @staticmethod
    def _find_best_node_ucb(self, node: Node, c=1):
        parent_visits = node.action.visit_count

        best_child = None
        best_score = 0.0
        for child in node.childs:  # type; State
            score = MctsCythonized._ucb_value(parent_visits, child.action.win_count, child.action.visit_count, c)
            if score >= best_score:
                best_child = child
                best_score = score

        if best_child is None:
            print("No best Children Found")

        # print(f" best child: {best_child.action.card}, best score: {best_score}")
        return best_child

    @staticmethod
    def _ucb_value(self, total_visits: int, node_win_count: float, node_visits: int, c) -> float:
        if node_visits == 0:
            return sys.maxsize
        ucb = (node_win_count / node_visits) + c * math.sqrt(math.log(total_visits, math.e) / node_visits)
        return ucb