#!/usr/bin/python3

class TripGenerator:
    """
    Performs all stages of trip generation

    Process transit state files (snapshots of GPS locations
    taken every 15 seconds) (process_state)
      - update a trip - add a vehicle snapshot to it
      - create a trip - current state has (vehicle, route, pattern) but not previous
    An ongoing trip (ie. we're creating it here) is (vehicle, route, pattern)
    A trip (ie. as stored in the db) is (start_time, vehicle, route, pattern)
    
    A trip is essentially finished when it can no longer be continued in the
    next transistate - the TripMerger merges trips that should've been together
    """
    def __init__(agency, bucket, start_epoch, end_epoch):
        self.agency = agency
        self.bucket = bucket
        self.trips = {}
        start_minute = start_epoch // 60
        end_minute = None
        if end_epoch:
            end_minute = end_epoch // 60
        while end_minute == None or start_minute <= end_minute:
            for transistate in fetch_states(minute=start_minute):
                process_state(transistate=transistate)

    def fetch_states(minute):
        """Fetch transistates corresponding to that minute (based on epoch)
        :param minute: Epoch (which is at a minute)
        :type minute: Number (epoch in seconds)
        """
        s3_state_links = get_links(bucket=self.bucket, minute=minute)
        return [
            read_s3_gzip(bucket=self.bucket, key=link)
            for link in s3_state_links
        ]

    def process_state(transistate):
        """Uses transistate to extend a trip or start a new one
        :param transistate: state of a transit network
        :type transistate: dict
        """
        prev_trip = self.trips.get((
            transistate['vehicle'],
            transistate['route'],
            transistate['pattern'],
        ))
        if prev_trip != None
            start_trip(transistate)
            continue
        transistate['start_time'] = prev_trip['start_time']
        insert_trip(transistate)

    def start_trip(transistate):
        """Starts a new trip using that transistate
        :param transistate: state of a transit network
        :type transistate: dict
        """
        transistate['start_time'] = transistate['time']
        self.trips[(
            transistate['vehicle'],
            transistate['route'],
            transistate['pattern']
        )] = transistate
        insert_trip(transistate)


    