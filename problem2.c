#include <mpi.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int next_rank = (rank + 1) % size;
    int prev_rank = (rank - 1 + size) % size;

    char message[100];
    sprintf(message, "Hello from process %d", rank);

    char received_message[100];

    MPI_Sendrecv(message, strlen(message) + 1, MPI_CHAR, next_rank, 0,
                 received_message, sizeof(received_message), MPI_CHAR, prev_rank, 0,
                 MPI_COMM_WORLD, MPI_STATUS_IGNORE);

    printf("Process %d received: %s\n", rank, received_message);

    MPI_Finalize();
    return 0;
}