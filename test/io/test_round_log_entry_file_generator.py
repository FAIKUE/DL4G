import unittest
import logging
import os.path

from source.jass.ion.log_parser_swisslos import LogParserSwisslos
from source.jass.ion.round_log_entry_file_generator import RoundLogEntryFileGenerator
from source.jass.ion.round_log_entry_serializer import RoundLogEntrySerializer

TEST_FILE_IN = '../resources/small_log.txt'
TEST_FILE_OUT = '__test_'


class RoundLogEntryFileGeneratorTestCase(unittest.TestCase):
    def test_parser_and_generator(self):
        # read a log file from swisslos and convert it
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        rnd_log_entries = LogParserSwisslos.parse_rounds(TEST_FILE_IN)
        total_entries = len(rnd_log_entries)

        max_entries = 4
        with RoundLogEntryFileGenerator(TEST_FILE_OUT, max_entries=max_entries) as file:
            for rnd_log_entry in rnd_log_entries:
                file.add_entry(rnd_log_entry)

        # check if files have been generated and can be read
        number_of_files = total_entries // max_entries
        if total_entries % max_entries != 0:
            number_of_files += 1

        for i in range(number_of_files):
            filename = '{}{:02d}{}'.format(TEST_FILE_OUT, i+1, RoundLogEntryFileGenerator.EXTENSION)
            self.assertTrue(os.path.exists(filename))

            entries = RoundLogEntrySerializer.round_log_entries_from_file(filename)
            if i == number_of_files-1:
                self.assertEqual(total_entries % max_entries, len(entries))
            else:
                self.assertEqual(max_entries, len(entries))
            os.remove(filename)


if __name__ == '__main__':
    unittest.main()
