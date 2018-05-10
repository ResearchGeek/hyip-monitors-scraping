'''
Represents a single HYIP entity

@since 1.0
@author Oskar Jarczyk
'''


class Hyip:

    def __init__(self):
        self.payment_methods = []

    repository_name = None
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

    def get_name(self):
        return self.repository_name

    def set_name(self, name):
        self.repository_name = name

    def get_period(self):
        return self.period

    def set_period(self, period):
        self.period = period

    def get_plan_details(self):
        return self.plan_details

    def set_plan_details(self, plan_details):
        self.plan_details = plan_details

    def get_withdraw_type(self):
        return self.withdraw_type

    def set_withdraw_type(self, withdraw_type):
        self.withdraw_type = withdraw_type

    def get_principal_return(self):
        return self.principal_return

    def set_principal_return(self, principal_return):
        self.principal_return = principal_return

    def get_life_time(self):
        return self.life_time

    def set_life_time(self, life_time):
        self.life_time = life_time

    def get_monitoring(self):
        return self.monitoring

    def set_monitoring(self, monitoring):
        self.monitoring = monitoring

    def get_payouts(self):
        return self.payouts

    def set_payouts(self, payouts):
        self.payouts = payouts

    def get_admin_rate(self):
        return self.admin_rate

    def set_admin_rate(self, admin_rate):
        self.admin_rate = admin_rate

    def get_user_rate(self):
        return self.user_rate

    def set_user_rate(self, user_rate):
        self.user_rate = user_rate

    def get_funds_return(self):
        return self.funds_return

    def set_funds_return(self, funds_return):
        self.funds_return = funds_return

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_min_deposit(self):
        return self.min_deposit

    def set_min_deposit(self, min_deposit):
        self.min_deposit = min_deposit

    def get_max_deposit(self):
        return self.max_deposit

    def set_max_deposit(self, max_deposit):
        self.max_deposit = max_deposit

    def get_referral_bonus(self):
        return self.referral_bonus

    def set_referral_bonus(self, referral_bonus):
        self.referral_bonus = referral_bonus

    def get_plan(self):
        return self.plan

    def set_plan(self, plan):
        self.plan = plan

    def get_ssl(self):
        return self.ssl

    def set_ssl(self, ssl):
        self.ssl = ssl

    def get_ddos_protect(self):
        return self.ddos_protect

    def set_ddos_protect(self, ddos_protect):
        self.ddos_protect = ddos_protect

    def get_days_online(self):
        return self.days_online

    def set_days_online(self, days_online):
        self.days_online = days_online

    def get_payment_methods(self):
        return self.payment_methods

    def set_payment_methods(self, payment_methods):
        self.payment_methods = payment_methods

    def add_payment_method(self, payment_method):
        self.payment_methods.append(payment_method)
