# C-tokenizer
A C language tokenizer implemented by pure Python, can be used to tokenize C code in Python

# example

## tokenize code from string
```Python
from c_tokenizer import *

codeString = '''
int main()
{
	char* inputString = input();
	printf("%s", inputString);
	return 0;
}
'''
codeStream = CodeReader.readFromString(codeString)
tokenStream = TokenStream(codeStream)
print(tokenStream)
```

###output
```
[(typeof = 5 (NEWLINE), string = '\n'),
(typeof = 2 (NAME), string = 'int'),
(typeof = 2 (NAME), string = 'main'),
(typeof = 1 (OP), string = '('),
(typeof = 1 (OP), string = ')'),
(typeof = 5 (NEWLINE), string = '\n'),
(typeof = 1 (OP), string = '{'),
(typeof = 5 (NEWLINE), string = '\n'),
(typeof = 2 (NAME), string = 'char'),
(typeof = 1 (OP), string = '*'),
(typeof = 2 (NAME), string = 'inputString'),
(typeof = 1 (OP), string = '='),
(typeof = 2 (NAME), string = 'input'),
(typeof = 1 (OP), string = '('),
(typeof = 1 (OP), string = ')'),
(typeof = 1 (OP), string = ';'),
(typeof = 5 (NEWLINE), string = '\n'),
(typeof = 2 (NAME), string = 'printf'),
(typeof = 1 (OP), string = '('),
(typeof = 3 (STRING), string = '"%s"'),
(typeof = 1 (OP), string = ','),
(typeof = 2 (NAME), string = 'inputString'),
(typeof = 1 (OP), string = ')'),
(typeof = 1 (OP), string = ';'),
(typeof = 5 (NEWLINE), string = '\n'),
(typeof = 2 (NAME), string = 'return'),
(typeof = 0 (NUM), string = '0'),
(typeof = 1 (OP), string = ';'),
(typeof = 5 (NEWLINE), string = '\n'),
(typeof = 1 (OP), string = '}'),
(typeof = 5 (NEWLINE), string = '\n'),
(typeof = 5 (NEWLINE), string = '\n')]
```


## tokenize code from file
```Python
from c_tokenizer import *

codeStream = CodeReader.readFromFile(path="example.c") # replace it with you own file path
tokenStream = TokenStream(codeStream)
print(tokenStream)
```


