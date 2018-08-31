# HSLU
#
# Created by Thomas Koller on 31.12.17

""" Implementation of rules of jass game"""

from jass.base.const import *
from jass.base.round import Round
from jass.base.player_round import PlayerRound


class Rule:
    """
    Class for implementing rules of the jass game. Currently, only the basic rules (for Schieber with trump)
    is implemented.
    """

    @staticmethod
    def get_valid_cards(hand: np.array, current_trick: np.ndarray or list, move_nr: int, trump: int) -> np.array:
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

    @staticmethod
    def get_valid_cards_from_player_round(player_rnd: PlayerRound):
        return Rule.get_valid_cards(player_rnd.hand,
                                    player_rnd.current_trick,
                                    player_rnd.nr_cards_in_trick,
                                    player_rnd.trump)

    @staticmethod
    def validate_round(rnd: Round):
        """
        Validate all tricks (and all moves in the tricks) for a round to verify that the played card is included
        in the valid card set. The round must contain the information about all the played cards.
        Args:
            rnd: a complete round
        """
        player_rnds = PlayerRound.all_from_complete_round(rnd)
        for i, player_rnd in enumerate(player_rnds):
            nr_trick, move_in_trick = divmod(i, 4)
            card_played = rnd.tricks[nr_trick, move_in_trick]
            Rule.validate_player_round(player_rnd, card_played)

    @staticmethod
    def validate_player_round(player_rnd: PlayerRound, card_played: int) -> None:
        """
        Validate that the played card is among the valid cards for that round. An assertion error is thrown
        if that is not the case
        Args:
            player_rnd: the player round that is validated
            card_played: the actual card played
        """
        valid_cards = Rule.get_valid_cards_from_player_round(player_rnd)
        assert valid_cards[card_played] == 1
