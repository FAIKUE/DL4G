# HSLU
#
# Created by Thomas Koller on 15.07.19
#
import json
from datetime import datetime
from jass.io.round_log_entry import RoundLogEntry
from jass.io.round_serializer import RoundSerializer, DATE_FORMAT


class RoundLogEntrySerializer:
    """
    Read and write RoundLogEntry objects from dict.
    """
    @staticmethod
    def round_log_entry_to_dict(round_log_entry: RoundLogEntry) -> dict:
        """
        Generate the dict for an entry.
        Args:
            round_log_entry: log entry for which to generate the dict

        Returns:
            dict to contain the log entry
        """
        return dict(
            round=RoundSerializer.round_to_dict(round_log_entry.rnd),
            date=datetime.strftime(round_log_entry.date, DATE_FORMAT),
            player_ids=round_log_entry.player_ids)

    @staticmethod
    def round_log_entry_from_dict(entry_dict: dict) -> RoundLogEntry:
        """
        Create a round log entry from a dict
        Args:
            entry_dict:

        Returns:
            new round log entry
        """
        date = datetime.strptime(entry_dict['date'], DATE_FORMAT)
        rnd = RoundSerializer.round_from_dict(entry_dict['round'])
        player_ids = entry_dict['player_ids']
        return RoundLogEntry(rnd=rnd, date=date, player_ids=player_ids)

    @staticmethod
    def round_log_entries_from_file(filename: str) -> [RoundLogEntry]:
        """
        Read round log entries
        Args:
            filename: name for the file to read from

        Returns:
            Array or log entries
        """
        entries = []
        with open(filename, mode='r') as file:
            for line in file:
                line_dict = json.loads(line)
                round_log_entry = RoundLogEntrySerializer.round_log_entry_from_dict(line_dict)
                entries.append(round_log_entry)
        return entries

