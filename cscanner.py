from ply import lex
from ply import yacc

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
  literals = ['=',']','[','&','+','-','.','?','!',',',':','\'']
  def __init__(self, data):
    # print kw.get("file", 0)
    self.lexer = lex.lex(module=self,debug=1)

    # Give the lexer some input
    # self.lexer.input(data)
    self.input_data = data

    self.yacc = yacc.yacc(module=self,debug=1)
    self.charcount = 0
    self.logtokens = False
    self.source = ""
    self.tokens = ""

  def log_tokens(self, txt):
    self.logtokens = True
    self.tokenlog = open(txt,'wa')

  def run(self):
    self.yacc.parse(self.input_data)
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
  
  def t_CONSTANT(self,t):
    r"[0-9]+|[0-9]*\.[0-9]" # add hexadecimal
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_STRING_LITERAL(self,t):
    r'\"(?s).*\"|\'.(?s)*\''
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_SIZEOF(self,t):
    r"SIZEOF"
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_PTR_OP(self,t):
    r"\*"
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_INC_OP(self,t):
    r"\+\+"
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_DEC_OP(self,t):
    r"--"
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_LEFT_OP(self,t):
    r"<<"
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_RIGHT_OP(self,t):
    r">>"
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_LE_OP(self,t):
    r"<="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_GE_OP(self,t):
    r">="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_EQ_OP(self,t):
    r"=="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_NE_OP(self,t): 
    r"!="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_AND_OP(self,t):
    r"&"
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_OR_OP(self,t):
    r"\|\|"
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_MUL_ASSIGN(self,t):
    r"\*="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t


  def t_DIV_ASSIGN(self,t):
    r"/="


    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_MOD_ASSIGN(self,t):
    r"%="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_ADD_ASSIGN(self,t):
    r"\+="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_SUB_ASSIGN(self,t):
    r"-="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_LEFT_ASSIGN(self,t):
    r"<<="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_RIGHT_ASSIGN(self,t):
    r">>="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_AND_ASSIGN(self,t):
    r"&="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_XOR_ASSIGN(self,t):
    r"\^="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_OR_ASSIGN(self,t):
    r"\|="
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_ELLIPSIS(self,t):
    r"\.\.\."
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_COMMENT(self,t):
    r'//(?s).*?\n|/\*(?s).*\?*/'
    #print("COMMENT")

  def t_IDENTIFIER(self, t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    if t.value in reserved:
      t.type = reserved[t.value]
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  # Ignore the spaces and tabs -- comments
  t_ignore = r' \t'

  # Define a rule so we can track line numbers
  def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    #self.lexer.lexpos = 1
    if self.logtokens and self.source != "":
      #self.source += "\n"
      self.tokens += "\n"
      self.tokenlog.write("/*"+self.source + "*/\n")
      self.tokenlog.write(self.tokens)
      self.source = ""
      self.tokens = ""
  # Lex Error message
  def t_error(self,t):
    
    return ""

  def t_OPENBRACK(self,t):
    r'{'
    
    #print('PUSH ONTO STACK')
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  	
  def t_CLOSEBRACK(self,t):
    r'}'
    
    #print('POP OFF STACK')
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t

  def t_SEMI(self,t):
    r'\;'
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_OPENPARAN(self,t):
    r'\('
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t
  def t_CLOSEPARAN(self,t):
    r'\)'
    
    if self.logtokens:
      self.source += t.value + " " 
      self.tokens += t.type + " "
    return t 
