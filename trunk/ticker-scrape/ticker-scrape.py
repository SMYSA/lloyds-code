import httplib
import socket

def make_request():
  h = httplib.HTTPConnection("download.finance.yahoo.com")
  h.request("GET", "/d/quotes.csv?s=GOOG+srs+skf+uyg+&f=sb2b3ghjkv")
  r = h.getresponse()
  d = r.read()
  h.close()
  print d

make_request()
