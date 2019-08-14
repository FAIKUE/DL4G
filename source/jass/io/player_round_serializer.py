# HSLU
#
# Created by Thomas Koller on 16.07.19
#
# Adapted from PlayerRoundLogParser to match the refactoring of similar classes

import numpy as np
import logging

from jass.base.const import card_ids, convert_one_hot_encoded_cards_to_str_encoded_list, card_strings, \
    convert_int_encoded_cards_to_str_encoded, JASS_ALL, partner_player, next_player
from jass.base.player_round import PlayerRound
from jass.base.player_round_cheating import PlayerRoundCheating


class PlayerRoundSerializer:
    """
    Class for generation and parsing of the dict/json representation of a PlayerRound.

    """
    # Identifier for format version
    FORMAT_VERSION = 'V0.1'

    @staticmethod
    def player_round_to_dict(player_rnd: PlayerRound) -> dict:
        """
        Generate dict from player round.

        Changed: Adapted from player_service.request_generator to use the same format, even as this
        format has some redundancy and still needs some values to be computed after parsing
        Changed: Added a format version in the dict to support multiple formats later

        TODO: adapt request_generator to actually use this class now

        Args:
            player_rnd: round to generate dict from

        Returns:
            generated dict
        """
        data = PlayerRoundSerializer._player_round_to_dict_base(player_rnd)

        # Information for the 4 players
        # currently only hand is used, and it is only filled out for the current player, other data could
        # be supported in the future, for example 'weisen'
        hand_empty = dict(hand=[])
        player = [hand_empty, hand_empty, hand_empty, hand_empty]
        hand = dict(hand=convert_one_hot_encoded_cards_to_str_encoded_list(player_rnd.hand))
        player[player_rnd.player] = hand
        data['player'] = player

        return data

    @staticmethod
    def player_round_from_dict(round_dict: dict) -> PlayerRound or None:
        """
        Generate a player round from a dict representation
        Args:
            round_dict: dict representation

        Returns:
            player round from the dict or None if there was an error
        """

        # if the version is present, it must be the correct version
        # if it is not there we accept the data for backward compatibility and in the future will assume this
        # version number if absent
        if 'version' in round_dict:
            if round_dict['version'] != PlayerRoundSerializer.FORMAT_VERSION:
                logging.getLogger(__name__).error('Unexpected format version: {}'.format(round_dict['version']))
                return None

        jass_typ = round_dict['jassTyp']
        if jass_typ not in JASS_ALL:
            logging.getLogger(__name__).error('Unexpected jass type: {}'.format(jass_typ))
            return None

        dealer = round_dict['dealer']
        player = round_dict['currentPlayer']

        if 'trump' in round_dict:
            trump = round_dict['trump']
        else:
            trump = None

        if 'tss' in round_dict and round_dict['tss'] == 1:
            forehand = False
            declared_trump = partner_player[next_player[dealer]]
        elif trump is not None:
            # only set if trump has been declared
            forehand = True
            declared_trump = next_player[dealer]
        else:
            # beginning of the game, when trump has not been set yet
            forehand = None
            declared_trump = None

        # generate the player round with the information so far (rule will be determined from the jass type)
        rnd = PlayerRound(
            dealer=dealer,
            player=player,
            trump=trump,
            forehand=forehand,
            declared_trump=declared_trump,
            jass_type=jass_typ,
            rule=None)

        tricks = round_dict['tricks']
        for i, trick in enumerate(tricks):
            cards = trick['cards']
            rnd.nr_played_cards += len(cards)
            rnd.tricks[i] = PlayerRoundSerializer._get_id_trick_from_constants(cards)
            if 'win' in trick:
                rnd.trick_winner[i] = trick['win']
            if 'points' in trick:
                rnd.trick_points[i] = trick['points']
            # first must be present for all tricks
            if 'first' in trick:
                rnd.trick_first_player[i] = trick['first']
            else:
                logging.getLogger(__name__).error('No first player set in trick {}'.format(i))

        rnd.nr_tricks, rnd.nr_cards_in_trick = divmod(rnd.nr_played_cards, 4)

        # current trick points to the correct trick
        rnd.current_trick = rnd.tricks[rnd.nr_tricks]

        for i, player_data in enumerate(round_dict['player']):
            if 'hand' in player_data and len(player_data['hand']) > 0:
                hand = player_data['hand']
                if rnd.player != i:
                    # found hand at the wrong position
                    logging.getLogger(__name__).error('Found hand at position for wrong player: pos={}, '
                                                      'id={}'.format(i, rnd.player))
                    return None
                for card_constant in hand:
                    rnd.hand[card_ids[card_constant]] = 1

        rnd.calculate_points_from_tricks()
        return rnd

        #
        # utility methods
        #

    @staticmethod
    def _player_round_to_dict_base(player_rnd: PlayerRound or PlayerRoundCheating):
        """
        Convert the common part of a PlayerRound or PlayerRoundCheating to a dict, all except the player (hand)
        information, which is different.
        Args:
            player_rnd: player round to convert

        Returns:
            generated dict
        """
        data = dict()
        data['version'] = PlayerRoundSerializer.FORMAT_VERSION
        data['dealer'] = int(player_rnd.dealer)

        # additionally to the specification, save the current player (if set)
        if player_rnd.player is not None:
            data['currentPlayer'] = int(player_rnd.player)

        if player_rnd.trump is not None:
            data['trump'] = int(player_rnd.trump)

        # tss only needs to be present if its value is 1
        if player_rnd.forehand is False:
            data['tss'] = 1

        # played tricks
        tricks = []

        # full tricks
        for i in range(player_rnd.nr_tricks):
            # cards of tricks
            # cards_int = player_rnd.tricks[i, :].tolist()
            cards = convert_int_encoded_cards_to_str_encoded(player_rnd.tricks[i, :])
            trick = dict(
                cards=cards,
                points=int(player_rnd.trick_points[i]),
                win=int(player_rnd.trick_winner[i]),
                first=int(player_rnd.trick_first_player[i]))
            tricks.append(trick)

        # add last (current) trick
        if player_rnd.nr_cards_in_trick > 0:
            cards_int = player_rnd.current_trick[0:player_rnd.nr_cards_in_trick].tolist()
            cards = convert_int_encoded_cards_to_str_encoded(cards_int)
            trick = dict(
                cards=cards,
                first=int(player_rnd.trick_first_player[player_rnd.nr_tricks]))
            tricks.append(trick)
        data['tricks'] = tricks

        # jass type
        data['jassTyp'] = player_rnd.jass_type
        return data

    @staticmethod
    def _get_id_trick_from_constants(constant_trick):
        cards = [card_ids[card] for card in constant_trick]
        while len(cards) < 4:
            cards.append(-1)
        return np.array(cards)

    @staticmethod
    def _add_tricks_to_dict(player_round, player_round_dict):
        player_round_dict['tricks'] = []

        # the number of tricks to save in the file, the completed and current trick must be saved
        nr_tricks = player_round.nr_tricks
        if player_round.nr_cards_in_trick > 0:
            nr_tricks += 1

        for i in range(0, nr_tricks):
            player_round_dict['tricks'].append(dict(
                cards=[card_strings[card] for card in player_round.tricks[i]],
                points=int(player_round.trick_points[i]),
                win=int(player_round.trick_winner[i]),
                first=int(player_round.trick_first_player[i])
            ))


