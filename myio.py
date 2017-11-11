import urllib.request, urllib.parse
import http.client
import os, sys
from html.parser import HTMLParser

def dbg(text):  print (text, file= sys.stderr)

def attend_to_http_proxy():
  if 'http_proxy' in os.environ:
    http_proxy= os.environ['http_proxy']
    if http_proxy== '':  return
    proxies = {'http':  http_proxy, 'https': http_proxy}
    proxy_support = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    sys.stderr.write("myio proxy: '"+ http_proxy+ "'\n")

def dourl(url, htmlparser, postdict= None):
  # fetch the url and parse it through htmlparser
  # htmlparser should be some derived class of html.parser.HTMLParser
  # postdict is optional dictionary of post data
  attend_to_http_proxy()

  postdata= None
  if (postdict):  postdata = urllib.parse.urlencode(postdict).encode()

  try:
    req = urllib.request.Request(url, data= postdata, 
       headers= { 'User-Agent':
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '+
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
       } )
    r1 = urllib.request.urlopen(req, timeout=20)
  except Exception as e:
    return "FAILED "+ url+ " EXCEPTION "+ str(e)
  if r1.status!= 200:
    return "STATUS "+ str(r1.status)+ ' '+ r1.reason

  data1 = r1.read(); # bytes object
  decoded= data1.decode("utf-8", errors='ignore')
  #print(decoded)
  htmlparser.feed(decoded)
  return "STATUS "+ str(r1.status)+ ' '+ r1.reason


#---------------------------------------------------------------------
class DuckResultParser(HTMLParser):
  hrefurl= ''; inhref= False;  prevurl= '';  count= 0;

  def __init__(self, max=500):
    HTMLParser.__init__(self)
    self.max= max;

  def doit(self, keywords):
    url= 'https://duckduckgo.com/html'
    dd= {};  dd['q']= ' '.join(keywords);
    status= dourl(url, self, dd)
    return status

  def handle_starttag(self, tag, attrs):
    if tag=='a':  return self.handle_startatag(tag, attrs)

  def handle_startatag(self, tag, attrs):
    self.hreftitle= ''
    for attr in attrs:
      ttype= attr[0];  val= attr[1]
      if ttype=='href':
        self.inhref= True; self.hrefurl= val

  def handle_data(self, data):
    if self.inhref:
      self.hreftitle= self.hreftitle+ ' '+ DuckResultParser.html_decrappify(data)

  def handle_endtag(self, tag):
    if self.inhref:  self.handle_href()
    self.inhref= False;

  def handle_href(self):
    hrefurl= self.hrefurl
    if hrefurl== self.prevurl:  return
    if (hrefurl.startswith('http') and not ('duckduckgo.com' in hrefurl)):
      self.handle_search_result(hrefurl, self.hreftitle)
    self.hrefurl= '';  self.hreftitle= ''
    self.prevurl= hrefurl

  def html_decrappify(html):
    html = html.replace('\n', ' ').replace('\r', '')
    return html

 
