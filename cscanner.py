from ply import lex
from ply import yacc
import logging
from symboltable import SymbolTable

# tokens 'IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', 'SIZEOF', 'PTR_OP', 
#'INC_OP', 'DEC_OP', 'LEFT_OP', 'RIGHT_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP', 
#'AND_OP', 'OR_OP', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 
#'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN', 
#'TYPE_NAME', 'TYPEDEF', 'EXTERN', 'STATIC', 'AUTO', 'REGISTER', 
#'CHAR', 'SHORT', 'INT', 'LONG', 'SIGNED', 'UNSIGNED', 'FLOAT', 'DOUBLE', 
#'CONST', 'VOLATILE', 'VOID', 'STRUCT', 'UNION', 'ENUM', 'ELLIPSIS', 
#'CASE', 'DEFAULT', 'IF', 'ELSE', 'SWITCH', 'WHILE', 'DO', 'FOR', 
#'GOTO', 'CONTINUE', 'BREAK', 'RETURN""

reserved = {'auto' : 'AUTO', 'if' : 'IF', 'break' : 'BREAK', 'int' : 'INT', 'case' : 'CASE', 
            'long' : 'LONG', 'char' : 'CHAR', 'register' : 'REGISTER', 'continue' : 'CONTINUE', 
            'return' : 'RETURN', 'default' : 'DEFAULT', 'short' : 'SHORT', 'do' : 'DO', 
            'sizeof' : 'SIZEOF', 'double' : 'DOUBLE', 'static' : 'STATIC', 'else' : 'ELSE', 
            'struct' : 'STRUCT', 'switch' : 'SWITCH', 'extern' : 'EXTERN', 'typedef' : 'TYPEDEF', 
            'float' : 'FLOAT', 'union' : 'UNION', 'for' : 'FOR', 'unsigned' : '', 'goto' : 'GOTO', 
            'while' : 'WHILE', 'const' : 'CONST', 'void' : 'VOID'}


