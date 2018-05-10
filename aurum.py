# coding=UTF-8

import csv
import codecs
from hyip import Hyip
import sys
import getopt
from bs4 import BeautifulSoup
from lxml import html, etree
import datetime
import requests
import six
from six.moves import cStringIO
from six.moves import urllib

'''
Downloads data from popular HYIP monitors

@version 1.1 Aurum

Changelog

** 10.05.2018 - Moved code to compatible with Python3 and 2 (through six package)
** 09.05.2018 - Starting investigating perils and promises of this module
** 21.02.2014 - Initial working version

@author Oskar Jarczyk
@since 1.0
@update 10.05.2018
'''

version_name = 'version 1.1 codename: Aurum'

today = datetime.date.today()
result_filename = 'hyip' + today.strftime('-%d-%b-%Y') + '.csv'


def isWindows():
    if sys.platform.startswith('win'):
        return True
    else:
        return False


def isLinux():
    if sys.platform.startswith('linux'):
        return True
    else:
        return False


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
        return [six.text_type(s) for s in row]  # TODO: check if we should do .encode('utf-8')

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
        # ... and re-encode it into the target encoding
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
        six.print_(line)


goldpoll_url = 'http://www.goldpoll.com/'
popularhyip_url = 'http://www.popularhyip.com/'
verbose = False


def makeHeaders():
    with open(result_filename, 'ab') as result_csvfile:
            result_writer = UnicodeWriter(result_csvfile)
            if add_delimiter_info:
                result_writer.writerow(['sep=' + MyDialect.delimiter])
            result_writer.writerow(['Name', 'Status', 'URL', 'Clean URL', 'Payouts', 'Life time',
                                   'Monitoring', 'Admin rate', 'User rate', 'Funds return',
                                   'Min deposit', 'Max deposit', 'Referral bonus', 'Payment methods', 'Plan'])
            result_csvfile.close()


def output(hyip, portalname):
    with open(portalname + '-' + result_filename, 'ab') as result_csvfile:
            result_writer = UnicodeWriter(result_csvfile)
            result_writer.writerow([hyip.get_name(), hyip.getStatus(), hyip.getUrl(),
                                   'http://' + urllib.prase(hyip.getUrl()).netloc, hyip.getPayouts(), hyip.getLife_time(),
                                    hyip.getMonitoring(), hyip.getAdmin_rate(), hyip.getUser_rate(), hyip.getFunds_return(),
                                    hyip.getMin_deposit(), hyip.getMax_deposit(), hyip.getReferral_bonus(),
                                    str(hyip.getPayment_methods()), hyip.getPlan()])
            result_csvfile.close()


