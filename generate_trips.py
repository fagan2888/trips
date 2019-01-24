#!/usr/bin/python3

class TripGenerator:
    """
    Performs all stages of trip generation

    Process transit state files (snapshots of GPS locations
    taken every 15 seconds) (process_state)
      - update a trip - add a vehicle snapshot to it
      - create a trip - current state has (vehicle, route, direction) but not previous
      - finish a trip - previous state has (vehicle, route, direction) but not current
    """
    def __init__(agency, bucket, start_epoch, end_epoch):
        self.agency = agency
        self.bucket = bucket
        start_minute = start_epoch // 60
        end_minute = None
        if end_epoch:
            end_minute = end_epoch // 60
        while end_minute == None or start_minute <= end_minute:
            fetch_states(start_minute)

    def fetch_states(minute):
      pass

    def process_state(transistate):
      pass

    def start_trip(state):
      pass

    def finish_trip(trip):
      pass

    