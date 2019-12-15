from source.jass.base.const import *
from source.jass.base.player_round_cheating import PlayerRound
from source.jass.base.player_round_cheating import PlayerRoundCheating
from source.jass.base.round_factory import get_round_from_player_round
import random


class Sampler:
    @staticmethod
    def sample(rnd: PlayerRound) -> PlayerRoundCheating:
        sampled_cards = np.ones(36, int)
        np.ma.masked_where(rnd.hand == 1, sampled_cards).filled(0)
        hands = np.zeros(shape=[4, 36], dtype=np.int)

        # give the own player the correct hand and the other players sampled hands
        for i in range(0, 4):
            if i == rnd.player:
                hands[i] = rnd.hand
            else:
                new_hands, sampled_cards = Sampler.__get_hands(sampled_cards)
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
