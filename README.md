## How to run the checker.py

A checker is provided to help you debug your codes. The checker, given a.dat file with the input
data and a .sol file with the solution in the format described below, tests whether all constraints are
satisfied. On the other hand, *it is not checked if the solution is optimal* (because that would
require solving the optimization problem!). The checker is written in Python and should be called e.g.:

```sh
python checker.py input.dat output.sol.
```

Solutions should be written as a sequence of lines. Each line should contain a pair of the form a b where 1 ≤a ≤b ≤N, meaning that the machine is ON from time a to time b, both included. *Pairs should not overlap*. For instance, the first of the solutions in the above example could be represented as follows:

```txt
1 2
4 6
```

Considering our directories:

```sh
python checker.py project.1.dat project/CPLEX_project/output.sol
```

Expected output:

```txt
Energy consumption is 8
OK
```

Testing all `.dat` files on the `.mod` (use `python` or `python3`, depending on your Python version):

```sh
for dat in project/project.*.dat; do
    sol="$(basename "$dat" .dat).sol"
    echo "Testing $dat"
    python3 checker.py "$dat" "$sol"
done
```

OUTPUT:

```txt
Testing project/project.1.dat
Energy consumption is 8
OK
Testing project/project.2.dat
Energy consumption is 2
OK
Testing project/project.3.dat
Energy consumption is 13
OK
Testing project/project.4.dat
Energy consumption is 7
OK
Testing project/project.5.dat
Energy consumption is 6
OK
Testing project/project.6.dat
Energy consumption is 8
OK
```


--curret solution before the fix: 
----------------_ <Heuristics.datParser.DATAttributes object at 0x10601e8e0> <Heuristics.datParser.DATAttributes object at 0x10601e520>
Solving the Problem...
cond0: True, cond1: True, cond2: True
Elap. Time (s)   Obj. Value     Iterations
t=0 profit=0/2000
t=88 profit=2436/2000
    0.20170426   2719.00000000              1
IS local search
    0.22603226   2719.00000000              1
Evaluation Performance:
  Num. solutions constructed 1
  Total Eval. Time      0.2260301113128662 s
  Avg. Time / solution 226.0301113128662 ms
Final Solution: z = 2719.00000000;
ON intervals (start end, 1-based):
44 88

mac@Danielas-MacBook-Air project % python3 -m Heuristics.Main----
Solving the Problem...
cond0: True, cond1: True, cond2: True
Elap. Time (s)   Obj. Value     Iterations
t=0 profit=0/1000
t=45 profit=279/1000
t=159 profit=716/1000
t=274 profit=1123/1000
    0.43173695   1053.00000000              1
IS local search
    0.76943588   942.00000000              1
Evaluation Performance:
  Num. solutions constructed 1
  Total Eval. Time      0.7694339752197266 s
  Avg. Time / solution 769.4339752197266 ms
Final Solution: z = 942.00000000;
ON intervals (start end, 1-based):
1 45
105 157
201 273

VS


Solving the Problem...
cond0: True, cond1: True, cond2: True
Elap. Time (s)   Obj. Value     Iterations
    0.76724505   850.00000000              1
IS local search
    0.79484010   847.00000000              1
Evaluation Performance:
  Num. solutions constructed 1
  Total Eval. Time      0.7948381900787354 s
  Avg. Time / solution 794.8381900787354 ms
Final Solution: z = 847.00000000;
ON intervals (start end, 1-based):
1 45
88 159
303 347

