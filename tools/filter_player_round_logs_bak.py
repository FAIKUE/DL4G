import argparse

from jass.ion.player_id_filter import FilterPlayedGamesRelative, FilterPlayedGamesAbsolute, FilterStdRelative, \
    FilterStdAbsolute, FilterMeanRelative, FilterMeanAbsolute, PlayerStatFilter
from jass.ion.player_round_log_filter import PlayerRoundLogFilter


PREFIX_FILENAME = "filtered_"

# >python tools\player_round_log_filter.py -src tools/player_logs.txt -dest tools/ -statfile tools/player_all_
# stat.json -mean_abs 75 -mean_best_perc 0.5 -played_ga
# mes_abs 30 -std_abs 90 -std_best_perc 0.5 -played_games_most_perc 0.1


def main():
    parser = argparse.ArgumentParser(description='argparse for log conversion to player round')

    parser.add_argument('--src', help='Single log (no special command) or folder (--dir or --r) containing logs '
                                     'to convert. Absolute paths and relative paths to the work directory (not '
                                     'necessarily script directory) work',
                        required=True)
    parser.add_argument('--dest', help='Directory, where the logs will be saved. Filename is automatically generated. '
                                      'Absolute paths and relative paths to the work directory (not '
                                      'necessarily script directory) work',
                        required=True)
    parser.add_argument('--stat', help='Filename (including path) to the statistic json file to be used.',
                        required=True)

    parser.add_argument('--dir', dest='search_directory', action='store_const',
                        const=True, default=False,
                        help='Converts all the files in a directory (default: only one file)')

    parser.add_argument('--r', dest='recursive_file_search', action='store_const',
                        const=True, default=False,
                        help='Searches all sub folders as well as the given directory.')

    parser.add_argument('-mean_abs', type=float, help='only writes out moves from players with a mean'
                                                                        'equal or above the given parameter')

    parser.add_argument('-mean_best_perc', type=float,
                        help='only writes out moves from the best percentage of players measured by the mean.'
                                '0.2 writes out the best 20%% of players. Must be between 0 and 1.')

    parser.add_argument('-std_abs', type=float,
                        help='only writes out moves from players with a standard deviation equal or --BELOW-- the '
                             'given parameter')

    parser.add_argument('-std_best_perc', type=float,
                        help='0.2 writes out the 20%% of players with the LOWEST standard deviation. '
                             'Must be between 0 and 1.')

    parser.add_argument('-played_games_abs', type=float,
                        help='only writes out players with equal or more games played then the parameter')

    parser.add_argument('-played_games_most_perc', type=float,
                        help='0.2 wirtes out the 20%% of players with the most played games. Must be between 0 and 1.')

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

    log_filter = PlayerRoundLogFilter(source=args.src, destination=args.dest, player_filter=player_filter,
                                      directory=args.search_directory, recursive=args.recursive_file_search)
    log_filter.filter()


if __name__ == '__main__':
    main()