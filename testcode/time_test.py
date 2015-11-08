#!/usr/bin/env python
import random
import time
from datetime import datetime, date

time_time = time.time()
timestamp = long(time_time * 1000)
print timestamp
print time_time

time_ = lambda: int(round(time.time() * 1000))
print time_()
time.sleep(0.005)
print time_()


def date_time_milliseconds(date_time_obj):
    return int(time.mktime(date_time_obj.timetuple()) * 1000)


print date_time_milliseconds(datetime.strptime(datetime.strftime(date.today(), "%Y-%m"), "%Y-%m"))

print date_time_milliseconds(datetime.strptime('2015-02', "%Y-%m"))

print "asdfadsf\\\\adfjadsf//asdfjadslfj".replace("/", "|").replace("\\", "|")
