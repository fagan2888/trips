#!/usr/bin/python3
import requests

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
    def __init__(self, agency, bucket, start_epoch, end_epoch):
        self.agency = agency
        start_minute = start_epoch // 60
        end_minute = None
        if end_epoch:
            end_minute = end_epoch // 60
        ongoing_trips = set() # trip keys
        self.trips = {} # ongoing trips dict
        while end_minute == None or start_minute - 1 <= end_minute:
            # TODO - add some kind of sleep/delay here
            transistates = []
            if start_minute <= end_minute:
                transistates = self.fetch_states(minute=start_minute)
            processed_trips = set([
                self.process_state(transistate=transistate)
                for transistate in transistates
            ])
            finished_trips = ongoing_trips.difference(processed_trips)
            for trip in finished_trips:
                self.finish_trip(trip)
            ongoing_trips = processed_trips
            start_minute += 1
                
    def fetch_states(self, minute):
        """Fetch transistates corresponding to that minute (based on epoch)
        :param minute: Epoch (which is at a minute)
        :type minute: Number (epoch in seconds)
        :return transistates: list of states
        :rtype transistates: list of dict
        """
        return requests.get('http://localhost:5353', params={
          'agency': self.agency,
          'start_epoch': minute*60000, # JS epochs are in ms
          'end_epoch': minute*60000,
        }).json()

    def get_transistate_key(self, transistate):
        return (
            transistate['vid'],
            transistate['rid'],
            transistate['did'],
        )

    def process_state(self, transistate):
        """Uses transistate to extend a trip or start a new one
        :param transistate: state of a transit network
        :type transistate: dict
        :return trip: key for an ongoing trip
        :rtype trip: dict
        """
        ongoing_trip = self.trips.get(
            self.get_transistate_key(transistate=transistate),
            [],
        )
        ongoing_trip.append({
            'time': transistate['vtime'],
            'lat': transistate['lat'],
            'lon': transistate['lon'],
            'heading': transistate['heading'],
        })
        self.trips[
            self.get_transistate_key(transistate=transistate)
        ] = ongoing_trip
        return self.get_transistate_key(transistate)

    def finish_trip(self, trip):
        transistates = self.trips[trip]
        self.trips.pop(trip)
        trip += (transistates[0]['time'],)
        print({trip: transistates})




    