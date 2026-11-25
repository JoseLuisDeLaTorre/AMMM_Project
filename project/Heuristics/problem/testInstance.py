from types import SimpleNamespace

from Heuristics.problem.TimePeriod import TimePeriod
from Heuristics.problem.solution import Solution
from Heuristics.solvers.solver_Greedy import Solver_Greedy


class TestInstance:
    def __init__(self, config):
        profits = [1,9,1,3,4,5]
        energies = [1,2,2,3,3,3]
        self.timePeriods = [
            TimePeriod(timeId, 0, energy, profit)
            for timeId, (energy, profit) in enumerate(zip(energies, profits))
        ]
        self.config = config

    def getTimePeriods(self):
        return self.timePeriods

    def createSolution(self):
        solution = Solution(
            timePeriods=self.timePeriods,
            minimumOnPeriods=2,
            maximumOnPeriods=4,
            minimumProfit=14,
        )
        solution.setVerbose(self.config.verbose)
        return solution


def main():
    config = SimpleNamespace(solver="Greedy", verbose=False, localSearch=False)
    instance = TestInstance(config)
    solution = Solver_Greedy(config, instance).solve()

    if not solution.isFeasible():
        raise AssertionError("Expected the completed schedule to be feasible")
    if solution.statuses != [1,1,0,1,1,1]:
        raise AssertionError("expected solution not match")
    
    print("Solution statuses:", solution.statuses)
    print("Solution fitness:", solution.fitness)


if __name__ == "__main__":
    main()

# Run from the project directory: python3 -m Heuristics.problem.testInstance