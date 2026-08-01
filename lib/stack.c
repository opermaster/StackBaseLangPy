#include "stack.h"
#include <stdlib.h>
#include <string.h>
void stack_init(Stack* stack) {
    stack->sp = 0;
}
 
void push(Stack* stack, Value v) {
    if (stack->sp >= STACK_CAPACITY) {
        fprintf(stderr, "Stack overflow\n");
        exit(1);
    }
    stack->data[stack->sp++] = v;
}
 
Value pop(Stack* stack) {
    if (stack->sp <= 0) {
        fprintf(stderr, "Stack underflow\n");
        exit(1);
    }
    return stack->data[--stack->sp];
}
 
Value peek(Stack* stack) {
    if (stack->sp <= 0) {
        fprintf(stderr, "Stack underflow (peek)\n");
        exit(1);
    }
    return stack->data[stack->sp - 1];
}
 
bool stack_is_empty(Stack* stack) {
    return stack->sp == 0;
}
 
void print_stack(Stack s) {
    for (int i = s.sp - 1; i >= 0; i--) {
        switch (s.data[i].type) {
            case TYPE_INT:
                printf("[%d]=%d\n", i, s.data[i].as.i);
                break;
            case TYPE_FLOAT:
                printf("[%d]=%f\n", i, s.data[i].as.f);
                break;
            case TYPE_STRING:
                printf("[%d]=\"%s\"\n", i, s.data[i].as.s);
                break;
            case TYPE_BOOL:
                printf("[%d]=%s\n", i, s.data[i].as.b ? "true" : "false");
                break;
            case TYPE_ARRAY:
                printf("[%d]=<array %p>\n", i, s.data[i].as.obj);
                break;
        }
    }
}
bool compare_strings(const char* a, const char* b){
    int a_len = strlen(a);
    int b_len = strlen(b);
    
    if( a_len != b_len) return false;
    for(int i =0 ;i< a_len ;i++){
        if(a[i] != b[i]) return false;
    }
    return true;
}
bool compare_strings_leng(const char* a, const char* b){
    int a_len = strlen(a);
    int b_len = strlen(b);
    
    if( a_len == b_len) return true;
    return a_len > b_len;
}
bool compare_strings_lenl(const char* a, const char* b){
    int a_len = strlen(a);
    int b_len = strlen(b);
    
    if( a_len == b_len) return true;
    return a_len < b_len;
}

void op_add(Stack* s) {
    Value b = pop(s); 
    Value a = pop(s); 
 
    if (a.type == TYPE_INT && b.type == TYPE_INT)          push_int(s,a.as.i + b.as.i);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_FLOAT) push_float(s,a.as.f + b.as.f);
    else if (a.type == TYPE_INT && b.type == TYPE_FLOAT)   push_float(s,(float)a.as.i + b.as.f);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_INT)   push_float(s,a.as.f + (float)b.as.i);
    else {
        fprintf(stderr, "Type error: cannot add these types\n");
        exit(1);
    }
}
void op_minus(Stack* s){
    Value b = pop(s); 
    Value a = pop(s); 

    if (a.type == TYPE_INT && b.type == TYPE_INT)          push_int(s,a.as.i - b.as.i);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_FLOAT) push_float(s,a.as.f - b.as.f);
    else if (a.type == TYPE_INT && b.type == TYPE_FLOAT)   push_float(s,(float)a.as.i - b.as.f);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_INT)   push_float(s,a.as.f - (float)b.as.i);
    else {
        fprintf(stderr, "Type error: cannot add these types\n");
        exit(1);
    }
}
void op_div(Stack* s){
    Value b = pop(s); 
    Value a = pop(s); 
 
    if (a.type == TYPE_INT && b.type == TYPE_INT)          push_int(s,a.as.i / b.as.i);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_FLOAT) push_float(s,a.as.f / b.as.f);
    else if (a.type == TYPE_INT && b.type == TYPE_FLOAT)   push_float(s,(float)a.as.i / b.as.f);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_INT)   push_float(s,a.as.f / (float)b.as.i);
    else {
        fprintf(stderr, "Type error: cannot add these types\n");
        exit(1);
    }
}
void op_mul(Stack* s){
    Value b = pop(s); 
    Value a = pop(s);
    
    if (a.type == TYPE_INT && b.type == TYPE_INT)          push_int(s,a.as.i * b.as.i);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_FLOAT) push_float(s,a.as.f * b.as.f);
    else if (a.type == TYPE_INT && b.type == TYPE_FLOAT)   push_float(s,(float)a.as.i * b.as.f);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_INT)   push_float(s,a.as.f * (float)b.as.i);
    else {
        fprintf(stderr, "Type error: cannot add these types\n");
        exit(1);
    }
   
}
void push_int(Stack* stack, int value) {
    push(stack, (Value){ .type = TYPE_INT, .as.i = value });
}
 
