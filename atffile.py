import sys
import os
import json
from atfflex import AtfLexer
from atfyacc import AtfParser

def File_To_String(fileName):
    with open(fileName, 'r') as myfile:
        data=myfile.read()
    return data.split("&P")

if __name__ == "__main__":
    # Build the lexer
    #fileName = sys.argv[1]
    fileName = json.loads(sys.argv[1])
    languageFile = json.loads(sys.argv[2])

    lexer = AtfLexer(fileName, languageFile).lexer
    content_list = File_To_String("/atfchecker_data/storage/"+str(fileName))

    for content in content_list[1:]:
        parser = AtfParser(fileName, languageFile).parser
        text = parser.parse("&P"+content, lexer=lexer)

        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)

os.remove("/atfchecker_data/storage/"+fileName)

with open("/atfchecker_data/output/"+fileName, 'r') as myfile:
    parseResult = myfile.read()

os.remove("/atfchecker_data/output/"+fileName)
print json.dumps(parseResult)

#Home Ubuntu
#python atffile.py /home/prajput/atfparser/cdli_atf_20161022.txt
#python atffile.py /home/prajput/atfparser/broad_sample.atf

#Home Mac-Pro
#python atffile.py /Users/User/Documents/atfparser/broad_sample.atf
#python atffile.py /Users/User/Documents/atfparser/cdli_atf_20161022.txt

#Lab
#python atffile.py /Users/cdlilab/Documents/atfparser/cdli_atf_20161022.txt
#python atffile.py /Users/cdlilab/Documents/atfparser/broad_sample.atf

#Send File One by One
#data.split("&P")
