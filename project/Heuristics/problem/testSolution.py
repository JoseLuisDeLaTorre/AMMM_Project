from Heuristics.problem.solution import Solution

from Heuristics.problem.TimePeriod import TimePeriod

profits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
energies = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
timePeriods = [
    TimePeriod(timeId, 0, energy, profit)
    for timeId, (energy, profit) in enumerate(zip(energies, profits))
]

solution = Solution(
    timePeriods=timePeriods,
    minimumOnPeriods=3,
    maximumOnPeriods=4,
    minimumProfit=3,
)

assignments = solution.findFeasibleAssignments(0)
for assignment in assignments:
    print(assignment)