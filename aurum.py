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

import csv
import scream
import codecs
import cStringIO
from hyip import Hyip
import urllib2
import __builtin__
import sys
import getopt
from bs4 import BeautifulSoup
from lxml import html, etree
import datetime
import requests
import urlparse


today = datetime.date.today()
result_filename = 'hyip' + today.strftime('-%d-%b-%Y') + '.csv'


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


goldpoll_url = 'http://www.goldpoll.com/'
popularhyip_url = 'http://www.popularhyip.com/'


def makeHeaders():
    with open(result_filename, 'ab') as result_csvfile:
            result_writer = UnicodeWriter(result_csvfile)
            if add_delimiter_info:
                result_writer.writerow(['sep=' + MyDialect.delimiter])
            result_writer.writerow(['Name', 'Status', 'URL', 'Clean URL', 'Payouts', 'Life time',
                                   'Monitoring', 'Admin rate', 'User rate', 'Funds return',
                                   'Min deposit', 'Max deposit', 'Referral bonus', 'Payment methods'])
            result_csvfile.close()


def output(hyip):
    with open(result_filename, 'ab') as result_csvfile:
            result_writer = UnicodeWriter(result_csvfile)
            result_writer.writerow([hyip.getName(), hyip.getStatus(), hyip.getUrl(),
                                   'http://' + urlparse.urlparse(hyip.getUrl()).netloc, hyip.getPayouts(), hyip.getLife_time(),
                                   hyip.getMonitoring(), hyip.getAdmin_rate(), hyip.getUser_rate(), hyip.getFunds_return(),
                                   hyip.getMin_deposit(), hyip.getMax_deposit(), hyip.getReferral_bonus(), str(hyip.getPayment_methods())])
            result_csvfile.close()


#class MyHTTPErrorProcessor(urllib2.HTTPErrorProcessor):
#    def http_response(self, request, response):
#        code, msg, hdrs = response.code, response.msg, response.info()
#        # only add this line to stop 302 redirection.
#        print response
#        if code == 302: return response
#        if not (200 <= code < 300):
#            response = self.parent.error(
#             'http', request, response, code, msg, hdrs)
#         print response
#     return response
# https_response = http_response


