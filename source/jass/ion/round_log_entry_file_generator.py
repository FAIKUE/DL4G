# Copyright 2019 HSLU. All Rights Reserved.
#
# Created by Thomas Koller on 28.02.19
#
#
import json
import random
import logging

from jass.ion.log_entries import RoundLogEntry
from jass.ion.round_log_entry_serializer import RoundLogEntrySerializer


class RoundLogEntryFileGenerator:
    """
    Create a file of log entries with each entry in a separate line of the file. Files are split to contain
    no more than the indicated max_entries lines. Entries are first collected into a buffer and shuffled
    before writing.

    The class should be used as a context manager within "with" in python
    """
    EXTENSION = '.txt'

    def __init__(self, basename: str, max_entries: int, max_buffer: int=10000):
        """
        Initialize the generator.

        Args:
            basename: basename of the generated files, this should include the whole file path
            max_entries: maximal entries per file
            max_buffer: size of the buffer that will be shuffled
        """
        self._basename = basename
        self._extension = RoundLogEntryFileGenerator.EXTENSION
        self._max_entries = max_entries
        self._max_buffer = max_buffer
        self._current_file_number = 0
        self._nr_lines_in_file = 0

        self._file = None
        self._buffer = []

    def __enter__(self):
        """
        Start of context region.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        End of context region, writes the buffer and closes the file.
        """
        if len(self._buffer) > 0:
            self._write_buffer()
        if self._file is not None:
            self._file.close()

    def _open_new_file(self):
        if self._file is not None:
            self._file.close()
        self._current_file_number += 1
        filename = self._basename + '{:02d}'.format(self._current_file_number) + self._extension
        logging.getLogger(__name__).info('Writing file: {}'.format(filename))
        self._file = open(filename, mode='w')
        self._nr_lines_in_file = 0

    def _write_buffer(self):
        random.shuffle(self._buffer)
        for line in self._buffer:
            if self._nr_lines_in_file >= self._max_entries or self._file is None:
                self._open_new_file()

            self._file.write(line)
            self._file.write('\n')
            self._nr_lines_in_file += 1
        self._buffer.clear()

    def add_entry(self, rnd_log_entry: RoundLogEntry) -> None:
        """
        Add an entry to the file
        Args:
            rnd_log_entry: entry to add
        """
        rounds_dict = RoundLogEntrySerializer.round_log_entry_to_dict(rnd_log_entry)
        line = json.dumps(rounds_dict, separators=(',', ':'))
        self._buffer.append(line)
        if len(self._buffer) > self._max_buffer:
            self._write_buffer()
