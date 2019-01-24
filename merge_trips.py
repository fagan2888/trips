#!/usr/bin/python3


class TripMerger:
    """
    Merges trips that are clearly linked

    eg. We start the TripGenerator at 5am, but one trip is running from 4:50-5:10am.
    Then there'd be two separate trips. Since the same (route, vehicle, direction)
    combination would appear to end and then suddenly start, we set the trip IDs
    of the second trips to the first one.
    Another useful case would be if a bus disappears then reappears shortly after
    (assuming it keeps its (route, vehicle, direction) combo)
    """
    pass
