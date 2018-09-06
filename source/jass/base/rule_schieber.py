# HSLU
#
# Created by Thomas Koller on 31.12.17

""" Implementation of rules of jass game"""

from jass.base.const import *
from jass.base.rule import Rule


class RuleSchieber(Rule):
    """
    Class for implementing rules of the jass game for the variation for 'Schieber'. These are:
    - The game is played with trump

    """

    def get_valid_cards(self, hand: np.array, current_trick: np.ndarray or list, move_nr: int, trump: int or None) -> np.array:
        """
        Get the valid cards that can be played by the current player. (It is implemented as one long function
        in order to take advantage of intermediate results of calculation.)

        Args:
            hand: one-hot encoded array of hands owned by the player
            current_trick: array with the indices of the cards for the previous moves in the current trick
            move_nr: which move the player has to make in the current trick, 0 for first move, 1 for second and so on
            trump: trump color (or 'obe', 'une')

        Returns:
            one-hot encoded array of valid moves
        """
        # play anything on the first move
        if move_nr == 0:
            return hand

        # get the color of the first played card and check if we have that color
        color_played = color_of_card[current_trick[0]]
        have_color_played = (np.sum(hand * color_masks[color_played, :]) > 0)

        if trump >= 4:
            # obe or une declared
            if have_color_played:
                # must give the correct color
                return hand * color_masks[color_played, :]
            else:
                # play anything, if we don't have the color
                return hand
        else:
            #
            # round with trumps declared (not 'obe' or 'une')
            #

            # check number of trumps we have and number of cards left, in order to simplify some of the conditions
            number_of_trumps = np.sum(hand * color_masks[trump, :])
            number_of_cards = np.sum(hand)

            #
            # the played color was trump
            #
            if color_played == trump:
                if number_of_trumps == 0:
                    # no more trumps, play anything
                    return hand
                elif number_of_trumps == 1:
                    if hand[trump * 9 + J_offset]:
                        # we have only trump jack, so we can play anything
                        return hand
                    else:
                        # we have just one trump and must play it
                        return hand * color_masks[trump, :]
                else:
                    # we have more than one trump, so we must play one of them
                    return hand * color_masks[trump, :]
            #
            # the played color was not trump
            #
            else:
                # check if anybody else (player 1 or player 2) played a trump, and if yes how high
                lowest_trump_played = None
                trump_played = False

                if move_nr > 1:
                    # check player 1
                    if color_of_card[current_trick[1]] == trump:
                        trump_played = True
                        lowest_trump_played = current_trick[1]
                    # check player 2
                    if move_nr == 3:
                        if color_of_card[current_trick[2]] == trump:
                            trump_played = True
                            if lowest_trump_played is not None:
                                # 2 trumps were played, so we must compare
                                if lowest_trump_played < current_trick[2]:
                                    # move from player 2 is lower (as its index value is higher)
                                    lowest_trump_played = current_trick[2]
                            else:
                                # this is the only trump played, so it is the lowest
                                lowest_trump_played = current_trick[2]

                #
                # nobody played a trump, so we do not need to consider any restrictions on playing trump ourselves
                #
                if not trump_played:
                    if have_color_played:
                        # must give a color or can give any trump
                        color_cards = hand * color_masks[color_played, :]
                        trump_cards = hand * color_masks[trump, :]
                        return color_cards + trump_cards
                    else:
                        # we do not have the color, so we can play anything, including any trump
                        return hand

                #
                # somebody played a trump, so we have the restriction that we can not play a lower trump, with
                # the exception if we only have trump left
                #
                else:
                    if number_of_trumps == number_of_cards:
                        # we have only trump left, so we can give any of them
                        return hand
                    else:
                        #
                        # find the valid trumps to play
                        #

                        # all trumps in hand
                        trump_cards = hand * color_masks[trump, :]

                        # higher trump cards in hand
                        higher_trump_cards = trump_cards * higher_trump[lowest_trump_played, :]

                        # lower trump cards in hand
                        lower_trump_cards = trump_cards * lower_trump[lowest_trump_played, :]

                    if have_color_played:
                        # must give a color or a higher trump
                        color_cards = hand * color_masks[color_played, :]
                        return color_cards + higher_trump_cards
                    else:
                        # play anything except a lower trump
                        not_lower_trump_cards = 1 - lower_trump_cards
                        return hand * not_lower_trump_cards

    def calc_points(self, trick: np.ndarray, is_last: bool, trump: int = -1) -> int:
        """
        Calculate the points from the cards in the trick according to the given trump

        Args:
            trick: the trick
            is_last: true if this is the last trick
            trump: trump for the round
        """
        return int(np.sum(card_values[trump, trick])) + (5 if is_last else 0)

    def calc_winner(self, trick: np.ndarray, first_player: int, trump: int = -1) -> int:
        """
        Calculate the winner of a completed trick.

        Second implementation in an attempt to be more efficient, while the implementation is somewhat longer
        and more complicated it is about 3 times faster than the previous method.

        Precondition:
            0 <= trick[i] <= 35, for i = 0..3
        Args:
            trick: the completed trick
            first_player: the first player of the trick
            trump: trump for the round
        Returns:
            the player who won this trick
        """
        color_of_first_card = color_of_card[trick[0]]
        if trump == UNE_UFE:
            # lowest card of first color wins
            winner = 0
            lowest_card = trick[0]
            for i in range(1, 4):
                # (lower card values have a higher card index)
                if color_of_card[trick[i]] == color_of_first_card and trick[i] > lowest_card:
                    lowest_card = trick[i]
                    winner = i
        elif trump == OBE_ABE:
            # highest card of first color wins
            winner = 0
            highest_card = trick[0]
            for i in range(1, 4):
                if color_of_card[trick[i]] == color_of_first_card and trick[i] < highest_card:
                    highest_card = trick[i]
                    winner = i
        elif color_of_first_card == trump:
            # trump mode and first card is trump: highest trump wins
            winner = 0
            highest_card = trick[0]
            for i in range(1, 4):
                # lower_trump[i,j] checks if j is a lower trump than i
                if color_of_card[trick[i]] == trump and lower_trump[trick[i], highest_card]:
                    highest_card = trick[i]
                    winner = i
        else:
            # trump mode, but different color played on first move, so we have to check for higher cards until
            # a trump is played, and then for the highest trump
            winner = 0
            highest_card = trick[0]
            trump_played = False
            trump_card = None
            for i in range(1, 4):
                if color_of_card[trick[i]] == trump:
                    if trump_played:
                        # second trump, check if it is higher
                        if lower_trump[trick[i], trump_card]:
                            winner = i
                            trump_card = trick[i]
                    else:
                        # first trump played
                        trump_played = True
                        trump_card = trick[i]
                        winner = i
                elif trump_played:
                    # color played is not trump, but trump has been played, so ignore this card
                    pass
                elif color_of_card[trick[i]] == color_of_first_card:
                    # trump has not been played and this is the same color as the first card played
                    # so check if it is higher
                    if trick[i] < highest_card:
                        highest_card = trick[i]
                        winner = i
        # adjust actual winner by first player
        return (first_player - winner) % 4

