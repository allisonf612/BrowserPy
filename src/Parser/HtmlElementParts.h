#ifndef XMLSCRAPER_H
#define XMLSCRAPER_H

#include <string>
#include <cstring>
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include "ITokCollection.h"
#include "Tokenizer.h"
#include "XmlElementParts.h"



class HtmlParts
{
    enum NodeType {OPENING_TAG, CLOSING_TAG, PLAIN_TEXT, NONE} ;
    std::map < NodeType, std::string > nodeType_s;
public:
    HtmlParts(XmlParts* pNodes);
    ~HtmlParts();
    bool get();
    int length();
    void clear();
    std::string toString();
    std::string show();
    std::map < std::string, std::string > attributes;

    bool isLink();
    bool isDiv();
    bool isH2();
    
    bool isProductLink(); // Craigslist-specific
    bool isPostBody();
    bool isPostTitle();
    bool isPlainText();

    bool isOpeningTag();
    bool isClosingTag();

private:
    XmlParts* pNodes;
    std::string tagName;
    NodeType nodeType;
    void setType(NodeType nodeType);
    void setType();
    NodeType getType();
    std::string showType();
    void setTagName(std::string tagName);
    void setTagName();
    std::string getTagName();
};

inline int HtmlParts::length() { return pNodes->length(); }

inline void HtmlParts::clear() { setType(); setTagName(); attributes.clear(); }

inline void HtmlParts::setType() { setType(NONE); }

inline void HtmlParts::setType(NodeType nodeType) { this->nodeType = nodeType; }

inline HtmlParts::NodeType HtmlParts::getType() { return nodeType; }

inline std::string HtmlParts::showType() { return nodeType_s[nodeType]; }

inline void HtmlParts::setTagName(std::string tagName) { this->tagName = tagName; }

inline void HtmlParts::setTagName() { setTagName("none"); }

inline std::string HtmlParts::getTagName() { return tagName; }

inline bool HtmlParts::isLink() { return (getTagName() == "a"); }

inline bool HtmlParts::isDiv() { return (getTagName() == "div"); }

inline bool HtmlParts::isH2() { return (getTagName() == "h2"); }

inline bool HtmlParts::isOpeningTag() { return (getType() == OPENING_TAG); }

inline bool HtmlParts::isClosingTag() { return (getType() == CLOSING_TAG); }

inline bool HtmlParts::isPlainText() { return (getType() == PLAIN_TEXT); }

#endif
