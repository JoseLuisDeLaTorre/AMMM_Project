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
    def __init__(self, timeId, status, energy):
        self.timeId = timeId
        self.status = status
        self.energy = energy

    def __str__(self):
        return "<time_%d, status_%d>: energy: %.2f" % (
            self.timeId,
            self.status,
            self.energy,
        )


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
        if any(status not in (0, 1) for status in self.statuses):
            return False

        # Check profit threshold
        profit = 0.0
        for i in range(0, len(self.timePeriods)):
            profit += self.timePeriods[i].getProfit() * self.statuses[i]
        if profit < self.T:
            return False

        # Check run length (max and min) to respect L and U params
        # The idea is iterate over time periods keeping the count of the current consecutive ON,
        # and in each iteration check if the runLength is valid for the min and the max lenghts.
        runLength = 0
        for status in self.statuses + [0]:
            if status:
                runLength += 1
                if runLength > self.U:
                    return False
            elif runLength:
                if runLength < self.L:
                    return False
                runLength = 0

        return True

    # Objective function: minimize the total energy used
    def updateObjective(self):
        self.fitness = 0.0
        for i in range(0, len(self.timePeriods)):
            self.fitness += self.timePeriods[i].getEnergy() * self.statuses[i]

    # Kept as an alias for the original solution interface
    #def updateHighestRatio(self):
    #    self.updateObjective()

    # Check if is out of bounds, then check previous state
    # 

    def isOnChainFeasible(self, initialTimeId, finalTimeId):
        # save initial states 
        statesBackup = self.statuses[initialTimeId:finalTimeId]
        validation = True
        for timeId in range(initialTimeId, finalTimeId):
            if not self.isFeasibleToSetTimeON(timeId):
                validation = False
                break
            self.statuses[timeId] = 1
        #revert changes
        self.statuses[initialTimeId:finalTimeId] = statesBackup
        return validation


    def isFeasibleToSetTimeON(self, timeId):
        if not 0 <= timeId < len(self.statuses):
            return False
        previousStatus = self.statuses[timeId]
        self.statuses[timeId] = 1
        feasible = self.isAssignmentFeasible()
        self.statuses[timeId] = previousStatus
        return feasible

    def isFeasibleToAssignOFF(self, timeId):
        if not 0 <= timeId < len(self.statuses):
            return False
        previousStatus = self.statuses[timeId]
        self.statuses[timeId] = 0
        feasible = self.isAssignmentFeasible()
        self.statuses[timeId] = previousStatus
        return feasible

    def assign(self, timeId, status=1):
        if not 0 <= timeId < len(self.statuses) or status not in (0, 1):
            return False
        self.statuses[timeId] = status
        self.updateObjective()
        return True

    def unassign(self, timeId):
        return self.assign(timeId, 0)

    def findFeasibleAssignments(self, timeId):
        feasibleAssignments = []
        # The comparison will be done using a windows frame between 
        # min L and max U
        # S0, S1 ... SL
        # ...
        # S0 S1 ... SU
        # S1 S2 ... SU
        # All this will be evaluated as feasible in the iteration, next time
        # will start at time i + k, being k the last time frime of the selected window

        timeBlocks = []
        timeEnergies = []
        timeProfits = []
        timeRatio = []


        for l in range(0, self.L  ):
            for u in range(self.L , self.L + self.U ):
                if timeId+u < len(self.statuses)+1:

                    timeBlocks.append((timeId+l, timeId+u))
                    timeEnergies.append(sum(self.timePeriods[t].getEnergy() for t in range(timeId+l, timeId+u)))
                    timeProfits.append(sum(self.timePeriods[t].getProfit() for t in range(timeId+l, timeId+u)))
                    timeRatio.append(timeEnergies[-1]/timeProfits[-1] if timeProfits[-1] > 0 else float('inf'))
                    if self.isOnChainFeasible(timeId+l, timeId+u):
                        #Assign all the status from timeId+l to timeId+u as ON
                        for t in range(timeId+l, timeId+u):
                            self.statuses[t] = 1
                            energy = self.timePeriods[t].getEnergy()
                            #profit = self.timePeriods[t].getProfit()
                            feasibleAssignments.append(Assignment(t, 1, energy))


                        #Unassign all the status from timeId+l to timeId+u as OFF
                        for t in range(timeId+l, timeId+u):
                            self.statuses[t] = 0

        print("Time blocks:", timeBlocks)
        print("Time energies:", timeEnergies)
        print("Time profits:", timeProfits)
        print("Time ratio:", timeRatio)
        """         for status in (0, 1):
            self.statuses[timeId] = status
            if self.isAssignmentFeasible():
                energy = self.timePeriods[timeId].getEnergy() * status
                feasibleAssignments.append(Assignment(timeId, status, energy))
        self.statuses[timeId] = previousStatus """
        return feasibleAssignments

    def findBestFeasibleAssignment(self, timeId):
        assignments = self.findFeasibleAssignments(timeId)
        if not assignments:
            return None

        bestAssignment = assignments[0]
        for assignment in assignments[1:]:
            if assignment.energy < bestAssignment.energy:
                bestAssignment = assignment
        return bestAssignment

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
