# HSLU
#
# Created by Thomas Koller on 18.09.19
#
"""
Read input files that contain complete Rounds and output a csv file containing the information for trump.

The output format is:
 - hand of the player
 - 0/1 if the action was forehand or not
 - player id of the player making the action (optional)
 - the action
"""
import csv
import os
import argparse
import logging

from jass.base.const import PUSH_ALT, next_player, partner_player
from jass.base.player_round import PlayerRound
from jass.ion.round_log_entry_serializer import RoundLogEntrySerializer


def generate_logs_trump(files, output_dir: str, add_player_id: bool = False):
    os.makedirs(output_dir, exist_ok=True)
    logger = logging.getLogger(__name__)

    nr_entries_read = 0
    nr_entries_written = 0
    for file_in in files:
        logger.info('Reading file: {}'.format(file_in))

        # open a file for each input file and write it to the output directory
        basename = os.path.basename(file_in)
        basename, _ = os.path.splitext(basename)
        filename = basename + '.csv'
        filename = os.path.join(output_dir, filename)

        with open(filename, mode='w', newline='') as file_out:
            csv_writer = csv.writer(file_out)

            entries = RoundLogEntrySerializer.round_log_entries_from_file(file_in)
            for entry in entries:
                nr_entries_read += 1

                # feature for first trump action
                player_rnd = PlayerRound.trump_from_complete_round(entry.rnd, forehand=True)
                entry_csv = player_rnd.hand.tolist()

                player = next_player[entry.rnd.dealer]
                if entry.rnd.forehand:
                    # add a boolean (1) for forehand
                    entry_csv.append(1)
                    if add_player_id:
                        entry_csv.append(entry.player_ids[player])
                    entry_csv.append(entry.rnd.trump)
                else:
                    entry_csv.append(0)
                    if add_player_id:
                        entry_csv.append(entry.player_ids[player])
                    entry_csv.append(PUSH_ALT)
                nr_entries_written += 1
                csv_writer.writerow(entry_csv)

                # feature for second trump action
                if not entry.rnd.forehand:
                    player_rnd = PlayerRound.trump_from_complete_round(entry.rnd, forehand=False)
                    player = partner_player[next_player[entry.rnd.dealer]]
                    entry_csv = player_rnd.hand.tolist()
                    entry_csv.append(0)
                    if add_player_id:
                        entry_csv.append(entry.player_ids[player])
                    entry_csv.append(entry.rnd.trump)
                    nr_entries_written += 1
                    csv_writer.writerow(entry_csv)

    print('Entries read: {}'.format(nr_entries_read))
    print('Entries written: {}'.format(nr_entries_written))


def main():
    parser = argparse.ArgumentParser(description='Convert files with rounds to csv for trump')
    parser.add_argument('--output_dir', type=str, help='Directory for output files', default='')
    parser.add_argument('--id', action='store_true', help='Set if player ids should be in the log file')

    parser.add_argument('files', type=str, nargs='+', help='The input files')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    generate_logs_trump(args.files, args.output_dir, args.id)


if __name__ == '__main__':
    main()
