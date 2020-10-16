NUM = 0
OP = 1
NAME = 2
STRING = 3
CHAR = 4
NEWLINE = 5
variableName = {
    0: 'NUM',
    1: 'OP',
    2: 'NAME',
    3: 'STRING',
    4: 'CHAR',
    5: 'NEWLINE'
}


class CodeStream:
    codeLines: list

    def __init__(self, codeLines: list) -> None:
        self.codeLines = codeLines

    def __getitem__(self, index):
        return self.codeLines[index]

    def append(self, codeLine: str) -> None:
        self.codeLines.append(codeLine)


class CodeReader:
    @staticmethod
    def readFromFile(path: str) -> CodeStream:
        with open(path, 'r') as file:
            return CodeStream(file.readlines())

    @staticmethod
    def readFromString(code: str) -> CodeStream:
        return CodeStream([line + '\n' for line in code.split('\n')])


class Token:
    def __init__(self, typeof: int, string: str) -> None:
        self.typeof: int = typeof
        self.string: str = string

    def __getitem__(self, index):
        if index == 0:
            return self.typeof
        elif index == 1:
            return self.string
        else:
            raise IndexError('Token object index is from 0 to 1')

    def __str__(self) -> str:
        return f'(typeof = {self.typeof} ({variableName[self.typeof]}), string = {self.string})'

    def __repr__(self):
        return f'(typeof = {self.typeof} ({variableName[self.typeof]}), string = {repr(self.string)})'


