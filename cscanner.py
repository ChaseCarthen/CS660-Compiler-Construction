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
            'WHILE', 'DO', 'FOR', 'GOTO', 'CONTINUE', 'BREAK', 'RETURN','OPENBRACK','CLOSEBRACK','SEMI','OPENPARAN','CLOSEPARAN']

  precedence =  []
  literals = ['=',']','[','&','+','-','.','?','!',',',':','\'']
  def __init__(self, data):
    # print kw.get("file", 0)
    self.lexer = lex.lex(module=self,debug=1)

    # Give the lexer some input
    # self.lexer.input(data)
    self.input_data = data

    self.yacc = yacc.yacc(module=self,debug=1)

  def run(self):
    self.yacc.parse(self.input_data)

  def test_running(self):
    while True:
      tok = self.lexer.token()
      if not tok: 
          break      # No more input
      print(tok)


  
  t_CONSTANT = r"[0-9]+|[0-9]*\.[0-9]" # add hexadecimal
  t_STRING_LITERAL = r'\"(?s).*\"|\'.(?s)*\''
  t_SIZEOF = r"SIZEOF"
  t_PTR_OP = r"\*"
  t_INC_OP = r"\+\+"
  t_DEC_OP = r"--"
  t_LEFT_OP = r"<<"
  t_RIGHT_OP = r">>"
  t_LE_OP = r"<="
  t_GE_OP = r">="
  t_EQ_OP = r"=="
  t_NE_OP = r"!="
  t_AND_OP = r"&"
  t_OR_OP = r"\|\|"
  t_MUL_ASSIGN = r"\*"
  t_DIV_ASSIGN = r"/"
  t_MOD_ASSIGN = r"%"
  t_ADD_ASSIGN = r"\+="
  t_SUB_ASSIGN = r"-="
  t_LEFT_ASSIGN = r"<<="
  t_RIGHT_ASSIGN = r">>="
  t_AND_ASSIGN = r"&="
  t_XOR_ASSIGN = r"\^="
  t_OR_ASSIGN = r"\|="
  t_ELLIPSIS = r"\.\.\."

  def t_IDENTIFIER(self, t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
      t.type = reserved[t.value]
    return t

  # Ignore the spaces and tabs
  t_ignore = " \t"

  # Define a rule so we can track line numbers
  def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += len(t.value)

  # Lex Error message
  def t_error(self,t):
    return ""

  def t_OPENBRACK(self,t):
  	r'{'
  	print('PUSH ONTO STACK')
  	return t
  	
  def t_CLOSEBRACK(self,t):
  	r'}'
  	print('POP OFF STACK')
  	return t

  def t_SEMI(self,t):
  	r'\;'
  	return t
  def t_OPENPARAN(self,t):
  	r'\('
  	return t
  def t_CLOSEPARAN(self,t):
  	r'\)'
  	return t 
