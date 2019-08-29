# HSLU
#
# Created by Thomas Koller on 18.07.19
#
import argparse
import os
import logging
import json

from jass.io.log_entry_file_generator import LogEntryFileGenerator
from jass.io.player_id_filter import PlayerStatFilter, FilterMeanAbsolute, FilterMeanRelative, FilterStdAbsolute, \
    FilterStdRelative, FilterPlayedGamesAbsolute, FilterPlayedGamesRelative


def filter_player_round_logs(files:[str],
                             stat_filter: PlayerStatFilter,
                             output: str,
                             output_dir: str,
                             max_rounds: int):
    os.makedirs(output_dir, exist_ok=True)
    basename = os.path.join(output_dir, output)

    logger = logging.getLogger(__name__)

    player_ids_ok = stat_filter.filter()

    nr_entries_read = 0
    nr_entries_written = 0
    # Generator will split the output into files
    with LogEntryFileGenerator(basename, max_entries=max_rounds) as generator:
        for file_name in files:
            logger.info('Reading file: {}'.format(file_name))
            with open(file_name, mode='r') as file:
                for line in file:
                    nr_entries_read += 1
                    line_dict = json.loads(line)
                    # we do not actually need to reconstruct the  PlayerRoundLogEntry object, as we will just
                    # write out the line as we get it
                    player_id = line_dict['player_id']
                    if player_id in player_ids_ok:
                        nr_entries_written += 1
                        # add line without the last character, which is the newline
                        generator.add_entry_line(line[:-1])
    print('Entries read: {}'.format(nr_entries_read))
    print('Entries written: {}'.format(nr_entries_written))


def main():
    parser = argparse.ArgumentParser(description='Filter player rounds according to statistics')

    parser.add_argument('--output', type=str, help='Base name of the output files', default='')
    parser.add_argument('--output_dir', type=str, help='Directory for output files', default='')
    parser.add_argument('--max_rounds', type=int, default=100000, help='Maximal number of rounds in one file')
    parser.add_argument('--stat', help='filename json file containing the statistics.',
                        required=True)
    parser.add_argument('files', type=str, nargs='+', help='The player round log files')

    parser.add_argument('--mean_abs', type=float, help='only writes out moves from players with a mean'
                                                      'equal or above the given parameter')

    parser.add_argument('--mean_best_perc', type=float,
                        help='only writes out moves from the best percentage of players measured by the mean.'
                             '0.2 writes out the best 20%% of players. Must be between 0 and 1.')

    parser.add_argument('--std_abs', type=float,
                        help='only writes out moves from players with a standard deviation equal or --BELOW-- the '
                             'given parameter')

    parser.add_argument('--std_best_perc', type=float,
                        help='0.2 writes out the 20%% of players with the LOWEST standard deviation. '
                             'Must be between 0 and 1.')

    parser.add_argument('--played_games_abs', type=float,
                        help='only writes out players with equal or more games played then the parameter')

    parser.add_argument('--played_games_most_perc', type=float,
                        help='0.2 writes out the 20%% of players with the most played games. Must be between 0 and 1.')

    args = parser.parse_args()

    player_filter = PlayerStatFilter(args.stat)
    if args.mean_abs:
        player_filter.add_filter(FilterMeanAbsolute(args.mean_abs))

    if args.mean_best_perc:
        player_filter.add_filter(FilterMeanRelative(1 - args.mean_best_perc))

    if args.std_abs:
        player_filter.add_filter(FilterStdAbsolute(args.std_abs))

    if args.std_best_perc:
        player_filter.add_filter(FilterStdRelative(1 - args.std_best_perc))

    if args.played_games_abs:
        player_filter.add_filter(FilterPlayedGamesAbsolute(args.played_games_abs))

    if args.played_games_most_perc:
        player_filter.add_filter(FilterPlayedGamesRelative(1 - args.played_games_most_perc))

    filter_player_round_logs(args.files, player_filter, args.output, args.output_dir, args.max_rounds)
if __name__ == '__main__':
    main()

