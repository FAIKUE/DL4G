# HSLU
#
# Created by Thomas Koller on 06.09.18
#

from source.jass.base.const import JASS_SCHIEBER_1000, JASS_SCHIEBER_2500, JASS_HEARTS
from source.jass.base.rule_hearts import RuleHearts
from source.jass.base.rule_schieber import RuleSchieber


def get_rule(jass_type: str):
    """
    Get the correct rule object depending on the jass type.

    Args:
        jass_type: the jass type
    Returns:
        the appropriate Rule object for the type
    """
    if jass_type == JASS_SCHIEBER_1000:
        return RuleSchieber()
    elif jass_type == JASS_SCHIEBER_2500:
        return RuleSchieber()
    elif jass_type == JASS_HEARTS:
        return RuleHearts()
    else:
        raise ValueError('Type of jass unknown: {}'.format(jass_type))