class Tokenizer:
    isMultilineCommentGoingToEndedThisLine: bool = True
    NUMS: set = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    OPS: dict = {'+': ['++', '+='],
                 '-': ['--', '-=', '->'],
                 '*': ['*='],
                 '/': ['/='],
                 '%': ['%='],
                 '=': ['=='],
                 '!': ['!='],
                 '>': ['>=', '>>'],
                 '<': ['<=', '<<'],
                 '|': ['||'],
                 '&': ['&&'],
                 '~': [],
                 ',': [],
                 '(': [],
                 ')': [],
                 '[': [],
                 ']': [],
                 '{': [],
                 '}': [],
                 '?': [],
                 '#': [],
                 '.': [],
                 ';': []}
    # Despite 'sizeof' is an operator in C language, it will be regarded as a NMAE during token-making
    letters: set = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}

    @staticmethod
    def recognizeNumToken(codeLine: str, beginIndex: int) -> tuple:
        # (token, endIndex) endIndex is the new begin index of the next token
        analyzedCodeLine = codeLine[beginIndex:]
        if analyzedCodeLine[0] == '0':
            if analyzedCodeLine[:2] == '0x':
                for index0, char in enumerate(analyzedCodeLine):
                    if (char in Tokenizer.OPS) or (char not in Tokenizer.NUMS and char not in Tokenizer.letters):
                        token: Token = Token(NUM, analyzedCodeLine[:index0])
                        endIndex: int = index0
                        return token, beginIndex + endIndex
            elif analyzedCodeLine[:2] == '0b':
                for index0, char in enumerate(analyzedCodeLine):
                    if (char in Tokenizer.OPS) or (index0 >= 2 and char not in ('0', '1')):
                        token: Token = Token(NUM, analyzedCodeLine[:index0])
                        endIndex: int = index0
                        return token, beginIndex + endIndex
            elif analyzedCodeLine[:2] == '0.':
                for index0, char in enumerate(analyzedCodeLine):
                    if (index0 != 1 and char in Tokenizer.OPS) or (index0 != 1 and char not in Tokenizer.NUMS):
                        token: Token = Token(NUM, analyzedCodeLine[:index0])
                        endIndex: int = index0
                        return token, beginIndex + endIndex
            else:
                for index0, char in enumerate(analyzedCodeLine):
                    if char not in Tokenizer.NUMS:
                        token: Token = Token(NUM, analyzedCodeLine[:index0])
                        endIndex: int = index0
                        return token, beginIndex + endIndex
        else:
            isDotMet: bool = False
            for index0, char in enumerate(analyzedCodeLine):
                if isDotMet:
                    if char not in Tokenizer.NUMS:
                        token: Token = Token(NUM, analyzedCodeLine[:index0])
                        endIndex: int = index0
                        return token, beginIndex + endIndex
                else:
                    if char == '.':
                        isDotMet = True
                    elif char not in Tokenizer.NUMS:
                        token: Token = Token(NUM, analyzedCodeLine[:index0])
                        endIndex: int = index0
                        return token, beginIndex + endIndex

    @staticmethod
    def recognizeOpToken(codeLine: str, beginIndex: int) -> tuple:  # (token, endIndex)
        analyzedCodeLine = codeLine[beginIndex:]
        if not Tokenizer.OPS[analyzedCodeLine[0]]:
            return Token(OP, analyzedCodeLine[0]), beginIndex + 1
        else:
            possibleOp = analyzedCodeLine[0: 2]
            if possibleOp in Tokenizer.OPS[analyzedCodeLine[0]]:
                return Token(OP, possibleOp), beginIndex + 2
            else:
                return Token(OP, analyzedCodeLine[0]), beginIndex + 1

    @staticmethod
    def recognizeNameToken(codeLine: str, beginIndex: int) -> tuple:
        analyzedCodeLine = codeLine[beginIndex:]
        for index0, char in enumerate(analyzedCodeLine):
            if char in Tokenizer.OPS or char in (' ', "'", '"', '\n', '\t'):
                return Token(NAME, analyzedCodeLine[:index0]), beginIndex + index0

    @staticmethod
    def recognizeStringToken(codeLine: str, beginIndex: int) -> tuple:
        analyzedCodeLine = codeLine[beginIndex:]
        hasEffectiveEscapeCharacter: bool = False
        for index0, char in enumerate(analyzedCodeLine):
            if hasEffectiveEscapeCharacter:
                hasEffectiveEscapeCharacter = False
            else:
                if char == '\\':
                    hasEffectiveEscapeCharacter = True
                elif index0 != 0 and char == '"':
                    return Token(STRING, analyzedCodeLine[:index0 + 1]), beginIndex + index0 + 1

    @staticmethod
    def recognizeCharToken(codeLine: str, beginIndex: int) -> tuple:
        analyzedCodeLine = codeLine[beginIndex:]
        hasEffectiveEscapeCharacter: bool = False
        for index0, char in enumerate(analyzedCodeLine):
            if hasEffectiveEscapeCharacter:
                hasEffectiveEscapeCharacter = False
            else:
                if char == '\\':
                    hasEffectiveEscapeCharacter = True
                elif index0 != 0 and char == "'":
                    return Token(CHAR, analyzedCodeLine[:index0 + 1]), beginIndex + index0 + 1

    @staticmethod
    def recognizeCommentToken(codeLine: str, beginIndex: int) -> tuple:
        # if meet codeLine like this: int a = 9; /* a is count */ double b = 6.6;
        # then return (endIndex,)
        # else if meet multiline, return (None,)
        # if meet single line comment, return (endIndex,), endIndex is the index of \n
        analyzedCodeLine = codeLine[beginIndex:]
        if Tokenizer.isMultilineCommentGoingToEndedThisLine:
            if analyzedCodeLine[:2] == '//':
                if analyzedCodeLine[-1] == '/n':
                    return (len(codeLine) - 1,)
                else:
                    return (len(codeLine),)
            elif analyzedCodeLine[:2] == '/*':
                findIndex = analyzedCodeLine.find('*/')
                if findIndex != -1:
                    return (beginIndex + findIndex + 2,)
                else:
                    Tokenizer.isMultilineCommentGoingToEndedThisLine = False
                    return (None,)

        else:
            findIndex = analyzedCodeLine.find('*/')
            if findIndex != -1:
                Tokenizer.isMultilineCommentGoingToEndedThisLine = True
                return (beginIndex + findIndex + 2,)
            else:
                return (None,)

    @staticmethod
    def toToken(codeLine: str) -> list:
        tokenList: list = []
        tokenRangeBeginIndex: int = 0
        for index, char in enumerate(codeLine):
            if not Tokenizer.isMultilineCommentGoingToEndedThisLine:
                if not index:
                    tokenRangeBeginIndex = Tokenizer.recognizeCommentToken(codeLine, index)[0]
                else:
                    return []
            else:
                if index >= tokenRangeBeginIndex:
                    if char == '/' and codeLine[index + 1] in ('/', '*'):
                        tokenRangeBeginIndex = Tokenizer.recognizeCommentToken(codeLine, index)[0]
                    elif char in Tokenizer.NUMS:
                        token, tokenRangeBeginIndex = Tokenizer.recognizeNumToken(codeLine, index)
                        tokenList.append(token)
                    elif char in Tokenizer.OPS:
                        token, tokenRangeBeginIndex = Tokenizer.recognizeOpToken(codeLine, index)
                        tokenList.append(token)
                    elif char == '"':
                        token, tokenRangeBeginIndex = Tokenizer.recognizeStringToken(codeLine, index)
                        tokenList.append(token)
                    elif char == "'":
                        token, tokenRangeBeginIndex = Tokenizer.recognizeCharToken(codeLine, index)
                        tokenList.append(token)
                    elif char == '\n':
                        tokenList.append(Token(NEWLINE, '\n'))
                    elif char not in (' ', '\t'):
                        token, tokenRangeBeginIndex = Tokenizer.recognizeNameToken(codeLine, index)
                        tokenList.append(token)
                else:
                    continue
        return tokenList


class TokenStream:
    def __init__(self, codeStream: CodeStream) -> None:  # codeStream object must have an interface named '__getitem__'
        self.tokenStream: list = list()
        for codeLine in codeStream:
            self.tokenStream.extend(Tokenizer.toToken(codeLine))

    def __getitem__(self, index):
        return self.tokenStream[index]

    def append(self, token: Token) -> None:
        self.tokenStream.append(token)

    def __str__(self):
        return '[' + ',\n'.join([repr(token) for token in self.tokenStream]) + ']'



