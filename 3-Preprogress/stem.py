#!/usr/bin/python
# -*- coding: UTF-8 -*-

from nltk.stem import SnowballStemmer
from xml.dom.minidom import parse
import xml.dom.minidom
import os
from xml.dom import minidom
from nltk.tokenize import WordPunctTokenizer

import sys
reload(sys)
sys.setdefaultencoding('utf8')
n=0

def wordtokenizer(sentence):
    #分段
    words = WordPunctTokenizer().tokenize(sentence)
    return words

for fpathe,dirs,fs in os.walk("E:\\XML_OUT\\Version alteration\\"):
  for f in fs:
    #print f
    xmlfile= os.path.join(fpathe,f)
    #print  xmlfile
    #xmlfile 保存了xml文件及路径

    DOMTree = xml.dom.minidom.parse(xmlfile)
    bug = DOMTree.documentElement

    newdoc=minidom.Document()
    newbug=newdoc.createElement("bug")
    newdoc.appendChild(newbug)

    newid=newdoc.createElement("id")
    newtitle=newdoc.createElement("title")

    # 错误，应按属性赋值
    #myid=id.childNodes[0].data
    myid=bug.getAttribute("id")
    newid.appendChild(newdoc.createTextNode(myid))
    newbug.appendChild(newid)
    #print myid

    titles=bug.getElementsByTagName('title')
    for title in titles:
        mytitle=title.childNodes[0].data
        newtitle.appendChild(newdoc.createTextNode(mytitle))
        newbug.appendChild(newtitle)
        #print mytitle
    sentences=bug.getElementsByTagName("sentence")
    for s in sentences:
        #print s
        #print "....."
        sentence=" "
        sentence=s.childNodes[0].data
        #print sentence #即每个sentence中的内容
        words= wordtokenizer(sentence)
        list = []
        mysentence=" "
        for word in words:
            #print word
            snowball_stemmer = SnowballStemmer("english")
            newword = snowball_stemmer.stem(word)
           # print word
            list.append(newword)
            #print list
            mysentence = " ".join(list)#需要把单词放到数组中

        newsentence=newdoc.createElement("sentence")
        newsentence.appendChild(newdoc.createTextNode(mysentence))
        newbug.appendChild(newsentence)

    outpath="E:\\STEM\\Version alteration\\"
    outfile= os.path.join(outpath,f)
    newfile = file(outfile, "w")
    newdoc.writexml(newfile,addindent='',newl='\n',encoding = 'utf-8')
    newfile.close()
    n=n+1
    print n




