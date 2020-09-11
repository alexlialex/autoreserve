import datetime
from datetime import timedelta

class dateutility:
    def __init__(self):
        self.update()

    def get_date_str(self, date):
        return date.strftime("%B %d, %Y")

    def get_current(self):
        self.update()
        return self.get_date_str(self.current)

    def get_latest_available_dt(self):
        self.update()
        return self.current + timedelta(days=6)

    def get_latest_available_str(self):
        return self.get_date_str(self.get_latest_available_dt())

    def int_to_time(self, n):
        # n in the form HHMM
        n = int(n)
        return datetime.time(int(n / 100), n % 100, 0)

    def increment_time(self, time_obj, mins):
        t = datetime.datetime.combine((self.get_latest_available_dt()).date(), time_obj)
        if mins >= 0:
            return (t + timedelta(minutes=mins)).time()
        else:
            return (t - timedelta(minutes=mins * -1)).time()

    def update(self):
        self.current = datetime.datetime.now()