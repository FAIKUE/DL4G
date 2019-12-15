# HSLU
#
# Created by Thomas Koller on 03.02.2019
#

import argparse
import os

import numpy as np
from source.jass.ion.log_entry_file_generator import LogEntryFileGenerator
from source.jass.ion.round_log_entry_serializer import RoundLogEntrySerializer
from source.jass.ion.log_parser_swisslos import LogParserSwisslos


def main():
    parser = argparse.ArgumentParser(description='Read log files and convert them to train, val and test files')
    parser.add_argument('--output', type=str, help='Base name of the output files', default='')
    parser.add_argument('--output_dir', type=str, help='Directory for output files')
    parser.add_argument('--train_split', type=float, default=0.4, help='Percentage of train data')
    parser.add_argument('--val_split', type=float, default=0.4, help='Percentage of validation data')
    parser.add_argument('--test_split', type=float, default=0.2, help='Percentage of test data')
    parser.add_argument('--seed', type=int, default=42, help='Seed for random number generator')
    parser.add_argument('--max_rounds', type=int, default=50000, help='Maximal number of rounds in one file')
    parser.add_argument('files', type=str, nargs='+', help='The log files')
    arg = parser.parse_args()

    if arg.output_dir is not None:
        if not os.path.exists(arg.output_dir):
            print('Creating directory {}'.format(arg.output_dir))
            os.makedirs(arg.output_dir)
        basename = os.path.join(arg.output_dir, arg.output)
    else:
        basename = arg.output

    nr_train = 0
    nr_val = 0
    nr_test = 0
    nr_total = 0
    prob = [arg.train_split, arg.val_split, arg. test_split]
    np.random.seed(arg.seed)

    with LogEntryFileGenerator(basename + 'train_', arg.max_rounds) as train, \
            LogEntryFileGenerator(basename + 'val_', arg.max_rounds) as val, \
            LogEntryFileGenerator(basename + 'test_', arg.max_rounds) as test:
        for f in arg.files:
            log_entries = LogParserSwisslos.parse_rounds(f)
            nr_total += len(log_entries)

            for entry in log_entries:
                entry_data = RoundLogEntrySerializer.round_log_entry_to_dict(entry)
                set_chosen = np.random.choice(3, p=prob)
                if set_chosen == 0:
                    train.add_entry(entry_data)
                    nr_train += 1
                elif set_chosen == 1:
                    val.add_entry(entry_data)
                    nr_val += 1
                elif set_chosen == 2:
                    test.add_entry(entry_data)
                    nr_test += 1

                _print_progress(nr_total)

    print('Train: {}\tVal: {}\tTest: {}\tTotal: {}'.format(nr_train, nr_val, nr_test, nr_total))


def _print_progress(nr_rounds):
    if nr_rounds % 1000 == 0:
        print('.', end='', flush=True)
    if nr_rounds % 100000 == 0:
        # new line
        print('')


if __name__ == '__main__':
    main()

