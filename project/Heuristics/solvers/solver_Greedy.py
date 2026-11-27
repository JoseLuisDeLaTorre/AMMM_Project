'''
AMMM Lab Heuristics
Greedy solver
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
'''

import random, time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_Greedy(_Solver):

    def _selectCandidate(self, candidateList):
        if self.config.solver == 'Greedy':
            return min(candidateList, key=lambda candidate: candidate.rate)
        return random.choice(candidateList)

    def construction(self):
        pre_solution = self.instance.createSolution()
        timePeriods = self.instance.getTimePeriods()
        preselectedCandidates = []

        timeId = 0
        while timeId < len(timePeriods):
            #Remove validation and let the algorithm to check all the time, and to gather all the candidates before choosing one
            #if currentProfit >= solution.T:
            #    break

            candidateList = pre_solution.findFeasibleAssignments(timeId)

            if not candidateList:
                # print(f"t={timeId} profit={currentProfit:g}/{solution.T:g}: no candidate")
                if not pre_solution.assign(timeId, 0):
                    raise RuntimeError("Could not leave the current period OFF")
                timeId += 1
                continue

            candidate = self._selectCandidate(candidateList)
            preselectedCandidates.append(candidate)

            # print(
            #     f"t={timeId} profit={currentProfit:g}/{solution.T:g}: "
            #     f"assign [{candidate.startTime}, {candidate.endTime}) "
            #     f"rate={candidate.rate:.3g}"
            # )

            if not pre_solution.assign(
                startTime=candidate.startTime,
                endTime=candidate.endTime,
                status=candidate.status,
            ):
                raise RuntimeError("Could not apply the selected assignment")
            timeId = candidate.endTime
            # print("Jumping to timeId:", timeId, "after assignment")

        # Now that we iterate for all the times, sort the list and select candidates until reched the min profit
        preselectedCandidates.sort(key=lambda candidate: candidate.rate)
        currentProfit = 0
        solution = self.instance.createSolution()
        for candidate in preselectedCandidates:
            if not solution.assign(
                startTime=candidate.startTime,
                endTime=candidate.endTime,
                status=candidate.status,
            ):
                raise RuntimeError("Could not apply the selected assignment")
            currentProfit += candidate.profit
            if currentProfit >= solution.T:
                break

        if currentProfit < solution.T or not solution.isAssignmentFeasible():
            solution.makeInfeasible()

        return solution

    def solve(self, **kwargs):
        self.startTimeMeasure()

        solver = kwargs.get('solver', None)
        if solver is not None:
            self.config.solver = solver
        localSearch = kwargs.get('localSearch', None)
        if localSearch is not None:
            self.config.localSearch = localSearch


        solution = self.construction()
        self.writeLogLine(solution.getFitness(),1)

        if self.config.localSearch:
            print("IS local search")
            localSearch = LocalSearch(self.config, None)
            endTime = self.startTime + getattr(self.config, 'maxExecTime', float('inf'))
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)


        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.getFitness(), 1)
        self.numSolutionsConstructed = 1
        self.printPerformance()


        return solution


