# Controller.py
# Author: Allison Figus
# Controller forwards user events from the View to the Model

from Model import Model
from View import View
import os


class Controller:

    def navigationPressed(self, linkButton, navLinks, model):
      navLinks.set_curr(linkButton)
      if (navLinks.get_curr() == 0):
        model.load_index()
      elif (navLinks.get_curr() == 1):
        model.load_subcategory(navLinks.get_location())

      
    # Override gtkmozembed handling
    def open_uri(self, browser, uri, navLinks, model):
      (path, file) = os.path.split(uri)
      if (navLinks.get_curr() == 0):
        name = file.split('.')[0]
        model.load_subcategory(file)
        navLinks.set_curr(index = 1, title = name, location = file)
      elif (navLinks.get_curr() == 1):
        title = model.load_post(file)
        navLinks.set_curr(index = 2, title = title, location = file)

      return True

    def load(self, presenter, presenter_data, model, view):
      url = presenter_data

      model.load_url(url)
      view.index.pressed()

    def clear(self, presenter, model, view):
      model.clear_keywords()
      view.index.pressed()

    def keyword_entry(self, user_data, model, view):
      keyword = user_data.get_text()
      user_data.set_text("")

      model.add_keyword(keyword)
      view.index.pressed()

