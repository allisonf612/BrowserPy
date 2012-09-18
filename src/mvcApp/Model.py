# Model.py
# Author: Allison Figus

# The Model retrieves data from the web, processes and caches it,
# and serves it to its observers


import pygtk
pygtk.require('2.0')
import urllib
import process
import os


def process_data(raw_data, dir):
  rule = process.linkTitles
  data = rule(raw_data)

  # turn data into a list of links.
  urlList = data.split("<br/>")

  cache = os.listdir(dir)

  for url in urlList:
    (dirUrl, bitUrl) = os.path.split(url)
    if (not (bitUrl in cache)):
      # only crawl new posts
      print bitUrl + ": crawling new post"
      crawl(url, bitUrl, dir)
    else:
      print bitUrl + ": post already in cache"

  return data

#####
# Visits the link and saves
# pertinent portion to a text file with link as the name
##
def crawl(url, bitUrl, dir):
  try:
    urlFile = urllib.urlopen(url)
    urlData = urlFile.read()

    postData = process.postData(urlData)

    try:
      filename = os.path.join(dir, bitUrl)
      crawledFile = open(filename, 'w')
      crawledFile.write(postData)

    except IOError:
      print "writing crawled data failed for " + bitUrl

  except IOError:
      print "reading url data failed for " + bitUrl


def getData(bitUrl, dir):
  data = ""
  print "getData: bitUrl- " + bitUrl + " dir- " + dir
  filename = os.path.join(dir, bitUrl)
  if ( os.path.exists(filename) & (not (os.stat(filename)[6] == 0) )):
    file = open(filename, 'r')
    try:
      data = file.read()

    except IOError:
      print "get Data error"

    finally:
      file.close()

  return data


def getTitle(bitUrl, dir):
  title = ""
  filename = os.path.join(dir, bitUrl)
  if ( os.path.exists(filename) & (not (os.stat(filename)[6] == 0) )):

    try:

      file = open(filename, 'r')
      data = file.read()
      title = process.getTitle(data)

    except IOError:
      print "print Title error"

    finally:
      file.close()
      
  return title

# Returns a list of words
def getPlainText(bitUrl, dir):
  plain_text = []
  filename = os.path.join(dir, bitUrl)
  if ( os.path.exists(filename) & (not (os.stat(filename)[6] == 0) )):

    try:
      file = open(filename, 'r')
      data = file.read()
      raw_plain_text = process.getPlainText(data).split()
      for word in raw_plain_text:
        word = word.lower()
        plain_text.append(word)

    except IOError:
      print "print Title error"

    finally:
      file.close()

  return plain_text

# Keyword search of a crawled file
#   returns True/False
def searchFile(bitUrl, dir, keyword):
  plain_text = getPlainText(bitUrl, dir)
  return (keyword in plain_text)

def searchDir(dir, keyword):
  found = []
  try:
    files = os.listdir(dir)

    for f in files:
      if (searchFile(f, dir, keyword)):
        found.append( (f, getTitle(f, dir)) )

  except IOError:
    print "error listing files in (Model)searchDir"

  return found

def count_entries(path):
  num_entries = 0

  try:
    file = open(path, 'rb')
    raw = file.read()
    stripped = raw.strip("<br/>")
    split = stripped.split("<br/>")
    entries = []
    for entry in split:
        if len(entry) != 0:
            entries.append(entry)
    num_entries = len(entries)
  except IOError:
    print "Error counting entries in " + path
  
  return num_entries


class Model:
    __baseuri = ""
    __basedir = ""
    __dataLoc = "data"
    __keyLoc = "keys"
    __raw_data = ""
    __categories = ""

    def __get_dataLoc(self):
      return os.path.join(self.__basedir, self.__dataLoc)

    def __get_keyLoc(self):
      return os.path.join(self.__basedir, self.__keyLoc)


    def add_observer(self, observer):
      self.__observers.append(observer)

    def __notify_observers(self, raw_data, proc_data, base_uri):
      for observer in self.__observers:
        observer(raw_data, proc_data, base_uri)


    def load_url(self, url):
      try:
        f = urllib.urlopen(url)
        self.__raw_data = f.read()
        f.close()
        proc_data = process_data(self.__raw_data, self.__get_dataLoc())#, self.__process_rules)
        
        self.__update_keywords()
        self.__categories = self.__get_keywords()
        self.__notify_observers(self.__raw_data, self.__categories, self.__baseuri)
      except IOError:
        print "Not connected to internet"


    def load_index(self):
      self.__categories = self.__get_keywords()
      self.__notify_observers(self.__raw_data, self.__categories, self.__baseuri)

    def load_subcategory(self, file):
      self.__notify_observers(self.__raw_data, getData(file, self.__get_keyLoc()), self.__baseuri)
      
    def load_post(self, file):
      self.__notify_observers(self.__raw_data, getData(file, self.__get_dataLoc()), self.__baseuri)
      return getTitle(file, self.__get_dataLoc())


    # remove all keyword files
    def clear_keywords(self):

      try:
        files = self.__get_keyFiles()

        for file in files:
          path = os.path.join(self.__get_keyLoc(), file)
          os.remove(path)

      except IOError:
        print "Error clearing keywords"

      finally:
        self.load_index()

    def __get_keyFiles(self):
      return os.listdir(self.__get_keyLoc())

    def __get_keywords(self):
      keywords = ""

      try:
        files = self.__get_keyFiles()

        for file in files:
          path = os.path.join(self.__get_keyLoc(), file)
          keyword = file.split('.')[0]
          link = "<a href='"+ path +"'>"+keyword+" ("+str(count_entries(path))+")</a><br/>"
          keywords += link
      
      except IOError:
          print "Error in __get_keywords()"

      return keywords


    # Naive implementation
    def __update_keywords(self, keyword = None):
      if keyword == None:
        for file in self.__get_keyFiles():
          self.__update_keywords(file)
      else:
        try:
          keypath = os.path.join(self.__get_keyLoc(), keyword)
          keyFile = open(keypath, 'w')
          found = searchDir(self.__get_dataLoc(), keyword)

          for (data, title) in found:
            link = "<a href='"+ os.path.join('../', self.__dataLoc, data) +"'>"+title+"</a>"
            keyFile.write(link + "<br/>")
          keyFile.close()

        except IOError:
          print "error writing " + keypath

    def add_keyword(self, keyword):
      addKeyword = False

      keyword = keyword.lower()

      try:
        files = self.__get_keyFiles()
        
        if (keyword in files):
          addKeyword = False

        else:
          addKeyword = True

        if (addKeyword):
          self.__update_keywords(keyword)
          
      except IOError:
        print "add_keyword failed from join or listdir"

      finally:
        pass

      self.load_index()


    def __init__(self):
      self.__observers = []
      self.__basedir = os.path.join(os.getcwd(), "")
      self.__baseuri = "file://" + self.__basedir
