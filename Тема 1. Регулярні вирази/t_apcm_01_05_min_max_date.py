# Мінімальна та максимальна дата

import re
from datetime import datetime

P_DATE = r'\b\d{2}\.\d{2}\.\d{4}'

filename = input("ім'я файлу: ")
with open(filename, 'r') as f:
    cnt = ' '.join(f.read().split())

dates = re.findall(P_DATE, cnt)
dates_converted = list(map(lambda d: datetime.strptime(d, "%d.%m.%Y"), dates))

min_date = min(dates_converted)
max_date = max(dates_converted)

print("min: {}, max: {}".format(min_date, max_date))

td = max_date - min_date
print("днів між:", td.days)

print("день тижня макс дати:", max_date.weekday())

