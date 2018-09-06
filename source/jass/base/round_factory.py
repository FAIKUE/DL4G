# HSLU
#
# Created by Thomas Koller on 05.09.18
#

from jass.base.const import JASS_SCHIEBER_1000, JASS_SCHIEBER_2500, JASS_HEARTS
from jass.base.round import Round
from jass.base.round_schieber import RoundSchieber
from jass.base.round_hearts import RoundHeartsTeam


def get_round(jass_type: str, dealer: int or None = None) -> Round:
    """
    Get the correct round object depending on the jass type
    Args:
        jass_type: the jass type
        dealer: dealer of the round

    Returns:
        the appropriate Round object for the type
    """
    if jass_type == JASS_SCHIEBER_1000:
        return RoundSchieber(dealer=dealer)
    elif jass_type == JASS_SCHIEBER_2500:
        return RoundSchieber(dealer=dealer)
    elif jass_type == JASS_HEARTS:
        return RoundHeartsTeam(dealer=dealer)
    else:
        raise ValueError('Type of jass unknown: {}'.format(jass_type))
