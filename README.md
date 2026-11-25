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
