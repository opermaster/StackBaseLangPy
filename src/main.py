from enum import Enum
# printf("%d %d", 12,13)
# 13 12 "%d %d" printf

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
    with open(file_path,"w") as file:
        #Header
        file.write("// Header\n")
        file.write("#include <stdio.h>\n")
        file.write("#include \"stack.h\"\n")
        file.write("\nint main(){\n")
        file.write("\tStack s; \n\tstack_init(&s);\n")

        for token in tokens:
            match token[0]:
                case TokenType.Int:
                    file.write(f"\t//PUSH INT `{token[1]}`\n")
                    file.write(f"\tpush_int(&s,{token[1]});\n")
                case TokenType.Str:
                    file.write(f"\t//PUSH STR `\"{token[1]}\"`\n")
                    file.write(f"\tpush_string(&s,\"{token[1]}\");\n")
                case TokenType.Lit:
                    match token[1]:
                        case "+":
                            file.write(f"\t//PLUS\n")
                            file.write(f"\top_add(&s);\n")
                        case "print":
                            file.write(f"\t//PRINT\n")
                            file.write(f"\top_print(&s);\n")
        file.write("\treturn 0;\n")
        file.write("};\n")
program = """1 5 +
\"%d\\n\" print
\"Hello world!\\n\" print
"""

tokens = tokenize(program)

for token in tokens:
    print(token)

compile_tokens(tokens,".\\build\\output.c")
