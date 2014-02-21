# coding=UTF-8
'''
Downloads data from popular hyip monitors

@version 1.0 Midnight

Midnight is a leisure planet visited by the Doctor and Donna in the episode of the same name.
It has golden spas, anti-gravity restaurants, sapphire waterfalls, and a landscape of diamonds.
The planet's sun emits x-tonic radiation, which vaporises organic matter and can only be viewed
safely through sufficiently thick finito glass. The radiation poisons the diamonds, so the planet's
surface can never be touched.

@author Oskar Jarczyk
@since 1.0
@update 21.02.2014
'''

version_name = 'version 1.0 codename: Midnight'
pull_request_filename = 'hyip.csv'

import csv
import scream
import codecs
import cStringIO
import requests
import urllib2
import __builtin__
import sys
import getopt
from bs4 import BeautifulSoup
from lxml import html, etree


class MyDialect(csv.Dialect):
    strict = True
    skipinitialspace = True
    quoting = csv.QUOTE_MINIMAL
    delimiter = ','
    escapechar = '\\'
    quotechar = '"'
    lineterminator = '\n'


class ReadDialect(csv.Dialect):
    strict = True
    skipinitialspace = False
    quoting = csv.QUOTE_NONE
    delimiter = ','
    escapechar = '\\'
    lineterminator = '\n'


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=ReadDialect, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=MyDialect, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def usage():
    f = open('usage.txt', 'r')
    for line in f:
        print line


if __name__ == "__main__":
    scream.say('Start main execution')
    scream.say(version_name)
    scream.say('Program warming up, this should take just seconds..')

    method = 'native'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:v", ["help", "method=", "verbose"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-v", "--verbose"):
            __builtin__.verbose = True
            scream.intelliAurom_verbose = True
            scream.ssay('Enabling verbose mode.')
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-m", "--method"):
            method = a

    url = 'http://www.goldpoll.com/'

    if method == 'native':
        doc = html.parse(url)
        #print etree.tostring(doc)
        elements_c10 = doc.xpath('//table[@class="cl0"]')
        scream.ssay(len(elements_c10))

        for element in elements_c10:
            scream.ssay('Parsing HYIP..')
            local_soup = BeautifulSoup(etree.tostring(element))
            small2 = local_soup.findAll("td", {"class": "small2"})
            tabl0 = local_soup.findAll("td", {"class": "tabl0"})
            cl2 = local_soup.findAll("td", {"class": "cl2"})
            scream.ssay(small2)
            scream.ssay(cl2)
            scream.ssay(tabl0)
    elif method == 'urllib2':
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        the_page = response.read()
        webpage = the_page.decode("ISO-8859-1")
        parser = etree.HTMLParser()
        tree = etree.fromstring(webpage, parser)
        elements_c10 = tree.xpath('//table[@class="cl0"]')
        scream.ssay(elements_c10)
