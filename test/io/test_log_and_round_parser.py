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
        rnds = log_parser.parse_rounds_all()

        for rnd_all in rnds:
            rnd = rnd_all['round']
            date = rnd_all['date']
            players = rnd_all['players']
            generated_dict = RoundGenerator.generate_dict_all(rnd, date, players)

            rnd_parsed, date_parsed, players_parsed = RoundParser.parse_round_all(generated_dict)

            self.assertEqual(rnd, rnd_parsed)
            self.assertEqual(date, date_parsed)
            self.assertEqual(players, players_parsed)


if __name__ == '__main__':
    unittest.main()
