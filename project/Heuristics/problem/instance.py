"""
AMMM Lab Heuristics
Representation of a problem instance
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from Heuristics.problem.solution import Solution

from Heuristics.problem.TimePeriod import TimePeriod


class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        print("----------------_",config, inputData)
        self.L = inputData.L
        self.U = inputData.U
        self.T = inputData.T
        
        nTimes =  inputData.N

        P = inputData.P
        E = inputData.E

        self.timePeriods = [None] * nTimes
        for tId in range(0, nTimes):
            self.timePeriods[tId] = TimePeriod(tId, 0, E[tId], P[tId])


    def getNumTimePeriods(self):
        return len(self.timePeriods)        

    def getTimePeriods(self):
        return self.timePeriods

    def createSolution(self):
        solution = Solution(
            self.timePeriods,
            minimumOnPeriods=self.L,
            maximumOnPeriods=self.U,
            minimumProfit=self.T,
        )
        solution.setVerbose(self.config.verbose)
        return solution

    #MAX energy, set as true the periods that uses less energy
    def checkInstance(self):

        profit = 0.0
        
        for i in self.timePeriods:
            profit += i.getProfit()

        # Max profit can be reached
        cond0 = profit >= self.T

        # N is more than L and U
        cond1 = self.getNumTimePeriods() >= self.L and self.getNumTimePeriods() >= self.U

        # U is more than or equal to L
        cond2 = self.U >= self.L

        print('cond0: %s, cond1: %s, cond2: %s' % (str(cond0), str(cond1), str(cond2)))

        return cond0 and cond1 and cond2

  