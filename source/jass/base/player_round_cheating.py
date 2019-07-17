# HSLU
#
# Created by Thomas Koller on 05.09.2018
#

from typing import List
import numpy as np

from jass.base.const import next_player, partner_player
from jass.base.round import Round
from jass.base.player_round import PlayerRound


class PlayerRoundCheating(PlayerRound):
    """
    Class for one round of jass from the players point of view, but containing the information of the hands of all
    players in addition to the information contained in PlayerRound.
    """

    def __init__(self,
                 dealer=None,
                 player=None,
                 trump=None,
                 forehand=None,
                 declared_trump=None,
                 jass_type=None,
                 rule=None) -> None:
        """
        Initialize the class. If dealer is supplied the player and dealer will be set accordingly and only the
        cards will have to be initialized separately to put the object in a consistent initial configuration.

        Args:
            dealer: the dealer or None if it should remain uninitialized
        """
        super(PlayerRoundCheating, self).__init__(dealer=dealer, player=player,
                                                  trump=trump, forehand=forehand, declared_trump=declared_trump,
                                                  jass_type=jass_type, rule=rule)
        # the current hands of all the player
        self.hands = np.zeros(shape=[4, 36], dtype=np.int32)

    def __repr__(self):
        """
        Build representation string of the object. This will also be used by str.
        Returns:
            String representation of the object
        """
        return str(self.__dict__)

    def __eq__(self, other: 'PlayerRoundCheating'):
        """
        Compare two instances. Useful for tests when the representations are encoded and decoded. The objects are
        considered equal if they have the same properties. As the properties are numpy arrays, we can not compare
        dict directly.
        Args:
            other: the other object to compare to.

        Returns:
            True if the objects are the same.
        """
        # noinspection PyPep8
        return self.dealer == other.dealer and \
               self.player == other.player and \
               self.trump == other.trump and \
               self.forehand == other.forehand and \
               self.declared_trump == other.declared_trump and \
               (self.hands == other.hands).all() and \
               (self.hand == other.hand).all() and \
               (self.tricks == other.tricks).all() and \
               (self.trick_first_player == other.trick_first_player).all() and \
               (self.trick_winner == other.trick_winner).all() and \
               (self.trick_points == other.trick_points).all() and \
               self.nr_tricks == other.nr_tricks and \
               (self.current_trick == other.current_trick).all() and \
               self.nr_cards_in_trick == other.nr_cards_in_trick and \
               self.nr_played_cards == other.nr_played_cards and \
               self.points_team_0 == other.points_team_0 and \
               self.points_team_1 == other.points_team_1

    def set_from_round(self, rnd: Round):
        """
        Initialize PlayerRound from a Round at the same card. The data in arrays is copied from the round.
        Args:
            rnd:
        """
        super().set_from_round(rnd)
        self.hands[:, :] = rnd.hands[:, :]

    def set_from_round_shared(self, rnd: Round):
        """
        Initialize PlayerRound from a full Round at the same card. The data in arrays is shared between the
        PlayerRound and Round, so it should not be changed. As arrays are already allocated in __init__ and
        overwritten here, the method is best employed when the object is used several times.

        Args:
            rnd:
        """
        super().set_from_round_shared(rnd)
        self.hands = rnd.hands

    @staticmethod
    def from_complete_round(rnd: Round, cards_played: int) -> 'PlayerRoundCheating':
        """
        Create a PlayerRound object from a complete Round object for a specific card.

        Preconditions:
            0 <= cards_played <= 35
            rnd.nr_played_cards == 36

        Args:
            rnd: The Round from which to create the PlayerRound.
            cards_played: the number of cards played for which the PlayerRound should be created

        Returns:
            a PlayerRound object for the state when the cards have been played.

        """
        player_rnd = PlayerRoundCheating(dealer=rnd.dealer,
                                         trump=rnd.trump,
                                         declared_trump=rnd.declared_trump,
                                         forehand=rnd.forehand,
                                         jass_type=rnd.jass_type,
                                         rule=rnd.rule)

        player_rnd.nr_played_cards = cards_played

        # calculate the number of tricks played and how many cards in the current trick
        player_rnd.nr_tricks, player_rnd.nr_cards_in_trick = divmod(cards_played, 4)

        # copy the trick first player, this is also available after making trump, when no trick has been played yet
        player_rnd.trick_first_player[0:player_rnd.nr_tricks + 1] = rnd.trick_first_player[0:player_rnd.nr_tricks + 1]

        if cards_played > 0:
            if player_rnd.nr_cards_in_trick == 0:
                # only full tricks
                player_rnd.tricks[0:player_rnd.nr_tricks, :] = rnd.tricks[0:player_rnd.nr_tricks, :]

                # current trick is empty (or none if last card)
                if cards_played == 36:
                    player_rnd.current_trick = None
                else:
                    # this is the next trick, after the full ones
                    player_rnd.current_trick = player_rnd.tricks[player_rnd.nr_tricks]

            else:
                # copy all the full tricks first
                player_rnd.tricks[0:player_rnd.nr_tricks, :] = rnd.tricks[0:player_rnd.nr_tricks, :]

                # copy the trick in progress
                player_rnd.tricks[player_rnd.nr_tricks, 0:player_rnd.nr_cards_in_trick] = \
                    rnd.tricks[player_rnd.nr_tricks, 0:player_rnd.nr_cards_in_trick]
                # make sure the current trick points to that
                player_rnd.current_trick = player_rnd.tricks[player_rnd.nr_tricks]
            # copy the results from the tricks
            player_rnd.trick_winner[0:player_rnd.nr_tricks] = rnd.trick_winner[0:player_rnd.nr_tricks]
            player_rnd.trick_points[0:player_rnd.nr_tricks] = rnd.trick_points[0:player_rnd.nr_tricks]

            player_rnd.calculate_points_from_tricks()

            # determine player
            player_rnd.player = (player_rnd.trick_first_player[player_rnd.nr_tricks]-player_rnd.nr_cards_in_trick) % 4
        else:
            # no cards played yet
            player_rnd.player = next_player[player_rnd.dealer]

        # determine hand still held by the player, which are the cards that the player will play in the next
        # tricks of the full rnd, that are not played yet

        # add cards for completed tricks
        nr_tricks_completed = player_rnd.nr_tricks
        if player_rnd.nr_cards_in_trick != 0:
            # there is a non complete trick, treat it specially by adding the cards not yet played in the current trick
            player = (rnd.trick_first_player[player_rnd.nr_tricks]-player_rnd.nr_cards_in_trick) % 4
            for card_nr in range(player_rnd.nr_cards_in_trick, 4):
                card_played = rnd.tricks[player_rnd.nr_tricks, card_nr]
                player_rnd.hands[player, card_played] = 1
                player = next_player[player]
            # exclude this trick from the full tricks
            nr_tricks_completed += 1
        for rnd_nr in range(nr_tricks_completed, 9):
            player = rnd.trick_first_player[rnd_nr]
            for card_nr in range(4):
                card_played = rnd.tricks[rnd_nr, card_nr]
                player_rnd.hands[player, card_played] = 1
                player = next_player[player]

        player_rnd.hand = player_rnd.hands[player_rnd.player, :]

        return player_rnd

    @staticmethod
    def all_from_complete_round(rnd: Round) -> List['PlayerRoundCheating']:
        """
        Get all 36 player rounds from a complete round
        Args:
            rnd: The Round from which to create the PlayerRound.

        Returns:
            the list of player_rounds for cards 0..35
        """
        return [PlayerRoundCheating.from_complete_round(rnd, i) for i in range(0, 36)]

    @staticmethod
    def trump_from_complete_round(rnd: Round, forehand: bool) -> 'PlayerRoundCheating' or None:
        """
        Create a player round from a complete round for the state of trump selection.
        Args:
            rnd: a complete round
            forehand: true if the trump selection should be for the forehand player, false if it should be for the
            rearhand player after push

        Returns:
            a PlayerRound for trump selection or None if trump selection was asked to be returned for rearhand, when
            there was no rearhand trump selection in that round
        """
        if not forehand and rnd.forehand:
            return None

        player_rnd = PlayerRoundCheating(dealer=rnd.dealer)

        if forehand:
            player_rnd.player = next_player[player_rnd.dealer]
            player_rnd.forehand = None
        else:
            player_rnd.player = partner_player[next_player[player_rnd.dealer]]
            player_rnd.forehand = False

        # determine hand held by the players at the beginning of the game, this are the hands of all cards played
        for rnd_nr in range(9):
            player = rnd.trick_first_player[rnd_nr]
            for card_nr in range(4):
                card_played = rnd.tricks[rnd_nr, card_nr]
                player_rnd.hands[player, card_played] = 1
                player = next_player[player]

        # copy hand of the player
        player_rnd.hand = player_rnd.hands[player_rnd.player, :]

        return player_rnd

    def assert_invariants(self) -> None:
        """
        Validates the internal consistency and throws an assertion exception if an error is detected.
        """
        # trump declaration
        if self.trump is not None:
            if self.forehand:
                assert self.declared_trump == next_player[self.dealer]
            else:
                assert self.declared_trump == partner_player[next_player[self.dealer]]
            assert self.player is not None

        # trick winners
        if self.nr_tricks > 0:
            assert self.trick_first_player[0] == next_player[self.dealer]
        for i in range(1, self.nr_tricks):
            assert self.trick_winner[i - 1] == self.trick_first_player[i]

        # cards played
        assert self.nr_played_cards == 4 * self.nr_tricks + self.nr_cards_in_trick

        # cards in hand
        assert self.hands.sum() == 36 - self.nr_played_cards
        # print(self.hands)
        # print(self.hand)
        # print(self.hand.sum())
        assert self.hand.sum() == 9 - self.nr_tricks

        # check current trick
        if self.nr_played_cards == 36:
            assert self.current_trick is None
        else:
            nr_cards_in_current_trick = np.count_nonzero(self.current_trick[:] > -1)
            expected_cards_in_current_trick = (self.nr_played_cards % 4)
            assert nr_cards_in_current_trick == expected_cards_in_current_trick


