from datetime import timedelta, date


def daterange(start_date, end_date, inclusive=True):
    if inclusive:
        included_dates = 1
    else:
        included_dates = 0
    for n in range(int((end_date-start_date).days+included_dates)):
        yield start_date + timedelta(n)


def test_daterange():
    start_date = date(2017,8,11)
    end_date = date(2017,8,29)
    for fetch_date in daterange(start_date, end_date, inclusive=True):
        print(fetch_date.strftime('%d_%m_%Y'))