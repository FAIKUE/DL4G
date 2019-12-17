from jass.base.const import *
from jass.base.player_round import PlayerRound
from jass.player.player import Player
from jass.base.rule_schieber import RuleSchieber
from jass.player.fabian_mcts.mcts import MCTS
from jass.player.fabian_mcts.mcts_threaded import MCTSThreaded
import logging


class FabianMCTSPlayer(Player):
    """
    Implementation of a player to play Jass using Monte Carlo Tree Search.
    """

    def __init__(self, ucb_c=1, threads=10):
        self._logger = logging.getLogger(__name__)
        self._rule = RuleSchieber()
        self.ucb_c = ucb_c
        self.threads = threads

    def select_trump(self, rnd: PlayerRound) -> int:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump
        """

        # select the trump with best score according to jass experience
        high_cards = []

        for i in range(4):
            for j in range(i * 9, i * 9 + 5):
                high_cards.append(j)

        best_trump = 0
        max_points_in_trump = 0
        max_score_in_trump = 0

        for trump in trump_ints:
            score_in_trump = 0

            if trump < OBE_ABE:
                cards_of_this_color = convert_one_hot_encoded_cards_to_int_encoded_list(np.split(rnd.hand, 4)[trump])
                cards_of_other_colors = [card for card in convert_one_hot_encoded_cards_to_int_encoded_list(rnd.hand) if card not in convert_one_hot_encoded_cards_to_int_encoded_list(rnd.hand * color_masks[trump])]

                has_bauer = J_offset in cards_of_this_color
                has_ass = A_offset in cards_of_this_color
                has_naell = Nine_offset in cards_of_this_color

                if has_bauer and len(cards_of_this_color) >= 4:
                    temp_score_in_trump = 50 + len(cards_of_this_color) - 4
                    print(f"bauer und andere karten der farbe with score {temp_score_in_trump}")
                    if temp_score_in_trump > score_in_trump:
                        score_in_trump = temp_score_in_trump
                elif has_ass and has_naell and len(cards_of_this_color) >= 5:
                    temp_score_in_trump = 50 + len(cards_of_this_color) - 5
                    print(f"ass und näll und andere karten der farbe with score {temp_score_in_trump}")
                    if temp_score_in_trump > score_in_trump:
                        score_in_trump = temp_score_in_trump
                elif has_ass and has_naell and has_bauer:
                    temp_score_in_trump = 50 + len(cards_of_this_color) - 3
                    print(f"ass und näll und bauer with score {temp_score_in_trump}")
                    if temp_score_in_trump > score_in_trump:
                        score_in_trump = temp_score_in_trump
                elif has_bauer and has_naell and len(cards_of_this_color) >= 3 and rnd.hand[DA] + rnd.hand[HA] + rnd.hand[SA] + rnd.hand[CA] >= 2:
                    temp_score_in_trump = 40 + len(cards_of_this_color) - 3 + rnd.hand[DA] + rnd.hand[HA] + rnd.hand[SA] + rnd.hand[CA] - 2
                    print(f"bauer und näll und andere karten der farbe und andere asse with score {temp_score_in_trump}")
                    if temp_score_in_trump > score_in_trump:
                        score_in_trump = temp_score_in_trump
                elif has_bauer and has_naell and len(cards_of_this_color) >= 3 and len([i for i in cards_of_other_colors if i in high_cards]) >= 4:
                    temp_score_in_trump = 40 + len(cards_of_this_color) - 3 + len([i for i in cards_of_other_colors if i in high_cards]) - 4
                    print(f"bauer und näll und andere karten der farbe und andere gute karten with score {temp_score_in_trump}")
                    if temp_score_in_trump > score_in_trump:
                        score_in_trump = temp_score_in_trump
                else:
                    points_in_trump = (rnd.hand * card_values[trump]).sum()
                    if points_in_trump > max_points_in_trump:
                        max_points_in_trump = points_in_trump
                        best_trump = trump
            elif trump == OBE_ABE:
                high_cards_i_have = [i for i in high_cards if
                                     i in convert_one_hot_encoded_cards_to_int_encoded_list(rnd.hand)]

                if len(high_cards_i_have) > 5:
                    temp_score_in_trump = 50 + len(high_cards_i_have) - 6
                    print(f"hohe karten with score {temp_score_in_trump}")
                    if temp_score_in_trump > score_in_trump:
                        score_in_trump = temp_score_in_trump
            else:
                low_cards = []
                for i in range(0, 4):
                    for j in range(i * 9 + 4, i * 9 + 9):
                        low_cards.append(j)

                low_cards_i_have = [i for i in low_cards if
                                    i in convert_one_hot_encoded_cards_to_int_encoded_list(rnd.hand)]

                if len(low_cards_i_have) > 5:
                    temp_score_in_trump = 50 + len(low_cards_i_have) - 6
                    print(f"tiefe karten with score {temp_score_in_trump}")
                    if temp_score_in_trump > score_in_trump:
                        score_in_trump = temp_score_in_trump

            if score_in_trump > max_score_in_trump:
                max_score_in_trump = score_in_trump
                best_trump = trump
        if max_score_in_trump == 0 and rnd.forehand is None:
            best_trump = PUSH
            print(f"Pushed trump selection to other player "
                  f"with {max_points_in_trump} points in the cards for the best trump")
        else:
            print(f"Selected trump {trump_strings_german_long[best_trump]} with score {max_score_in_trump} and {max_points_in_trump} points in the cards. hand: {rnd.hand}")
        return best_trump

    def play_card(self, player_rnd: PlayerRound) -> int:
        """
        Player returns a card to play based on the given round information.

        Args:
            player_rnd: current round

        Returns:
            card to play, int encoded
        """
        #best_card = MCTS.monte_carlo_tree_search(player_rnd)
        valid_cards = np.flatnonzero(player_rnd.get_valid_cards())
        print(f"valid cards: {valid_cards}, standard probability: {1/len(valid_cards)}")
        if len(valid_cards) == 1:
            return valid_cards[0]

        mcts_threaded = MCTSThreaded(player_rnd, self.threads, self.ucb_c)
        best_card = mcts_threaded.run()

        return best_card
