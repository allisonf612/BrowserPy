/*
* HtmlElementParts.cpp -- Scrapes data from a stream of XmlParts
* Author: Allison Figus
* Note: mimics the design of Dr. Fawcett's XmlElementParts
*/



#include "HtmlElementParts.h"

//----< construct XmlParts instance >---------------------------

HtmlParts::HtmlParts(XmlParts* pNodes) : pNodes(pNodes), nodeType(NONE)
{
    nodeType_s[OPENING_TAG] = "opening tag";
    nodeType_s[CLOSING_TAG] = "closing tag";
    nodeType_s[PLAIN_TEXT] = "plain-text";
    nodeType_s[NONE] = "none";
}
//----< destructor >-------------------------------------------

HtmlParts::~HtmlParts()
{
}


bool HtmlParts::isProductLink()
{
    bool isProductLink = false;

    if (this->isLink())
    {
        if(this->attributes["href"].find("http://syracuse.craigslist.org/sys/") != std::string::npos)
            isProductLink = true;
    }

    return isProductLink;
}

bool HtmlParts::isPostBody()
{
    bool isPostBody = false;

    if (this->isDiv())
    {
        if (this->attributes["id"].find("userbody") != std::string::npos)
            isPostBody = true;
    }

    return isPostBody;
}

bool HtmlParts::isPostTitle()
{
    bool isPostTitle = false;

    if ( this->isOpeningTag() && this->isH2() )
        isPostTitle = true;


    return isPostTitle;
}

//----< identify an XmlNode >------------------

bool HtmlParts::get()
{
    clear();
  if (pNodes->get())
  {
      if ((*pNodes)[0] == "<")
      {
          if ((*pNodes)[1] == "/")
          {
              setType(CLOSING_TAG);
              setTagName((*pNodes)[2]);
              if ((*pNodes)[3] != ">")
              {
                  std::cout << "Parsing error";
              }
          }
          else
          {
              setType(OPENING_TAG);
              setTagName((*pNodes)[1]);
              
              int i = 2;
              std::string key, value;
              while ((*pNodes)[i] != ">" && pNodes->length() > i + 3)
              {
                  key = (*pNodes)[i];
                  value = (*pNodes)[i + 2];
                  // strip surrounding quotes...
                  size_t pos;
                  while ((pos = value.find('"')) != std::string::npos)
                      value.erase(pos, 1);

                  attributes[key] = value;

                  i += 3;
              }
          }
      }
      else
      {
          setType(PLAIN_TEXT);
      }
  }
  else
      return false;

  return true;
}

//----< collect semi-expression as space-seperated string >----

std::string HtmlParts::show()
{
    std::cout << showType() << ", " << getTagName() << ":" ;

    for( std::map<std::string,std::string>::iterator iter = attributes.begin(); iter != attributes.end(); ++iter ) {
      std::cout << (*iter).first << " is " << (*iter).second << std::endl;
    }

    return pNodes->show();
}

std::string HtmlParts::toString()
{
    std::string nodeString = "";

    /*
     * HTML requires < be immediately followed (no space) by
     * next char...
     */
    switch(this->getType()) {
        case OPENING_TAG:
            nodeString.append( (*pNodes)[0] ).append( (*pNodes)[1] );
            for (int i = 2; i < pNodes->length(); ++i)
            {
                nodeString.append( " " ).append( (*pNodes)[i] );
            }
            break;
        case CLOSING_TAG:
            nodeString.append( (*pNodes)[0] ).append( (*pNodes)[1] ).append( (*pNodes)[2] );
            for (int i = 3; i < pNodes->length(); ++i)
            {
                nodeString.append( " " ).append( (*pNodes)[i] );
            }
            break;

        case PLAIN_TEXT:
            nodeString.append( (*pNodes)[0] );
            for (int i = 1; i < pNodes->length(); ++i)
            {
                nodeString.append( " " ).append( (*pNodes)[i] );
            }
            break;
        default:
            // error
            break;
    }

    return nodeString;
}


//----< test stub >--------------------------------------------

#ifdef TEST_XMLSCRAPER

int main(int argc, char* argv[])
{
  std::cout << "\n  Testing HtmlParts class\n "
            << std::string(23,'=') << std::endl;
  std::cout
    << "\n  Note that quotes are returned as single tokens\n\n";

  if(argc < 2)
  {
    std::cout
      << "\n  please enter name of file to process on command line\n\n";
    return 1;
  }

  for(int i=1; i<argc; ++i)
  {
    std::cout << "\n  Processing file " << argv[i];
    std::cout << "\n  " << std::string(16 + strlen(argv[i]),'-') << "\n\n";
    try
    {
      Toker toker(argv[i]);
      toker.setMode(Toker::xml);
      XmlParts parts(&toker);
      HtmlParts scraper(&parts);
      std::cout << "Links in this page:" << std::endl;
      while(scraper.get())
      {
          if (scraper.isLink())
              std::cout << scraper.attributes["href"] << std::endl;
      }
      std::cout << "\n\n";
    }
    catch(std::runtime_error ex)
    {
      std::cout << "\n " << ex.what() << "\n\n";
    }
    catch(std::exception ex)
    {
      std::cout << "\n  " << ex.what() << "\n\n";
    }
  }
}

#endif
