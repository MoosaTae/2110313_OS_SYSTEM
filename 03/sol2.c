#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  pid_t pid;

  pid = fork();
  if (pid < 0) {
    printf("Error : cannot fork\n");
    exit(1);
  } else if (pid == 0) {
    if (argc < 2) {
      printf("please enter UNIX command\n");
      exit(1);
    }

    execvp(argv[1], &argv[1]);

  } else {
    wait(NULL);
    return (0);
  }
}
