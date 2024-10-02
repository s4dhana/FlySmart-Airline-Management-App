from ._anvil_designer import Main_PageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Main_Page(Main_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Flight_Details')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('My_Flights')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('weather')

  def image_1_show(self, **event_args):
    """This method is called when the Image is shown on the screen"""
    pass