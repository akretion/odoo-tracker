# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from functools import wraps
import cProfile

from time import perf_counter as time_now

import csv
import subprocess
from os import path
import os


class TrackerOuput(object):

    def __init__(self):
        super(TrackerOuput, self).__init__()
        self.writer = None

    def create(self, fcsvname):
        output = open(fcsvname, "w")
        self.writer = csv.DictWriter(output, fieldnames=[
            "model",
            "method",
            "duration",
            "args",
            "kwargs",
            ])
        self.writer.writeheader()

    def writerow(self, data):
        self.writer.writerow(data)

    def ready(self):
        return bool(self.writer)

tracker_output = TrackerOuput()


def profile_call(directory, fname, func, *args, **kwargs):
    if not os.path.exists(directory):
        os.makedirs(directory)
    start = time_now()
    fcsvname = os.path.join(directory, "%s.csv" % fname)
    fcprofname = os.path.join(directory, "%s.cprof" % fname)
    fxdotname = os.path.join(directory, "%s.xdot" % fname)
    tracker_output.create(fcsvname)
    profile = cProfile.Profile()
    result = profile.runcall(func, *args, **kwargs)
    print("Duration: ", time_now() - start)
    profile.dump_stats(fcprofname)
    subprocess.call(["gprof2dot", "-f", "pstats", "-o", fxdotname, fcprofname])

def tracker(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start = time_now()
        result = func(self, *args, **kwargs)
        duration = time_now() - start
        if tracker_output.ready():
            tracker_output.writerow({
                'model': self._name,
                'method': func.__name__,
                'duration': duration,
                'args': args,
                'kwargs': kwargs,
                })
        return result
    return wrapper

