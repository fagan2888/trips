#!/usr/bin/python3

# Running from 2018-11-18 (start of November TTC board period) to now

# Usage: start epoch should reflect a period in which no trips are in-progress for the period
# you wish to measure (eg. one full weekday).
# It should be before regular service (5:30am weekdays for the TTC) is scheduled, but after
# the last night bus is scheduled to start (usually about 5:20am for the TTC on weekdays)
# For 24-hour routes, using the time of the first morning departure is recommended

# Sample Usage:
# python3 main.py --agency="muni" --bucket="orion-trips" --start-epoch=1549332763 --end-epoch=1549332765

# Monday February 4 at 6am to Tuesday February 5 at 2:30am
# python3 main.py --agency="ttc" --bucket="orion-trips" --start-epoch=1549278000 --end-epoch=1549351800

# TODO - add option so after end-epoch it keeps going (ie. trips starting 6am-2am for ttc)
# Do daily-dumps ONLY for trips, then it's useful (a states daily-dump is useless, remove that from orion)
# For now, just manually run trip_generator as a batch in an ec2 box - write trips AND daily dumps

# in the future, trips will be in DB, but daily dumps will still be made on S3

import sys
import getopt
from generate_trips import TripGenerator

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
        '--bucket <name of S3 bucket to use for trips>'
        '--start-epoch <all trips starting at or after this time, in seconds>'
        '--end-epoch [Optional] <last time a trip can start, in seconds>'
        ))
    for opt, arg in opts:
        if opt == '--agency':
            agency = arg
        if opt == '--bucket':
            bucket = arg
        if opt == '--start-epoch':
            start_epoch = int(arg)
        if opt == '--end-epoch':
            end_epoch = int(arg)
    trip_generator = TripGenerator(
        agency=agency,
        bucket=bucket,
        start_epoch=start_epoch,
        end_epoch=end_epoch,
    )


if __name__ == "__main__":
    main(sys.argv[1:])


