// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the OPL variables.

int N = ...;
int L = ...;
int U = ...;
int T = ...;

int P[1..N] = ...;
int E[1..N] = ...;

// Define here your decision variables and
// any other auxiliary OPL variables you need.
// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>

dvar boolean R[1..N]; // Indicates if the machine is running at the time i
dvar int S[1..N]; // Indicates how many time has been staying the machine on the same state at time i

//<<<<<<<<<<<<<<<<

// You can run an execute block if needed.

execute {

//>>>>>>>>>>>>>>>>

// ...
    
//<<<<<<<<<<<<<<<<
}

minimize // Write here the objective function.

//>>>>>>>>>>>>>>>>
sum(i in 1..N) R[i]*E[i];
//<<<<<<<<<<<<<<<<

subject to {

    // Write here the constraints.

    //>>>>>>>>>>>>>>>>

    // Constraint 1: We have a minimum profit threshold T to be reached
    sum(i in 1..N) R[i]*P[i] >= T;
    
    // Constraint 2: Minimum Run Length
    
    forall(i in 2..N) {
      
      ((1 - R[i-1]) + R[i] == 0) => S[i-1] >= L;
    }
    
    S[N] >= L;
    
    
    
    // Constraint 3: Maximum Run Length
    
    forall(i in 2..N) ((1 - R[i-1]) + R[i] == 0) => S[i-1] <= U;
    
    S[N] <= U;
      
    
    // Constraint 4: Constraints to make S[i] work
    
    forall(i in 2..N) {
	  
	  // If in the i-1 has the machine maintains the same state in i, then S[i] = S[i-1] + 1
	  (R[i] + R[i-1] - 1 >= 1) => S[i] == S[i-1] + 1;
	  ((1 - R[i]) + (1 - R[i-1]) - 1 >= 1) => S[i] == S[i-1] + 1;
	  
	  // If the machine changes state, then we must set S[i] = 1
	  (R[i] + (1 - R[i-1]) - 1 >= 1) => S[i] == 1;
	  ((1 - R[i]) + R[i-1] - 1 >= 1) => S[i] == 1;
	  
    }
    
    
    S[1] == 1;
    

    //<<<<<<<<<<<<<<<<
}

// You can run an execute block if needed.

execute {

//>>>>>>>>>>>>>>>>
	
	
	var start = 0;
	
	
	for (var i = 1; i <= N; ++i) {
	    if (R[i] > 0.5) {
	      if (start == 0) start = i;
	      if (i == N) writeln(start + " " + i);
	    } else if (start > 0) {
	      writeln(start + " " + (i - 1));
	      start = 0;
	    }
  }
	
	

//<<<<<<<<<<<<<<<<
}
