from ply import lex 

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
            'while' : 'WHILE'}


class Scanner():
  tokens = ['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', 'SIZEOF', 'PTR_OP', 'INC_OP', 'DEC_OP', 'LEFT_OP', 
            'RIGHT_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP', 'AND_OP', 'OR_OP', 'MUL_ASSIGN', 'DIV_ASSIGN', 
            'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN', 
            'XOR_ASSIGN', 'OR_ASSIGN', 'TYPE_NAME', 'TYPEDEF', 'EXTERN', 'STATIC', 'AUTO', 'REGISTER', 
            'CHAR', 'SHORT', 'INT', 'LONG', 'SIGNED', 'UNSIGNED', 'FLOAT', 'DOUBLE', 'CONST', 'VOLATILE', 
            'VOID', 'STRUCT', 'UNION', 'ENUM', 'ELLIPSIS', 'CASE', 'DEFAULT', 'IF', 'ELSE', 'SWITCH', 
            'WHILE', 'DO', 'FOR', 'GOTO', 'CONTINUE', 'BREAK', 'RETURN']

  precedence =  []

  def __init__(self, data):
    # print kw.get("file", 0)
    self.lexer = lex.lex(module=self)

    # Give the lexer some input
    self.lexer.input(data)

  def run(self):
    pass

  def test_running(self):
    while True:
      tok = self.lexer.token()
      if not tok: 
          break      # No more input
      print(tok)


  t_IDENTIFIER = r".+"
  t_CONSTANT = r".+"
  t_STRING_LITERAL = r".+"
  t_SIZEOF = r".+"
  t_PTR_OP = r".+"
  t_INC_OP = r".+"
  t_DEC_OP = r".+"
  t_LEFT_OP = r".+"
  t_RIGHT_OP = r".+"
  t_LE_OP = r".+"
  t_GE_OP = r".+"
  t_EQ_OP = r".+"
  t_NE_OP = r".+"
  t_AND_OP = r".+"
  t_OR_OP = r".+"
  t_MUL_ASSIGN = r".+"
  t_DIV_ASSIGN = r".+"
  t_MOD_ASSIGN = r".+"
  t_ADD_ASSIGN = r".+"
  t_SUB_ASSIGN = r".+"
  t_LEFT_ASSIGN = r".+"
  t_RIGHT_ASSIGN = r".+"
  t_AND_ASSIGN = r".+"
  t_XOR_ASSIGN = r".+"
  t_OR_ASSIGN = r".+"
  t_TYPE_NAME = r".+"
  t_TYPEDEF = r".+"
  t_EXTERN = r".+"
  t_STATIC = r".+"
  t_AUTO = r".+"
  t_REGISTER = r".+"
  t_CHAR = r".+"
  t_SHORT = r".+"
  t_INT = r".+"
  t_LONG = r".+"
  t_SIGNED = r".+"
  t_UNSIGNED = r".+"
  t_FLOAT = r".+"
  t_DOUBLE = r".+"
  t_CONST = r".+"
  t_VOLATILE = r".+"
  t_VOID = r".+"
  t_STRUCT = r".+"
  t_UNION = r".+"
  t_ENUM = r".+"
  t_ELLIPSIS = r".+"
  t_CASE = r".+"
  t_DEFAULT = r".+"
  t_IF = r".+"
  t_ELSE = r".+"
  t_SWITCH = r".+"
  t_WHILE = r".+"
  t_DO = r".+"
  t_FOR = ".+"
  t_GOTO = r".+"
  t_CONTINUE = r".+"
  t_BREAK = r".+"
  t_RETURN = r".+"

  t_ignore = " \t"

  # Define a rule so we can track line numbers
  def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += len(t.value)

  def t_error(self,t):
    return ""

