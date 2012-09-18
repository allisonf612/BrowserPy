# View.py
# Author: Allison Figus
#
# A Browser consists of a scraped view plus 
# a set of navigation tools: keyword entry plus
# limited breadcrumb trail navigation
#
# The scraped view
# provides a custom representation of the
# data in the model


import pygtk
pygtk.require('2.0')
import gtk
import Presenter



class NavLinks(gtk.HBox):
  __curr_index = 0

  def pos(self, item):
    for n in range(len(self.__allLinks)):
      if self.__allLinks[n] == item:
        return n
    return -1

  def set_curr(self, item = None, index = -1, title = None, location = None):
    if item == None:
      self.__curr_index = index
    else:
      self.__curr_index = self.pos(item)

    if title != None:
      self.__allLinks[index].set_label(title)

    if location != None:
      self.__allLinks[index].location = location
      
    self.__display()
  
  def get_curr(self):
    return self.__curr_index

  def get_location(self):
    return self.__allLinks[self.get_curr()].location

  def __display(self):
    for n in self:
      if self.pos(n) > self.__curr_index:
        n.hide()
      else:
        n.show()

  def append(self, item):
    self.pack_start(item, False)
    self.__allLinks.append(item)

  def __init__(self):
    gtk.HBox.__init__(self)
    self.__allLinks = []

class LinkButton(gtk.Button):
  # return True halts signal propogation
  def override_focus(self, calling_widget, data):
    return True

  def __init__(self, label, location = None):
    gtk.Button.__init__(self, label)
    self.location = location
    self.set_focus_on_click(False)
    self.set_relief(gtk.RELIEF_NONE)
    self.connect("focus", self.override_focus)

class View(gtk.Window):

    def update_navBar(self, location):
        self.navBar.set_text(location)


    def close_window(self, caller_widget):
        gtk.main_quit() # Close the app fully


    def __init__(self, url):
        self.url = url
        
        gtk.Window.__init__(self)
        self.set_title("Site Scraper: Craigslist")

        self.connect("destroy", self.close_window)

        vbox = gtk.VBox()
        self.add(vbox)
        vbox.show()


        frame1 = gtk.Frame()
        frame1.show()
        vbox.pack_start(frame1, False)
        self.__frame1 = frame1

        vpane = gtk.VPaned()
        frame1.add(vpane)
        vpane.show()
        self.__vpane = vpane

        navBox = gtk.VBox()
        navBox.show()
        vpane.add1(navBox)
        self.__navBox = navBox

        navLinks = NavLinks()
        navLinks.show()
        navBox.pack_start(navLinks, False)
        self.navLinks = navLinks

        index = LinkButton("index", location = "keywords.html")
        index.show()
        navLinks.append(index)
        self.index = index

        subcategory = LinkButton("subcategory")
        navLinks.append(subcategory)
        self.subcategory = subcategory

        post = LinkButton("post")
        navLinks.append(post)
        self.post = post

        keywordBox = gtk.HBox()
        keywordBox.show()
        navBox.pack_start(keywordBox, False)

        keywordLabel = gtk.Label("Add keyword:")
        keywordLabel.show()
        keywordBox.pack_start(keywordLabel, False)

        keywordSearch = gtk.Entry()
        keywordSearch.show()
        keywordBox.pack_start(keywordSearch)
        self.keywordSearch = keywordSearch

        buttonBox = gtk.HBox()
        buttonBox.show()
        navBox.pack_start(buttonBox, False)

        buttonLabel = "Reload web data"
        loadButton = gtk.Button(label=buttonLabel)
        loadButton.show()
        buttonBox.pack_start(loadButton, False)
        self.loadButton = loadButton

        clearButton = gtk.Button("Clear Keywords")
        clearButton.show()
        buttonBox.pack_start(clearButton, False)
        self.clearButton = clearButton

        browser1 = Presenter.Scraped_Browser()
        vpane.add2(browser1)
        browser1.set_size_request(600,600)
        browser1.show()
        self.browser1 = browser1
    

    def run(self):
        self.show()
        self.loadButton.clicked()
        gtk.main()
