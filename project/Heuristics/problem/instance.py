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
        self.L = 3
        self.U = 4
        self.T = 1
        
        nTimes =  10  #inputData.nTimes

        P = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        E = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

        self.timePeriods = [None] * nTimes
        for tId in range(0, nTimes):
            self.timePeriods[tId] = TimePeriod(tId, 0, E[tId], P[tId])


    def getNumTimePeriods(self):
        return len(self.timePeriods)        

    def getTimePeriods(self):
        return self.timePeriods

    def createSolution(self):
        solution = Solution(self.timePeriods)
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

           
"""
maxLengthChain = 0.0  #consecutives ON
minLengthChain = 0.0  #consecutives OFF
for i in self.timePeriods:
    profit += i.getProfit()
    energy += i.getEnergy()
    for j in self.timePeriods:
        currentMaxLengthChain = 0.0
        currentMinLengthChain = 0.0
        if i.getId() < j.getId():
            if i.getStatus() == 1 and j.getStatus() == 1:
                currentMaxLengthChain += 1
            elif i.getStatus() == 0 and j.getStatus() == 0:
                currentMinLengthChain += 1
        if currentMaxLengthChain > maxLengthChain:
            maxLengthChain = currentMaxLengthChain
        if currentMinLengthChain > minLengthChain:
            minLengthChain = currentMinLengthChain

            
# Cannot be turned off without having L consecutive periods
if minLengthChain < self.L:
    return False

# Cannot be on more than U consecutive periods
if maxLengthChain > self.U:
    return False

# Minimum profit treshold T must be reached
if profit < self.T:
    return False

# Must end being turned off
if self.timePeriods[self.getNumTimePeriods()-1].getStatus() != 0:
    return False """