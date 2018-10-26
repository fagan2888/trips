#!/usr/bin/python3

import sys
import getopt


def main(argv):
    """Entry point for Trip Generator
    --agency: name of agency to use
    --bucket: name of S3 bucket to use
    --ongoing: key of ongoing file to load

    """
    try:
        opts, args = getopt.getopt(argv, "", ["agency=", "bucket=", "ongoing="])
    except getopt.GetoptError:
        print (('main.py --agency <name of agency to use>' 
        '--bucket <name of S3 bucket to use>'
        '--ongoing <key of ongoing file to load>'
        ))
    for opt, arg in opts:
        if opt == '--agency':
            agency = arg
        if opt == '--bucket':
            bucket = arg
        if opt == '--ongoing':
            ongoing = arg
    print (agency, bucket, ongoing)


if __name__ == "__main__":
    main(sys.argv[1:])


