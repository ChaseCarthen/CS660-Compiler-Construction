from ply import lex
from ply import yacc
import logging
from symboltable import SymbolTable
import os

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
            'float' : 'FLOAT', 'union' : 'UNION', 'for' : 'FOR', 'unsigned' : 'UNSIGNED', 'goto' : 'GOTO', 
            'while' : 'WHILE', 'const' : 'CONST', 'void' : 'VOID', 'enum':'ENUM', 'signed' : 'SIGNED','volatile' : 'VOLATILE'}


class Scanner():
  tokens = ['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', 'SIZEOF', 'PTR_OP', 'INC_OP', 'DEC_OP', 'LEFT_OP', 
            'RIGHT_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP', 'AND_OP', 'OR_OP', 'MUL_ASSIGN', 'DIV_ASSIGN', 
            'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN', 
            'XOR_ASSIGN', 'OR_ASSIGN', 'TYPEDEF', 'EXTERN', 'STATIC', 'AUTO', 'REGISTER', 
            'CHAR', 'SHORT', 'INT', 'LONG', 'SIGNED', 'UNSIGNED', 'FLOAT', 'DOUBLE', 'CONST', 'VOLATILE', 
            'VOID', 'STRUCT', 'UNION', 'ENUM', 'ELLIPSIS', 'CASE', 'DEFAULT', 'IF', 'ELSE', 'SWITCH', 
            'WHILE', 'DO', 'FOR', 'GOTO', 'CONTINUE', 'BREAK', 'RETURN','OPENBRACK','CLOSEBRACK','SEMI','OPENPARAN','CLOSEPARAN', 'COMMENT','DUMPSYMBOL']

  precedence =  []
  literals = ['=',']','[','&','+','-','.','?','!',',',':','*','<','>','^','|','%']
  def __init__(self,data,parselog,parsefile,tokenfile):
    
    # To enable a more verbose logger -- this is so we can see all of the production that were taken in the grammar.
    self.parselog = parselog

    # set up the logger to log info... We added a flag for when not to output this info
    if self.parselog:
      logging.basicConfig(
        level = logging.INFO,
        filename = parsefile,
        filemode = "w",
        format = "%(filename)10s:%(lineno)4d:%(message)s"
      )

      # We need to make some kind of error logger.

      log = self.log = logging.getLogger()


    
    if self.parselog:
      self.lexer = lex.lex(module=self,debuglog=log)#,debug=True)
    else:
      self.lexer = lex.lex(module=self)

    # Give the lexer some input
    # self.lexer.input(data)
    self.input_data = data



    if self.parselog:
      self.yacc = yacc.yacc(module=self,debuglog=log)#,debug=True)
    else:
      self.yacc = yacc.yacc(module=self)



    self.source = "" # this will keep track of what source we have seen so far
    self.tokens = ""  # this will keep track the tokens that we have seen so far
    self.reduction_list = [] # this will keep track of what tokens we have acquired
    self.typelist = []

    # our token log file
    self.log_tokens(tokenfile)

    # The symbol table
    self.symbol_table = SymbolTable()

    # Keeps track of the beginnings of lines this so we can make nice errors like fff< void main().
    self.lines = [0]
    for i in data.split('\n'):
      self.lines.append(self.lines[-1]+len(i)+1)

  def logging(self,typed,value):
      self.source += value + " " 
      self.tokens += typed + " "
      if self.parselog:
        self.log.info("Line Number: " + str(self.lexer.lineno) + " Token: " + str(typed) + " Value: " + str(value))

  def loginfo(self,string):
    if self.parselog:
      self.log.info(string)

  def set_symbol_table(self,sym):
    self.symbol_table = sym

  def log_tokens(self, txt):
    self.logtokens = True
    self.tokenlog = open(txt,'wa')

  def run(self):
    self.loginfo("==============================Starting    LINE NUMBER: " + str(1) + "======================")
    if self.parselog:
      self.yacc.parse(self.input_data,debug=self.log)
    else:
      self.yacc.parse(self.input_data)

  def scan(self,string):
    self.lexer.input(string)
    i = 0
    while os.path.exists("token%s.txt" % i):
      i += 1
    path = "token%s.txt" % i
    self.log_tokens(path)
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
    self.logging(t.type,t.value)
    return t

  def t_CONSTANT(self,t):
    r"(0[xX][a-fA-F0-9]+(u|U|l|L)*?)|0[0-9]+(u|U|l|L)*?|\'(\\.|[^\\\'])\'|[0-9]+[Ee][+-]?[0-9]+(f|F|l|L)?|([0-9]*\.[0-9]+([Ee][+-]?[0-9]+)?(f|F|l|L)?)|([0-9]+((u|U|l|L)*|\.?[0-9]*([Ee][+-]?[0-9]+)?(f|F|l|L)?))" # add hexadecimal
    self.logging(t.type,t.value)
    return t
  # Help from here http://www.lysator.liu.se/c/ANSI-C-grammar-l.html
  # should this second half be a constant for 'somechar'...
  def t_STRING_LITERAL(self,t):
    r'\"(\\.|[^\\\"])*\"'
    self.logging(t.type,t.value)
    return t
  #def t_SIZEOF(self,t):
  #  r"SIZEOF|sizeof"
  #  self.logging(t.type,t.value)
  #  return t

  def t_INC_OP(self,t):
    r"\+\+"
    self.logging(t.type,t.value)
    return t

  def t_DEC_OP(self,t):
    r"--"
    self.logging(t.type,t.value)
    return t

  def t_LEFT_OP(self,t):
    r"<<"
    self.logging(t.type,t.value)
    return t

  def t_RIGHT_OP(self,t):
    r">>"
    self.logging(t.type,t.value)
    return t

  def t_LE_OP(self,t):
    r"<="
    self.logging(t.type,t.value)
    return t

  def t_GE_OP(self,t):
    r">="
    self.logging(t.type,t.value)
    return t

  def t_EQ_OP(self,t):
    r"=="
    self.logging(t.type,t.value)
    return t

  def t_NE_OP(self,t): 
    r"!="
    self.logging(t.type,t.value)
    return t
  def t_AND_OP(self,t):
    r"&&" 
    self.logging(t.type,t.value)
    return t
  def t_OR_OP(self,t):
    r"\|\|"
    self.logging(t.type,t.value)
    return t
  def t_MUL_ASSIGN(self,t):
    r"\*="
    self.logging(t.type,t.value)
    return t

  def t_DIV_ASSIGN(self,t):
    r"/="
    self.logging(t.type,t.value)
    return t
  def t_MOD_ASSIGN(self,t):
    r"%="    
    self.logging(t.type,t.value)
    return t
  def t_ADD_ASSIGN(self,t):
    r"\+="
    self.logging(t.type,t.value)
    return t
  def t_SUB_ASSIGN(self,t):
    r"-="
    self.logging(t.type,t.value)
    return t
  def t_LEFT_ASSIGN(self,t):
    r"<<="
    self.logging(t.type,t.value)
    return t
  def t_RIGHT_ASSIGN(self,t):
    r">>="
    self.logging(t.type,t.value)
    return t
  def t_AND_ASSIGN(self,t):
    r"&=" 
    self.logging(t.type,t.value)
    return t
  def t_XOR_ASSIGN(self,t):
    r"\^="
    self.logging(t.type,t.value)
    return t
  def t_OR_ASSIGN(self,t):
    r"\|="
    self.logging(t.type,t.value)
    return t
  def t_ELLIPSIS(self,t):
    r"\.\.\."
    self.logging(t.type,t.value)
    return t

  def t_COMMENT(self,t):
    r'//(?s).*?\n|/\*(?s).*?\*/'

  def t_IDENTIFIER(self, t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
      t.type = reserved[t.value]
    else:
      typeval = self.symbol_table.CheckForType(t.value)
      if typeval != None:
        t.value = str(typeval)
        t.type = "INT" # Hack to get it through
    self.logging(t.type,t.value)
    return t

  # Ignore the spaces and tabs -- comments
  t_ignore = ' \t'

  # Define a rule so we can track line numbers
  def t_newline(self, t):
    r'\n+'
    
    t.lexer.lineno += len(t.value)

    self.loginfo("tokens : " + self.tokens)
    self.loginfo("source : " + self.source)

    self.tokens += "\n"
    self.tokenlog.write("/*"+self.source + "*/\n")
    self.tokenlog.write(self.tokens)

    self.source = ""
    self.tokens = ""
    self.loginfo("==============================Completed LINE NUMBER: " + str(t.lexer.lineno-1) + "======================")
    self.loginfo("==============================Starting    LINE NUMBER: " + str(t.lexer.lineno) + "======================")

  def highlightstring(self,string,position): 
    if position <= len(string):
      print string
      a = ""
      for i in range(position-1):
        a += ' '
      a += '^'
      print a


  # Lex Error message
  def t_error(self,t):
    print "FOUND LEXICAL ERROR ON LINE: "  + str(t.lineno) + " " + self.lexer.lexdata[t.lexer.lexpos]
    self.highlightstring(self.lexer.lexdata.split('\n')[self.lexer.lineno-1],t.lexer.lexpos-self.lines[self.lexer.lineno-1]+1)
    t.lexer.skip(1)

  def t_requal(self,t):
    r'='
    t.type = '='
    self.logging(t.type,t.value)
    return t
  def t_rstar(self,t):
    r'\*'
    print "STAR"
    t.type = "*"
    self.logging(t.type,t.value)
    return t
  def t_rexclaim(self,t):
    r"!"
    t.type = "!"
    self.logging(t.type,t.value)
    return t
  def t_rquestion(self,t):
    r'\?'
    t.type = "?"
    self.logging(t.type,t.value)
    return t

  def t_rplus(self,t):
    r"\+"
    t.type = "+"
    self.logging(t.type,t.value)
    return t

  def t_rminus(self,t):
    r"-"
    t.type = "-"
    self.logging(t.type, t.value)
    return t

  def t_rand(self,t):
    r"&"
    t.type = "&"
    self.logging(t.type,t.value)
    return t

  def t_rdot(self,t):
    r'\.'
    t.type = "."
    self.logging(t.type,t.value)
    return t
  def t_rcolon(self,t):
    r":"
    t.type = ":"
    self.logging(t.type,t.value)
    return t
  def t_lbrack(self,t):
    r"\["
    t.type = "["
    self.logging(t.type,t.value)
    return t
  def t_rbrack(self,t):
    r"]"
    t.type = "]"
    self.logging(t.type,t.value)
    return t
  def t_rcomma(self,t):
    r","
    t.type = ","
    self.logging(t.type,t.value)
    return t
  def t_le(self,t):
    r"<"
    t.type = "<"
    self.logging(t.type,t.value)
    return t
  def t_ge(self,t):
    r">"
    t.type = ">"
    self.logging(t.type,t.value)
    return t
  def t_pipe(self,t):
    r"\|"
    t.type = "|"
    self.logging(t.type,t.value)
    return t
  def t_modulo(self,t):
    r'%'
    t.type = "%"
    self.logging(t.type,t.value)
    return t
  def t_carrot(self,t): # Bugs Bunny
    r"\^"
    t.type = "^"
    self.logging(t.type,t.value)
    return t
  def t_OPENBRACK(self,t):
    r'{'
    self.logging(t.type,t.value)
    return t
  def t_CLOSEBRACK(self,t):
    r'}'
    #print('POP OFF STACK')
    self.logging(t.type,t.value)
    return t
  def t_SEMI(self,t):
    r'\;'
    self.logging(t.type,t.value)
    return t
  def t_OPENPARAN(self,t):
    r'\('
    self.logging(t.type,t.value)
    return t
  def t_CLOSEPARAN(self,t):
    r'\)'
    self.logging(t.type,t.value)
    return t 
  # Dump symbol is @
  def t_DUMPSYMBOL(self,t):
    r'@'
    self.symbol_table.StackDump()
    self.logging(t.type,t.value)

