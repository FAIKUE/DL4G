import logging
import unittest

from jass.io.log_parser import LogParser
from jass.io.round_generator import RoundGenerator
from jass.io.round_parser import RoundParser


class LogRoundParserTestCase(unittest.TestCase):
    def test_parser_and_generator(self):
        # read a log file and convert it
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        log_parser = LogParser('../resources/small_log.txt')
        rnd_log_entries = log_parser.parse_rounds()

        for rnd_log_entry in rnd_log_entries:
            generated_dict = RoundGenerator.generate_dict_all(rnd_log_entry.rnd, rnd_log_entry.date, rnd_log_entry.players)

            rnd_parsed, date_parsed, players_parsed = RoundParser.parse_round_all(generated_dict)

            self.assertEqual(rnd_log_entry.rnd, rnd_parsed)
            self.assertEqual(rnd_log_entry.date, date_parsed)
            self.assertEqual(rnd_log_entry.players, players_parsed)


if __name__ == '__main__':
    unittest.main()
