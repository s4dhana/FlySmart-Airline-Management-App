from ._anvil_designer import My_FlightsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class My_Flights(My_FlightsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    data = self.compile_tables()
    self.repeating_panel_1.items = data
    Notification("Welcome Sadhana!").show()

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Main_Page')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    data = self.compile_tables()
    self.repeating_panel_1.items = data
    self.checkIfCancelled(data)
    
  def checkIfCancelled(self,data):
    for i in data:
      if i["cancelled"]:
        name=i["name"]
        alert(f"Flight {name} is cancelled! Looking for other flights.")
        self.rescheduleFlight(i["destination"],i["start"],i["seatsAvailable"],name)
        
  def rescheduleFlight(self,destination,start,seats,f):
    flights = app_tables.flights.search(destination=destination)
    found = False
    for flight in flights:
      if flight['seatsAvailable'] != 0 and f != flight['name']:
        found = True
        name,time = flight['name'],flight['time']
        if confirm(f"Flight {name} starting from {start} to {destination} is available for {time}. Proceed to booking ?"):
          self.bookFlight(name)
          Notification("Flight successfully booked. Please refresh").show()
          return

    if not found:
      Notification("Sorry, No other flights found to reschedule.").show()
      return
  
  def bookFlight(self,name):
    anvil.server.call('update_flight_details',name)
    
  def compile_tables(self):
    flights = [f['flightName'] for f in app_tables.myflights.search(name="sadhana")]
    result = [
        {
            'name':       row["name"],
            'start': row["start"],
            'destination':     row["destination"],
            'time':     row["time"],
            'cancelled':     row["cancelled"],
            'seatsAvailable': row['seatsAvailable'],
        }
        for row in app_tables.flights.search(name=flights[0])
    ]
    
    return result