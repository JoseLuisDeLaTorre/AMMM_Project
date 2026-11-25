# Scheduling Heuristics

## Run

Run from the `project` directory:

```bash
python3 -m Heuristics.Main
```

To use another
configuration:

```bash
python3 -m Heuristics.Main --configFile config.dat
```

## Input data

The DAT input file defines the horizon, run-length limits, profit target, and
per-period profit and energy values:

```text
N = 6;
L = 2;
U = 3;
T = 18;
P = [3 5 3 3 9 10];
E = [6 9 5 3 3 8];
```

`N` is the number of periods; `L` and `U` are the minimum and maximum ON-run
lengths; `T` is the minimum total profit; and `P` and `E` contain profit and
energy values for each period. Both vectors must contain `N` non-negative
numbers, and the run lengths must satisfy `1 <= L <= U <= N`.


