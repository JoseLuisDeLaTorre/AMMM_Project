"""
AMMM Lab Heuristics
Local Search algorithm
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

import copy
import time
from Heuristics.solver import _Solver
from AMMMGlobals import AMMMException



class Move(object):
    def __init__(self, timeIds, currentStatuses, newStatuses):
        self.timeIds = timeIds
        self.currentStatuses = currentStatuses
        self.newStatuses = newStatuses

    def __str__(self):
        return "Move(timeIds=%s, currentStatuses=%s, newStatuses=%s)" % (
            self.timeIds,
            self.currentStatuses,
            self.newStatuses,
        )


class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)

        if self.nhStrategy not in ("TaskExchange", "Reassignment"):
            raise AMMMException("Select a valid nh strat: %s" % self.nhStrategy)
        if self.policy not in ("FirstImprovement", "BestImprovement"):
            raise AMMMException("Select a valid policy: %s" % self.policy)

    
    def _isFeasible(self, solution):
        if not solution.isFeasible():
            return False
        if not solution.isAssignmentFeasible():
            return False

        profit = 0
        for timeId in range(len(solution.timePeriods)):
            profit += (
                solution.timePeriods[timeId].getProfit()
                * solution.statuses[timeId]
            )

        if(profit < solution.T):
            return False
        
        return True

    def createNeighborSolution(self, solution, move):
        newSolution = copy.copy(solution)
        newSolution.statuses = solution.statuses.copy()
        for index in range(len(move.timeIds)):
            timeId = move.timeIds[index]
            if solution.statuses[timeId] != move.currentStatuses[index]:
                return None
            newSolution.statuses[timeId] = move.newStatuses[index]

        if not self._isFeasible(newSolution):
            return None

        newSolution.updateObjective()
        return newSolution

    # Apply changes that are defined in the moves
        # First improvement would return first neighbor that improves the incumbent solution
        # Best improvement would return the best neighbor that improves the incumbent solution
    def _explore(self, solution, moves):
        bestNeighbor = None
        bestFitness = solution.getFitness()

        for move in moves:
            if time.time() >= self.endTime:
                break

            neighbor = self.createNeighborSolution(solution, move)
            if neighbor is None or neighbor.getFitness() >= bestFitness:
                continue
            if self.policy == "FirstImprovement":
                return neighbor

            bestNeighbor = neighbor
            bestFitness = neighbor.getFitness()
        return bestNeighbor

    # Reassignment, flip the binary status one by one and check if it is feasible and if it is better
    def exploreReassignment(self, solution):
        moves = []
        nsize = len(solution.statuses)
        
        for i in range(nsize):
            status = solution.statuses[i]
            moves.append(Move([i],[status],[1-status]))
        return self._explore(solution, moves)

        endsON = []
        endsOFF = []
        middle = []
        last_on = 0
        for i in range(0,nsize+1):
            if i == 0: prev = 0
            else: prev = solution.statuses[i-1]
            if i == nsize: cur = 0
            else: cur = solution.statuses[i]
            
            if prev == 0 and cur == 1:
                endsON.append(i)
                if i != 0: endsOFF.append(i-1)
                last_on = i
            if prev == 1 and cur == 0:
                endsON.append(i-1)
                if i < nsize: endsOFF.append(i)

                start = last_on
                end = i-1
                if end-start+1 <= 2*solution.L: continue
                for j in range(start+solution.L, end-solution.L+1):
                    middle.append(j)

        candidatesON = endsON + middle
        candidatesOFF = endsOFF

        for timeId1 in candidatesON:
            for timeId2 in candidatesOFF:

                move = Move([timeId1,timeId2],[1,0],[0,1])
                moves.append(move)

        return self._explore(solution, moves)

    # Exchange: obtain on periods and off periods
    #  for each on period take one off period and exchange them
    def exploreExchange(self, solution):
        onPeriods = []
        offPeriods = []
        for timeId in range(len(solution.statuses)):
            status = solution.statuses[timeId]
            if status == 1:
                onPeriods.append(timeId)
            elif status == 0:
                offPeriods.append(timeId)
        moves = []
        for onTimeId in onPeriods:
            for offTimeId in offPeriods:
                move = Move(
                    [onTimeId, offTimeId],
                    [1, 0],
                    [0, 1],
                )
                moves.append(move)
        return self._explore(solution, moves)

    def exploreNeighborhood(self, solution):
        if self.nhStrategy == "TaskExchange":
            return self.exploreExchange(solution)
        return self.exploreReassignment(solution)

    def solve(self, **kwargs):
        incumbent = kwargs.get("solution")
        if incumbent is None:
            raise AMMMException("[local search] No solution could be retrieved")

        incumbent.updateObjective()
        if not self._isFeasible(incumbent):
            incumbent.makeInfeasible()
            return incumbent

        startTime = kwargs.get("startTime", time.time())
        self.endTime = kwargs.get("endTime")
        if self.endTime is None:
            self.endTime = startTime + self.maxExecTime

        while time.time() < self.endTime:
            neighbor = self.exploreNeighborhood(incumbent)
            if neighbor is None:
                break
            incumbent = neighbor

        return incumbent
