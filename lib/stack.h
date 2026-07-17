#ifndef STACK_H
#define STACK_H
 
#include <stdio.h>
#include <stdbool.h>

 
typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING,
    TYPE_BOOL,
    TYPE_ARRAY,
    TYPE_PTR
} ValueType;
 

typedef struct Value{
    ValueType type;
    union {
        int   i;
        float f;
        char* s;
        bool  b;
        void* obj;
	    struct Value* ptr;
    } as;
}Value;

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

void push_int(Stack* stack, int value);
void push_float(Stack* stack, float value);
void push_string(Stack* stack, const char* value);
void push_bool(Stack* stack, bool value);
void push_ptr(Stack* stack, Value* ptr);

void op_deref(Stack* stack);
void op_store(Stack* stack);

void op_printf(Stack* stack);
void op_scanf(Stack* stack);
void op_fgets(Stack* stack, int max_len);

void op_add(Stack* s);
void op_minus(Stack* s);
void op_div(Stack* s);
void op_mul(Stack* s);

#endif // STACK_H
