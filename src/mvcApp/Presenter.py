# Presenter.py
# Author: Allison Figus


import gtk
import gtkmozembed
import os



class Browser(gtkmozembed.MozEmbed):

  # Block all direct user interaction with Raw browser
  def override_open_uri(self, mozembed, uri):
    return True

  def present_data(self, raw_data, proc_data, base_uri):
    self.render_data(raw_data, long(len(raw_data)), base_uri, 'text/html')

  def get_data(self):
    return self.get_location()

  def __init__(self):
    gtkmozembed.MozEmbed.__init__(self)
    # Commented out 9/18/2012
    #self.connect("open-uri", self.override_open_uri)


class Scraped_Browser(Browser):

  def present_data(self, raw_data, proc_data, base_uri):
    self.__base_uri = base_uri
    self.render_data(proc_data, long(len(proc_data)), base_uri, 'text/html')

  def __init__(self):
    Browser.__init__(self)
    self.__base_uri = ""


