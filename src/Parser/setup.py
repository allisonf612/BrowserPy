from distutils.core import setup, Extension

data_processing = Extension('process',
                    sources = ['process.cpp', 'Tokenizer.cpp', 'XmlElementParts.cpp', 'HtmlElementParts.cpp'])

setup (name = 'BrowserPy',
       version = '1.0',
       description = 'Python/C++ Web Scraper',
       ext_modules = [data_processing])