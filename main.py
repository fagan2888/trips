#!/usr/bin/python3

# Running from 2018-11-18 (start of November TTC board period) to now

# Usage: start epoch should reflect a period in which no trips are in-progress for the period
# you wish to measure (eg. one full weekday).
# It should be before regular service (5:30am weekdays for the TTC) is scheduled, but after
# the last night bus is scheduled to start (usually about 5:20am for the TTC on weekdays)
# For 24-hour routes, using the time of the first morning departure is recommended

import sys
import getopt


def main(argv):
    try:
        opts, args = getopt.getopt(
            argv,
            "",
            ["agency=", "bucket=", "start-epoch=", "end-epoch="],
        )
    except getopt.GetoptError:
        print (('main.py '
        '--agency <name of agency to use>' 
        '--bucket <name of S3 bucket to use>'
        '--start-epoch <all trips starting at or after this time, in seconds>'
        '--end-epoch [Optional] <all trips ending at or before this time, in seconds>'
        ))
    for opt, arg in opts:
        if opt == '--agency':
            agency = arg
        if opt == '--bucket':
            bucket = arg
        if opt == '--start-epoch':
            start_epoch = arg
        if opt == '--end-epoch':
            end_epoch = arg
    trip_generator = TripGenerator(
        agency=agency,
        bucket=bucket,
        ongoing_path=ongoing_path,
        start_epoch=start_epoch,
        end_epoch=end_epoch,
    )


if __name__ == "__main__":
    main(sys.argv[1:])


