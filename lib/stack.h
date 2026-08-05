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
    TYPE_PTR,
    TYPE_CHAR
} ValueType;
 

typedef struct Value{
    ValueType type;
    union {
        int   i;
        float f;
        char* s;
        bool  b;
        void* obj;
        char  c;
	    struct Value* ptr;
    } as;
}Value;

typedef struct {
    int length;     
    int capacity;  
    Value* items;   
} ArrayObject;

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
bool  is_truthy(Value v);

void push_int(Stack* stack, int value);
void push_float(Stack* stack, float value);
void push_string(Stack* stack, const char* value);
void push_bool(Stack* stack, bool value);
void push_char(Stack* stack, char  value);
void push_ptr(Stack* stack, Value* ptr);

void op_deref(Stack* stack);
void op_store(Stack* stack);

void op_arr_get(Stack* stack);
void op_arr_set(Stack* stack);

void op_printf(Stack* stack);
void op_scanf(Stack* stack);
void op_fgets(Stack* stack);
void op_sizeof(Stack* stack);
void op_strlen(Stack* stack);
   
void op_add(Stack* s);
void op_minus(Stack* s);
void op_div(Stack* s);
void op_mul(Stack* s);

void op_equals(Stack* s);
void op_greater_equals(Stack* s);
void op_less_equals(Stack* s);
void op_and(Stack* s);

ArrayObject* array_create(Stack* s, ValueType elem_type);
Value array_get(ArrayObject* arr, int index);
void  array_set(ArrayObject* arr, int index, Value v);
void*  alloc_string(Stack* s);

#endif // STACK_H
