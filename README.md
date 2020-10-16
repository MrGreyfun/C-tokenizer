# C-tokenizer
A C language tokenizer implemented by pure Python, can be used to tokenize C code in Python

# example

## tokenize code from file
'''
from c_tokenizer import *

codeStream = CodeReader.readFromFile(path="example.c") # replace it with you own file path
tokenStream = TokenStream(codeStream)
print(tokenStream)
'''