void push_float(Stack* stack, float value) {
    push(stack, (Value){ .type = TYPE_FLOAT, .as.f = value });
}
 
void push_string(Stack* stack, const char* value) {
    push(stack, (Value){ .type = TYPE_STRING, .as.s = (char*)value });
}
 
void push_bool(Stack* stack, bool value) {
    push(stack, (Value){ .type = TYPE_BOOL, .as.b = value });
}
void push_ptr(Stack* stack, Value* ptr) {
    push(stack, (Value){ .type = TYPE_PTR, .as.ptr = ptr });
}
void op_deref(Stack* stack) {
    Value ptr_value = pop(stack);
    if (ptr_value.type != TYPE_PTR) {
        fprintf(stderr, "deref: value on stack is not a pointer\n");
        exit(1);
    }
    push(stack, *(ptr_value.as.ptr)); 
}
void op_store(Stack* stack) {
    Value ptr_value = pop(stack);   
    Value value = pop(stack);      
    if (ptr_value.type != TYPE_PTR) {
        fprintf(stderr, "store: value on stack is not a pointer\n");
        exit(1);
    }
    *(ptr_value.as.ptr) = value;
}
int count_format_specifiers(const char* fmt) {
    int count = 0;
    for (const char* p = fmt; *p; p++) {
        if (*p == '%' && *(p + 1) != '\0') {
            if (*(p + 1) == '%') {
                p++; 
            } else {
                count++;
                p++;
            }
        }
    }
    return count;
}
void op_printf(Stack* stack) {
    Value fmt = pop(stack);
    if (fmt.type != TYPE_STRING) {
        fprintf(stderr, "op_print: expected a format string on top of stack\n");
        exit(1);
    }
 
    int argc = count_format_specifiers(fmt.as.s);
    if (argc > 64) {
        fprintf(stderr, "op_print: too many arguments\n");
        exit(1);
    }
 
    Value tmp[64];
    for (int i = 0; i < argc; i++) {
        tmp[i] = pop(stack);
    }
 
    Value args[64];
    for (int i = 0; i < argc; i++) {
        args[i] = tmp[argc - 1 - i];
    }
 
    int arg_index = 0;
    const char* p = fmt.as.s;
    while (*p) {
        if (*p == '%' && *(p + 1) != '\0') {
            char spec = *(p + 1);
            if (spec == '%') {
                putchar('%');
                p += 2;
                continue;
            }
            if (arg_index >= argc) {
                fprintf(stderr, "op_print: not enough arguments for format string\n");
                exit(1);
            }
            Value v = args[arg_index++];
            switch (spec) {
                case 'd':
                    if (v.type != TYPE_INT) {
                        fprintf(stderr, "op_print: %%d expects an int\n");
                        exit(1);
                    }
                    printf("%d", v.as.i);
                    break;
                case 'f':
                    if (v.type != TYPE_FLOAT) {
                        fprintf(stderr, "op_print: %%f expects a float\n");
                        exit(1);
                    }
                    printf("%f", v.as.f);
                    break;
                case 's':
                    if (v.type != TYPE_STRING) {
                        fprintf(stderr, "op_print: %%s expects a string\n");
                        exit(1);
                    }
                    printf("%s", v.as.s);
                    break;
                case 'b':
                    if (v.type != TYPE_BOOL) {
                        fprintf(stderr, "op_print: %%b expects a bool\n");
                        exit(1);
                    }
                    printf("%s", v.as.b ? "true" : "false");
                    break;
                default:
                    fprintf(stderr, "op_print: unknown format specifier %%%c\n", spec);
                    exit(1);
            }
            p += 2;
        } else {
            putchar(*p);
            p++;
        }
    }
}
void op_scanf(Stack* stack) {
    Value fmt = pop(stack);
    if (fmt.type != TYPE_STRING) {
        fprintf(stderr, "op_scanf: expected a format string on top of stack\n");
        exit(1);
    }
 
    int argc = count_format_specifiers(fmt.as.s);
    if (argc > 64) {
        fprintf(stderr, "op_scanf: too many arguments\n");
        exit(1);
    }
 
    Value tmp[64];
    for (int i = 0; i < argc; i++) {
        tmp[i] = pop(stack);
    }
 
    Value args[64];
    for (int i = 0; i < argc; i++) {
        args[i] = tmp[argc - 1 - i];
    }
 
    int arg_index = 0;
    const char* p = fmt.as.s;
    while (*p) {
        if (*p == '%' && *(p + 1) != '\0') {
            char spec = *(p + 1);
            if (spec == '%') {
                putchar('%');
                p += 2;
                continue;
            }
            if (arg_index >= argc) {
                fprintf(stderr, "op_scanf: not enough arguments for format string\n");
                exit(1);
            }
            Value v = args[arg_index++];
            if (v.type != TYPE_PTR) {
                fprintf(stderr, "op_scanf: expected a pointer (variable), got value\n");
                exit(1);
            }
            switch (spec) {
                case 'd':
                    if (v.as.ptr->type !=TYPE_INT ){
                        fprintf(stderr, "op_scanf: %%d expects a *int\n");
                    }
                    scanf("%d", &(v.as.ptr->as.i));
                    break;
                case 'f':
                    if (v.as.ptr->type !=TYPE_FLOAT) {
                        fprintf(stderr, "op_scanf: %%f expects a *float\n");
                        exit(1);
                    }
                    scanf("%f", &(v.as.ptr->as.f));
                    break;
                case 's':
                    if (v.as.ptr->type !=TYPE_STRING) {
                        fprintf(stderr, "op_scanf: %%s expects a string\n");
                        exit(1);
                    }
                    scanf("%s", &(v.as.ptr->as.s));
                    break;
                case 'b':
                    if (v.as.ptr->type !=TYPE_BOOL) {
                        fprintf(stderr, "op_scanf: %%b expects a *bool\n");
                        exit(1);
                    }
                    scanf("%s", &(v.as.ptr->as.b));
                    break;
                default:
                    fprintf(stderr, "op_scanf: unknown format specifier %%%c\n", spec);
                    exit(1);
            }
            p += 2;
        } else {
            putchar(*p);
            p++;
        }
    }
}
void op_fgets(Stack* stack, int max_len) {
    Value ptr_value = pop(stack);
    if (ptr_value.type != TYPE_PTR) {
        fprintf(stderr, "read_line: expected a pointer on the stack\n");
        exit(1);
    }
 
    Value* target = ptr_value.as.ptr;
    if (target->type != TYPE_STRING || target->as.s == NULL) {
        fprintf(stderr, "read_line: target variable is not an allocated string buffer\n");
        exit(1);
    }
 
    if (fgets(target->as.s, max_len, stdin) == NULL) {
        target->as.s[0] = '\0'; 
        return;
    }
 
    size_t len = strlen(target->as.s);
    if (len > 0 && target->as.s[len - 1] == '\n') {
        target->as.s[len - 1] = '\0';
    }
}
void op_sizeof(Stack* stack) {
    Value v = pop(stack);
 
    switch (v.type) {
        case TYPE_ARRAY: {
            ArrayObject* arr = (ArrayObject*)v.as.obj;
            push(stack, (Value){ .type = TYPE_INT, .as.i = arr->length });
            break;
        }
        case TYPE_STRING:
            push(stack, (Value){ .type = TYPE_INT, .as.i = (int)strlen(v.as.s) });
            break;
        default:
            fprintf(stderr, "op_sizeof: unsupported type (expected array or string, did you forget 'deref'?)\n");
            exit(1);
    }
}
void op_strlen(Stack* stack) {
    Value s = pop(stack);
    if(s.type == TYPE_STRING){
        push_int(stack,strlen(s.as.s));
    }else {
        fprintf(stderr, "op_strlen: unsupported type (expected string)\n");
        exit(1);
    } 
    
}
void op_equals(Stack* s){
    Value b = pop(s); 
    Value a = pop(s);
    
    if (a.type == TYPE_INT && b.type == TYPE_INT)             push_bool(s,a.as.i == b.as.i);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_FLOAT)    push_bool(s,a.as.f == b.as.f);
    else if (a.type == TYPE_INT && b.type == TYPE_FLOAT)      push_bool(s,(float)a.as.i == b.as.f);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_INT)      push_bool(s,a.as.f == (float)b.as.i);
    else if (a.type == TYPE_STRING && b.type == TYPE_STRING ) push_bool(s, compare_strings(a.as.s, b.as.s));
    else {
        fprintf(stderr, "Type error: cannot compare these types\n");
        exit(1);
    }
}
void op_greater_equals(Stack* s){
    Value b = pop(s); 
    Value a = pop(s);
    
    if (a.type == TYPE_INT && b.type == TYPE_INT)             push_bool(s,a.as.i >= b.as.i);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_FLOAT)    push_bool(s,a.as.f >= b.as.f);
    else if (a.type == TYPE_INT && b.type == TYPE_FLOAT)      push_bool(s,(float)a.as.i >= b.as.f);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_INT)      push_bool(s,a.as.f >= (float)b.as.i);
    else if (a.type == TYPE_STRING && b.type == TYPE_STRING ) push_bool(s, compare_strings_leng(a.as.s, b.as.s));
    else {
        fprintf(stderr, "Type error: cannot compare these types\n");
        exit(1);
    }
}
void op_less_equals(Stack* s){
    Value b = pop(s); 
    Value a = pop(s);
    
    if (a.type == TYPE_INT && b.type == TYPE_INT)             push_bool(s,a.as.i <= b.as.i);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_FLOAT)    push_bool(s,a.as.f <= b.as.f);
    else if (a.type == TYPE_INT && b.type == TYPE_FLOAT)      push_bool(s,(float)a.as.i <= b.as.f);
    else if (a.type == TYPE_FLOAT && b.type == TYPE_INT)      push_bool(s,a.as.f <= (float)b.as.i);
    else if (a.type == TYPE_STRING && b.type == TYPE_STRING ) push_bool(s, compare_strings_lenl(a.as.s, b.as.s));
    else {
        fprintf(stderr, "Type error: cannot compare these types\n");
        exit(1);
    }
}
bool is_truthy(Value v) {
    switch (v.type) {
        case TYPE_BOOL:   return v.as.b;
        case TYPE_INT:    return v.as.i != 0;
        case TYPE_FLOAT:  return v.as.f != 0.0f;
        case TYPE_STRING: return v.as.s != NULL && v.as.s[0] != '\0';
        case TYPE_PTR:    return v.as.ptr != NULL;
        case TYPE_ARRAY:  return v.as.obj != NULL;
        default:          return false;
    }
}
ArrayObject* array_create(int capacity, ValueType elem_type) {
    if (capacity <= 0) {
        fprintf(stderr, "array_create: capacity must be positive\n");
        exit(1);
    }
 
    ArrayObject* arr = malloc(sizeof(ArrayObject));
    arr->capacity = capacity;
    arr->length = capacity;
 
    arr->items = malloc(sizeof(Value) * capacity);
    for (int idx = 0; idx < capacity; idx++) {
        arr->items[idx].type = elem_type;
        memset(&arr->items[idx].as, 0, sizeof(arr->items[idx].as));
    }
 
    return arr;
}
 
