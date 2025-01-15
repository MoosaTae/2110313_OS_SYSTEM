#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
  int id = fork();
  if (id > 0) {
    printf("I am the parent process. My PID is %d\n", getpid());
    wait(NULL);
  } else if (id == 0) {
    printf("I am the child process. My PID is %d and my parent's PID is %d\n",
           getpid(), getppid());

    int child_id = fork();
    if (child_id > 0) {
      wait(NULL);
    } else if (child_id == 0) {
      printf("I am the grandchild process. My PID is %d and my parent's PID is "
             "%d\n",
             getpid(), getppid());
    } else {
      printf("fail to fork\n");
      return 1;
    }
  } else {
    printf("fail to fork\n");
    return 1;
  }

  return 0;
}
