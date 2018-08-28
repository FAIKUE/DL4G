# HSLU
#
# Created by Thomas Koller on 09.01.18
#
"""Classes to implement the current state of a game used for learning and determining moves"""

from jass_base.game import Round
from jass_base.game_const import *

class GameState:
    """Contains all the information about the game at the time to make a specific move by a player. This information
    consists of:
    - the dealer
    - the player that declared trump,
    - the trump chosen
    - trump was declared forehand (derived information)
    - the cards of the current player (hand)
    - the number of tricks that have been played so far,
    - the cards that have already been played and who played them
    - the number of points that have been made by the current jass_players team in this round
    - the number of points that have been made by the opponent team in this round
    - the number of cards played in the current trick
    - the cards played in the current trick
    - the current player
    - the actual card played (for learning)

    We currently use a slightly abbreviated game state, that does not include the round a player played a specific card.
    We do not yet include information about "weis", i.e. about cards that another player holds or that other jass_players
    know that we hold. We do not use information about the points in the whole game, only in the current round.

    The GameState information can be stored using the standard player encoding (0=North, etc.) or by transferring it,
    so that the current player is player 0. This encoding will be needed for learning and determining the next move. We
    allow both possibilities for easier testing and provide methods to switch them.

    The GameState can be determined from the round information. A complete round will give 36 states.
    """

    def __init__(self):
        self.current_player = int
        self.dealer = int
        self.declared_trump = int
        self.trump = int
        self.forehand = bool
        self.nr_tricks_played = 0
        self.cards_played_in_round = None               # 1-hot encoded
        self.hand = None                                # 1-hot encoded
        self.points_own = 0
        self.points_opponent = 0
        self.nr_cards_played = 0
        self.cards_played_in_trick = []
        self.card_played = int
        self.valid = None                               # valid cards, calculated if needed

    @staticmethod
    def get_game_states(rnd: Round) -> List['GameState']:

        """
        Get the game stats for a (complete) round
        Returns:
            List of GameState, one for each card played
        """
        result = []                                     # List[GameState]
        cards_played_in_round = np.zeros([4, 36], np.int32)
        points_made_team_0 = 0
        points_made_team_1 = 0
        for trick_nr, t in enumerate(rnd.tricks):
            current_player = t.first_player
            cards_played_in_trick = []
            for cards_played in range(4):
                gs = GameState()

                # copy data from the round
                gs.dealer = rnd.dealer
                gs.declared_trump = rnd.declared_trump
                gs.trump = rnd.trump
                gs.forehand = rnd.forehand

                # copy data from the trick
                gs.nr_tricks_played = trick_nr
                gs.cards_played_in_round = np.copy(cards_played_in_round)
                if current_player == 0 or current_player == 2:
                    gs.points_own = points_made_team_0
                    gs.points_opponent = points_made_team_1
                else:
                    gs.points_own = points_made_team_1
                    gs.points_opponent = points_made_team_0

                # copy data from current plays in trick
                gs.current_player = current_player
                current_player = next_player[current_player]
                gs.nr_cards_played = cards_played

                # calculate cards still in hand
                gs.hand = np.copy(rnd.played_cards[gs.current_player])
                gs.hand -= cards_played_in_round[gs.current_player]

                # calculate cards played
                gs.cards_played_in_trick = cards_played_in_trick[:]
                gs.card_played = t.cards[cards_played]
                cards_played_in_trick.append(gs.card_played)

                result.append(gs)

            # update information
            cards_played_in_round += t.get_cards_enc_player()
            if t.winner == 0 or t.winner == 2:
                points_made_team_0 += t.points
            else:
                points_made_team_1 += t.points

        return result

    @staticmethod
    def get_last_game_state(rnd: Round) -> 'GameState':
        """
        Get the last game state of a (incomplete) round corresponding to the next card to play.
        Args:
            rnd: The round

        Returns:
            the last game state in the round
        """
        gs = GameState()

        gs.dealer = rnd.dealer
        gs.declared_trump = rnd.declared_trump
        gs.trump = rnd.trump
        gs.forehand = rnd.forehand

        # complete tricks played
        gs.nr_tricks_played = len(rnd.tricks)

        gs.hand = rnd.current_hand
        gs.nr_cards_played = len(rnd.current_trick.cards)
        gs.cards_played_in_trick = rnd.current_trick.cards

        gs.current_player = (4 + rnd.current_trick.first_player - gs.nr_cards_played) % 4

        # calculate values from all tricks
        gs.cards_played_in_round = np.zeros([4, 36], np.int32)
        points_made_team_0 = 0
        points_made_team_1 = 0

        for trick in rnd.tricks:
            gs.cards_played_in_round += trick.get_cards_enc_player()
            if trick.winner == 0 or trick.winner == 2:
                points_made_team_0 += trick.points
            else:
                points_made_team_1 += trick.points

        if gs.current_player == 0 or gs.current_player == 2:
            gs.points_own = points_made_team_0
            gs.points_opponent = points_made_team_1
        else:
            gs.points_own = points_made_team_1
            gs.points_opponent = points_made_team_0

        # gs.valid = Rule.get_valid_cards_from_game_state(gs)
        return gs


    @staticmethod
    def normalize(gs: 'GameState') -> 'GameState':
        """
        Return a new game state with the data normalized, so that the current player is player 0
        Args:
            gs: the game state from which to create a normalized game state

        Returns:
            a new game state, where the current player is player 0
        """
        gs_new = GameState()

        # the number offset that a player id must be shifted (note that the shifts are by numbering order, not by
        # the sequence of the jass_players turn)
        gs_new.current_player = 0
        offset = -gs.current_player

        gs_new.dealer = (gs.dealer + offset) % 4
        gs_new.declared_trump = (gs.declared_trump + offset) % 4
        gs_new.trump = gs.trump
        gs_new.forehand = gs.forehand
        gs_new.nr_tricks_played = gs.nr_tricks_played
        gs_new.cards_played_in_round = np.roll(gs.cards_played_in_round, offset, axis=0)
        gs_new.hand = np.copy(gs.hand)
        gs_new.points_own = gs.points_own
        gs_new.points_opponent = gs.points_opponent
        gs_new.nr_cards_played = gs.nr_cards_played
        gs_new.cards_played_in_trick = gs.cards_played_in_trick[:]
        gs_new.card_played = gs.card_played

        return gs_new




