#include <stdio.h>
#include <stdbool.h>
typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING,
    TYPE_BOOL,
    TYPE_ARRAY
} ValueType;

typedef struct {
    ValueType type;
    union {
	int i;
	float f;
	char* s;
	bool b;
	void* obj;	
    } as;
} Value;

typedef struct {
    Value data[1000];
    int sp;
} Stack;

void push(Stack* stack, Value v){
    stack->data[stack->sp++]=v;
}
Value pop(Stack* stack){
    return stack->data[stack->sp--];
}
void print_stack(Stack s){
    for (int i = s.sp-1; i>=0;i--){
	switch (s.data[i].type){
	case TYPE_INT:
	  printf("[%d]=%d\n",i, s.data[i].as.i);
	  break;
        }
    }
}
int main(){
    printf("Hello seamen!\n");
    Stack s;
    s.sp = 0;
    printf("%d\n",s.sp);
    push(&s,(Value){.type=TYPE_INT, .as.i=1});
    push(&s,(Value){.type=TYPE_INT, .as.i=2});
    push(&s,(Value){.type=TYPE_INT, .as.i=3});
    push(&s,(Value){.type=TYPE_INT, .as.i=4});
    print_stack(s);
    return 0;
}
