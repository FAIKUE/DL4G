# HSLU
#
# Created by Thomas Koller on 05.09.2018

import numpy as np
from source.jass.base.const import color_of_card, color_masks, HEARTS, SQ
from source.jass.base.rule import Rule


class RuleHearts(Rule):
    """
    Class for implementing rules of the jass game for hearts. The rules are as follows:
    - The winner of a trick is determined by the basic jass rules without trump, i.e. like "obe"
    - Each heart card gives a penalty of 1 point.
    - The SQ card gives a penalty of 9 points.
    - The valid cards are determined like in 'obe', i.e. you have to give the same color as the color of the first
    card if you have this color
    """

    def get_valid_cards(self, hand: np.array,
                        current_trick: np.ndarray or list,
                        move_nr: int,
                        trump: int or None) -> np.array:
        """
        Get the valid cards that can be played by the current player.

        Args:
            hand: one-hot encoded array of hands owned by the player
            current_trick: array with the indices of the cards for the previous moves in the current trick
            move_nr: which move the player has to make in the current trick, 0 for first move, 1 for second and so on
            trump: not used for hearts

        Returns:
            one-hot encoded array of valid moves
        """
        # play anything on the first move
        if move_nr == 0:
            return hand

        # get the color of the first played card and check if we have that color
        color_played = color_of_card[current_trick[0]]
        have_color_played = (np.sum(hand * color_masks[color_played, :]) > 0)

        if have_color_played:
            # must give the correct color
            return hand * color_masks[color_played, :]
        else:
            # play anything, if we don't have the color
            return hand

    def calc_points(self, trick: np.ndarray, is_last: bool, trump: int = -1) -> int:
        """
        Calculate the points from the cards in the trick. In hearts these are penalty points, in order to be able
        to determine the winner by the maximum of the score in all jass types, we count the penalty points negative.

        Args:
            trick: the trick
            is_last: true if this is the last trick, ignored for hearts
            trump: not used for hearts
        """
        hearts = color_masks[HEARTS, :]
        points = -hearts[trick].sum()
        if trick[0] == SQ or trick[1] == SQ or trick[2] == SQ or trick[3] == SQ:
            points -= 9
        return points

    def calc_winner(self, trick: np.ndarray, first_player: int, trump: int = -1) -> int:
        """
        Calculate the winner of a completed trick.

        Precondition:
            0 <= trick[i] <= 35, for i = 0..3
        Args:
            trick: the completed trick
            first_player: the first player of the trick
            trump: not used for hearts
        Returns:
            the player who won this trick
        """
        color_of_first_card = color_of_card[trick[0]]
        # highest card of first color wins
        winner = 0
        highest_card = trick[0]
        for i in range(1, 4):
            if color_of_card[trick[i]] == color_of_first_card and trick[i] < highest_card:
                highest_card = trick[i]
                winner = i
        return (first_player - winner) % 4
