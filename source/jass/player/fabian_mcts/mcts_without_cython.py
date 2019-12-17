import math
import random
import time
import copy

from jass.base.const import *
from jass.base.player_round import PlayerRound
from jass.base.player_round_cheating import PlayerRoundCheating
from jass.base.round_factory import get_round_from_player_round
from jass.player.random_player_schieber import RandomPlayerSchieber


def monte_carlo_tree_search(rnd: PlayerRound, run_time_seconds=9000, c=1):
    start_time = time.time()
    end_time = start_time + run_time_seconds

    sampled_round = _sample(rnd)
    root_node = Node()
    root_node.player_nr = rnd.player
    root_node.round = sampled_round
    simulated_rounds = 0
    while time.time() < end_time:
        promising_node, depth = _select_promising_node(root_node, c)

        valid_cards = np.flatnonzero(promising_node.round.get_valid_cards())
        playable_cards = list(set(valid_cards) - set(promising_node.get_child_cards()))

        if playable_cards:
            card = np.random.choice(valid_cards)
            win, played_round = _simulate_round(sampled_round, card, (((depth + sampled_round.player) % 2) == 0))
            new_node = Node()
            new_node.parent = promising_node
            new_node.round = played_round
            new_node.player_nr = ((promising_node.player_nr + 1) % 4)
            new_node.card = card
            promising_node.add_child(new_node)
            _back_propagation(new_node, sampled_round.player, win)
        simulated_rounds += 1
    #winner = root_node.get_child_with_max_visit_count()
    #print(f"{simulated_rounds} rounds simulated in {run_time_seconds} seconds")
    #print(f"winner: {winner.card} with visit count {winner.visit_count} ({round(winner.visit_count/simulated_rounds, 3)}), valid cards: {np.flatnonzero(sampled_round.get_valid_cards())}")
    return root_node

def _select_promising_node(root_node, c):
    node = root_node
    depth = 0
    while len(node.childs) != 0:
        node = _find_best_node_ucb(node, c)
        depth += 1
    return node, depth

# def _expand_node(node: Node, round: PlayerRound, int depth):
#     valid_cards = np.flatnonzero(round.get_valid_cards())
#     cdef int card
#     for card in valid_cards:
#         new_node = Node()
#         new_node.parent = node
#         new_node.round = round
#         new_node.player_nr = ((depth + node.player_nr) % 4)
#         new_node.card = card
#         node.add_child(new_node)

def _simulate_round(round: PlayerRound, card, my_play: bool) -> (bool, PlayerRound):
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

    win = my_points > enemy_points and my_play
    return win, played_round

def _back_propagation(node, player_nr, win: bool):
    temp_node = node
    while temp_node:
        temp_node.increment_visit()
        if win:
            temp_node.win_count += 1
        else:
            temp_node.lose_count += 1
        temp_node = temp_node.parent

def _sample(rnd: PlayerRound) -> PlayerRoundCheating:
    sampled_cards = np.ones(36, int)
    np.ma.masked_where(rnd.hand == 1, sampled_cards).filled(0)
    hands = np.zeros(shape=[4, 36], dtype=np.int)

    # give the own player the correct hand and the other players sampled hands
    for i in range(0, 4):
        if i == rnd.player:
            hands[i] = rnd.hand
        else:
            new_hands, sampled_cards = __get_hands(sampled_cards)
            hands[i] = new_hands

    return get_round_from_player_round(rnd, hands)

def __get_hands(sampled_cards: np.array):
    one_hand = np.zeros(shape=36, dtype=int)
    for i in range(0, 9):
        card = random.choice(np.flatnonzero(sampled_cards))
        sampled_cards[card] = 0
        one_hand[card] = 1

    return one_hand, sampled_cards

def _ucb_value(total_visits, node_win_count, node_visits, c) -> float:
    if node_visits == 0:
        return 2147483647
    ucb = (node_win_count / node_visits) + c * math.sqrt(math.log(total_visits, math.e) / node_visits)
    return ucb

def _find_best_node_ucb(node, c):
    parent_visits = node.visit_count

    best_child = None
    best_score = -1.0
    for child in node.childs:  # type; State
        score = _ucb_value(parent_visits, child.win_count, child.visit_count, c)
        if score > best_score:
            best_child = child
            best_score = score

    if best_child is None:
        print("No best Children Found")

    # print(f" best child: {best_child.card}, best score: {best_score}")
    return best_child

class Node:
    def __init__(self) -> None:
        self.parent = None
        self.childs = []  # Node
        self.player_nr = 0
        self.win_score = 0.0
        self.win_count = 0
        self.lose_count = 0
        self.visit_count = 0
        self.round = None
        self.card = None

    def increment_visit(self):
        self.visit_count += 1

    def get_random_child(self) -> 'Node':
        return np.random.choice(self.childs)

    def add_child(self, node: 'Node'):
        self.childs.append(node)

    def get_child_with_max_score(self) -> 'Node':
        best_child = self.childs[0]
        for child in self.childs:
            if child.win_score > best_child.win_score:
                best_child = child
        return best_child

    def get_child_with_max_visit_count(self) -> 'Node':
        best_child = self.childs[0]
        for child in self.childs:
            if child.visit_count > best_child.visit_count:
                best_child = child
        return best_child

    def get_child_cards(self):
        child_cards = []
        for child in self.childs:
            child_cards.append(child.card)
        return child_cards
