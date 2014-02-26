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
    life_time = None
    monitoring = None
    admin_rate = None
    user_rate = None
    funds_return = None
    referral_bonus = None
    plan = None
    days_online = None

    def getName(self):
        return self.repository_name

    def setName(self, name):
        self.repository_name = name

    def getLife_time(self):
        return self.life_time

    def setLife_time(self, life_time):
        self.life_time = life_time

    def getMonitoring(self):
        return self.monitoring

    def setMonitoring(self, monitoring):
        self.monitoring = monitoring

    def getAdmin_rate(self):
        return self.admin_rate

    def setAdmin_rate(self, admin_rate):
        self.admin_rate = admin_rate

    def getUser_rate(self):
        return self.user_rate

    def setUser_rate(self, user_rate):
        self.user_rate = user_rate

    def setUrl(self, url):
        self.url = url

    def getUrl(self):
        return self.url

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def getMin_deposit(self):
        return self.min_deposit

    def setMin_deposit(self, min_deposit):
        self.min_deposit = min_deposit

    def getMax_deposit(self):
        return self.max_deposit

    def setMax_deposit(self, max_deposit):
        self.max_deposit = max_deposit

    def getPlan(self):
        return self.status

    def setPlan(self, plan):
        self.plan = plan

    def getDays_online(self):
        return self.days_online

    def setDays_online(self, days_online):
        self.days_online = days_online
