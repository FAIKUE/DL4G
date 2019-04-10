import argparse
import glob
import json
import os

from jass.base.const import *
from jass.base.player_round import PlayerRound
from jass.io.log_parser import LogParser


class PlayerRoundLogGenerator:
    """
    Generate Player Round logs from Swisslos Logs
    Can be called via command line

    Parse one file:
    python player_round_log_generator.py -src ..\\..\\..\\test\\resources\\log.txt -dest .\\results

    Parse one folder:
    python player_round_log_generator.py -src ..\\..\\..\\test\\resources -dest .\\results --dir

    Parse folders recursively:
    python player_round_log_generator.py -src ..\\..\\..\\test\\resources -dest .\\results --dir --recursive
    """
    def __init__(self, source: str, destination: str, directory=False, recursive=False):
        self.source = source
        self.destination = destination
        self.search_directory = directory
        self.recursive_search = recursive

    def parse(self):
        """
        Parses the swiss los logs at the given directory and saves them as player round logs in the given destination
        :return:
        """
        if self.search_directory and self.recursive_search:
            self._parse_directory_recursive()
        elif self.search_directory:
            self._parse_directory(self.source, self.destination + "\\")
        else:
            self._parse_file(self.source, self.destination)

    def _parse_directory_recursive(self):
        # os.walk returns a tuple, the first element is the complete directory path
        directories = [directory[0] for directory in os.walk(self.source)]
        # The first element is always empty (it points to the initial directory) It is replaced with "\\"
        # so that it is consistent in its syntax with the other list elements
        directories[0] = "\\"
        for directory in directories:
            print(directory)
            subdirectory = directory.replace(self.source, '')
            self._parse_directory(directory, self.destination + subdirectory)

    def _parse_directory(self, source_directory, destination_directory):
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        os.chdir(source_directory)
        for file in glob.glob("*.txt"):
            print(file)
            self._parse_file(source_directory + "\\" + file, destination_directory)
            break

    def _parse_file(self, file_path_name: str, destination_directory: str):
        filename = os.path.basename(file_path_name)
        log_parser = LogParser(file_path_name)
        rounds_with_player = log_parser.parse_rounds_and_players()
        player_round_dictionaries = self._rounds_to_player_rounds_dict(rounds_with_player)
        self._generate_logs(player_round_dictionaries, destination_directory + "\player_round_" + filename)

    def _rounds_to_player_rounds_dict(self, rounds: [dict]):
        player_rounds = self._rounds_to_player_rounds(rounds)
        player_round_dicts = []
        for rnd in player_rounds:
            player_round_dicts.append(self._dict_from_round(rnd))

        return player_round_dicts

    def _rounds_to_player_rounds(self, rounds: [dict]) -> [dict]:
        player_rounds = []
        for rnd in rounds:
            player_rounds += self._round_to_player_rounds(rnd)

        return player_rounds

    @staticmethod
    def _round_to_player_rounds(rnd) -> [PlayerRound]:
        return [dict(round=player_round, players=rnd["players"]) for player_round
                in PlayerRound.all_from_complete_round(rnd["round"])]

    @staticmethod
    def _dict_from_round(round_dict: dict) -> {}:
        player_round = round_dict["round"]
        player_ids = round_dict["players"]
        player_round_dict = dict()
        player_round_dict["dealer"] = player_round.dealer
        player_round_dict["declaredtrump"] = player_round.declared_trump
        player_round_dict["trump"] = player_round.trump
        player_round_dict["forehand"] = player_round.forehand
        player_round_dict["pointsteamown"] = int(player_round.points_team_own)
        player_round_dict["pointsteamopponent"] = int(player_round.points_team_opponent)
        player_round_dict["nrplayedcards"] = player_round.nr_played_cards
        player_round_dict["player"] = int(player_round.player)
        player_round_dict["player_id"] = player_ids[player_round.player]
        player_round_dict["hand"] = convert_one_hot_encoded_cards_to_str_encoded_list(player_round.hand)
        player_round_dict["nrcardsintrick"] = player_round.nr_cards_in_trick
        player_round_dict["currenttrick"] = [card_strings[card] for card in player_round.current_trick if card != -1]
        PlayerRoundLogGenerator._add_tricks_to_dict(player_round, player_round_dict)

        return player_round_dict

    @staticmethod
    def _add_tricks_to_dict(player_round, player_round_dict):
        player_round_dict["tricks"] = []
        for i in range(0, int(player_round.nr_played_cards / 4)):
            player_round_dict["tricks"].append(dict(
                cards=[card_strings[card] for card in player_round.tricks[i]],
                points=int(player_round.trick_points[i]),
                win=int(player_round.trick_winner[i]),
                first=int(player_round.trick_first_player[i])
            ))

    @staticmethod
    def _generate_logs(player_rounds_dict, filename):
        file = open(filename, 'w')
        for player_round in player_rounds_dict:
            json.dump(player_round, file, separators=(',', ':'))
            file.write('\n')
        file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='argparse for log conversion to player round')
    parser.add_argument('-src', help='Single log or folder containing logs to convert')
    parser.add_argument('-dest', help='Directory, where the logs will be saved. Filename is automatically generated.')
    parser.add_argument('--dir', dest='search_directory', action='store_const',
                        const=True, default=False,
                        help='Converts all the files in a directory (default: only one file)')
    parser.add_argument('--r', dest='recursive_file_search', action='store_const',
                        const=True, default=False,
                        help='Searches all sub folders as well (has no effect if --dir is not used as well)')
    args = parser.parse_args()
    parser = PlayerRoundLogGenerator(args.src, args.dest, args.search_directory, args.recursive_file_search)
    parser.parse()

