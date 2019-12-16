# HSLU
#
# Created by Thomas Koller on 19.07.19
#
import numpy as np
import logging

from jass.base.const import convert_one_hot_encoded_cards_to_str_encoded_list, get_cards_encoded, \
    get_cards_encoded_from_str
from jass.base.label_play import LabelPlay
from jass.base.label_trump import LabelTrump


class LabelPlaySerializer:
    """
    Class for generation and parsing of the dict/json representation of a label for card play.
    """
    @staticmethod
    def label_to_dict(label: LabelPlay) -> dict:
        """
        Convert a label to a dict
        Args:
            label: label to convert

        Returns:
            dict representation of the label
        """
        return dict(
            card_played=int(label.card_played),
            points_in_trick_own=int(label.points_in_trick_own),
            points_in_trick_other=int(label.points_in_trick_other),
            trick_winner=int(label.trick_winner),
            points_in_round_own=int(label.points_in_round_own),
            points_in_round_other=int(label.points_in_round_other),
            hands_player_0=convert_one_hot_encoded_cards_to_str_encoded_list(label.hands[0, :]),
            hands_player_1=convert_one_hot_encoded_cards_to_str_encoded_list(label.hands[1, :]),
            hands_player_2=convert_one_hot_encoded_cards_to_str_encoded_list(label.hands[2, :]),
            hands_player_3=convert_one_hot_encoded_cards_to_str_encoded_list(label.hands[3, :])
        )

    @staticmethod
    def label_from_dict(data: dict) -> LabelPlay:
        """
        Convert a dict to a label. If the dict does not contain the expected keys, an exception will be thrown
        Args:
            data: dict

        Returns:
            label from the data in the dict
        """
        hands = np.zeros(shape=[4, 36], dtype=np.int32)
        try:
            hands[0, :] = get_cards_encoded_from_str(data['hands_player_0'])
            hands[1, :] = get_cards_encoded_from_str(data['hands_player_1'])
            hands[2, :] = get_cards_encoded_from_str(data['hands_player_2'])
            hands[3, :] = get_cards_encoded_from_str(data['hands_player_3'])
        except KeyError as e:
            logging.getLogger(__name__).error('Key error: {}, data: {}'.format(e, data))
            raise e

        return LabelPlay(card_played=data['card_played'],
                         points_in_trick_own=data['points_in_trick_own'],
                         points_in_trick_other=data['points_in_trick_other'],
                         trick_winner=data['trick_winner'],
                         points_in_round_own=data['points_in_round_own'],
                         points_in_round_other=data['points_in_round_other'],
                         hands=hands)


class LabelTrumpSerializer:
    """
    Class for generation and parsing of the dict/json representation of a label for trump.
    """
    @staticmethod
    def label_to_dict(label: LabelTrump) -> dict:
        """
        Convert a label to a dict
        Args:
            label: label to convert

        Returns:
            dict representation of the label
        """
        return dict(
            trump=int(label.trump)
        )

    @staticmethod
    def label_from_dict(data: dict) -> LabelTrump:
        """
        Convert a dict to a label. If the dict does not contain the expected keys, an exception will be thrown
        Args:
            data: dict

        Returns:
            label from the data in the dict
        """
        try:
            trump = data['trump']
        except KeyError as e:
            logging.getLogger(__name__).error('Key error: {}, data: {}'.format(e, data))
            raise e

        return LabelTrump(trump=trump)