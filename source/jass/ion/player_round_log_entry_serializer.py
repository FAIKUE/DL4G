# HSLU
#
# Created by Thomas Koller on 15.07.19
#

import json
from datetime import datetime

from source.jass.ion.label_serializer import LabelPlaySerializer, LabelTrumpSerializer
from source.jass.ion.log_entries import RoundLogEntry, PlayerRoundLogEntry, PlayerRoundTrumpLogEntry
from source.jass.ion.player_round_serializer import PlayerRoundSerializer
from source.jass.ion.round_serializer import RoundSerializer, DATE_FORMAT


class PlayerRoundLogEntrySerializer:
    """
    Read and write PlayerRoundLogEntry objects from dict.
    """
    @staticmethod
    def entry_to_dict(round_log_entry: PlayerRoundLogEntry) -> dict:
        """
        Generate the dict for an entry.
        Args:
            round_log_entry: log entry for which to generate the dict

        Returns:
            dict to contain the log entry
        """
        return dict(
            round=PlayerRoundSerializer.player_round_to_dict(round_log_entry.player_rnd),
            date=datetime.strftime(round_log_entry.date, DATE_FORMAT),
            player_id=round_log_entry.player_id,
            label=LabelPlaySerializer.label_to_dict(round_log_entry.label)
        )

    @staticmethod
    def entry_from_dict(entry_dict: dict) -> PlayerRoundLogEntry:
        """
        Create a round log entry from a dict
        Args:
            entry_dict:

        Returns:
            new round log entry
        """
        date = datetime.strptime(entry_dict['date'], DATE_FORMAT)
        player_rnd = PlayerRoundSerializer.player_round_from_dict(entry_dict['round'])
        player_id = entry_dict['player_id']
        label = LabelPlaySerializer.label_from_dict(entry_dict['label'])
        return PlayerRoundLogEntry(player_rnd=player_rnd, date=date, player_id=player_id, label=label)

    @staticmethod
    def entries_from_file(filename: str) -> [PlayerRoundLogEntry]:
        """
        Read player round log entries.
        Args:
            filename: name for the file to read from

        Returns:
            Array of log entries
        """
        entries = []
        with open(filename, mode='r') as file:
            for line in file:
                line_dict = json.loads(line)
                round_log_entry = PlayerRoundLogEntrySerializer.entry_from_dict(line_dict)
                entries.append(round_log_entry)
        return entries


class PlayerRoundLogTrumpEntrySerializer:
    """
    Read and write PlayerRoundTrumpLogEntry objects from dict.
    """
    @staticmethod
    def entry_to_dict(round_log_entry: PlayerRoundTrumpLogEntry) -> dict:
        """
        Generate the dict for an entry.
        Args:
            round_log_entry: log entry for which to generate the dict

        Returns:
            dict to contain the log entry
        """
        return dict(
            round=PlayerRoundSerializer.player_round_to_dict(round_log_entry.player_rnd),
            date=datetime.strftime(round_log_entry.date, DATE_FORMAT),
            player_id=round_log_entry.player_id,
            label=LabelTrumpSerializer.label_to_dict(round_log_entry.label)
        )

    @staticmethod
    def entry_from_dict(entry_dict: dict) -> PlayerRoundTrumpLogEntry:
        """
        Create a round log entry from a dict
        Args:
            entry_dict:

        Returns:
            new round log entry
        """
        date = datetime.strptime(entry_dict['date'], DATE_FORMAT)
        player_rnd = PlayerRoundSerializer.player_round_from_dict(entry_dict['round'])
        player_id = entry_dict['player_id']
        label = LabelTrumpSerializer.label_from_dict(entry_dict['label'])
        return PlayerRoundTrumpLogEntry(player_rnd=player_rnd, date=date, player_id=player_id, label=label)

    @staticmethod
    def entries_from_file(filename: str) -> [PlayerRoundTrumpLogEntry]:
        """
        Read player round log entries.
        Args:
            filename: name for the file to read from

        Returns:
            Array of log entries
        """
        entries = []
        with open(filename, mode='r') as file:
            for line in file:
                line_dict = json.loads(line)
                round_log_entry = PlayerRoundLogTrumpEntrySerializer.entry_from_dict(line_dict)
                entries.append(round_log_entry)
        return entries

