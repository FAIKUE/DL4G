# HSLU
#
# Created by Thomas Koller on 04.08.18
#

import numpy as np

from jass.base.const import *
from jass.base.round import Round


class PlayerRound:
    """
    Class for one round of jass from the players point of view. It contains all the information about the round
    that the player can observe at a specific time in the round. Similar to the class Round, PlayerRound captures
    the information at different stages of the game, like:
    - Player can choose to select a trump or push the right to make trump to his partner
    - Player needs to select trump after his partner pushed
    - Player needs to play a card.
    """

    def __init__(self,
                 dealer=None,
                 player=None,
                 trump=None,
                 forehand=None,
                 declared_trump=None) -> None:
        """
        Initialize the class. If dealer is supplied the player and dealer will be set accordingly and only the
        cards will have to be initialized separately to put the object in a consistent initial configuration.

        Args:
            dealer: the dealer or None if it should remain uninitialized
        """
        #
        # general information about the round
        #

        # dealer of the round
        self.dealer = dealer        # type: int

        # player of the next action, i.e. declaring trump or playing a card, i.e. player whose view of the
        # round this class describes
        self.player = player

        # selected trump
        self.trump = trump               # type: int

        # true if trump was declared forehand, false if it was declared rearhand, None if it has not been declared yet
        self.forehand = forehand            # type: int

        # the player, who declared trump (derived)
        self.declared_trump = declared_trump      # type: int

        #
        # information about held and played cards
        #

        # the current hands of the player
        self.hand = np.zeros(shape=36, dtype=np.int32)

        # the tricks played so far, with the cards of the tricks int encoded in the order they are played
        # a value of -1 indicates that the card has not been played yet
        self.tricks = np.full(shape=[9, 4], fill_value=-1, dtype=np.int32)

        # the winner of the tricks
        self.trick_winner = np.full(shape=9, fill_value=-1, dtype=np.int32)

        # the points made in the tricks
        self.trick_points = np.zeros(shape=9, dtype=np.int32)

        # the first player of the trick (derived)
        self.trick_first_player = np.full(shape=9, fill_value=-1, dtype=np.int32)

        # the number of completed tricks
        self.nr_tricks = 0

        # the current trick is a view onto self.trick
        self.current_trick = self.tricks[0, :]

        # the number of cards in the current trick
        self.nr_cards_in_trick = 0

        # the total number of played cards
        self.nr_played_cards = 0

        self.points_team_0 = 0          # points made by the team of players 0 and 2
        self.points_team_1 = 0          # points made by the team of players 1 and 3

    def set_from_round(self, rnd: Round):
        """
        Initialize PlayerRound from a full Round at the same card. The data in arrays is copied from the round.


        Args:
            rnd:
        """
        self.dealer = rnd.dealer
        self.player = rnd.player
        self.trump = rnd.trump
        self.forehand = rnd.forehand
        self.declared_trump = rnd.declared_trump
        self.hand[:] = rnd.hands[self.player, :]
        self.tricks[:, :] = rnd.tricks[:, :]
        self.trick_winner = rnd.trick_winner
        self.trick_points = rnd.trick_points
        self.trick_first_player = rnd.trick_first_player
        self.current_trick = rnd.current_trick
        self.nr_tricks = rnd.nr_tricks
        self.nr_cards_in_trick = rnd.nr_cards_in_trick
        self.nr_played_cards = rnd.nr_played_cards
        self.points_team_0  = rnd.points_team_0
        self.points_team_1 = rnd.points_team_1

    def set_from_round_shared(self, rnd: Round):
        """
        Initialize PlayerRound from a full Round at the same card. The data in arrays is shared between the
        PlayerRound and Round, so it should not be changed. As arrays are already allocated in __init__ and
        overwritten here, the method is best employed when the object is used several times.

        Args:
            rnd:
        """
        self.dealer = rnd.dealer
        self.player = rnd.player
        self.trump = rnd.trump
        self.forehand = rnd.forehand
        self.declared_trump = rnd.declared_trump
        self.hand = rnd.hands[self.player, :]
        self.tricks = rnd.tricks
        self.trick_winner = rnd.trick_winner
        self.trick_points = rnd.trick_points
        self.trick_first_player = rnd.trick_first_player
        self.current_trick = rnd.current_trick
        self.nr_tricks = rnd.nr_tricks
        self.nr_cards_in_trick = rnd.nr_cards_in_trick
        self.nr_played_cards = rnd.nr_played_cards
        self.points_team_0  = rnd.points_team_0
        self.points_team_1 = rnd.points_team_1

    def get_current_trick(self) -> np.ndarray:
        return self.tricks[self.nr_tricks, :]

    def _calculate_points_from_tricks(self) -> None:
        """
        Calculate the points of the teams from the trick points and trick winners.
        """
        self.points_team_0 = 0
        self.points_team_1 = 0
        for trick in range(self.nr_tricks):
            if self.trick_winner[trick] == 0 or self.trick_winner[trick] == 2:
                self.points_team_0 += self.trick_points[trick]
            else:
                self.points_team_1 += self.trick_points[trick]

    @staticmethod
    def from_complete_round(rnd: Round, cards_played: int) -> 'PlayerRound':
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
        player_rnd = PlayerRound(dealer=rnd.dealer,
                                 trump=rnd.trump,
                                 declared_trump=rnd.declared_trump,
                                 forehand=rnd.forehand)

        player_rnd.nr_played_cards = cards_played
        # calculate the number of tricks we need and how many cards are left
        player_rnd.nr_tricks, player_rnd.nr_cards_in_trick = divmod(cards_played, 4)

        # copy the trick first player, this is also available after making trump, when no trick has been played yet
        player_rnd.trick_first_player[0:player_rnd.nr_tricks + 1] = rnd.trick_winner[0:player_rnd.nr_tricks + 1]

        if cards_played > 0:
            # copy all the tricks
            player_rnd.tricks[0:player_rnd.nr_tricks, :] = rnd.tricks[0:player_rnd.nr_tricks, :]
            player_rnd.current_trick[0:player_rnd.nr_cards_in_trick] = \
                rnd.tricks[player_rnd.nr_tricks, 0:player_rnd.nr_cards_in_trick]
            # copy the results from the tricks
            player_rnd.trick_winner[0:player_rnd.nr_tricks] = rnd.trick_winner[0:player_rnd.nr_tricks]
            player_rnd.trick_points[0:player_rnd.nr_tricks] = rnd.trick_points[0:player_rnd.nr_tricks]

            player_rnd._calculate_points_from_tricks()

        # incomplete
        return player_rnd

    def assert_invariants(self) -> None:
        """
        Validates the internal consistency and throws an assertion exception if an error is detected.
        """
        # trump declaration
        if self.forehand is not None:
            if self.forehand:
                assert self.declared_trump == next_player[self.dealer]
            else:
                assert self.declared_trump == partner_player[next_player[self.dealer]]

        # trick winners
        if self.nr_tricks > 0:
            assert self.trick_first_player[0] == next_player[self.dealer]
        for i in range(1, self.nr_tricks):
            assert self.trick_winner[i - 1] == self.trick_first_player[i]

        # cards played
        assert self.nr_played_cards == 4 * self.nr_tricks + self.nr_cards_in_trick

