# HSLU
#
# Created by Thomas Koller on 24.07.18
#
from jass.base.const import JASS_SCHIEBER_1000, next_player, partner_player, PUSH
from jass.base.round import Round
from jass.base.rule_schieber import RuleSchieber


class RoundSchieber(Round):
    """
    Class for one round (game) of Schieber. The variant of schieber has the following rules:
    - The next player after the dealer has the right to select trump, if he does not want to select a trump, s/he can
    pass to the partner player, which then has to select trump
    - The possible trump values are any of the 4 colors and 'obe' and 'une'
    """

    def __init__(self, dealer=None, jass_type=JASS_SCHIEBER_1000) -> None:
        """
        Initialize the class. If dealer is supplied the player and dealer will be set accordingly and only the
        cards will have to be initialized separately to put the object in a consistent initial configuration.

        Args:
            dealer: the dealer or None if it should remain uninitialized
            jass_type: the exact jass type to use as there might be several types of Schieber that use the same
            RoundSchieber class
        """
        super(RoundSchieber, self).__init__(dealer=dealer)
        self.rule = RuleSchieber()
        self.jass_type = jass_type

    def action_trump(self, action: int)->None:
        """
        Execute trump action on the current round.

        Preconditions:
            (action == PUSH) => (self.forehand == None)
            self.nr_played_cards == 0
            (self.forehand == None) => self.player == next_player[player.dealer]
            (self.forehand == False) => self.player == partner_player[next_player[player.dealer]
            not (self.forehand == True)

        Postcondistions:
            see assert_invariants

        Args:
            action: the action to perform, which is either a trump selection or a pass (if allowed)
        """
        if self.forehand is None:
            # this is the action done by the forehand player
            if action == PUSH:
                self.forehand = False
                # next action is to select trump by the partner
                self.player = partner_player[self.player]
            else:
                self.trump = action
                self.declared_trump = self.player
                self.forehand = True
                # next action is to play card, but this is done by the current player
                self.trick_first_player[0] = self.player
        elif self.forehand is False:
            self.trump = action
            self.declared_trump = self.player
            # next action is to play card, but the partner has to play
            self.player = next_player[self.dealer]
            self.trick_first_player[0] = self.player
        else:
            raise ValueError('Unexpected value')

    def assert_invariants(self)->None:
        """
        Validates the internal consistency and throws an assertion exception if an error is detected.
        """
        # trump declaration should be present
        if self.forehand is not None:
            if self.forehand:
                assert self.declared_trump == next_player[self.dealer]

            else:
                # either trump has been declared or not yet
                assert self.trump is None or self.declared_trump == partner_player[next_player[self.dealer]]
            assert self.dealer is not None

        # trick winners
        if self.nr_tricks > 0:
            assert self.trick_first_player[0] == next_player[self.dealer]
        for i in range(1, self.nr_tricks):
            assert self.trick_winner[i-1] == self.trick_first_player[i]

        # cards played
        assert self.nr_played_cards == 4*self.nr_tricks + self.nr_cards_in_trick

        # total number of cards
        played_cards = self.tricks.flatten() > -1
        nr_played_cards = played_cards.sum()
        nr_cards_in_hand = self.hands.flatten().sum()
        assert nr_played_cards + nr_cards_in_hand == 36

        # number of points
        points_team_0 = 0
        points_team_1 = 0
        for trick in range(self.nr_tricks):
            if self.trick_winner[trick] == 0 or self.trick_winner[trick] == 2:
                points_team_0 += self.trick_points[trick]
            else:
                points_team_1 += self.trick_points[trick]
        assert points_team_0 == self.points_team_0
        assert points_team_1 == self.points_team_1
