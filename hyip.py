'''
Represents a single Hyip being

@since 1.0
@author Oskar Jarczyk
'''


class Hyip():

    def __init__(self):
        self.payment_methods = []

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
    plan_details = None
    period = None
    days_online = None
    payment_methods = None
    principal_return = None
    withdraw_type = None
    ssl = None
    ddos_protect = None

    def getName(self):
        return self.repository_name

    def setName(self, name):
        self.repository_name = name

    def getPeriod(self):
        return self.period

    def setPeriod(self, period):
        self.period = period

    def getPlan_details(self):
        return self.plan_details

    def setPlan_details(self, plan_details):
        self.plan_details = plan_details

    def getWithdraw_type(self):
        return self.withdraw_type

    def setWithdraw_type(self, withdraw_type):
        self.withdraw_type = withdraw_type

    def getPrincipal_return(self):
        return self.principal_return

    def setPrincipal_return(self, principal_return):
        self.principal_return = principal_return

    def getLife_time(self):
        return self.life_time

    def setLife_time(self, life_time):
        self.life_time = life_time

    def getMonitoring(self):
        return self.monitoring

    def setMonitoring(self, monitoring):
        self.monitoring = monitoring

    def getPayouts(self):
        return self.payouts

    def setPayouts(self, payouts):
        self.payouts = payouts

    def getAdmin_rate(self):
        return self.admin_rate

    def setAdmin_rate(self, admin_rate):
        self.admin_rate = admin_rate

    def getUser_rate(self):
        return self.user_rate

    def setUser_rate(self, user_rate):
        self.user_rate = user_rate

    def getFunds_return(self):
        return self.funds_return

    def setFunds_return(self, funds_return):
        self.funds_return = funds_return

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

    def getReferral_bonus(self):
        return self.referral_bonus

    def setReferral_bonus(self, referral_bonus):
        self.referral_bonus = referral_bonus

    def getPlan(self):
        return self.plan

    def setPlan(self, plan):
        self.plan = plan

    def getSsl(self):
        return self.ssl

    def setSsl(self, ssl):
        self.ssl = ssl

    def getDdos_protect(self):
        return self.ddos_protect

    def setDdos_protect(self, ddos_protect):
        self.ddos_protect = ddos_protect

    def getDays_online(self):
        return self.days_online

    def setDays_online(self, days_online):
        self.days_online = days_online

    def getPayment_methods(self):
        return self.payment_methods

    def setPayment_methods(self, payment_methods):
        self.payment_methods = payment_methods

    def addPayment_method(self, payment_method):
        self.payment_methods.append(payment_method)
