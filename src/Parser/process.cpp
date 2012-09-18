/*
 * process.cpp
 * Author: Allison Figus
 * Creating a C/C++ extension for computationally expensive processing
 * Note: Some use of Dr. Fawcett's sample code (test stub for XmlElementParts)
 */

#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "HtmlElementParts.h"



static PyObject *
process_linkTitles(PyObject *self, PyObject *args)
{
    const char *doc_buffer;
    std::string processed_doc = "";

    if (!PyArg_ParseTuple(args, "s", &doc_buffer))
        return NULL;

    try
    {
      Toker toker(doc_buffer, false);
      toker.setMode(Toker::xml);
      XmlParts parts(&toker);
      HtmlParts scraper(&parts);

      bool listHead = true;

      while(scraper.get())
      {
          // identify product links
          if (scraper.isProductLink())
          {
              if (listHead) {
                  processed_doc += scraper.attributes["href"];
                  listHead = false;
              }
              else
              processed_doc +=  "<br/>" + scraper.attributes["href"];
          }
      }

    }
    catch(std::runtime_error ex)
    {
      std::cout << "\n " << ex.what() << "\n\n";
    }
    catch(std::exception ex)
    {
      std::cout << "\n  " << ex.what() << "\n\n";
    }

    return Py_BuildValue("s", processed_doc.c_str());
}

static PyObject *
process_postData(PyObject *self, PyObject *args)
{
        const char *doc_buffer;
    std::string processed_doc = "";

    if (!PyArg_ParseTuple(args, "s", &doc_buffer))
        return NULL;

    try
    {
      Toker toker(doc_buffer, false);
      toker.setMode(Toker::xml);
      XmlParts parts(&toker);
      HtmlParts scraper(&parts);

      while(scraper.get())
      {
          // Building a (partial) tree
          // Search for closing tag to select all content in between
          if ( scraper.isPostTitle() )
          {
              processed_doc += scraper.toString();
              while ( scraper.get() && !(scraper.isClosingTag() && scraper.isH2()) )
                  processed_doc += scraper.toString();

              processed_doc += scraper.toString();
          }

          if (scraper.isPostBody())
          {
              /*
               * Note: this will fail if there are nested <div></div>
               */
              while ( scraper.get() && !(scraper.isClosingTag() && scraper.isDiv()) )
              {
                  // String value of current node
                   processed_doc += scraper.toString();
              }
          }
      }

    }
    catch(std::runtime_error ex)
    {
      std::cout << "\n " << ex.what() << "\n\n";
    }
    catch(std::exception ex)
    {
      std::cout << "\n  " << ex.what() << "\n\n";
    }

    return Py_BuildValue("s", processed_doc.c_str());
}

static PyObject *
process_getTitle(PyObject *self, PyObject *args)
{
    const char *doc_buffer;
    std::string processed_doc = "";

    if (!PyArg_ParseTuple(args, "s", &doc_buffer))
        return NULL;

    try
    {
      Toker toker(doc_buffer, false);
      toker.setMode(Toker::xml);
      XmlParts parts(&toker);
      HtmlParts scraper(&parts);

      while(scraper.get())
      {
          // Building a (partial) tree
          // Search for closing tag to select all content in between
          if ( scraper.isPostTitle() )
          {
              while ( scraper.get() && !(scraper.isClosingTag() && scraper.isH2()) )
                  processed_doc += scraper.toString();
          }
      }
    }
    catch(std::runtime_error ex)
    {
      std::cout << "\n " << ex.what() << "\n\n";
    }
    catch(std::exception ex)
    {
      std::cout << "\n  " << ex.what() << "\n\n";
    }

    return Py_BuildValue("s", processed_doc.c_str());
}

/*
 Return only plain text, no tags
 */
static PyObject *
process_getPlainText(PyObject *self, PyObject *args)
{
    const char *doc_buffer;
    std::string processed_doc = "";


    if (!PyArg_ParseTuple(args, "s", &doc_buffer))
        return NULL;

    try
    {
      Toker toker(doc_buffer, false);
      toker.setMode(Toker::xml);
      XmlParts parts(&toker);
      HtmlParts scraper(&parts);

      while(scraper.get())
      {
          // Extra spacing doesn't matter
          if ( scraper.isPlainText() )
          {
              processed_doc += " " + scraper.toString() + " ";
          }
      }

    }
    catch(std::runtime_error ex)
    {
      std::cout << "\n " << ex.what() << "\n\n";
    }
    catch(std::exception ex)
    {
      std::cout << "\n  " << ex.what() << "\n\n";
    }

    return Py_BuildValue("s", processed_doc.c_str());
}

static PyMethodDef ProcessMethods[] = {
    {"linkTitles",  process_linkTitles, METH_VARARGS,
     "Get link titles"},
    {"getTitle", process_getTitle, METH_VARARGS,
     "Get title from a post"},
    {"getPlainText", process_getPlainText, METH_VARARGS,
     "Get plain text from a post"},
    {"postData", process_postData, METH_VARARGS,
     "Get post data"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

extern "C" PyMODINIT_FUNC
initprocess(void)
{
    (void) Py_InitModule("process", ProcessMethods);
}




extern "C" int
main(int argc, char *argv[])
{
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initprocess();

    return 0;
}
