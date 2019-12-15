# HSLU
#
# Created by Thomas Koller on 18.07.19
#
import os
import logging
import argparse

from source.jass.base.const import next_player, same_team, PUSH_ALT
from source.jass.base.label_play import LabelPlay
from source.jass.base.label_trump import LabelTrump
from source.jass.base.player_round import PlayerRound
from source.jass.base.round_utils import calculate_starting_hands_from_round
from source.jass.ion.log_entries import PlayerRoundLogEntry, PlayerRoundTrumpLogEntry
from source.jass.ion.log_entry_file_generator import LogEntryFileGenerator
from source.jass.ion.player_round_log_entry_serializer import PlayerRoundLogEntrySerializer, PlayerRoundLogTrumpEntrySerializer
from source.jass.ion.round_log_entry_serializer import RoundLogEntrySerializer


def generate_logs(files, output: str, output_dir: str, max_rounds: int):
    os.makedirs(output_dir, exist_ok=True)
    basename = os.path.join(output_dir, output)

    logger = logging.getLogger(__name__)

    nr_entries_read = 0
    nr_entries_written = 0
    # Generator will split the output into files
    with LogEntryFileGenerator(basename, max_entries=max_rounds, shuffle=True) as generator:
        for file in files:
            logger.info('Reading file: {}'.format(file))
            entries = RoundLogEntrySerializer.round_log_entries_from_file(file)
            for entry in entries:
                nr_entries_read += 1
                player_rounds = PlayerRound.all_from_complete_round(entry.rnd)
                hands = calculate_starting_hands_from_round(entry.rnd)
                for card_id, player_rnd in enumerate(player_rounds):
                    # look at the trick information for the next card
                    trick = card_id % 4 + 1
                    trick_winner = entry.rnd.trick_winner[trick]
                    if same_team[player_rnd.player, trick_winner]:
                        points_in_trick_own = entry.rnd.trick_points[trick]
                        points_in_trick_other = 0
                    else:
                        points_in_trick_own = 0
                        points_in_trick_other = entry.rnd.trick_points[trick]
                    label = LabelPlay(
                        card_played=entry.rnd.get_card_played(card_id),
                        points_in_trick_own=points_in_trick_own,
                        points_in_trick_other=points_in_trick_other,
                        trick_winner=trick_winner,
                        points_in_round_own=entry.rnd.get_points_for_player(player_rnd.player),
                        points_in_round_other=entry.rnd.get_points_for_player(next_player[player_rnd.player]),
                        hands=hands)
                    entry_new = PlayerRoundLogEntry(player_rnd=player_rnd,
                                                    date=entry.date,
                                                    player_id=entry.player_ids[player_rnd.player],
                                                    label=label)
                    entry_new_dict = PlayerRoundLogEntrySerializer.entry_to_dict(entry_new)
                    nr_entries_written += 1
                    generator.add_entry(entry_new_dict)
    print('Entries read: {}'.format(nr_entries_read))
    print('Entries written: {}'.format(nr_entries_written))


def generate_logs_trump(files, output: str, output_dir: str, max_rounds: int):
    os.makedirs(output_dir, exist_ok=True)
    basename = os.path.join(output_dir, output)

    logger = logging.getLogger(__name__)

    nr_entries_read = 0
    nr_entries_written = 0
    # Generator will split the output into files
    with LogEntryFileGenerator(basename, max_entries=max_rounds, shuffle=True) as generator:
        for file in files:
            logger.info('Reading file: {}'.format(file))
            entries = RoundLogEntrySerializer.round_log_entries_from_file(file)
            for entry in entries:
                nr_entries_read += 1

                # feature for first trump action
                player_rnd = PlayerRound.trump_from_complete_round(entry.rnd, forehand=True)
                if entry.rnd.forehand:
                    label = LabelTrump(entry.rnd.trump)
                else:
                    label = LabelTrump(PUSH_ALT)

                entry_new = PlayerRoundTrumpLogEntry(player_rnd=player_rnd,
                                                     date=entry.date,
                                                     player_id=entry.player_ids[player_rnd.player],
                                                     label=label)
                entry_new_dict = PlayerRoundLogTrumpEntrySerializer.entry_to_dict(entry_new)
                nr_entries_written += 1
                generator.add_entry(entry_new_dict)

                # feature for second trump action
                if not entry.rnd.forehand:
                    player_rnd = PlayerRound.trump_from_complete_round(entry.rnd, forehand=False)
                    label = LabelTrump(entry.rnd.trump)
                    entry_new = PlayerRoundTrumpLogEntry(player_rnd=player_rnd,
                                                         date=entry.date,
                                                         player_id=entry.player_ids[player_rnd.player],
                                                         label=label)
                    entry_new_dict = PlayerRoundLogTrumpEntrySerializer.entry_to_dict(entry_new)
                    nr_entries_written += 1
                    generator.add_entry(entry_new_dict)
    print('Entries read: {}'.format(nr_entries_read))
    print('Entries written: {}'.format(nr_entries_written))


def main():
    parser = argparse.ArgumentParser(description='Convert files with rounds to player rounds')
    parser.add_argument('--trump', action='store_true', help='Generate player rounds for trump decision')
    parser.add_argument('--output', type=str, help='Base name of the output files', default='')
    parser.add_argument('--output_dir', type=str, help='Directory for output files', default='')
    parser.add_argument('--max_rounds', type=int, default=100000, help='Maximal number of rounds in one file')
    parser.add_argument('files', type=str, nargs='+', help='The log files')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    if args.trump:
        generate_logs_trump(args.files, args.output, args.output_dir, args.max_rounds)
    else:
        generate_logs(args.files, args.output, args.output_dir, args.max_rounds)


if __name__ == '__main__':
    main()
