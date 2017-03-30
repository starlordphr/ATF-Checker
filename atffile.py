import sys
from atfflex import AtfLexer
from atfyacc import AtfParser

def File_To_String(fileName):
    with open(fileName, 'r') as myfile:
        data=myfile.read()
    return data

if __name__ == "__main__":
    # Build the lexer
    lexer = AtfLexer().lexer
    content = File_To_String(sys.argv[1])
    parser = AtfParser().parser
    text = parser.parse(content, lexer=lexer)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

#python atffile.py /Users/smith/Documents/atfparser/cdli_atf_20161022.txt
