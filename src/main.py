from enum import Enum
import os


class State(Enum):
    Start   = 0
    InInt   = 1
    InFloat = 2
    InStr   = 3
    InLit   = 4

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
TYPE_MAP = {
    "int":    ("TYPE_INT",    "0"),
    "float":  ("TYPE_FLOAT",  "0.0f"),
    "string": ("TYPE_STRING", "NULL"),
    "bool":   ("TYPE_BOOL",   "false"),
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
                elif c.isspace() or c=='\0'or c=='\n':
                    i+=1
                    continue
                else:
                    ttype = TokenType.Lit
                    value += c
                    state = State.InLit

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
                    
        i+=1
    if value != "":
        tokens.append((ttype,value))
    return tokens

def compile_tokens(tokens,file_path):
    declared_vars = set()
    with open(file_path,"w") as file:
        #Header
        file.write("// Header\n")
        file.write("#include <stdio.h>\n")
        file.write("#include \"stack.h\"\n")
        file.write("\nint main(){\n")
        file.write("\tStack s; \n\tstack_init(&s);\n")
        file.write("// BODY\n")
        i = 0
        
        while(i< len(tokens)):
            token = tokens[i]
            match token[0]:
                case TokenType.Int:
                    file.write(f"\t//PUSH INT `{token[1]}`\n")
                    file.write(f"\tpush_int(&s,{token[1]});\n")
                case TokenType.Str:
                    file.write(f"\t//PUSH STR `\"{token[1]}\"`\n")
                    file.write(f"\tpush_string(&s,\"{token[1]}\");\n")
                case TokenType.Float:
                    file.write(f"\t//PUSH FLOAT  `\"{token[1]}\"`\n")
                    file.write(f"\tpush_float(&s,{token[1]}f);\n")
                case TokenType.Lit:
                    match token[1]:
                        case "+":
                            file.write(f"\t//PLUS\n")
                            file.write(f"\top_add(&s);\n")
                        case "-":
                            file.write(f"\t//MINUS\n")
                            file.write(f"\top_minus(&s);\n")
                        case "/":
                            file.write(f"\t//DIV\n")
                            file.write(f"\top_div(&s);\n")
                        case "*":
                            file.write(f"\t//MUL\n")
                            file.write(f"\top_mul(&s);\n")
                        case "print":
                            file.write(f"\t//PRINT\n")
                            file.write(f"\top_print(&s);\n")
                        case "let":
                            type_name = tokens[i + 1][1]
                            var_name = tokens[i + 2][1]
                        
                            if type_name not in TYPE_MAP:
                                raise SyntaxError(f"Unknown type '{type_name}' in let")

                            c_type_enum, default_val = TYPE_MAP[type_name]
                            field = {"TYPE_INT": "i", "TYPE_FLOAT": "f",
                                     "TYPE_STRING": "s", "TYPE_BOOL": "b"}[c_type_enum]

                            file.write(f"\t//LET {type_name} {var_name}\n")
                            file.write(
                                f"\tValue {var_name} = (Value){{ .type = {c_type_enum}, "
                                f".as.{field} = {default_val} }};\n"
                            )

                            declared_vars.add(var_name)
                            i += 3
                            continue

                        case "store":
                            file.write(f"\t//STORE\n")
                            file.write(f"\top_store(&s);\n")
    
                        case "deref":
                            file.write(f"\t//DEREF\n")
                            file.write(f"\top_deref(&s);\n")
                            
                        case _ if token[1] in declared_vars:
                            file.write(f"\t//PUSH_PTR {token[1]}\n")
                            file.write(f"\tpush_ptr(&s, &{token[1]});\n")
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
    # python main.py program.em build/output.c
    import sys
    if len(sys.argv) != 3:
        print("Usage: python compiler.py <input_file> <output_file.c>")
        sys.exit(1)
 
    compile_file(sys.argv[1], sys.argv[2], verbose=False)
