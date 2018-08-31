# HSLU
#
# Created by Thomas Koller on 09.12.17

"""
Calculate statistics of trumps in games
"""

from jass.base.round import Round
from jass.base.const import *


class TrumpStat:
    """
    Statistics of features of a hand when declaring a trump. The class calculates if the cards match the features
    and then increment the counters of forehand (Vorhand) or rearhand (geschoben). The positive counters are
    incremented when the statistics match, and the player chooses trump according to the statistics, the negative
    counters are incremented, when the statistics match, but the player chooses something else as trump.
    """
    def __init__(self):
        self.description = 'No stat'
        #
        # number of times for forehand (or first options)
        self.counter_pos_forehand = 0
        self.counter_neg_forehand = 0
        # number of times for rearhand (geschoben)
        self.counter_pos_rearhand = 0
        self.counter_neg_rearhand = 0
        # total number of rounds that were submitted for examination, and total number of matches
        self.counter_total = 0
        self.counter_total_match = 0

    def add_round(self, r: Round):
        """
        Add a round and calculate the statistics of it. If the trump declaration was passed from forehand to
        backhand, the statistics is updated for both hands
        Args:
            r: the round
        """
        if r.forehand:
            self.add_hand(r.hands[r.declared_trump, :], r.trump, True)
        else:
            # add forehand action
            player_hand = r.hands[partner_player[r.declared_trump], :]
            self.add_hand(player_hand, PUSH, True)
            # add rearhand action
            player_hand = r.hands[r.declared_trump, :]
            self.add_hand(player_hand, r.trump, False)

    def add_hand(self, hand, trump, forehand):
        """
        Add a hand and calculate statistics from it
        Args:
            hand: hand of the player
            trump: declared trump action
            forehand:
        """
        self.counter_total += 1
        if self._match_positive(hand, trump):
            self.counter_total_match += 1
            if forehand:
                self.counter_pos_forehand += 1
            else:
                self.counter_pos_rearhand += 1
        else:
            if self._match_negative(hand, trump):
                self.counter_total_match += 1
                if forehand:
                    self.counter_neg_forehand += 1
                else:
                    self.counter_neg_rearhand += 1

    def _match_positive(self, hands: np.ndarray, trump: int):
        pass

    def _match_negative(self, hands: np.ndarray, trump: int):
        pass

    def _match_other_trumps_from_positive(self, hands: np.ndarray, trump: int):
        # helper function to calculate negative matches, by checking if any of the other trumps match the positive
        # criteria
        for t in range(4):
            if t == trump:
                continue
            if self._match_positive(hands, t):
                return True
        return False

    # some helper methods for calculations
    @staticmethod
    def _number_of_trumps(hands: np.ndarray, trump: int):
        if trump > 3:
            return 0
        else:
            return np.sum(hands[trump*9:(trump+1)*9])

    @staticmethod
    def _has_trump_jack(hands: np.ndarray, trump: int):
        return trump <= 3 and hands[trump*9+J_offset] == 1

    @staticmethod
    def _has_trump_nine(hands: np.ndarray, trump: int):
        return trump <= 3 and hands[trump * 9 + Nine_offset] == 1

    @staticmethod
    def _number_of_aces(hands: np.ndarray):
        return np.sum(hands[[DA, HA, SA, CA]])


class AllStat:
    """
    Calculate all the statistics of the supplied statistic classes
    """
    def __init__(self):
        self.stat = []

    def add_statistic(self, statistic: TrumpStat):
        self.stat.append(statistic)

    def add_round(self, r: Round):
        for s in self.stat:
            s.add_round(r)

    def add_hand(self, hand, trump, forehand):
        for s in self.stat:
            s.add_hand(hand, trump, forehand)

    def get_statistics(self):
        result = {}

        for s in self.stat:
            percentage_forehand = s.counter_pos_forehand / (s.counter_pos_forehand + s.counter_neg_forehand)
            percentage_rearhand = s.counter_pos_rearhand / (s.counter_pos_rearhand + s.counter_neg_rearhand)
            percentage_match = s.counter_total_match / s.counter_total
            entry = {'forehand': percentage_forehand,
                     'rearhand': percentage_rearhand,
                     'matches': percentage_match}
            result[s.description] = entry

        return result


class JackNine5orMoreStat(TrumpStat):
    def __init__(self):
        super().__init__()
        self.description = "Jack, Nine, 5 trumps"

    def _match_positive(self, hands: np.ndarray, trump: int):
        return self._number_of_trumps(hands, trump) >= 5 and \
               self._has_trump_jack(hands, trump) and \
               self._has_trump_nine(hands, trump)

    def _match_negative(self, hands: np.ndarray, trump: int):
        return self._match_other_trumps_from_positive(hands, trump)


class JackNine4(TrumpStat):
    def __init__(self):
        super().__init__()
        self.description = "Jack, Nine, 4 trumps"

    def _match_positive(self, hands: np.ndarray, trump: int):
        return self._number_of_trumps(hands, trump) == 4 and \
               self._has_trump_jack(hands, trump) and \
               self._has_trump_nine(hands, trump)

    def _match_negative(self, hands: np.ndarray, trump: int):
        return self._match_other_trumps_from_positive(hands, trump)


class JackNine3(TrumpStat):
    def __init__(self):
        super().__init__()
        self.description = "Jack, Nine, 3 trumps"

    def _match_positive(self, hands: np.ndarray, trump: int):
        return self._number_of_trumps(hands, trump) == 3 and \
               self._has_trump_jack(hands, trump) and \
               self._has_trump_nine(hands, trump)

    def _match_negative(self, hands: np.ndarray, trump: int):
        return self._match_other_trumps_from_positive(hands, trump)


class Aces4(TrumpStat):
    def __init__(self):
        super().__init__()
        self.description = "Obe, 4 aces"

    def _match_positive(self, hands: np.ndarray, trump: int):
        return self._number_of_aces(hands) == 4 and trump == OBE_ABE

    def _match_negative(self, hands: np.ndarray, trump: int):
        return self._number_of_aces(hands) == 4 and trump != OBE_ABE



