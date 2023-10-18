import fileinput
from Lexer import *

class Interpreter:
    def __init__(self, lexer):
        self.sym_tab = {}
        self.lexer = lexer
        self.current_token = None   
    
    def statements(self):
        statements = []
        while self.current_token.type != EOF:
            statement = self.statement()
            statements.append(statement)
        self.eat(EOF)
        return statements
    
    def statement(self):
        if self.lexer.lookahead1token()!=None and self.lexer.lookahead1token().type==EQUALS:
            self.assignment_statement()
        else:
            print(self.term())
            
    def term(self):
        result = self.factor()
        while self.current_token.type == MULTIPLY:
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
        return result

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return int(token.value)
        elif token.type == VARIABLE:
            self.eat(VARIABLE)
            value = self.sym_tab.get(token.value)
            if value is not None:
                return value
            else:
                raise Exception(f"Declaration of variable '{token.value}' is not found!")
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.term()
            self.eat(RPAREN)
            return result
        elif token.type == MULTIPLY:
            self.eat(MULTIPLY)
            return -self.factor()
        else:
            self.error()

    def assignment_statement(self):
        var_name = self.current_token.value
        self.eat(VARIABLE)
        self.eat(EQUALS)
        value = self.term()
        self.sym_tab[var_name]=value

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
        
    def error(self):
        raise Exception('Invalid syntax')

lexer = Lexer()
interpreter = Interpreter(lexer)
try:
    f = open("input.py")
    text = f.read()
    interpreter.lexer.reset()
    interpreter.lexer.tokenize(text)
    interpreter.current_token = interpreter.lexer.get_next_token()
    interpreter.statements()
except Exception as err:
    print(err)
