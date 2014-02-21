'''
Represents a single Hyip being

@since 1.0
@author Oskar Jarczyk
'''


class Hyip():

    element_type = 'Hyip'
    key = None

    def __init__(self):
        self.data = []

    name = None
    url = None
    status = None
    status_date = None
    payouts = None
    min_deposit = None
    max_deposit = None
    referral_bonus = None

    def setName(self, name):
        self.repository_name = name

    def getName(self):
        return self.repository_name

    def setUrl(self, url):
        self.url = url

    def getUrl(self):
        return self.url
