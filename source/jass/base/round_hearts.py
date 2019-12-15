# HSLU
#
# Created by Thomas Koller on 24.07.18
#
from source.jass.base.const import JASS_HEARTS, next_player
from source.jass.base.round import Round
from source.jass.base.rule_hearts import RuleHearts


class RoundHeartsTeam(Round):
    """
    Class for one round (game) of simple hearts. The variant of simple hearts has the following rules:
    - There is no trump, the rules are like for 'obe'
    - SQ is worth nine penalty points
    - Each heart is worth 9 points penalty
    - S/N and E/W are a team

    (Special rule that the penalty points are given to the other team if one player/team collects all 18 penalty
    points is omitted)

    """

    def __init__(self, dealer=None) -> None:
        """
        Initialize the class. If dealer is supplied the player and dealer will be set accordingly and only the
        cards will have to be initialized separately to put the object in a consistent initial configuration.

        Args:
            dealer: the dealer or None if it should remain uninitialized
        """
        super(RoundHeartsTeam, self).__init__(dealer=dealer)
        self.rule = RuleHearts()
        self.jass_type = JASS_HEARTS

    def action_trump(self, action: int)->None:
        """
        No trump for hearts, so this does nothing
        """

    def assert_invariants(self)->None:
        """
        Validates the internal consistency and throws an assertion exception if an error is detected.
        """
        assert self.dealer is not None

        # is None at the end of the game
        if self.nr_played_cards < 36:
            assert self.player is not None

        # trick winners
        if self.nr_tricks > 0:
            assert self.trick_first_player[0] == next_player[self.dealer]
        for i in range(1, self.nr_tricks):
            assert self.trick_winner[i-1] == self.trick_first_player[i]

        # cards played
        assert self.nr_played_cards == 4*self.nr_tricks + self.nr_cards_in_trick

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
