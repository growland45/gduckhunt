#!/usr/bin/python3
from html.parser import HTMLParser
import myio, g;
import os, sys
from tkinter import Tk

def dbg(text):
  print (text, file= sys.stderr)

class searchresultparser(myio.DuckResultParser):
  def __init__(self, gui):
    myio.DuckResultParser.__init__(self)
    self.gui= gui
  def handle_search_result(self, hrefurl, hreftitle):
    self.gui.handle_search_result(hrefurl, hreftitle)

class duckbuttons(g.gridframe):
  def populate(self):
    sp= searchresultparser(self)
    status= sp.doit(keywords)

  def handle_search_result(self, hrefurl, hreftitle):
    self.button(text=hreftitle, 
                command= lambda hrefurl= hrefurl: self.launchurl(hrefurl))
    self.label(hrefurl)
    self.newrow()
    print(hrefurl)

  def launchurl(self, hrefurl):
    os.system("chromium "+ hrefurl)

class gimmekeywords(g.packframe):
  def populate(self):
    title= 'I need some keywords';  self.title('Duck Hunt: '+ title);
    self.wlabel(title+ ' (blank delimited)')
    self.entryblank= self.entry(width= 70)
    self.okbutton(text= 'Fetch')

  def on_ok(self, *args):
    global keywords
    entryline= self.entryblank.get()
    dbg(entryline)
    keywords= entryline.split()
    g.killmain()

class mainframe(g.packframe):
  def populate(self):
    global keywords
    title= 'Search for: '+ ' '.join(keywords)
    self.title(title)
    self.wlabel(title)
    self.vscrollsubframe(duckbuttons)

if __name__ == '__main__':
  palette= { 'bggrid': '#6677aa', 'bgcolframe': '#445599' }
  argc= len(sys.argv)
  if argc< 2:  g.domain(gimmekeywords, palette)
  else:  keywords= sys.argv[1:]
  g.domain(mainframe, palette)



