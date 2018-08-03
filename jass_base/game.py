# HSLU
#
# Created by Thomas Koller on 07.12.17


"""
Classes for implementing the logic of jass_base games.
"""

from jass_base.game_const import *


class Round:
    """
    Class for one round (game) of jass_base.
    """

    def __init__(self) -> None:
        self.tricks = []                # type: List[Trick]
        self.current_trick = None       # type: Trick  # an incomplete trick, i.e. len(current_trick.cards) < 4
        self.played_cards = None        # type: np.array
        self.current_hand = None        # type: np.array  # 1-hot encoded np.array of size 36
        self.trump = None               # type: int
        self.forehand = True
        self.dealer = None              # type: int
        self.declared_trump = None      # type: int
        self.points_team_0 = 0          # points made by the team of jass_players 0 and 2
        self.points_team_1 = 0          # points made by the team of jass_players 1 and 3

    def add_trick(self, trick: 'Trick') -> None:
        self.tricks.append(trick)

    def calc_hands(self) -> None:
        """
        Calculate the played_cards from the available tricks and the points made from the completed tricks
        """
        self.played_cards = np.zeros([4, 36], np.int32)
        for trick in self.tricks:
            self.played_cards += trick.get_cards_enc_player()
            if trick.winner == 0 or trick.winner == 2:
                self.points_team_0 += trick.points
            else:
                self.points_team_1 += trick.points


class Trick:
    """
    A trick in a game.
    """

    def __init__(self, first_player: int = 0) -> None:
        # player that played the first card
        self.first_player = first_player
        self.winner = 0
        self.points = 0
        self.is_last = False                # true if last trick in the round

        # indexes of cards played in order that they have been played
        self._cards = []

    @property
    def cards(self) -> np.array:
        return self._cards

    @cards.setter
    def cards(self, cards: np.array):
        self._cards = cards

    def get_cards_enc(self) -> np.ndarray:
        """
        Get the cards 1-hot encoded
        Returns:
            1-hot encoded array of cards from this trick
        """
        result = np.zeros(36, np.int32)
        result[self.cards] = 1
        return result

    def get_cards_enc_player(self) -> np.ndarray:
        """
        Get the cards as 2-dim array result, so that result[p, c] == 1 <=> player p played card c in this trick

        Returns:
            numpy array
        """
        result = np.zeros([4,36], np.int32)
        player = self.first_player

        for i in range(4):
            result[player, self.cards[i]] = 1
            player = next_player[player]

        return result

    def calc_points(self, trump: int) -> None:
        """
        Calculate the points from the cards according to the given trump

        Args:
            trump: the trump color, as it is not contained in the tricks
        """
        self.points = np.sum(card_values[trump, self.cards]) + \
                      (5 if self.is_last else 0)

    def calc_winner(self, trump: int) -> int:
        """
        Calculates the winner of a complete trick.
        NOTE:
            - Callers must only call this method if the trick is complete.
            - The attribute self.winner is set to the calculated winner.

        Args:
            trump: the trump color

        Returns:
            the player who won this trick
        """
        assert DIAMONDS <= trump <= UNE_UFE
        assert len(self._cards) == 4

        enc_cards = self.get_cards_enc()
        first_color = color_of_card[self._cards[0]]
        enc_same_color_cards = enc_cards * color_masks[first_color, :]
        same_color_cards = np.flatnonzero(enc_same_color_cards)

        # Note that the cards are integers, numbered per color, in ascending order
        # starting with the ace. This means that the card with the lowest integer
        # value of a color is the highest in order.
        #
        # Exception: if trump == UNE_UFE, then its the other way around.

        if trump == OBE_ABE:
            winner_card = np.min(same_color_cards)
        elif trump == UNE_UFE:
            winner_card = np.max(same_color_cards)
        else:
            enc_trump_cards = enc_cards * color_masks[trump]
            trump_cards = np.flatnonzero(enc_trump_cards)

            # Special cases are 'J' and '9' of the trump color.
            trump_jack = trump * 9 + J_offset
            trump_nine = trump * 9 + Nine_offset

            if trump_jack in self._cards:
                winner_card = trump_jack
            elif trump_nine in self._cards:
                winner_card = trump_nine
            else:
                winner_card = np.min(trump_cards) if trump_cards.size > 0 else np.min(same_color_cards)

        winner_index = self._cards.tolist().index(winner_card)

        self.winner = (self.first_player - winner_index) % 4
        return self.winner