class Scanner():
  tokens = ['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', 'SIZEOF', 'PTR_OP', 'INC_OP', 'DEC_OP', 'LEFT_OP', 
            'RIGHT_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP', 'AND_OP', 'OR_OP', 'MUL_ASSIGN', 'DIV_ASSIGN', 
            'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN', 
            'XOR_ASSIGN', 'OR_ASSIGN', 'TYPEDEF', 'EXTERN', 'STATIC', 'AUTO', 'REGISTER', 
            'CHAR', 'SHORT', 'INT', 'LONG', 'SIGNED', 'UNSIGNED', 'FLOAT', 'DOUBLE', 'CONST', 'VOLATILE', 
            'VOID', 'STRUCT', 'UNION', 'ENUM', 'ELLIPSIS', 'CASE', 'DEFAULT', 'IF', 'ELSE', 'SWITCH', 
            'WHILE', 'DO', 'FOR', 'GOTO', 'CONTINUE', 'BREAK', 'RETURN','OPENBRACK','CLOSEBRACK','SEMI','OPENPARAN','CLOSEPARAN', 'COMMENT']

  precedence =  []
  literals = ['=',']','[','&','+','-','.','?','!',',',':','\'','*']
  def __init__(self, data):
    # print kw.get("file", 0)
    logging.basicConfig(
      level = logging.INFO,
      filename = "parselog.txt",
      filemode = "w",
      format = "%(filename)10s:%(lineno)4d:%(message)s"
    )
    log = self.log = logging.getLogger()
    self.lexer = lex.lex(module=self,debuglog=log,debug=True)

    # Give the lexer some input
    # self.lexer.input(data)
    self.input_data = data

    self.yacc = yacc.yacc(module=self,debuglog=log,debug=True)
    self.charcount = 0
    self.logtokens = False
    self.source = "" # this will keep track of what source we have seen so far
    self.tokens = ""  # this will keep track the tokens that we have seen so far
    self.reduction_list = [] # this will keep track of what tokens we have acquired
    self.log_tokens('tokens.txt')
    self.symbol_table = SymbolTable()
    self.lines = [0]

  def logging(self,typed,value):
      self.source += value + " " 
      self.tokens += typed + " "
      self.log.info("Line Number: " + str(self.lexer.lineno) + " Token: " + str(typed) + " Value: " + str(value))

  def set_symbol_table(self,sym):
    self.symbol_table = sym

  def log_tokens(self, txt):
    self.logtokens = True
    self.tokenlog = open(txt,'wa')

  def run(self):
    self.log.info("==============================Starting    LINE NUMBER: " + str(1) + "======================")
    self.yacc.parse(self.input_data,debug=self.log)
  def scan(self,string):
    self.lexer.input(string)
    self.log_tokens("tokens.txt")
    while(True):
      current = self.lexer.token()
      if current == None:
        break
      


  def test_running(self):
    while True:
      tok = self.lexer.token()
      if not tok: 
          break      # No more input
      print(tok)
      print(self.lexer.lexpos)

  def t_PTR_OP(self,t):
    "->"
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_CONSTANT(self,t):
    r"[0-9]+|[0-9]*\.[0-9]" # add hexadecimal
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  # Help from here http://www.lysator.liu.se/c/ANSI-C-grammar-l.html
  # should this second half be a constant for 'somechar'...
  def t_STRING_LITERAL(self,t):
    r'\"(\\.|[^\\\"])*\"|\'(\\.|[^\\\'])+\''
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_SIZEOF(self,t):
    r"SIZEOF"
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_INC_OP(self,t):
    r"\+\+"
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_DEC_OP(self,t):
    r"--"
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_LEFT_OP(self,t):
    r"<<"
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_RIGHT_OP(self,t):
    r">>"
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_LE_OP(self,t):
    r"<="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_GE_OP(self,t):
    r">="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_EQ_OP(self,t):
    r"=="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_NE_OP(self,t): 
    r"!="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_AND_OP(self,t):
    r"&"
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_OR_OP(self,t):
    r"\|\|"
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_MUL_ASSIGN(self,t):
    r"\*="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t


  def t_DIV_ASSIGN(self,t):
    r"/="


    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_MOD_ASSIGN(self,t):
    r"%="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_ADD_ASSIGN(self,t):
    r"\+="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_SUB_ASSIGN(self,t):
    r"-="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_LEFT_ASSIGN(self,t):
    r"<<="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_RIGHT_ASSIGN(self,t):
    r">>="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_AND_ASSIGN(self,t):
    r"&="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_XOR_ASSIGN(self,t):
    r"\^="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_OR_ASSIGN(self,t):
    r"\|="
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_ELLIPSIS(self,t):
    r"\.\.\."
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_COMMENT(self,t):
    r'//(?s).*?\n|/\*(?s).*?\*/'
    #print("COMMENT")

  def t_IDENTIFIER(self, t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    if t.value in reserved:
      t.type = reserved[t.value]
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  # Ignore the spaces and tabs -- comments
  t_ignore = ' \t'

  # Define a rule so we can track line numbers
  def t_newline(self, t):
    r'\n+'
    print "NEW LINE"
    self.lines.append(t.lexer.lexpos)
    t.lexer.lineno += len(t.value)
    #self.lexer.lexpos = 1
    if self.logtokens and self.source != "":
      #self.source += "\n"
      self.log.info("tokens : " + self.tokens)
      self.log.info("source : " + self.source)
      self.tokens += "\n"
      self.tokenlog.write("/*"+self.source + "*/\n")
      self.tokenlog.write(self.tokens)

      self.source = ""
      self.tokens = ""
    self.log.info("==============================Completed LINE NUMBER: " + str(t.lexer.lineno-1) + "======================")
    self.log.info("==============================Starting    LINE NUMBER: " + str(t.lexer.lineno) + "======================")
  # Lex Error message
  def t_error(self,t):
    
    return ""
  def t_requal(self,t):
    r'='
    t.type = '='
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_rstar(self,t):
    r'\*'
    print "STAR"
    t.type = "*"
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_rexclaim(self,t):
    r"!"
    t.type = "!"
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_rquestion(self,t):
    r'\?'
    t.type = "?"
    if self.logtokens:
        self.logging(t.type,t.value)
    return t

  def t_rplus(self,t):
    r"\+"
    t.type = "+"
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_rminus(self,t):
    r"-"
    t.type = "-"
    if self.logtokens:
      self.logging(t.type, t.value)
    return t

  def t_rand(self,t):
    r"&"
    t.type = "&"
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_rdot(self,t):
    r'\.'
    t.type = "."
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_rcolon(self,t):
    r":"
    t.type = ":"
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_lbrack(self,t):
    r"\["
    t.type = "["
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_rbrack(self,t):
    r"]"
    t.type = "]"
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_rcomma(self,t):
    r","
    t.type = ","
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_OPENBRACK(self,t):
    r'{'
    
    #print('PUSH ONTO STACK')

    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  	
  def t_CLOSEBRACK(self,t):
    r'}'
    
    #print('POP OFF STACK')
    if self.logtokens:
      self.logging(t.type,t.value)
    return t

  def t_SEMI(self,t):
    r'\;'
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_OPENPARAN(self,t):
    r'\('
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t
  def t_CLOSEPARAN(self,t):
    r'\)'
    
    if self.logtokens:
      self.logging(t.type,t.value)
    return t 
