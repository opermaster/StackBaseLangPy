from enum import Enum
import os


class State(Enum):
    Start     = 0
    InInt     = 1
    InFloat   = 2
    InStr     = 3
    InLit     = 4
    InEquals  = 5 # for == => =<
    InComment = 6

class TokenType(Enum):
    Int = 1
    Float = 2 
    Str = 3
    Lit = 4
    OParen = 5   # (
    CParen = 6   # )
    COParen = 7  # {
    CCParen = 8  # }
    SOParen = 9  # [
    SCParen = 10 # ]
    Comment = 11 #/* */
    
TYPE_MAP = {
    "int":    ("TYPE_INT",    "0",     "i"),
    "float":  ("TYPE_FLOAT",  "0.0f",  "f"),
    "string": ("TYPE_STRING", "NULL",  "s"),
    "bool":   ("TYPE_BOOL",   "false" ,"b"),
}

def tokenize(program):
    state = State.Start
    tokens = []
    value  = ""
    ttype  = TokenType.Lit

    i = 0
    
    while (i< len(program)):
        c = program[i]
            
        match state:
            case State.Start:
                if c.isdigit():
                    ttype = TokenType.Int
                    value += c
                    state = State.InInt
                elif c=='\"':
                    ttype = TokenType.Str
                    state = State.InStr
                elif c=="/" and i+1!=len(program) and program[i+1] =='*':
                    ttype = TokenType.Comment
                    state = State.InComment
                    value += c + program[i+1]
                    i+=1
                    
                elif c=='=':
                    state = State.InEquals
                    value += c
                    #ttype stays Lit
                elif c.isspace() or c=='\0'or c=='\n':
                    i+=1
                    continue
                elif c=='[':
                    ttype = TokenType.SOParen
                    value +=c
                    state = State.Start
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit
                elif c==']':
                    ttype = TokenType.SCParen
                    value +=c
                    state = State.Start
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit
                else:
                    ttype = TokenType.Lit
                    value += c
                    state = State.InLit
            case State.InComment:
                if value[-1] =='*' and c =='/':
                    ttype = TokenType.Comment
                    value +=c
                    state = State.Start
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit
                else:
                    value +=c
            case State.InInt:
                if c.isdigit():
                    value += c
                elif c=='.':
                    ttype = TokenType.Float
                    state = State.InFloat
                    value += c
                    
                elif c.isspace():
                    state = State.Start
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit
                else:
                    state = State.Start
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit
                    i-=1
                    
            case State.InFloat:
                if c.isdigit():
                    value += c

                elif c.isspace():
                    state = State.Start
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit
                    
            case State.InLit:
                if c.isspace():
                    state = State.Start
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit
                elif c in "[]{}()=":
                    state = State.Start
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit
                    i-=1
                else:
                    value +=c
                    
            case State.InStr:
                if c=='\"':
                    state = State.Start
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit
                    i+=1
                else:
                    value +=c
            case State.InEquals:
                if c in ">=<":
                    value +=c
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit
                else:
                    i-=1
                    tokens.append((ttype,value))
                    value = ""
                    ttype = TokenType.Lit

                state = State.Start
        i+=1
    if value != "":
        tokens.append((ttype,value))
    return tokens

