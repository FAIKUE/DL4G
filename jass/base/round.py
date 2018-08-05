# HSLU
#
# Created by Thomas Koller on 24.07.18
#
from jass.base.const import *


class Round:
    """
    Class for one round (game) of jass. The class contains the complete information about a round when it is either
    in play or complete, including the information of all the hands.

    A 'Round' object captures the information in the following stages of the game:
    - Cards have been dealt, but no trump is selected yet
    - The first player that is allowed to choose trump has passed this right to the partner (optional)
    - Trump has been declared by either player from the team that declares trump, but no card has been played yet
    - Between 1 and 35 cards have been played
    - The last card has been played, which is the end of the round

    In order to make the class slightly more efficient, the array holding the tricks is constructed in the beginning
    and filled.

    The member variables can be set directly or using methods. The methods will ensure the internal
    consistency of the variables, the method assert_invariants can be used during development to verify the
    consistency for the cases when the member variables are set directly.
    """

    def __init__(self, dealer=None) -> None:
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

        # player of the next action, i.e. declaring trump or playing a card
        if self.dealer is not None:
            # if the dealer is set, the first action is to declare trump
            self.player = next_player[self.dealer]
        else:
            self.player = None

        # selected trump
        self.trump = None               # type: int

        # true if trump was declared forehand, false if it was declared rearhand, None if it has not been declared yet
        self.forehand = None            # type: int

        # the player, who declared trump (derived)
        self.declared_trump = None      # type: int

        #
        # information about held and played cards
        #

        # the current hands of all the players, 1-hot encoded
        self.hands = np.zeros(shape=[4, 36], dtype=np.int32)

        # the tricks played so far, with the cards of the tricks int encoded in the order they are played
        # a value of -1 indicates that the card has not been played yet
        self.tricks = np.full(shape=[9, 4], fill_value=-1, dtype=np.int32)

        # the winner of the tricks
        self.trick_winner = np.full(shape=9, fill_value=-1, dtype=np.int32)

        # the points made in the tricks
        self.trick_points = np.zeros(shape=9, dtype=np.int32)

        # the first player of the trick (derived)
        self.trick_first_player = np.full(shape=9, fill_value=-1, dtype=np.int32)

        # the current trick is a view onto self.trick
        self.current_trick = self.tricks[0, :]
        # the number of completed tricks
        self.nr_tricks = 0
        # the number of card in the current trick
        self.cards_in_trick = 0
        # the total number of played cards
        self.nr_played_cards = 0

        self.points_team_0 = 0          # points made by the team of players 0 and 2
        self.points_team_1 = 0          # points made by the team of players 1 and 3

    def deal_cards(self)->None:
        """
        Deal cards randomly at beginning of the game.
        """
        cards = np.arange(0, 36, dtype=np.int32)
        np.random.shuffle(cards)

        # convert to one hot encoded, hands array must be zero before
        self.hands[0, cards[0:9]] = 1
        self.hands[1, cards[9:18]] = 1
        self.hands[2, cards[18:27]] = 1
        self.hands[3, cards[27:39]] = 1

    def action_trump(self, action: int)->None:
        """
        Execute trump action on the current round.

        Preconditions:
            (action == PASS) => (self.forehand == None)
            self.nr_played_cards == 0
            (self.forehand == None) => self.player == next_player[player.dealer]
            (self.forehand == False) => self.player == partner_player[next_player[player.dealer]

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
                # next action is to play card, but this is done by the current player
                self.trick_first_player[0] = self.player
        else:
            self.trump = action
            self.declared_trump = self.player
            # next action is to play card, but the partner has to play
            self.player = next_player[self.dealer]
            self.trick_first_player[0] = self.player

    def action_play_card(self, card: int)->None:
        """
        Play a card as the current player and update the state of the round.

        Preconditions:
            self.nr_played_cards < 36
            self.trump != None
            self.forehand != None
            self.hands[self.player,card] == 1

        Postconditions:
            see assert_invariants

        Args:
            card: The card to play
        """
        # remove card from player
        self.hands[self.player, card] = 0

        # place in trick
        self.current_trick[self.cards_in_trick] = card
        self.nr_played_cards += 1

        if self.cards_in_trick < 3:
            # trick is not yet finished
            self.cards_in_trick += 1
            self.player = next_player[self.player]
        else:
            # finish current trick
            self._end_trick()

    @staticmethod
    def calc_points(trick: np.ndarray, trump: int, is_last: bool) -> int:
        """
        Calculate the points from the cards in the trick according to the given trump

        Args:
            trick: the trick
            trump: the trump color
            is_last: true if this is the last trick
        """
        return int(np.sum(card_values[trump, trick])) + (5 if is_last else 0)

    @staticmethod
    def calc_winner(trick: np.ndarray, first_player: int, trump: int) -> int:
        """
        Calculate the winner of a completed trick.

        Second implementation in an attempt to be more efficient, while the implementation is somewhat longer
        and more complicated it is about 3 times faster than the previous method.

        Precondition:
            0 <= trick[i] <= 35, for i = 0..3
        Args:
            trick: the completed trick
            first_player: the first player of the trick
            trump: the trump color

        Returns:
            the player who won this trick
        """
        color_of_first_card = color_of_card[trick[0]]
        if trump == UNE_UFE:
            # lowest card of first color wins
            winner = 0
            lowest_card = trick[0]
            for i in range(1,4):
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

    def _end_trick(self) -> None:
        """
        End the current trick and update all the necessary fields.
        """
        # update information about the current trick
        points = self.calc_points(self.current_trick, self.trump, self.nr_played_cards == 36)
        self.trick_points[self.nr_tricks] = points
        winner = self.calc_winner(self.current_trick, self.trick_first_player[self.nr_tricks], self.trump)
        self.trick_winner[self.nr_tricks] = winner

        if winner == NORTH or winner == SOUTH:
            self.points_team_0 += points
        else:
            self.points_team_1 += points
        self.nr_tricks += 1
        self.cards_in_trick = 0

        if self.nr_tricks < 9:
            # not end of round
            # next player is the winner of the trick
            self.trick_first_player[self.nr_tricks] = winner
            self.player = winner
            self.current_trick = self.tricks[self.nr_tricks, :]
        else:
            # end of round
            self.player = None

    def assert_invariants(self)->None:
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
            assert self.trick_winner[i-1] == self.trick_first_player[i]

        # cards played
        assert self.nr_played_cards == 4*self.nr_tricks + self.cards_in_trick
