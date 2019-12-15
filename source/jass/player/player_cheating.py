# HSLU
#
# Created by Thomas Koller on 06.09.18
#
from source.jass.base.player_round_cheating import PlayerRoundCheating
from source.jass.player.player import Player


class PlayerCheating(Player):
    """
    Player that receives full information (through class PlayerRoundCheating) for determining the
    action.
    """
    def select_trump(self, rnd: PlayerRoundCheating) -> int or None:
        raise NotImplementedError()

    def play_card(self, rnd: PlayerRoundCheating) -> int:
        raise NotImplementedError
