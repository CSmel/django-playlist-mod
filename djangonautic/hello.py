from datetime import datetime, timedelta

dt = datetime.now().date()
start = dt - timedelta(days=dt.weekday())
print(start)