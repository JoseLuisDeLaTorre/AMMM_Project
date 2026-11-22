oblem can be modeled as a Mixed Integer Linear Program (MILP).
\

*The following sets and parameters are defined:*
- I: set of time periods, index i.
- N: number of discrete time periods of the planning horizon.
- L: Consecutive time periods that the machine must remain "ON".
- U: Consecutive time periods that the machine can remain "ON".
- T: minimum profit threshold to be reached.
- $P_i$: Profit in time period i.
- $E_i$: Amount of energy used during time period i.
\
*The following decision variables are also defined:*

- S_i: Binary. Equal to 1 if the machine is in production mode "ON" during time period i; 0 otherwise.
- ON_i: Binary. Equal to 1 if the machine changes its state from "OFF" to "ON" in time i; 0 otherwise.
\
*Finally, the MILP model for the problem is as follows:*

Objective function: minimize the total energy used over the planning horizon.

$ min (sum_(i in 1..N) E_i dot S_i;) $

*Subject to:*

- *Minimum Run Length:* when the machine is turned "ON", it must remain "ON" for at least L consecutive periods of time.

$ forall(i in 1..N-L+1),
	  sum_(j in i..i+L-1) S_j >= L dot "ON"_i;
$

- *Maximum Run Length:* The sum of consecutive $S_i$ being "ON" should be less or equal than U.
$
	forall(i in 1..N-U),
	  sum_( k in i..i+U) S_k <= U;
$

- *Boundaries*
  - *Respecting ending state:* the machine should be "OFF" at time N+1. This means it cannot be turned "ON" during the last L-1 periods of the planning horizon, since it there would not be enough time to satisfy the minimum run length. 

  $ "ON"_i = 0 space forall(i in N-L+2..N) $
  
  - *Respecting beginning state:* if the status at time i=1 is "ON", that mean the machine must turned "ON" at that moment.
  
  $ "ON"_1 = S_1 $

- *Threshold:* The total profit obtained during the planning horizon must be more than or equal to the minimum profit threshold T.

$ sum_(i in 1..N) S_i dot P_i >= T $

- *Linking constraints*

  - *Defining turned "ON":* when the state $S_i$ goes from 0 to 1 between periods $i-1$ and $i$, this implies that a turn "ON" action has happened. 
  
$  "ON"_i >= S_i - S_(i-1) space forall(i in 2..N) $

  - *Connecting $S_i$ with $"ON"_i$*: if the state of $S_i$ is 0, it cannot been a turned ON action during that period of time.
  
$ "ON"_i <= S_i space forall(i in 2..N) $

  - *Respecting switch conditions*: the machine can only be turned "ON" if its previous state was "OFF"
  
$	"ON"_i <= 1 - S_(i-1) space forall(i in 2..N) $
