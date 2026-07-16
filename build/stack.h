#ifndef STACK_H
#define STACK_H
 
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
        int   i;
        float f;
        char* s;
        bool  b;
        void* obj;
    } as;
} Value;
 
#define STACK_CAPACITY 1000
 
typedef struct {
    Value data[STACK_CAPACITY];
    int sp;
} Stack;
 
void  stack_init(Stack* stack);
void  push(Stack* stack, Value v);
Value pop(Stack* stack);
Value peek(Stack* stack);
bool  stack_is_empty(Stack* stack);
void  print_stack(Stack s);
void op_add(Stack* s);
void push_int(Stack* stack, int value);
void push_float(Stack* stack, float value);
void push_string(Stack* stack, const char* value);
void push_bool(Stack* stack, bool value);
void op_print(Stack* stack);
#endif // STACK_H
