"""
AMMM Lab Heuristics
Representation of a solution instance
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

from Heuristics.solution import _Solution


# This class stores the load of the highest loaded CPU
# when a task is assigned to a CPU.
class Assignment(object):
    def __init__(self, initialTimeId, endTimeId, energy,profit,rate, status=0):
        self.startTime = initialTimeId
        self.endTime = endTimeId
        self.energy = energy
        self.status = status
        self.profit = profit
        self.rate = rate

    def __str__(self):
        return f"Assignment(startTime={self.startTime}, endTime={self.endTime}, energy={self.energy}, status={self.status}, profit={self.profit}, rate={self.rate})"


class Solution(_Solution):
    def __init__(self, timePeriods, minimumOnPeriods=3, maximumOnPeriods=4,
                 minimumProfit=1):
        self.timePeriods = timePeriods
        self.L = minimumOnPeriods
        self.U = maximumOnPeriods
        self.T = minimumProfit
        # Vector of states
        self.statuses = [timePeriod.getStatus() for timePeriod in timePeriods]
        super().__init__()

    # ON_i is one when the machine changes from OFF to ON
    def getTurnedOn(self):
        turnedOn = []
        for i in range(0, len(self.statuses)):
            if i == 0:
                turnedOn.append(self.statuses[i])
            else:
                turnedOn.append(max(0, self.statuses[i] - self.statuses[i - 1]))
        return turnedOn

    # Check all the restrictions for the current assignment of time periods
    def isAssignmentFeasible(self):
        # Check profit threshold
        """  We cannot determinate the real profit yet, just at the end of the solution, maybe we can start all with 1
        and then check if the profit is enough, but this would complicate the max run - min run check, 
        so we will just check the profit at the end of the solution.
        profit = 0.0
        for i in range(0, len(self.timePeriods)):
            profit += self.timePeriods[i].getProfit() * self.statuses[i]
        if profit < self.T:
            return False 
        """
        
        # Check run length (max and min) to respect L and U params
        # The idea is iterate over time periods keeping the count of the current consecutive ON,
        # and in each iteration check if the runLength is valid for the min and the max lenghts.
        runLength = 0
        for status in self.statuses + [0]:
            if status:
                runLength += 1
                if runLength >= self.U:
                    # print(" - Max run exceeded")
                    return False
            elif runLength:
                if runLength < self.L:
                    # print(" - Min run too short")
                    return False
                runLength = 0

        return True

    # Objective function: minimize the total energy used
    def updateObjective(self):
        self.fitness = 0.0
        for i in range(0, len(self.timePeriods)):
            self.fitness += self.timePeriods[i].getEnergy() * self.statuses[i]


    def isOnChainFeasible(self, initialTimeId, finalTimeId):
        # save initial states 
        statesBackup = self.statuses[initialTimeId:finalTimeId]
        validation = True
        energy = 0
        profit = 0
        for timeId in range(initialTimeId, finalTimeId):
            self.statuses[timeId] = 1
            energy += self.timePeriods[timeId].getEnergy()
            profit += self.timePeriods[timeId].getProfit()

        
        feasible = self.isAssignmentFeasible()
        rate = energy / profit if profit > 0 else float("inf")
        # print(
        #     f"chain {initialTimeId}:{finalTimeId} feasible={feasible} "
        #     f"E={energy:g} P={profit:g} rate={rate:.3g} statuses {self.statuses}"
        # )
        #revert changes
        self.statuses[initialTimeId:finalTimeId] = statesBackup
        return feasible


    def assign(self, startTime, endTime, status=1):
        if endTime > len(self.statuses):
            return False
        for timeId in range(startTime, endTime):
            self.statuses[timeId] = status
        self.updateObjective()
        return True

    def unassign(self, timeId):
        return self.assign(timeId, 0)

    def findFeasibleAssignments(self, timeId):
        feasibleAssignments = []
        for l in range(0, self.L):
            for u in range(self.L , self.L + self.U ):
                if timeId+u < len(self.statuses)+1:       
                    if self.isOnChainFeasible(timeId+l, timeId+u):
                        energy = 0
                        profit = 0
                        rate = 0
                        #Assign all the status from timeId+l to timeId+u as ON
                        for t in range(timeId+l, timeId+u):
                            self.statuses[t] = 1
                            energy += self.timePeriods[t].getEnergy()
                            profit += self.timePeriods[t].getProfit()
                        #Calculate the energy/profit ratio

                        if profit > 0:
                            rate = energy / profit
                        
                        feasibleAssignments.append(Assignment(timeId+l, timeId+u, energy, profit, rate,1))

                        #Unassign all the status from timeId+l to timeId+u as OFF
                        for t in range(timeId+l, timeId+u):
                            self.statuses[t] = 0
        return feasibleAssignments

    def __str__(self):
        strSolution = 'z = %10.8f;\n' % self.fitness
        if self.fitness == float('inf'): return strSolution

        # S: decision variable containing the status of the machine
        statuses = self.statuses
        # ON: decision variable containing the periods where the machine is turned on
        turnedOn = self.getTurnedOn()

        strSolution += 's = [ '
        strSolution += ' '.join(str(status) for status in statuses)
        strSolution += ' ];\n'
        strSolution += 'on = [ '
        strSolution += ' '.join(str(status) for status in turnedOn)
        strSolution += ' ];\n'

        return strSolution

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
