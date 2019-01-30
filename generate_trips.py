#!/usr/bin/python3

class TripGenerator:
    """
    Performs all stages of trip generation

    Process transit state files (snapshots of GPS locations
    taken every 15 seconds) (process_state)
      - continue a trip - add a vehicle snapshot to it
      - create a trip - current state has (vehicle, route, pattern) but not previous
    An ongoing trip (ie. we're creating it here) is (vehicle, route, pattern)
    A trip (ie. as stored in the db/S3) is (start_time, vehicle, route, pattern)

    A trip is finished when it is not continued in the next transistate -
    the TripMerger merges trips that should've been together
    """
    def __init__(agency, bucket, start_epoch, end_epoch):
        self.agency = agency
        self.s3_helper = S3Helper(bucket=bucket)
        start_minute = start_epoch // 60
        end_minute = None
        if end_epoch:
            end_minute = end_epoch // 60
        self.ongoing_trips = set()
        while end_minute == None or start_minute <= end_minute:
            for transistates in fetch_states(minute=start_minute):
                processed_trips = set([
                    process_state(transistate=transistate)
                    for transistate in transistates
                ])
                finished_trips = ongoing_trips.difference(processed_trips)
                for trip in finished_trips:
                    self.finish_trip(trip)
                ongoing_trips = processed_trips
                

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
        :return trip: key for an ongoing trip
        :rtype trip: dict
        """
        ongoing_trip = self.trips.get((
            transistate['vehicle'],
            transistate['route'],
            transistate['pattern'],
        ), [])
        self.trips[(
            transistate['vehicle'],
            transistate['route'],
            transistate['pattern'],
        )] = ongoing_trip.append({
            'time': transistate['time'],
            'lat': transistate['lat'],
            'lon': transistate['lon'],
            'heading': transistate['heading'],
        })
        return (
            transistate['vehicle'],
            transistate['route'],
            transistate['pattern'],
        )

    def finish_trip(trip):
        transistates = self.trips[trip]
        start_time = transistates[0]['start_time']
        self.s3_helper.write(
            path='{route}/{pattern}/{start_time}/
        )




    