#!/usr/bin/python
import csv
import numpy as np
import re
import datetime
import itertools

class ParseCsvWithHeaders(object):
  
  def __init__(self, csvfile):
    f = open(csvfile, "r")
    reader = csv.reader(f)

    self.headers = reader.next()
    for varname in self.headers:
      setattr(self, varname, [])

    istime = re.compile(re.escape('time'), re.IGNORECASE)
    for row in reader:
      for col, varname in itertools.izip(row, self.headers):
        col_val = None
        if istime.findall(varname):
          col_val = datetime.datetime.fromtimestamp(float(col))
        else:
          col_val = float(col)
        getattr(self, varname).append(col_val)

    for varname in self.headers:
      setattr(self, "np_"+varname, np.array(getattr(self, varname)) )

