from source.jass.base.const import *
from source.jass.base.player_round_cheating import PlayerRound
from source.jass.base.player_round_cheating import PlayerRoundCheating
from source.jass.base.round_factory import get_round_from_player_round
import random


class Sampler:

    @staticmethod
    def sample(rnd: PlayerRound) -> PlayerRoundCheating:
        sampledCards = np.ones(36, int)
        np.ma.masked_where(rnd.hand == 1, sampledCards).filled(0)
        hands = np.zeros(shape=[4, 36], dtype=np.int)

        # Komischerweise spielt er mit random hands besser
        hands1, sampledCards = Sampler.__get_hands(sampledCards)

        hands2, sampledCards = Sampler.__get_hands(sampledCards)

        hands3, sampledCards = Sampler.__get_hands(sampledCards)

        players = list(range(0, 4))
        players.remove(rnd.player)
        hands[rnd.player] = rnd.hand

        hands[players[0]] = hands1
        hands[players[1]] = hands2
        hands[players[2]] = hands3

        # anhand des Spielers die hand richtig setzen
        # for j in range(0,4):
        #     if j == rnd.player:
        #         hands[j] = rnd.hand
        #     else:
        #         hands1, sampledCards = Sampler.__get_hands(sampledCards)
        #         hands[j] = hands1

        return get_round_from_player_round(rnd, hands)

    @staticmethod
    def __get_hands(sampled_cards: np.array):
        one_hand = np.zeros(shape=36, dtype=int)
        for i in range(0, 9):
            card = random.choice(np.flatnonzero(sampled_cards))
            sampled_cards[card] = 0
            one_hand[card] = 1

        return one_hand, sampled_cards
