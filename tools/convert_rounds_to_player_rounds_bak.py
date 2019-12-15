import argparse
from source.jass.ion.player_round_log_generator import PlayerRoundLogGenerator

PREFIX_CHEATING_FILENAME = "\player_round_cheating_"

PREFIX_FILENAME = "\player_round_"

def main():
    parser = argparse.ArgumentParser(description='argparse for log conversion to player round')
    parser.add_argument('--src', help='Single log (no special command) or folder (--dir or --r) containing logs '
                                     'to convert. Absolute paths and relative paths to the work directory (not '
                                     'necessarily script directory) work',
                        required=True)
    parser.add_argument('--dest', help='Directory, where the logs will be saved. Filename is automatically generated. '
                                      'Absolute paths and relative paths to the work directory (not '
                                      'necessarily script directory) work', required=True)
    parser.add_argument('--dir', dest='search_directory', action='store_const',
                        const=True, default=False,
                        help='Converts all the files in a directory (default: only one file)')
    parser.add_argument('--r', dest='recursive_file_search', action='store_const',
                        const=True, default=False,
                        help='Searches all sub folders as well as the given directory.')
    parser.add_argument('--cheating', dest='cheating', action='store_const',
                        const=True, default=False,
                        help='generates cheating player logs, all players hands are saved in ADDITION to the current '
                             'players hand (redundant information, this way cheating player logs can still be '
                             'parsed to player logs)')

    args = parser.parse_args()

    log_generator = PlayerRoundLogGenerator(args.src, args.dest, args.search_directory,
                                            args.recursive_file_search, args.cheating)
    log_generator.generate()


if __name__ == '__main__':
   main()
