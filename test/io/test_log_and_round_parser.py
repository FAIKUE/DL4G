import logging
import unittest

from jass.io.log_parser_swisslos import LogParserSwisslos
from jass.io.round_log_entry_serializer import RoundLogEntrySerializer

TEST_FILE = '../resources/small_log.txt'


class LogRoundParserTestCase(unittest.TestCase):
    def test_parser_and_generator(self):
        # read a log file from swisslos and convert it
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        rnd_log_entries = LogParserSwisslos.parse_rounds(TEST_FILE)

        for rnd_log_entry in rnd_log_entries:
            generated_dict = RoundLogEntrySerializer.round_log_entry_to_dict(rnd_log_entry)

            rnd_log_entry_parsed = RoundLogEntrySerializer.round_log_entry_from_dict(generated_dict)

            self.assertEqual(rnd_log_entry.rnd, rnd_log_entry_parsed.rnd)
            self.assertEqual(rnd_log_entry.date, rnd_log_entry_parsed.date)
            self.assertEqual(rnd_log_entry.player_ids, rnd_log_entry.player_ids)


if __name__ == '__main__':
    unittest.main()
