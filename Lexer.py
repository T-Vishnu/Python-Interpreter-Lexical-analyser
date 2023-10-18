INTEGER = 'INTEGER'
MULTIPLY = 'MULTIPLY'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
VARIABLE = 'VARIABLE'
EQUALS = 'EQUALS'
EOF = 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)

class Lexer:
    def __init__(self):
        self.tokens=[]
        self.token_idx = 0

    def tokenize(self, text):
        i = 0
        while(i < len(text)):
            if(text[i] == ' '):
                i += 1
                continue
            elif(text[i] == '\n'):
                i += 1
                continue
            elif(i+5<len(text) and text[i:i+5:1] == 'print'):
                i += 5
                continue
            elif (text[i].isdigit()):
                x = ""
                while ((i < len(text)) and text[i].isdigit()) :
                    x += text[i]
                    i += 1
                if(i < len(text) and text[i].isalpha()):
                    raise Exception('Invalid Syntax')
                else:
                    value = int(x)
                    token = Token(INTEGER,value)
                    self.tokens.append(token)
                    continue
            elif(text[i] == '*'):
                token = Token(MULTIPLY,'*')
                self.tokens.append(token)
                i += 1
            elif(text[i] == '('):
                token = Token(LPAREN,'\(')
                self.tokens.append(token)
                i += 1
            elif(text[i] == ')'):
                token = Token(RPAREN,'\)')
                self.tokens.append(token)
                i += 1
            elif(text[i] == '='):
                token = Token(EQUALS,'=')
                self.tokens.append(token)
                i += 1
            elif (text[i].isalpha()):
                x = ""
                while ((i < len(text)) and text[i].isalnum()) :
                    x += text[i]
                    i += 1
                value = x
                token = Token(VARIABLE,value)
                self.tokens.append(token)
                continue
            else:
                raise Exception('Lexical error')
            
        self.tokens.append(Token(EOF, None))

    
    def lookahead1token(self):
        if(self.token_idx >= len(self.tokens)):
            return None
        return self.tokens[self.token_idx]
    
    def get_next_token(self):
        if self.token_idx >= len(self.tokens):
            return None
        else:
            self.token_idx+=1
            return self.tokens[self.token_idx-1]

    def reset(self):
        self.tokens.clear()
        self.token_idx = 0
