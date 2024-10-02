import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import requests

@anvil.server.callable
def update_flight_details(name):
  # update seats in flights table
    # update flight name in my_flights table
    row = app_tables.flights.get(name=name)
    row.update(seatsAvailable=row['seatsAvailable']-1)

    row2 = app_tables.myflights.get(name="sadhana")
    row2.update(flightName=name)

@anvil.server.callable
def cancelFlight(location):
    rows = app_tables.flights.search(start=location)
    for row in rows:
      row.update(cancelled=True)
