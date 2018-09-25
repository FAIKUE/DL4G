# HSLU
#
# Created by Thomas Koller on 06.09.18
#

from jass.arena.arena import Arena
from jass.base.player_round_cheating import PlayerRoundCheating
from jass.player.player_cheating import PlayerCheating


class ArenaCheating(Arena):
    """
    Arena that uses PlayerRoundCheating to call the players, i.e. gives them the information about the other
    players hand. In all other functionality, it is the same as Arena.
    """

    def set_players(self,
                    north: PlayerCheating, east: PlayerCheating,
                    south: PlayerCheating, west: PlayerCheating) -> None:
        super().set_players(north, east, south, west)

    def get_player_round(self) -> PlayerRoundCheating:
        """
        Creates and returns an appropriate player round object to use for the players that is created from the
        current round. By default the object is a PlayerRound, but that can be overridden.

        Returns:

        """
        player_rnd = PlayerRoundCheating()
        player_rnd.set_from_round(self.current_rnd)
        return player_rnd

    # no longer necessary as basic implementation handles the PlayerRoundCheating now...

    # def play_round(self, dealer: int) -> None:
    #     """
    #     Play a complete round (36 cards). The results remains in self._rnd. Used PlayerRoundCheating
    #     to give the player full information
    #     """
    #     self._init_round(dealer)
    #     self.deal_cards()
    #     self._trump_strategy.determine_trump(rnd=self._rnd, arena=self)
    #
    #     player_rnd = PlayerRoundCheating()
    #     for cards in range(36):
    #         player_rnd.set_from_round(self._rnd)
    #         card_action = self._players[player_rnd.player].play_card(player_rnd)
    #         self._rnd.action_play_card(card_action)