if __name__ == "__main__":
    six.print_('Start main execution')
    six.print_(version_name)
    six.print_('Program warming up, this should take just seconds..')

    method = 'native'
    sites = None
    add_delimiter_info = False
    geckoname = 'PopularHYIP-gecko.htm'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:s:i:vd", ["help", "method=", "sites=", "input=", "verbose", "delimiter"])
    except getopt.GetoptError as err:
        # print help information and exit:
        six.print_(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-v", "--verbose"):
            # __builtin__.verbose = True
            verbose = True
            six.print_('Enabling verbose mode.')
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--delimiter"):
            add_delimiter_info = True
        elif o in ("-m", "--method"):
            method = a
        elif o in ("-s", "--sites"):
            sites = a
        elif o in ("-i", "--input"):
            geckoname = a

    makeHeaders()

    if 'goldpoll' in sites:
        if method == 'static':
            six.print_('Not supported yet! Use native or dont define @method at all')
        elif method == 'native':
            doc = html.parse(goldpoll_url)
            #print etree.tostring(doc)
            elements_c10 = doc.xpath('//table[@class="cl0"]')
            six.print_(len(elements_c10))

            for element in elements_c10:
                six.print_('')
                six.print_('Parsing HYIP..')
                hyip = Hyip()

                local_soup = BeautifulSoup(etree.tostring(element))
                hyip_name_tag = local_soup.find("a", {"class": "nhyip"})
                hyip_name = hyip_name_tag.string
                hyip_url = 'http://www.goldpoll.com' + hyip_name_tag['href']
                six.print_('Name: ' + hyip_name.strip())
                six.print_('URL: ' + hyip_url)
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
                    six.print_('redirects resolved')
                finally:
                    if final_redirect is None:
                        final_redirect = location_found
                six.print_(final_redirect)
                hyip.setUrl(final_redirect)

                small2 = local_soup.find("td", {"class": "small2"}).contents
                for content in small2:
                    string_content = str(content.string)
                    six.print_('small2 found:' + string_content)
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
                    six.print_('tabl0 found:' + str(content.string))
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
                    six.print_('cl2: ' + str(content.string))
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
                #six.print_(cl3)
                for content in cl3:
                    #six.print_('cl3: ' + str(content.string))
                    six.print_(content.attrs)
                    if 'src' in content.attrs:
                        #six.print_('payment method found')
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
                        six.print_('payment methods parsed')
                six.print_(small2)
                six.print_(cl2)
                six.print_(tabl0)

                output(hyip)
        elif method == 'mechanize':
            six.print_('Not supported yet! Use native or dont define @method at all')
        elif method == 'urllib2':
            six.print_('Not supported yet! Use native or dont define @method at all')
            exit(1)
            req = urllib.request(goldpoll_url)  # urllib2.Request(goldpoll_url)
            response = urllib.urlopen(req)  # urllib2.urlopen(req)
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
            six.print_(elements_c10)
    if 'popularhyip' in sites:
        if method == 'static':
            dir_separator = ('\\' if isWindows() else '/')
            doc = html.parse('input' + dir_separator + geckoname)
            #print etree.tostring(doc)
            elements_status1 = doc.xpath('//tr[@class="status1" and (not(@id))]')
            six.print_(len(elements_status1))
            for element in elements_status1:
                six.print_('')
                six.print_('Parsing HYIP..')
                hyip = Hyip()

                local_soup = BeautifulSoup(etree.tostring(element))
                hyip_name_tag = local_soup.find("div", {"class": "ramka"})
                hyip_name = six.text_type(hyip_name_tag.contents[0].string).strip()
                hyip_plan = six.text_type(hyip_name_tag.contents[2].string).strip()
                hyip_url_onclick = hyip_name_tag['onclick'].split('\'')
                hyip_url = 'http://www.popularhyip.com' + hyip_url_onclick[1]
                six.print_('Name: ' + hyip_name)
                six.print_('URL: ' + hyip_url)
                hyip.setName(hyip_name)
                six.print_(hyip_plan)
                hyip.setPlan(hyip_plan)

                session = requests.session()
                a = requests.adapters.HTTPAdapter(pool_connections=256, pool_maxsize=256, max_retries=10)
                session.mount('http://', a)
                r = session.get(hyip_url, allow_redirects=False, timeout=6)
                location_found = r.headers.get('location')
                final_redirect = None
                try:
                    for redirect in session.resolve_redirects(r, r.request):
                        final_redirect = redirect.headers.get('location')
                except:
                    #redirect broken, must quit
                    six.print_('redirects resolved')
                finally:
                    if final_redirect is None:
                        final_redirect = location_found
                six.print_(final_redirect)
                hyip.setUrl(final_redirect)
                hyip.setStatus('NOT PAYING')

                informations = local_soup.findAll("td")
                for i in informations:
                    six.print_(i.contents)
                hyip.setUser_rate(informations[2].contents[0].string.strip())
                hyip.setPayouts(informations[3].contents[0].contents[0].string.strip())
                hyip.setMonitoring(informations[4].contents[0].string.strip())
                hyip.setPlan_details(informations[5].contents[0].string.strip())
                hyip.setPrincipal_return(informations[6].contents[0].string.strip())
                hyip.setWithdraw_type(informations[7].contents[0].string.strip())

                hyip.setDays_online(informations[8].contents[0].string.strip())
                hyip.setMin_deposit(informations[10].contents[0].string.strip())
                hyip.setMax_deposit(informations[11].contents[0].string.strip())
                hyip.setReferral_bonus(informations[12].contents[0].string.strip())

                hyip.setSsl(informations[15].contents[0].string.strip())
                hyip.setDdos_protect(informations[14].contents[0].string.strip())
                for payi in informations[16].contents:
                    six.print_(payi.attrs)
                    if 'pm2' in payi['class']:
                        hyip.addPayment_method('PerfectM')
                    elif 'pm3' in payi['class']:
                        hyip.addPayment_method('Bankwire')
                    elif 'pm4' in payi['class']:
                        hyip.addPayment_method('BitCoin')
                    elif 'pm5' in payi['class']:
                        hyip.addPayment_method('Ego')
                    elif 'pm6' in payi['class']:
                        hyip.addPayment_method('Stp')
                    elif 'pm7' in payi['class']:
                        hyip.addPayment_method('Payza')
                six.print_(hyip.getPayment_methods())

                hyip.setLife_time('N/A')
                # get a "lifetime" from the "view full details"

                hyip.setFunds_return('N/A')
                hyip.setAdmin_rate('N/A')
                output(hyip, 'popularhyip')
            elements_status2 = doc.xpath('//tr[@class="status2" and (not(@id))]')
            six.print_(len(elements_status2))
            for element in elements_status2:
                six.print_('')
                six.print_('Parsing HYIP..')
                hyip = Hyip()

                local_soup = BeautifulSoup(etree.tostring(element))
                hyip_name_tag = local_soup.find("div", {"class": "ramka"})
                hyip_name = six.text_type(hyip_name_tag.contents[0].string).strip()
                hyip_plan = six.text_type(hyip_name_tag.contents[2].string).strip()
                hyip_url_onclick = hyip_name_tag['onclick'].split('\'')
                hyip_url = 'http://www.popularhyip.com' + hyip_url_onclick[1]
                six.print_('Name: ' + hyip_name)
                six.print_('URL: ' + hyip_url)
                hyip.setName(hyip_name)
                six.print_(hyip_plan)
                hyip.setPlan(hyip_plan)

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
                    six.print_('redirects resolved')
                finally:
                    if final_redirect is None:
                        final_redirect = location_found
                six.print_(final_redirect)
                hyip.setUrl(final_redirect)
                hyip.setStatus('PROBLEM')

                informations = local_soup.findAll("td")
                for i in informations:
                    six.print_(i.contents)
                hyip.setUser_rate(informations[2].contents[0].string.strip())
                hyip.setPayouts(informations[3].contents[0].contents[0].string.strip())
                hyip.setMonitoring(informations[4].contents[0].string.strip())
                hyip.setPlan_details(informations[5].contents[0].string.strip())
                hyip.setPrincipal_return(informations[6].contents[0].string.strip())
                hyip.setWithdraw_type(informations[7].contents[0].string.strip())

                hyip.setDays_online(informations[8].contents[0].string.strip())
                hyip.setMin_deposit(informations[10].contents[0].string.strip())
                hyip.setMax_deposit(informations[11].contents[0].string.strip())
                hyip.setReferral_bonus(informations[12].contents[0].string.strip())

                hyip.setSsl(informations[15].contents[0].string.strip())
                hyip.setDdos_protect(informations[14].contents[0].string.strip())
                for payi in informations[16].contents:
                    six.print_(payi.attrs)
                    if 'pm2' in payi['class']:
                        hyip.addPayment_method('PerfectM')
                    elif 'pm3' in payi['class']:
                        hyip.addPayment_method('Bankwire')
                    elif 'pm4' in payi['class']:
                        hyip.addPayment_method('BitCoin')
                    elif 'pm5' in payi['class']:
                        hyip.addPayment_method('Ego')
                    elif 'pm6' in payi['class']:
                        hyip.addPayment_method('Stp')
                    elif 'pm7' in payi['class']:
                        hyip.addPayment_method('Payza')
                six.print_(hyip.getPayment_methods())
                hyip.setLife_time('N/A')
                # get a "lifetime" from the "view full details"

                hyip.setFunds_return('N/A')
                hyip.setAdmin_rate('N/A')
                output(hyip, 'popularhyip')
            elements_status3 = doc.xpath('//tr[@class="status3" and (not(@id))]')
            six.print_(len(elements_status3))
            for element in elements_status3:
                six.print_('')
                six.print_('Parsing HYIP..')
                hyip = Hyip()

                local_soup = BeautifulSoup(etree.tostring(element))
                hyip_name_tag = local_soup.find("div", {"class": "ramka"})
                hyip_name = six.text_type(hyip_name_tag.contents[0].string).strip()
                hyip_plan = six.text_type(hyip_name_tag.contents[2].string).strip()
                hyip_url_onclick = hyip_name_tag['onclick'].split('\'')
                hyip_url = 'http://www.popularhyip.com' + hyip_url_onclick[1]
                six.print_('Name: ' + hyip_name)
                six.print_('URL: ' + hyip_url)
                hyip.setName(hyip_name)
                six.print_(hyip_plan)
                hyip.setPlan(hyip_plan)

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
                    six.print_('redirects resolved')
                finally:
                    if final_redirect is None:
                        final_redirect = location_found
                six.print_(final_redirect)
                hyip.setUrl(final_redirect)
                hyip.setStatus('WAITING')

                informations = local_soup.findAll("td")
                for i in informations:
                    six.print_(i.contents)
                hyip.setUser_rate(informations[2].contents[0].string.strip())
                hyip.setPayouts(informations[3].contents[0].contents[0].string.strip())
                hyip.setMonitoring(informations[4].contents[0].string.strip())
                hyip.setPlan_details(informations[5].contents[0].string.strip())
                hyip.setPrincipal_return(informations[6].contents[0].string.strip())
                hyip.setWithdraw_type(informations[7].contents[0].string.strip())

                hyip.setDays_online(informations[8].contents[0].string.strip())
                hyip.setMin_deposit(informations[10].contents[0].string.strip())
                hyip.setMax_deposit(informations[11].contents[0].string.strip())
                hyip.setReferral_bonus(informations[12].contents[0].string.strip())

                hyip.setSsl(informations[15].contents[0].string.strip())
                hyip.setDdos_protect(informations[14].contents[0].string.strip())
                for payi in informations[16].contents:
                    six.print_(payi.attrs)
                    if 'pm2' in payi['class']:
                        hyip.addPayment_method('PerfectM')
                    elif 'pm3' in payi['class']:
                        hyip.addPayment_method('Bankwire')
                    elif 'pm4' in payi['class']:
                        hyip.addPayment_method('BitCoin')
                    elif 'pm5' in payi['class']:
                        hyip.addPayment_method('Ego')
                    elif 'pm6' in payi['class']:
                        hyip.addPayment_method('Stp')
                    elif 'pm7' in payi['class']:
                        hyip.addPayment_method('Payza')
                six.print_(hyip.getPayment_methods())
                hyip.setLife_time('N/A')
                # get a "lifetime" from the "view full details"

                hyip.setFunds_return('N/A')
                hyip.setAdmin_rate('N/A')
                output(hyip, 'popularhyip')
            elements_status4 = doc.xpath('//tr[@class="status4" and (not(@id))]')
            six.print_(len(elements_status4))
            for element in elements_status4:
                six.print_('')
                six.print_('Parsing HYIP..')
                hyip = Hyip()

                local_soup = BeautifulSoup(etree.tostring(element))
                hyip_name_tag = local_soup.find("div", {"class": "ramka"})
                hyip_name = six.text_type(hyip_name_tag.contents[0].string).strip()
                hyip_plan = six.text_type(hyip_name_tag.contents[2].string).strip()
                hyip_url_onclick = hyip_name_tag['onclick'].split('\'')
                hyip_url = 'http://www.popularhyip.com' + hyip_url_onclick[1]
                six.print_('Name: ' + hyip_name)
                six.print_('URL: ' + hyip_url)
                hyip.setName(hyip_name)
                six.print_(hyip_plan)
                hyip.setPlan(hyip_plan)

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
                    six.print_('redirects resolved')
                finally:
                    if final_redirect is None:
                        final_redirect = location_found
                six.print_(final_redirect)
                hyip.setUrl(final_redirect)
                hyip.setStatus('PAYING')

                informations = local_soup.findAll("td")
                for i in informations:
                    six.print_(i.contents)
                hyip.setUser_rate(informations[2].contents[0].string.strip())
                hyip.setPayouts(informations[3].contents[0].contents[0].string.strip())
                hyip.setMonitoring(informations[4].contents[0].string.strip())
                hyip.setPlan_details(informations[5].contents[0].string.strip())
                hyip.setPrincipal_return(informations[6].contents[0].string.strip())
                hyip.setWithdraw_type(informations[7].contents[0].string.strip())

                hyip.setDays_online(informations[8].contents[0].string.strip())
                hyip.setMin_deposit(informations[10].contents[0].string.strip())
                hyip.setMax_deposit(informations[11].contents[0].string.strip())
                hyip.setReferral_bonus(informations[12].contents[0].string.strip())

                hyip.setSsl(informations[15].contents[0].string.strip())
                hyip.setDdos_protect(informations[14].contents[0].string.strip())
                for payi in informations[16].contents:
                    six.print_(payi.attrs)
                    if 'pm2' in payi['class']:
                        hyip.addPayment_method('PerfectM')
                    elif 'pm3' in payi['class']:
                        hyip.addPayment_method('Bankwire')
                    elif 'pm4' in payi['class']:
                        hyip.addPayment_method('BitCoin')
                    elif 'pm5' in payi['class']:
                        hyip.addPayment_method('Ego')
                    elif 'pm6' in payi['class']:
                        hyip.addPayment_method('Stp')
                    elif 'pm7' in payi['class']:
                        hyip.addPayment_method('Payza')
                six.print_(hyip.getPayment_methods())
                hyip.setLife_time('N/A')
                # get a "lifetime" from the "view full details"

                hyip.setFunds_return('N/A')
                hyip.setAdmin_rate('N/A')
                output(hyip, 'popularhyip')
        elif method == 'native':
            six.print_('Not supported yet! Use static or dont define @method at all')
            exit(1)
            doc = html.parse(popularhyip_url)
            #print etree.tostring(doc)
            elements_status4 = doc.xpath('//tr[@class="status4"]')
            six.print_(len(elements_status4))
        elif method == 'mechanize':
            six.print_('Not supported yet! Use static or dont define @method at all')
        elif method == 'urllib2':
            six.print_('Not supported yet! Use static or dont define @method at all')
