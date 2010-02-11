import csv
import datetime
import httplib
import os
import socket
import time

# Stock Market Hours: 6:30am - 1:00pm PST
# http://www.isthemarketopen.com/

MARKET_OPEN_TIME = datetime.datetime.now().replace(hour = 6,
                                                   minute = 30,
                                                   second = 0,
                                                   microsecond = 0)

MARKET_CLOSE_TIME = datetime.datetime.now().replace(hour = 13,
                                                    minute = 0,
                                                    second = 0,
                                                    microsecond = 0)

# Dow Jones Industrial Average -> indu
# Nasdaq Composite Index -> comp
# S&P 500 Index -> spx

STOCK_SYMBOLS = "goog+srs+skf+uyg+indu+comp+spx"

# Yahoo Tags
# s -> Symbol
# b2 -> Ask (Real-time)
# b3 -> Bid (Real-time)
# g -> Day's Low
# h -> Day's High
# j -> 52-Week Low
# k -> 52-Week High
# v -> Volume
# d1 -> Last Trade Date
# t1 -> Last Trade Time

TAGS = "sb2b3ghjkvd1t1"
NUM_FIELDS = 10

def GetRequestData():
  h = httplib.HTTPConnection("download.finance.yahoo.com")
  h.request("GET", "/d/quotes.csv?s=%s&f=%s" % (STOCK_SYMBOLS, TAGS))
  r = h.getresponse()
  h.close()
  return r.read().split("\r\n")


def GetDirectory():
  return os.path.join(os.environ["HOMEPATH"],
                      "My Documents",
                      "development",
                      "data",
                      "stock_data",
                      datetime.date.today().strftime("%Y-%m-%d"))


def GetFilename(sym):
  d = GetDirectory()
  if not os.path.exists(d):
    os.makedirs(d)
  return os.path.join(d, "%s.csv" % sym)


def QueryStockQuotes():
  reader = csv.reader(GetRequestData())
  for row in reader:
    if len(row) == NUM_FIELDS:
      writer = csv.writer(open(GetFilename(row[0]), "a"))
      writer.writerow(row +
                      [datetime.datetime.now().strftime("%Y/%m/%d.%H:%M:%S")])

if datetime.datetime.now() < MARKET_OPEN_TIME:
  sleep_period = (MARKET_OPEN_TIME - datetime.datetime.now()).seconds
  print "Market is not open yet, sleeping for %d seconds" % sleep_period
  time.sleep(sleep_period)

while datetime.datetime.now() < MARKET_CLOSE_TIME:
  QueryStockQuotes()
  time.sleep(5)

print "Finished collecting stats"
