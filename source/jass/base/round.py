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

    This is a base class that allows for implementations of different variants of the game.
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
            # if the dealer is set, the first action is usually carried out by the next player (subclasses can
            # override this
            self.player = next_player[self.dealer]
        else:
            self.player = None

        # (we keep the trump and forehand information in the base class, even as not all variations of the game will
        # need it)
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
        # if the dealer is defined, the first player of the first trick is usually the next player
        if dealer is not None:
            self.trick_first_player[0] = next_player[self.dealer]

        # the current trick is a view onto self.trick
        self.current_trick = self.tricks[0, :]

        # the number of completed tricks
        self.nr_tricks = 0
        # the number of card in the current trick
        self.nr_cards_in_trick = 0
        # the total number of played cards
        self.nr_played_cards = 0

        self.points_team_0 = 0          # points made by the team of players 0 and 2
        self.points_team_1 = 0          # points made by the team of players 1 and 3

        # create an appropriate object of type Rule that implements the rules for this round
        # must be set in the derived class
        self.rule = None

        # the jass_type (as used by the round_factory to create this type of round)
        self.jass_type = None

    def __eq__(self, other: 'Round'):
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
        if self.nr_played_cards == 36:
            assert self.current_trick is None
            assert other.current_trick is None
            current_tricks_same = True
        else:
            current_tricks_same = (self.current_trick == other.current_trick).all()
        return self.dealer == other.dealer and \
               self.player == other.player and \
               self.trump == other.trump and \
               self.forehand == other.forehand and \
               self.declared_trump == other.declared_trump and \
               (self.hands == other.hands).all() and \
               (self.tricks == other.tricks).all() and \
               (self.trick_first_player == other.trick_first_player).all() and \
               (self.trick_winner == other.trick_winner).all() and \
               (self.trick_points == other.trick_points).all() and \
               self.nr_tricks == other.nr_tricks and \
               current_tricks_same and \
               self.nr_cards_in_trick == other.nr_cards_in_trick and \
               self.nr_played_cards == other.nr_played_cards and \
               self.points_team_0 == other.points_team_0 and \
               self.points_team_1 == other.points_team_1

    def __repr__(self) -> str:
        """
        Return a representation of the round.

        Returns:
            String describing the round
        """
        return str(self.__dict__)

    def get_points_for_player(self, player: int):
        """
        Get the points for the specific player
        Returns:
            The points for the player
        """
        if player == 0 or player == 2:
            return self.points_team_0
        else:
            return self.points_team_1

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

    def set_hands(self, hands: np.array) -> None:
        """
        Set the hands (instead of dealing the cards). The used array is copied
        Args:
            hands: The hands
        """
        self.hands[:, :] = hands[:, :]

    def action_trump(self, action: int)->None:
        """
        Execute trump action on the current round. Must be implemented in the subclass

        Postcondistions:
            see assert_invariants

        Args:
            action: the action to perform, which is either a trump selection or a pass (if allowed)
        """
        raise NotImplementedError()

    def action_play_card(self, card: int)->None:
        """
        Play a card as the current player and update the state of the round.

        Preconditions:
            self.nr_played_cards < 36
            self.hands[self.player,card] == 1
            (trump selection done according to rules of the jass variation)

        Postconditions:
            see assert_invariants

        Args:
            card: The card to play
        """
        # remove card from player
        self.hands[self.player, card] = 0

        # place in trick
        self.current_trick[self.nr_cards_in_trick] = card
        self.nr_played_cards += 1

        if self.nr_cards_in_trick < 3:
            # trick is not yet finished
            self.nr_cards_in_trick += 1
            self.player = next_player[self.player]
        else:
            # finish current trick
            self._end_trick()

    def get_valid_cards(self):
        """
        Get the valid cards for the current player.

        Returns:

        """
        if self.nr_played_cards == 36:
            return None
        else:
            return self.rule.get_valid_cards(self.hands[self.player, :], self.current_trick,
                                             self.nr_cards_in_trick, self.trump)

    def get_card_played(self, move: int):
        """
        Get the card played in the indicated move.

        Precondition:
         0 <= move <= 35
         self.nr_played_cards <= move
        Args:
            move: the card of the move to get.
        Returns:
            the card played in the move
        """
        nr_trick, move_in_trick = divmod(move, 4)
        return self.tricks[nr_trick, move_in_trick]

    def _end_trick(self) -> None:
        """
        End the current trick and update all the necessary fields.
        """
        # update information about the current trick
        points = self.rule.calc_points(self.current_trick, self.nr_played_cards == 36, self.trump)
        self.trick_points[self.nr_tricks] = points
        winner = self.rule.calc_winner(self.current_trick, self.trick_first_player[self.nr_tricks], self.trump)
        self.trick_winner[self.nr_tricks] = winner

        if winner == NORTH or winner == SOUTH:
            self.points_team_0 += points
        else:
            self.points_team_1 += points
        self.nr_tricks += 1
        self.nr_cards_in_trick = 0

        if self.nr_tricks < 9:
            # not end of round
            # next player is the winner of the trick
            self.trick_first_player[self.nr_tricks] = winner
            self.player = winner
            self.current_trick = self.tricks[self.nr_tricks, :]
        else:
            # end of round
            self.player = None
            self.current_trick = None

    def assert_invariants(self)->None:
        """
        Validates the internal consistency and throws an assertion exception if an error is detected.
        """
        raise NotImplementedError()
