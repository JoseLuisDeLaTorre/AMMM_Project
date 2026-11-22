
"""
Time periods I, index i, status can be 0 or 1.
"""

class TimePeriod(object):
    def __init__(self, timeId, status, energy, profit):
        self._timeId = timeId
        self._status = status

        self._energy = energy
        self._profit = profit

    def getId(self):
        return self._timeId

    def getStatus(self):
        return self._status

    def getEnergy(self):
        return self._energy 

    def getProfit(self):
        return self._profit

    def __str__(self):
        return "_timeId: %d (status %d)" % (self._timeId, self._status)