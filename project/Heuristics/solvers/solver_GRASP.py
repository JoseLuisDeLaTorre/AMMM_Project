'''
AMMM Lab Heuristics
GRASP solver
Copyright 2018 Luis Velasco.

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
'''

import random
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha):

        # sort candidate assignments by rate in ascending order
        sortedCandidateList = sorted(candidateList, key=lambda candidate: candidate.rate)
        
        # compute boundary highest load as a function of the minimum and maximum highest loads and the alpha parameter
        minHLoad = sortedCandidateList[0].rate
        maxHLoad = sortedCandidateList[-1].rate
        boundaryHLoad = minHLoad + (maxHLoad - minHLoad) * alpha
        
        # find elements that fall into the RCL
        maxIndex = 0
        for candidate in sortedCandidateList:
            if candidate.rate <= boundaryHLoad:
                maxIndex += 1

        # create RCL and pick an element randomly
        rcl = sortedCandidateList[0:maxIndex]          # pick first maxIndex elements starting from element 0
        if not rcl: return None
        return random.choice(rcl)          # pick a candidate from rcl at random
    
    def _greedyRandomizedConstruction(self, alpha):
        solution = self.instance.createSolution()
        timePeriods = self.instance.getTimePeriods()

        timeId = 0
        while timeId < len(timePeriods):
            currentProfit = sum(
                period.getProfit() * solution.statuses[index]
                for index, period in enumerate(timePeriods)
            )
            print(f"t={timeId} profit={currentProfit:g}/{solution.T:g}")
            if currentProfit >= solution.T:
                break

            candidateList = solution.findFeasibleAssignments(timeId)

            if not candidateList:
                # print(f"t={timeId} profit={currentProfit:g}/{solution.T:g}: no candidate")
                if not solution.assign(timeId, 0):
                    raise RuntimeError("Could not leave the current period OFF")
                timeId += 1
                continue

            candidate = self._selectCandidate(candidateList, alpha)
            # print(
            #     f"t={timeId} profit={currentProfit:g}/{solution.T:g}: "
            #     f"assign [{candidate.startTime}, {candidate.endTime}) "
            #     f"rate={candidate.rate:.3g}"
            # )
            if not solution.assign(
                startTime=candidate.startTime,
                endTime=candidate.endTime,
                status=candidate.status,
            ):
                raise RuntimeError("Could not apply the selected assignment")
            timeId = candidate.endTime
            # print("Jumping to timeId:", timeId, "after assignment")

        if not solution.isAssignmentFeasible():
            solution.makeInfeasible()

        return solution
    
    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        incumbent.makeInfeasible()
        bestHighestLoad = incumbent.getFitness()
        self.writeLogLine(bestHighestLoad, 0)

        iteration = 0
        while not self.stopCriteria():
            iteration += 1
            
            # force first iteration as a Greedy execution (alpha == 0)
            alpha = 0 if iteration == 1 else self.config.alpha

            solution = self._greedyRandomizedConstruction(alpha)
            if self.config.localSearch:
                localSearch = LocalSearch(self.config, None)
                endTime = self.startTime + self.config.maxExecTime
                solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            if solution.isFeasible():
                solutionHighestLoad = solution.getFitness()
                if solutionHighestLoad < bestHighestLoad :
                    incumbent = solution
                    bestHighestLoad = solutionHighestLoad
                    self.writeLogLine(bestHighestLoad, iteration)

        self.writeLogLine(bestHighestLoad, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent

