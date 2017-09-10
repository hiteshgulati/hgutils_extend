from py_vollib.black_scholes_merton import black_scholes_merton as bs
import py_vollib.black_scholes_merton.implied_volatility as iv
from py_vollib.black_scholes_merton.greeks import numerical as greek_numerical
from py_vollib.black_scholes_merton.greeks import analytical as greek_analytical
from datetime import datetime
from calendar import monthrange
#print(bs(flag='c', S=899,K=900,t=(23/365),r=.1,sigma=.257,q=0))
print()


class Option:

    month_lookup = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN',
                    7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}

    def __init__(self, strike,
                 expiry_date, underlying = 'NIFTY',
                 interest_rate=.1, type='c'):
        self.type = type.upper() #call or put
        self.strike = strike
        self.expiry_date = expiry_date
        self.underlying = underlying.upper()
        self.interest_rate = interest_rate
        self.symbol = self.get_symbol()

    def get_symbol(self):
        symbol = self.underlying
        symbol += str(self.expiry_date.year)[-2:]
        symbol += self.month_lookup[self.expiry_date.month]
        symbol += str(self.strike)
        symbol += self.type + 'E'
        return symbol

    def _last_thursday(self, date_month=datetime.now()):
        mr = monthrange(date_month.year, date_month.month)
        last_thursday_date = mr[1]-(mr[0]+(mr[1] % 7)-1-3)
        return datetime(date_month.year,date_month.month,last_thursday_date)

    def days_to_expiry(self,from_date = datetime.today()):
        return (self.expiry_date - from_date).days

    def implied_price(self,spot, actual_volatility, on_date = datetime.today(),
                      interest_rate=None,
                      dividend_yield = 0):
        if not interest_rate:
            interest_rate = self.interest_rate
        return bs(flag=self.type, S=spot, K=self.strike,
                  t=self.days_to_expiry(on_date)/365, sigma=actual_volatility,
                  q=dividend_yield, r=interest_rate)

    def implied_volatility(self,spot, actual_price, on_date=datetime.today(),
                           interest_rate=None, dividend_yield = 0):
        if not interest_rate:
            interest_rate = self.interest_rate

        return iv.implied_volatility(price=actual_price, S=spot,K=self.strike,
                               t=self.days_to_expiry(on_date)/365,
                               r=interest_rate, q=dividend_yield, flag=self.type)


    def greeks(self, greek, spot, actual_price, on_date=datetime.today(),
              interest_rate=None, dividend_yield=0, type='a'):
        if not interest_rate:
            interest_rate=self.interest_rate
        implied_volatility = self.implied_volatility(spot=spot,
                                                     actual_price=actual_price,
                                                     on_date=on_date,
                                                     interest_rate=interest_rate,
                                                     dividend_yield=dividend_yield)
        greek_dict = {'d':'delta','t':'theta','g':'gamma','v':'vega','r':'rho'}
        if greek in greek_dict.keys():
            greek = greek_dict[greek]
        if greek not in greek_dict.values():
            greek = 'delta'
        if type == 'a':
            measure = getattr(greek_analytical,greek)(flag=self.type,S=spot,K=self.strike,
                                     t=self.days_to_expiry(on_date) / 365,
                                     r=interest_rate, sigma=implied_volatility,
                                     q=dividend_yield)
        elif type == 'n':
            measure = getattr(greek_numerical,greek)(flag=self.type,S=spot,K=self.strike,
                                     t=self.days_to_expiry(on_date) / 365,
                                     r=interest_rate, sigma=implied_volatility,
                                     q=dividend_yield)
        return measure


