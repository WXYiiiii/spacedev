from datetime import datetime, timedelta
start_date = (datetime.now() - timedelta(weeks=0)).date()

data = []
data.append(start_date)

print(start_date)
print(data)
