from ._anvil_designer import Flight_DetailsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Flight_Details(Flight_DetailsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_1.items = app_tables.flights.search()

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.repeating_panel_1.items = app_tables.flights.search()
      
    # Display something to the user so they know it worked:
    Notification("Refreshed flight details!").show()

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Main_Page')