#include <mpi.h>
#include <iostream>
#include <fstream>
#include <cstdio>
#include <cstdlib>
#include <cmath>
using namespace std;

main(int argc, char* argv[]) {

  MPI_Init(&argc, &argv);
  int rank, number_procs;

  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &number_procs);
  cout << "rank = " << rank << " number_procs= " << number_procs << endl;
  cout.flush();
  MPI_Barrier(MPI_COMM_WORLD);

  int max_iterations = 2000;
  bool finished=false;
  char command[180];
  int command_rv, scoop_rv, finalize_rv;
  int iteration=0;
  
  while (!finished) {
    cout << " rank=" << rank << " beginning parallel run job iteration=" << iteration << endl;
    cout.flush();

    sprintf(command, "./parallelEPrun.py %d", rank);
    command_rv=system(command);
    // might not even use the return code here -- idea that serialscoop would catch any problems.
    //cout << " rank=" << rank << " return code of parallelEPrun.py=" << command_rv << endl;
    //if (command_rv != 0) { MPI_Finalize(); } // ?

    MPI_Barrier(MPI_COMM_WORLD);

    if (rank==0) {
      sprintf(command, "./serialScoop.py %d", number_procs);
      scoop_rv=system(command);
    }
    MPI_Bcast(&scoop_rv, 1, MPI_INT, 0, MPI_COMM_WORLD); 

    cout << " rank=" << rank << " scoop_rv=" << scoop_rv << endl;
    cout.flush();

    MPI_Barrier(MPI_COMM_WORLD);
    iteration++;

    if (iteration >= max_iterations) {
      if (rank==0) cout << " Stopping: parallel simulation series iteration reached maximum " << iteration << endl;
      finished=true;
    }

    if (scoop_rv > 0) {
      if (rank==0) cout << " Stopping: serialScoop.py has requested we stop " << endl;
      finished=true;
    }

  }

  if (rank == 0)
  {
    sprintf(command,"./serialFinalize.py %d", number_procs);
    finalize_rv=system(command);
  }

  MPI_Finalize();
}