if __name__ == "__main__":
    scream.say('Start main execution')
    scream.say(version_name)
    scream.say('Program warming up, this should take just seconds..')

    method = 'native'
    sites = None
    add_delimiter_info = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:s:vd", ["help", "method=", "sites=", "verbose", "delimiter"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-v", "--verbose"):
            __builtin__.verbose = True
            scream.intelliAurom_verbose = True
            scream.say('Enabling verbose mode.')
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--delimiter"):
            add_delimiter_info = True
        elif o in ("-m", "--method"):
            method = a
        elif o in ("-s", "--sites"):
            sites = a

    makeHeaders()

    if 'goldpoll' in sites:
        if method == 'static':
            scream.log('Not supported yet! Use native or dont define @method at all')
        elif method == 'native':
            doc = html.parse(goldpoll_url)
            #print etree.tostring(doc)
            elements_c10 = doc.xpath('//table[@class="cl0"]')
            scream.ssay(len(elements_c10))

            for element in elements_c10:
                scream.ssay('')
                scream.ssay('Parsing HYIP..')
                hyip = Hyip()

                local_soup = BeautifulSoup(etree.tostring(element))
                hyip_name_tag = local_soup.find("a", {"class": "nhyip"})
                hyip_name = hyip_name_tag.string
                hyip_url = 'http://www.goldpoll.com' + hyip_name_tag['href']
                scream.say('Name: ' + hyip_name.strip())
                scream.say('URL: ' + hyip_url)
                hyip.setName(hyip_name.strip())

                session = requests.session()
                a = requests.adapters.HTTPAdapter(max_retries=5)
                session.mount('http://', a)
                r = session.get(hyip_url, allow_redirects=False)
                location_found = r.headers.get('location')
                final_redirect = None
                try:
                    for redirect in session.resolve_redirects(r, r.request):
                        final_redirect = redirect.headers.get('location')
                except:
                    #redirect broken, must quit
                    scream.ssay('redirects resolved')
                finally:
                    if final_redirect is None:
                        final_redirect = location_found
                scream.ssay(final_redirect)
                hyip.setUrl(final_redirect)

                small2 = local_soup.find("td", {"class": "small2"}).contents
                for content in small2:
                    string_content = str(content.string)
                    scream.ssay('small2 found:' + string_content)
                    if (content.string is not None) and ('lifetime' in content.string):
                        index = small2.index(content) + 1
                        hyip.setLife_time(small2[index].strip())
                    if (content.string is not None) and ('monitoring' in content.string):
                        index = small2.index(content) + 1
                        hyip.setMonitoring(small2[index].strip())
                    if (content.string is not None) and ('admin rate' in content.string):
                        index = small2.index(content) + 1
                        hyip.setAdmin_rate(small2[index].strip())
                    if (content.string is not None) and ('user rate' in content.string):
                        index = small2.index(content) + 1
                        hyip.setUser_rate(small2[index].strip())
                    if (content.string is not None) and ('funds return' in content.string):
                        index = small2.index(content) + 1
                        hyip.setFunds_return(small2[index].strip())
                tabl0 = local_soup.find("td", {"class": "tabl0"}).contents
                for content in tabl0:
                    scream.ssay('tabl0 found:' + str(content.string))
                    if (content.string is not None) and ('payouts' in content.string):
                        index = tabl0.index(content) + 1
                        hyip.setPayouts(tabl0[index].strip())
                    if (content.string is not None) and ('min deposit' in content.string):
                        index = tabl0.index(content) + 1
                        hyip.setMin_deposit(tabl0[index].strip())
                    if (content.string is not None) and ('max deposit' in content.string):
                        index = tabl0.index(content) + 1
                        hyip.setMax_deposit(tabl0[index].strip())
                    if (content.string is not None) and ('referral bonus' in content.string):
                        index = tabl0.index(content) + 1
                        hyip.setReferral_bonus(tabl0[index].strip())
                cl2 = local_soup.find("td", {"class": "cl2"}).contents
                for content in cl2:
                    scream.ssay('cl2: ' + str(content.string))
                    if (content.string is not None) and ('not paid' in content.string):
                        index = cl2.index(content) + 1
                        hyip.setStatus('NOT PAYING')
                    if (content.string is not None) and ('problem' in content.string):
                        index = cl2.index(content) + 1
                        hyip.setStatus('PROBLEM')
                    if (content.string is not None) and ('waiting' in content.string):
                        index = cl2.index(content) + 1
                        hyip.setStatus('WAITING')
                    if (content.string is not None) and ('paying' in content.string):
                        index = cl2.index(content) + 1
                        hyip.setStatus('PAYING')
                cl3_candidate = local_soup.find("td", {"class": "cl3"})
                if cl3_candidate is None:
                    cl3 = local_soup.find("td", {"width": "43"}).contents
                else:
                    cl3 = cl3_candidate.contents
                #scream.ssay(cl3)
                for content in cl3:
                    #scream.ssay('cl3: ' + str(content.string))
                    scream.ssay(content.attrs)
                    if 'src' in content.attrs:
                        #scream.ssay('payment method found')
                        if (content['src'] is not None) and ('ego' in content['src']):
                            #index = cl2.index(content) + 1
                            hyip.addPayment_method('Ego')
                        elif (content['src'] is not None) and ('paypal' in content['src']):
                            #index = cl2.index(content) + 1
                            hyip.addPayment_method('Paypal')
                        elif (content['src'] is not None) and ('payza' in content['src']):
                            #index = cl2.index(content) + 1
                            hyip.addPayment_method('Payza')
                        elif (content['src'] is not None) and ('perfectm' in content['src']):
                            #index = cl2.index(content) + 1
                            hyip.addPayment_method('PerfectM')
                        elif (content['src'] is not None) and ('stp' in content['src']):
                            #index = cl2.index(content) + 1
                            hyip.addPayment_method('Stp')
                        elif (content['src'] is not None) and ('pecunix' in content['src']):
                            #index = cl2.index(content) + 1
                            hyip.addPayment_method('Pecunix')
                        elif (content['src'] is not None) and ('/small.gif' in content['src']):
                            #index = cl2.index(content) + 1
                            hyip.addPayment_method('Bankwire')
                    else:
                        scream.ssay('payment methods parsed')
                scream.ssay(small2)
                scream.ssay(cl2)
                scream.ssay(tabl0)

                output(hyip)
        elif method == 'mechanize':
            scream.log('Not supported yet! Use native or dont define @method at all')
        elif method == 'urllib2':
            scream.log('Not supported yet! Use native or dont define @method at all')
            exit(1)
            req = urllib2.Request(goldpoll_url)
            response = urllib2.urlopen(req)
            the_page = response.read()
            webpage = the_page.decode("ISO-8859-1")
            parser = etree.HTMLParser()
            #jar = cookielib.FileCookieJar("cookies")
            #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
            #response = opener.open(hyip_url)
            #print response
            #exit(1)
            tree = etree.fromstring(webpage, parser)
            elements_c10 = tree.xpath('//table[@class="cl0"]')
            scream.ssay(elements_c10)
    if 'popularhyip' in sites:
        if method == 'static':
            doc = html.parse('input\\PopularHYIP-gecko.htm')
            #print etree.tostring(doc)
            elements_status1 = doc.xpath('//tr[@class="status1" and (not(@id))]')
            scream.ssay(len(elements_status1))
            for element in elements_status1:
                scream.ssay('')
                scream.ssay('Parsing HYIP..')
                hyip = Hyip()

                local_soup = BeautifulSoup(etree.tostring(element))
                hyip_name_tag = local_soup.find("div", {"class": "ramka"})
                hyip_name = hyip_name_tag.contents[0].string
                hyip_url_onclick = hyip_name_tag['onclick'].split('\'')
                hyip_url = 'http://www.popularhyip.com' + hyip_url_onclick[1]
                scream.say('Name: ' + hyip_name.strip())
                scream.say('URL: ' + hyip_url)
                hyip.setName(hyip_name.strip())

                session = requests.session()
                a = requests.adapters.HTTPAdapter(max_retries=5)
                session.mount('http://', a)
                r = session.get(hyip_url, allow_redirects=False)
                location_found = r.headers.get('location')
                final_redirect = None
                try:
                    for redirect in session.resolve_redirects(r, r.request):
                        final_redirect = redirect.headers.get('location')
                except:
                    #redirect broken, must quit
                    scream.ssay('redirects resolved')
                finally:
                    if final_redirect is None:
                        final_redirect = location_found
                scream.ssay(final_redirect)
                hyip.setUrl(final_redirect)
            elements_status2 = doc.xpath('//tr[@class="status2" and (not(@id))]')
            scream.ssay(len(elements_status2))
            for element in elements_status2:
                scream.ssay('')
                scream.ssay('Parsing HYIP..')
                hyip = Hyip()

                local_soup = BeautifulSoup(etree.tostring(element))
                hyip_name_tag = local_soup.find("div", {"class": "ramka"})
                hyip_name = hyip_name_tag.contents[0].string
                hyip_url_onclick = hyip_name_tag['onclick'].split('\'')
                hyip_url = 'http://www.popularhyip.com' + hyip_url_onclick[1]
                scream.say('Name: ' + hyip_name.strip())
                scream.say('URL: ' + hyip_url)
                hyip.setName(hyip_name.strip())

                session = requests.session()
                a = requests.adapters.HTTPAdapter(max_retries=5)
                session.mount('http://', a)
                r = session.get(hyip_url, allow_redirects=False)
                location_found = r.headers.get('location')
                final_redirect = None
                try:
                    for redirect in session.resolve_redirects(r, r.request):
                        final_redirect = redirect.headers.get('location')
                except:
                    #redirect broken, must quit
                    scream.ssay('redirects resolved')
                finally:
                    if final_redirect is None:
                        final_redirect = location_found
                scream.ssay(final_redirect)
                hyip.setUrl(final_redirect)
            elements_status3 = doc.xpath('//tr[@class="status3" and (not(@id))]')
            scream.ssay(len(elements_status3))
            for element in elements_status3:
                scream.ssay('')
                scream.ssay('Parsing HYIP..')
                hyip = Hyip()

                local_soup = BeautifulSoup(etree.tostring(element))
                hyip_name_tag = local_soup.find("div", {"class": "ramka"})
                hyip_name = hyip_name_tag.contents[0].string
                hyip_url_onclick = hyip_name_tag['onclick'].split('\'')
                hyip_url = 'http://www.popularhyip.com' + hyip_url_onclick[1]
                scream.say('Name: ' + hyip_name.strip())
                scream.say('URL: ' + hyip_url)
                hyip.setName(hyip_name.strip())

                session = requests.session()
                a = requests.adapters.HTTPAdapter(max_retries=5)
                session.mount('http://', a)
                r = session.get(hyip_url, allow_redirects=False)
                location_found = r.headers.get('location')
                final_redirect = None
                try:
                    for redirect in session.resolve_redirects(r, r.request):
                        final_redirect = redirect.headers.get('location')
                except:
                    #redirect broken, must quit
                    scream.ssay('redirects resolved')
                finally:
                    if final_redirect is None:
                        final_redirect = location_found
                scream.ssay(final_redirect)
                hyip.setUrl(final_redirect)
            elements_status4 = doc.xpath('//tr[@class="status4" and (not(@id))]')
            scream.ssay(len(elements_status4))
            for element in elements_status4:
                scream.ssay('')
                scream.ssay('Parsing HYIP..')
                hyip = Hyip()

                local_soup = BeautifulSoup(etree.tostring(element))
                hyip_name_tag = local_soup.find("div", {"class": "ramka"})
                hyip_name = hyip_name_tag.contents[0].string
                hyip_url_onclick = hyip_name_tag['onclick'].split('\'')
                hyip_url = 'http://www.popularhyip.com' + hyip_url_onclick[1]
                scream.say('Name: ' + hyip_name.strip())
                scream.say('URL: ' + hyip_url)
                hyip.setName(hyip_name.strip())

                session = requests.session()
                a = requests.adapters.HTTPAdapter(max_retries=5)
                session.mount('http://', a)
                r = session.get(hyip_url, allow_redirects=False)
                location_found = r.headers.get('location')
                final_redirect = None
                try:
                    for redirect in session.resolve_redirects(r, r.request):
                        final_redirect = redirect.headers.get('location')
                except:
                    #redirect broken, must quit
                    scream.ssay('redirects resolved')
                finally:
                    if final_redirect is None:
                        final_redirect = location_found
                scream.ssay(final_redirect)
                hyip.setUrl(final_redirect)
        elif method == 'native':
            scream.log('Not supported yet! Use static or dont define @method at all')
            exit(1)
            doc = html.parse(popularhyip_url)
            #print etree.tostring(doc)
            elements_status4 = doc.xpath('//tr[@class="status4"]')
            scream.ssay(len(elements_status4))
        elif method == 'mechanize':
            scream.log('Not supported yet! Use static or dont define @method at all')
        elif method == 'urllib2':
            scream.log('Not supported yet! Use static or dont define @method at all')
