#include <stdio.h>
#include "stack.h"
int main(){
    printf("Hello seamen!\n");
    Stack s;
    stack_init(&s);
    printf("%d\n",s.sp);
    push(&s,(Value){.type=TYPE_INT, .as.i=1});
    push(&s,(Value){.type=TYPE_INT, .as.i=2});
    push(&s,(Value){.type=TYPE_INT, .as.i=3});
    push(&s,(Value){.type=TYPE_INT, .as.i=4});
    print_stack(s);
    return 0;
}
