# Filter Players
# Mean points
# STD
# functionality: filter by points, filter by STD, combination of both, percentage of players
# fill
import argparse
import glob
import os
import sys

sys.path.insert(0, './source')
sys.path.insert(0, '../source')

from player_id_filter import *
from jass.io.player_round_log_parser import PlayerRoundLogParser

PREFIX_FILENAME = "filtered_"

# >python tools\player_round_log_filter.py -src tools/player_logs.txt -dest tools/ -statfile tools/player_all_
# stat.json -mean_abs 75 -mean_best_perc 0.5 -played_ga
# mes_abs 30 -std_abs 90 -std_best_perc 0.5 -played_games_most_perc 0.1
class PlayerRoundLogFilter:

    def __init__(self, source: str, destination: str, player_filter, directory=False, recursive=False):
        self.player_log_parser = PlayerRoundLogParser()
        self.player_filter = player_filter

        print("###################################################################################")
        print("Evaluates player ids to keep if this filter is used")
        print("NOTE: No file has been filtered yet. To use the filter, call the method 'filter'")
        print("###################################################################################")
        self.filtered_players = self.player_filter.filter()
        self.source = source
        self.destination = destination
        self.search_directory = directory
        self.recursive_search = recursive

    def filter(self):
        """
        Parses the swiss los logs at the given directory and saves them as player round logs in the given destination
        :return:
        """
        print("###################################################################################")
        print("Started filtering")
        if self.recursive_search:
            self._filter_directory_recursive()
        elif self.search_directory:
            self._filter_directory(self.source, self.destination + "\\")
        else:
            self._filter_file(self.source, self.destination)

        print("Finished filtering")
        print("###################################################################################")

    def _filter_directory_recursive(self):
        # os.walk returns a tuple, the first element is the complete directory path
        directories = [directory[0] for directory in os.walk(self.source)]

        # The first element is always empty (it points to the initial directory) with the initial source
        directories[0] = self.source
        number_of_directories = len(directories)

        for i, directory in enumerate(directories):
            print("-----------------")
            print("filtering directory (" + str(i + 1) + "/" + str(number_of_directories) + ")")
            subdirectory = directory.replace(self.source, '')
            self._filter_directory(directory, self.destination + subdirectory + "\\")

    def _filter_directory(self, source_directory, destination_directory):
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        if not os.path.isabs(source_directory):
            source_directory = os.getcwd() + "\\" + source_directory
        if not os.path.isabs(destination_directory):
            destination_directory = os.getcwd() + "\\" + destination_directory

        # os.chdir(source_directory)
        files = glob.glob(source_directory + "\\*.txt")
        number_of_files = len(files)
        for i, file in enumerate(files):
            print("filtering file " + file + " (" + str(i + 1) + "/" + str(number_of_files) + ")")
            self._filter_file(file, destination_directory)

    def _filter_file(self, file_path_name: str, destination_directory: str):
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        filename = os.path.basename(file_path_name)
        output_file = ""
        with open(file_path_name) as file:
            for line in file:
                player = self.player_log_parser.get_player_from_log_line(line)
                if player in self.filtered_players:
                    output_file += line

        output_filename = destination_directory + PREFIX_FILENAME + filename
        with open(output_filename, 'w') as file:
            file.write(output_file)
        # save file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='argparse for log conversion to player round')

    parser.add_argument('-src', help='Single log (no special command) or folder (--dir or --r) containing logs '
                                     'to convert. Absolute paths and relative paths to the work directory (not '
                                     'necessarily script directory) work')
    parser.add_argument('-dest', help='Directory, where the logs will be saved. Filename is automatically generated. '
                                      'Absolute paths and relative paths to the work directory (not '
                                      'necessarily script directory) work')
    parser.add_argument('-statfile', help='Filename (including path) to the statistic json file to be used.')

    parser.add_argument('--dir', dest='search_directory', action='store_const',
                        const=True, default=False,
                        help='Converts all the files in a directory (default: only one file)')

    parser.add_argument('--r', dest='recursive_file_search', action='store_const',
                        const=True, default=False,
                        help='Searches all sub folders as well as the given directory.')

    parser.add_argument('-mean_abs', default=0, type=float, help='only writes out moves from players with a mean'
                                                                        'equal or above the given parameter')

    parser.add_argument('-mean_best_perc', default=0, type=float,
                        help='only writes out moves from the best percentage of players measured by the mean.'
                                '0.2 writes out the best 20%% of players. Must be between 0 and 1.')

    parser.add_argument('-std_abs', type=float, default=0,
                        help='only writes out moves from players with a standard deviation equal or --BELOW-- the '
                             'given parameter')

    parser.add_argument('-std_best_perc', type=float, default=0,
                        help='0.2 writes out the 20%% of players with the LOWEST standard deviation. '
                             'Must be between 0 and 1.')

    parser.add_argument('-played_games_abs', type=float, default=0,
                        help='only writes out players with equal or more games played then the parameter')

    parser.add_argument('-played_games_most_perc', type=float, default=0,
                        help='0.2 wirtes out the 20%% of players with the most played games. Must be between 0 and 1.')

    args = parser.parse_args()

    player_filter = PlayerStatFilter(args.statfile)
    if args.mean_abs != 0:
        player_filter.add_filter(FilterMeanAbsolute(args.mean_abs))

    if args.mean_best_perc != 0:
        player_filter.add_filter(FilterMeanRelative(1 - args.mean_best_perc))

    if args.std_abs != 0:
        player_filter.add_filter(FilterStdAbsolute(args.std_abs))

    if args.std_best_perc != 0:
        player_filter.add_filter(FilterStdRelative(1 - args.std_best_perc))

    if args.played_games_abs != 0:
        player_filter.add_filter(FilterPlayedGamesAbsolute(args.played_games_abs))

    if args.played_games_most_perc != 0:
        player_filter.add_filter(FilterPlayedGamesRelative(1 - args.played_games_most_perc))

    log_filter = PlayerRoundLogFilter(source=args.src, destination=args.dest, player_filter=player_filter,
                                      directory=args.search_directory, recursive=args.recursive_file_search)
    log_filter.filter()