class PlayerRoundCheatingSerializer:
    """
    Class for generation and parsing of the dict/json representation of a PlayerRoundCheating.

    """
    # Identifier for format version
    FORMAT_VERSION = 'V0.1'

    @staticmethod
    def player_round_to_dict(player_rnd: PlayerRound) -> dict:
        """
        Generate dict from player round.

        Changed: Adapted from player_service.request_generator to use the same format, even as this
        format has some redundancy and still needs some values to be computed after parsing
        Changed: Added a format version in the dict to support multiple formats later

        TODO: adapt request_generator to actually use this class now

        Args:
            player_rnd: round to generate dict from

        Returns:
            generated dict
        """
        data = dict()
        data['version'] = PlayerRoundSerializer.FORMAT_VERSION
        data['dealer'] = int(player_rnd.dealer)

        # additionally to the specification, save the current player
        data['currentPlayer'] = player_rnd.player

        if player_rnd.trump is not None:
            data['trump'] = int(player_rnd.trump)

        # tss only needs to be present if its value is 1
        if player_rnd.forehand is False:
            data['tss'] = 1

        # played tricks
        tricks = []

        # full tricks
        for i in range(player_rnd.nr_tricks):
            # cards of tricks
            # cards_int = player_rnd.tricks[i, :].tolist()
            cards = convert_int_encoded_cards_to_str_encoded(player_rnd.tricks[i, :])
            trick = dict(
                cards=cards,
                points=int(player_rnd.trick_points[i]),
                win=int(player_rnd.trick_winner[i]),
                first=int(player_rnd.trick_first_player[i]))
            tricks.append(trick)

        # add last (current) trick
        if player_rnd.nr_cards_in_trick > 0:
            cards_int = player_rnd.current_trick[0:player_rnd.nr_cards_in_trick].tolist()
            cards = convert_int_encoded_cards_to_str_encoded(cards_int)
            trick = dict(
                cards=cards,
                first=player_rnd.trick_first_player[player_rnd.nr_tricks])
            tricks.append(trick)
        data['tricks'] = tricks

        # Information for the 4 players
        # currently only hand is used, and it is only filled out for the current player, other data could
        # be supported in the future, for example 'weisen'
        hand_empty = dict(hand=[])
        player = [hand_empty, hand_empty, hand_empty, hand_empty]
        hand = dict(hand=convert_one_hot_encoded_cards_to_str_encoded_list(player_rnd.hand))
        player[player_rnd.player] = hand
        data['player'] = player

        # jass type
        data['jassTyp'] = player_rnd.jass_type
        return data

    @staticmethod
    def player_round_from_dict(round_dict: dict) -> PlayerRound or None:
        """
        Generate a player round from a dict representation
        Args:
            round_dict: dict representation

        Returns:
            player round from the dict or None if there was an error
        """

        # if the version is present, it must be the correct version
        # if it is not there we accept the data for backward compatibility and in the future will assume this
        # version number if absent
        if 'version' in round_dict:
            if round_dict['version'] != PlayerRoundSerializer.FORMAT_VERSION:
                logging.getLogger(__name__).error('Unexpected format version: {}'.format(round_dict['version']))
                return None

        jass_typ = round_dict['jassTyp']
        if jass_typ not in JASS_ALL:
            logging.getLogger(__name__).error('Unexpected jass type: {}'.format(jass_typ))
            return None

        dealer = round_dict['dealer']
        player = round_dict['currentPlayer']

        if 'trump' in round_dict:
            trump = round_dict['trump']
        else:
            trump = None

        if 'tss' in round_dict and round_dict['tss'] == 1:
            forehand = False
            declared_trump = partner_player[next_player[dealer]]
        elif trump:
            # only set if trump has been declared
            forehand = True
            declared_trump = next_player[dealer]
        else:
            # beginning of the game, when trump has not been set yet
            forehand = None
            declared_trump = None

        # generate the player round with the information so far (rule will be determined from the jass type)
        rnd = PlayerRound(
            dealer=dealer,
            player=player,
            trump=trump,
            forehand=forehand,
            declared_trump=declared_trump,
            jass_type=jass_typ,
            rule=None)

        tricks = round_dict['tricks']
        for i, trick in enumerate(tricks):
            cards = trick['cards']
            rnd.nr_played_cards += len(cards)
            rnd.tricks[i] = PlayerRoundSerializer._get_id_trick_from_constants(cards)
            if 'win' in trick:
                rnd.trick_winner[i] = trick['win']
            if 'points' in trick:
                rnd.trick_points[i] = trick['points']
            if 'first' in trick:
                rnd.trick_first_player[i] = trick['first']

        rnd.nr_tricks, rnd.nr_cards_in_trick = divmod(rnd.nr_played_cards, 4)

        # current trick points to the correct trick
        rnd.current_trick = rnd.tricks[rnd.nr_tricks]

        for i, player_data in enumerate(round_dict['player']):
            if 'hand' in player_data and len(player_data['hand']) > 0:
                hand = player_data['hand']
                if rnd.player != i:
                    # found hand at the wrong position
                    logging.getLogger(__name__).error('Found hand at position for wrong player: pos={}, '
                                                      'id={}'.format(i, rnd.player))
                    return None
                for card_constant in hand:
                    rnd.hand[card_ids[card_constant]] = 1

        rnd.calculate_points_from_tricks()
        return rnd