Value array_get(ArrayObject* arr, int index) {
    if (index < 0 || index >= arr->length) {
        fprintf(stderr, "array_get: index %d out of bounds (length %d)\n", index, arr->length);
        exit(1);
    }
    return arr->items[index];
}
 
void array_set(ArrayObject* arr, int index, Value v) {
    if (index < 0 || index >= arr->length) {
        fprintf(stderr, "array_set: index %d out of bounds (length %d)\n", index, arr->length);
        exit(1);
    }
    arr->items[index] = v;
}
void op_arr_get(Stack* stack) {
    Value idx_v = pop(stack);
    Value arr_v = pop(stack);
 
    if (arr_v.type != TYPE_ARRAY) {
        fprintf(stderr, "op_arr_get: expected an array on the stack (did you forget 'deref'?)\n");
        exit(1);
    }
    if (idx_v.type != TYPE_INT) {
        fprintf(stderr, "op_arr_get: expected an int index\n");
        exit(1);
    }
 
    ArrayObject* arr = (ArrayObject*)arr_v.as.obj;
    Value result = array_get(arr, idx_v.as.i);
    //TODO: Make avaliable for strings
    push(stack, result);
}
 
void op_arr_set(Stack* stack) {
    Value value = pop(stack);
    Value idx_v = pop(stack);
    Value arr_v = pop(stack);
 
    if (arr_v.type != TYPE_ARRAY) {
        fprintf(stderr, "op_arr_set: expected an array on the stack (did you forget 'deref'?)\n");
        exit(1);
    }
    if (idx_v.type != TYPE_INT) {
        fprintf(stderr, "op_arr_set: expected an int index\n");
        exit(1);
    }
 
    ArrayObject* arr = (ArrayObject*)arr_v.as.obj;
    array_set(arr, idx_v.as.i, value);
     //TODO: Make avaliable for strings
}
