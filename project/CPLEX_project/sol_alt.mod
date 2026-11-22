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

//dvar boolean R[1..N]; // Indicates if the machine is running at the time i
//dvar int S[1..N]; // Indicates how many time has been staying the machine on the same state at time i

dvar boolean S[1..N]; // State of the machine in time i
dvar boolean ON[1..N]; // Change of state from OFF to ON


//<<<<<<<<<<<<<<<<

// You can run an execute block if needed.

execute {

//>>>>>>>>>>>>>>>>

// ...
    
//<<<<<<<<<<<<<<<<
}

minimize // Write here the objective function.

//>>>>>>>>>>>>>>>>
sum(i in 1..N) E[i] * S[i];
//<<<<<<<<<<<<<<<<

subject to {

    // Write here the constraints.

    //>>>>>>>>>>>>>>>>

	// Constraint 1: Minimun Run Length
	forall(i in 1..N-L+1){
	  sum(j in i..i+L-1) S[j] >= L * ON[i];
	}
	
	// Constraint 2: Max Run Length
	forall(i in 1..N-U){
	  sum( k in i..i+U) S[k] <= U;
	}
	
	// Boundaries
	// can not be on in the last L periods
	forall(i in N-L+2..N)
	  ON[i] == 0;
	  
	// 
	  
	//Start at 1
	ON[1] == S[1];

	
	// Threshold 
	sum(i in 1..N) S[i]*P[i] >= T;
	
	// Linking constraints
	
	forall(i in 2..N){
	  ON[i] >= S[i] - S[i-1];
	  ON[i] <= S[i];
	  ON[i] <= 1 - S[i-1];
	}

    //<<<<<<<<<<<<<<<<
}

// You can run an execute block if needed.

execute {

//>>>>>>>>>>>>>>>>
	
	var file = new IloOplOutputFile("./outputs/output"+N+".sol");
	var start = 0;
	
	
	for (var i = 1; i <= N; ++i) {
	    if (S[i] > 0.5) {
	      if (start == 0) start = i;
	      if (i == N) {
	        writeln(start + " " + i);
	      	file.writeln(start + " " + i);	      
	      };
	    } else if (start > 0) {
	      writeln(start + " " + (i - 1));
	      file.writeln(start + " " + (i - 1));
	      start = 0;
	    }
  	}
 	file.close();
}  
	
	

//<<<<<<<<<<<<<<<<

 