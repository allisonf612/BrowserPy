# browserpy.py
# Author: Allison Figus
#
# This is the main module for BrowserPy.
# The model, view, and controller classes are instantitated
# and connected by the App class.


from Model import *
from View import *
from Controller import Controller


class App:

    # Setting up these connections forms the event notification
    # system which the controller responds to
    #
    # Registering the controller as an observer of these events
    def register_controller(self, controller, model, view):
      view.loadButton.connect("clicked", controller.load, view.url, model, view)
      view.clearButton.connect("clicked", controller.clear, model, view)
      view.keywordSearch.connect("activate", controller.keyword_entry, model, view)

      # Navigation Links
      view.index.connect("pressed", controller.navigationPressed, view.navLinks, model)
      view.subcategory.connect("pressed", controller.navigationPressed, view.navLinks, model)
      view.post.connect("pressed", controller.navigationPressed, view.navLinks, model)

      view.browser1.connect("open-uri", controller.open_uri, view.navLinks, model)
      
    

    # Registering method object as the observer
    # This allows the observer's interface to be defined and the observable
    # to be generic.
    # Model: Observable
    # View: Observer...
    def register_view(self, model, observer):
      model.add_observer(observer.present_data)

    def start(self):
        self.__view.run()

    def __init__(self, url):
        self.__url = url

        ######
        # Instantiating the components
        ##
        # The model, view and controller may persist independently
        model = Model()
        controller = Controller()
        view = View(url)
        self.__view = view

        ######
        # Connecting the components: define associations
        ##
        
        # Registering controller as an observer of several events
        self.register_controller(controller, model, view)

        # Register the browser as an observer of the model
        self.register_view(model, view.browser1)


# This script manages the app
if __name__ == "__main__":
    import sys
    print "BrowserPy: Craigslist Web Scraping";
    uri = ''
    if len(sys.argv) > 1:  
        uri = sys.argv[1]
    app = App(uri)
    app.start()
