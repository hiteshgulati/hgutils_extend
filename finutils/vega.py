import gamma
from option import Option
from datetime import datetime

file = gamma.getsum()
print(type(file))


# sept28 = datetime(2017,9,28)
# a = Option(type='c',strike=880, expiry_date = sept28)
# today= datetime.today()
# print(a.implied_price(spot=895.95, actual_volatility=.2386))
# print(a.greeks(greek='delta',spot=895.95,actual_price=32.42))