def compile_tokens(tokens,file_path):
    declared_vars = set()
    var_sizes = {}      
    last_var_name = None
    indent = "\t"
    if_counter = 0
    cond_counter = 0
    with open(file_path,"w") as file:
        file.write("// HEADER\n")
        file.write("#include <stdio.h>\n")
        file.write("#include \"stack.h\"\n")
        file.write("#include <stdlib.h>\n")
        file.write("\nint main(){\n")
        file.write("\tStack s; \n\tstack_init(&s);\n")
        file.write("\t// BODY\n")
        
        i = 0
        
        while(i< len(tokens)):
            token = tokens[i]
            match token[0]:
                case TokenType.Int:
                    file.write(f"//PUSH INT `{token[1]}`\n")
                    file.write(f"{indent}push_int(&s,{token[1]});\n")
                case TokenType.Str:
                    file.write(f"//PUSH STR `\"{token[1]}\"`\n")
                    file.write(f"{indent}push_string(&s,\"{token[1]}\");\n")
                case TokenType.Float:
                    file.write(f"//PUSH FLOAT  `\"{token[1]}\"`\n")
                    file.write(f"{indent}push_float(&s,{token[1]}f);\n")
                case TokenType.Comment:
                    file.write(f"{token[1]}\n")
                case TokenType.Lit:
                    match token[1]:
                        case "+":
                            file.write(f"//PLUS\n")
                            file.write(f"{indent}op_add(&s);\n")
                        case "-":
                            file.write(f"//MINUS\n")
                            file.write(f"{indent}op_minus(&s);\n")
                        case "/":
                            file.write(f"//DIV\n")
                            file.write(f"{indent}op_div(&s);\n")
                        case "*":
                            file.write(f"//MUL\n")
                            file.write(f"{indent}op_mul(&s);\n")
                        case "==":
                            file.write(f"//EQUALS\n")
                            file.write(f"{indent}op_equals(&s);\n")
                        case "=<":
                            file.write(f"//LESS EQUALS\n")
                            file.write(f"{indent}op_less_equals(&s);\n")
                        case "=>":
                            file.write(f"//GREATER EQUALS\n")
                            file.write(f"{indent}op_greater_equals(&s);\n")
                        case "{":
                            file.write(indent+token[1]+'\n')
                            indent+='\t'
                        case "}":
                            indent = indent[:-1]
                            file.write(indent+token[1]+'\n')
                        case "printf":
                            file.write(f"//PRINTF\n")
                            file.write(f"{indent}op_printf(&s);\n")
                        case "scanf":
                            file.write(f"//SCANF\n")
                            file.write(f"{indent}op_scanf(&s);\n")
                        case "let":
                            type_name = tokens[i + 1][1]
                            var_name = tokens[i + 2][1]
                            isarray = False
                            c_type_enum, default_val, field = TYPE_MAP[type_name]
                            
                            if type_name not in TYPE_MAP:
                                raise SyntaxError(f"Unknown type '{type_name}' in let")
                            if tokens[i+3][0]==TokenType.SOParen:
                                isarray = True
                            if isarray:
                                if c_type_enum != "TYPE_STRING":
                                    raise SyntaxError("Now only support for 'string'-arrays (for fgets)")

                                array_size = int(tokens[i + 4][1])

                                file.write(f"//LET {type_name} {var_name}[{array_size}]\n")
                                file.write(
                                    f"{indent}Value {var_name} = (Value){{ .type = TYPE_STRING, "
                                    f".as.s = malloc({array_size} + 1) }};\n"
                                )
                                file.write(f"{indent}{var_name}.as.s[0] = '\\0';\n")

                                declared_vars.add(var_name)
                                var_sizes[var_name] = array_size  # buffer size for  "read"
                                i += 6  # let, type, name, '[', size, ']'
                                continue

                            file.write(f"//LET {type_name} {var_name}\n")
                            file.write(
                                f"{indent}Value {var_name} = (Value){{ .type = {c_type_enum}, "
                                f".as.{field} = {default_val} }};\n"
                            )

                            declared_vars.add(var_name)
                            i += 3
                            continue

                        case "store":
                            file.write(f"//STORE\n")
                            file.write(f"{indent}op_store(&s);\n")
    
                        case "deref":
                            file.write(f"//DEREF\n")
                            file.write(f"{indent}op_deref(&s);\n")
                        case "fgets":
                            if last_var_name is None or last_var_name not in var_sizes:
                                raise SyntaxError("read: before 'fgets' must be variable array ('buf fgets')")
                            size = var_sizes[last_var_name]
                            file.write(f"//fgets into {last_var_name}\n")
                            file.write(f"{indent}op_fgets(&s, {size});\n")
                        case "if":
                            file.write("//IF\n")
                            file.write(f"{indent}Value __cond{if_counter} = pop(&s);\n")
                            file.write(f"{indent}if (is_truthy(__cond{if_counter}))")
                            if_counter +=1
                        case "else":
                            file.write("//ELSE\n")
                            file.write(indent+"else")
                        case "while":
                            file.write(f"{indent}while (1)")
                        case "do":
                            file.write("//DO\n")
                            file.write(f"{indent}Value __cond{cond_counter} = pop(&s);\n")
                            file.write(f"{indent}if (!is_truthy(__cond{cond_counter})) break;\n")
                            cond_counter += 1
                        case _:
                            if token[1] in declared_vars:
                                file.write(f"//PUSH_PTR {token[1]}\n")
                                file.write(f"{indent}push_ptr(&s, &{token[1]});\n")
                                last_var_name = token[1]
                            else:
                                raise SyntaxError(f"Unknown literal: `{token[1]}`")
                            
            i+=1
        file.write("\treturn 0;\n};")
def compile_file(input_path: str, output_path: str, verbose: bool = False):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Source file not found: {input_path}")
 
    with open(input_path, "r", encoding="utf-8") as f:
        program = f.read()
 
    tokens = tokenize(program)
 
    if verbose:
        for token in tokens:
            print(token)

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
 
    compile_tokens(tokens, output_path)
 
    if verbose:
        print(f"Compiled '{input_path}' -> '{output_path}'")
 
 
if __name__ == "__main__":
    # python main.py program.txt build/output.c
    import sys
    if len(sys.argv) != 3:
        print("Usage: python compiler.py <input_file> <output_file.c>")
        sys.exit(1)
 
    compile_file(sys.argv[1], sys.argv[2], verbose=True)
