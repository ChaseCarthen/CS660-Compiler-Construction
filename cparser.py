start = 'translation_unit'


# -------------- RULES ----------------

def p_primary_expression_1(p):
    '''primary_expression : IDENTIFIER'''

def p_primary_expression_2(p):
    '''primary_expression : CONSTANT'''

def p_primary_expression_3(p):
    '''primary_expression : STRING_LITERAL'''

def p_primary_expression_4(p):
    '''primary_expression : OPENPARAN expression CLOSEPARAN'''

def p_postfix_expression_1(p):
    '''postfix_expression : primary_expression'''

def p_postfix_expression_2(p):
    '''postfix_expression : postfix_expression '[' expression ']'''

def p_postfix_expression_3(p):
    '''postfix_expression : postfix_expression OPENPARAN CLOSEPARAN'''

def p_postfix_expression_4(p):
    '''postfix_expression : postfix_expression OPENPARAN argument_expression_list CLOSEPARAN'''

def p_postfix_expression_5(p):
    '''postfix_expression : postfix_expression '.' IDENTIFIER'''

def p_postfix_expression_6(p):
    '''postfix_expression : postfix_expression PTR_OP IDENTIFIER'''

def p_postfix_expression_7(p):
    '''postfix_expression : postfix_expression INC_OP'''

def p_postfix_expression_8(p):
    '''postfix_expression : postfix_expression DEC_OP'''

def p_argument_expression_list_1(p):
    '''argument_expression_list : assignment_expression'''

def p_argument_expression_list_2(p):
    '''argument_expression_list : argument_expression_list ',' assignment_expression'''

def p_unary_expression_1(p):
    '''unary_expression : postfix_expression'''

def p_unary_expression_2(p):
    '''unary_expression : INC_OP unary_expression'''

def p_unary_expression_3(p):
    '''unary_expression : DEC_OP unary_expression'''

def p_unary_expression_4(p):
    '''unary_expression : unary_operator cast_expression'''

def p_unary_expression_5(p):
    '''unary_expression : SIZEOF unary_expression'''

def p_unary_expression_6(p):
    '''unary_expression : SIZEOF OPENPARAN type_name CLOSEPARAN'''

def p_unary_operator_1(p):
    '''unary_operator : '&'''

def p_unary_operator_2(p):
    '''unary_operator : '*'''

def p_unary_operator_3(p):
    '''unary_operator : '+'''

def p_unary_operator_4(p):
    '''unary_operator : '-'''

def p_unary_operator_5(p):
    '''unary_operator : '~'''

def p_unary_operator_6(p):
    '''unary_operator : '!'''

def p_cast_expression_1(p):
    '''cast_expression : unary_expression'''

def p_cast_expression_2(p):
    '''cast_expression : OPENPARAN type_name CLOSEPARAN cast_expression'''

def p_multiplicative_expression_1(p):
    '''multiplicative_expression : cast_expression'''

def p_multiplicative_expression_2(p):
    '''multiplicative_expression : multiplicative_expression '*' cast_expression'''

def p_multiplicative_expression_3(p):
    '''multiplicative_expression : multiplicative_expression '/' cast_expression'''

def p_multiplicative_expression_4(p):
    '''multiplicative_expression : multiplicative_expression '%' cast_expression'''

def p_additive_expression_1(p):
    '''additive_expression : multiplicative_expression'''

def p_additive_expression_2(p):
    '''additive_expression : additive_expression '+' multiplicative_expression'''

def p_additive_expression_3(p):
    '''additive_expression : additive_expression '-' multiplicative_expression'''

def p_shift_expression_1(p):
    '''shift_expression : additive_expression'''

def p_shift_expression_2(p):
    '''shift_expression : shift_expression LEFT_OP additive_expression'''

def p_shift_expression_3(p):
    '''shift_expression : shift_expression RIGHT_OP additive_expression'''

def p_relational_expression_1(p):
    '''relational_expression : shift_expression'''

def p_relational_expression_2(p):
    '''relational_expression : relational_expression '<' shift_expression'''

def p_relational_expression_3(p):
    '''relational_expression : relational_expression '>' shift_expression'''

def p_relational_expression_4(p):
    '''relational_expression : relational_expression LE_OP shift_expression'''

def p_relational_expression_5(p):
    '''relational_expression : relational_expression GE_OP shift_expression'''

def p_equality_expression_1(p):
    '''equality_expression : relational_expression'''

def p_equality_expression_2(p):
    '''equality_expression : equality_expression EQ_OP relational_expression'''

def p_equality_expression_3(p):
    '''equality_expression : equality_expression NE_OP relational_expression'''

def p_and_expression_1(p):
    '''and_expression : equality_expression'''

def p_and_expression_2(p):
    '''and_expression : and_expression '&' equality_expression'''

def p_exclusive_or_expression_1(p):
    '''exclusive_or_expression : and_expression'''

def p_exclusive_or_expression_2(p):
    '''exclusive_or_expression : exclusive_or_expression '^' and_expression'''

def p_inclusive_or_expression_1(p):
    '''inclusive_or_expression : exclusive_or_expression'''

def p_inclusive_or_expression_2(p):
    '''inclusive_or_expression : inclusive_or_expression '|' exclusive_or_expression'''

def p_logical_and_expression_1(p):
    '''logical_and_expression : inclusive_or_expression'''

def p_logical_and_expression_2(p):
    '''logical_and_expression : logical_and_expression AND_OP inclusive_or_expression'''

def p_logical_or_expression_1(p):
    '''logical_or_expression : logical_and_expression'''

def p_logical_or_expression_2(p):
    '''logical_or_expression : logical_or_expression OR_OP logical_and_expression'''

def p_conditional_expression_1(p):
    '''conditional_expression : logical_or_expression'''

def p_conditional_expression_2(p):
    '''conditional_expression : logical_or_expression '?' expression ':' conditional_expression'''

def p_assignment_expression_1(p):
    '''assignment_expression : conditional_expression'''

def p_assignment_expression_2(p):
    '''assignment_expression : unary_expression assignment_operator assignment_expression'''

def p_assignment_operator_1(p):
    '''assignment_operator : '='''

def p_assignment_operator_2(p):
    '''assignment_operator : MUL_ASSIGN'''

def p_assignment_operator_3(p):
    '''assignment_operator : DIV_ASSIGN'''

def p_assignment_operator_4(p):
    '''assignment_operator : MOD_ASSIGN'''

def p_assignment_operator_5(p):
    '''assignment_operator : ADD_ASSIGN'''

def p_assignment_operator_6(p):
    '''assignment_operator : SUB_ASSIGN'''

def p_assignment_operator_7(p):
    '''assignment_operator : LEFT_ASSIGN'''

def p_assignment_operator_8(p):
    '''assignment_operator : RIGHT_ASSIGN'''

def p_assignment_operator_9(p):
    '''assignment_operator : AND_ASSIGN'''

def p_assignment_operator_10(p):
    '''assignment_operator : XOR_ASSIGN'''

def p_assignment_operator_11(p):
    '''assignment_operator : OR_ASSIGN'''

def p_expression_1(p):
    '''expression : assignment_expression'''

def p_expression_2(p):
    '''expression : expression ',' assignment_expression'''

def p_constant_expression_1(p):
    '''constant_expression : conditional_expression'''

def p_declaration_1(p):
    '''declaration : declaration_specifiers SEMI'''

def p_declaration_2(p):
    '''declaration : declaration_specifiers init_declarator_list SEMI'''

def p_declaration_specifiers_1(p):
    '''declaration_specifiers : storage_class_specifier'''

def p_declaration_specifiers_2(p):
    '''declaration_specifiers : storage_class_specifier declaration_specifiers'''

def p_declaration_specifiers_3(p):
    '''declaration_specifiers : type_specifier'''

def p_declaration_specifiers_4(p):
    '''declaration_specifiers : type_specifier declaration_specifiers'''

def p_declaration_specifiers_5(p):
    '''declaration_specifiers : type_qualifier'''

def p_declaration_specifiers_6(p):
    '''declaration_specifiers : type_qualifier declaration_specifiers'''

def p_init_declarator_list_1(p):
    '''init_declarator_list : init_declarator'''

def p_init_declarator_list_2(p):
    '''init_declarator_list : init_declarator_list ',' init_declarator'''

def p_init_declarator_1(p):
    '''init_declarator : declarator'''

def p_init_declarator_2(p):
    '''init_declarator : declarator '=' initializer'''

def p_storage_class_specifier_1(p):
    '''storage_class_specifier : TYPEDEF'''

def p_storage_class_specifier_2(p):
    '''storage_class_specifier : EXTERN'''

def p_storage_class_specifier_3(p):
    '''storage_class_specifier : STATIC'''

def p_storage_class_specifier_4(p):
    '''storage_class_specifier : AUTO'''

def p_storage_class_specifier_5(p):
    '''storage_class_specifier : REGISTER'''

def p_type_specifier_1(p):
    '''type_specifier : VOID'''

def p_type_specifier_2(p):
    '''type_specifier : CHAR'''

def p_type_specifier_3(p):
    '''type_specifier : SHORT'''

def p_type_specifier_4(p):
    '''type_specifier : INT'''

def p_type_specifier_5(p):
    '''type_specifier : LONG'''

def p_type_specifier_6(p):
    '''type_specifier : FLOAT'''

def p_type_specifier_7(p):
    '''type_specifier : DOUBLE'''

def p_type_specifier_8(p):
    '''type_specifier : SIGNED'''

def p_type_specifier_9(p):
    '''type_specifier : UNSIGNED'''

def p_type_specifier_10(p):
    '''type_specifier : struct_or_union_specifier'''

def p_type_specifier_11(p):
    '''type_specifier : enum_specifier'''

def p_type_specifier_12(p):
    '''type_specifier : TYPE_NAME'''

def p_struct_or_union_specifier_1(p):
    '''struct_or_union_specifier : struct_or_union IDENTIFIER OPENBRACK struct_declaration_list CLOSEBRACK'''

def p_struct_or_union_specifier_2(p):
    '''struct_or_union_specifier : struct_or_union OPENBRACK struct_declaration_list CLOSEBRACK'''

def p_struct_or_union_specifier_3(p):
    '''struct_or_union_specifier : struct_or_union IDENTIFIER'''

def p_struct_or_union_1(p):
    '''struct_or_union : STRUCT'''

def p_struct_or_union_2(p):
    '''struct_or_union : UNION'''

def p_struct_declaration_list_1(p):
    '''struct_declaration_list : struct_declaration'''

def p_struct_declaration_list_2(p):
    '''struct_declaration_list : struct_declaration_list struct_declaration'''

def p_struct_declaration_1(p):
    '''struct_declaration : specifier_qualifier_list struct_declarator_list SEMI'''

def p_specifier_qualifier_list_1(p):
    '''specifier_qualifier_list : type_specifier specifier_qualifier_list'''

def p_specifier_qualifier_list_2(p):
    '''specifier_qualifier_list : type_specifier'''

def p_specifier_qualifier_list_3(p):
    '''specifier_qualifier_list : type_qualifier specifier_qualifier_list'''

def p_specifier_qualifier_list_4(p):
    '''specifier_qualifier_list : type_qualifier'''

def p_struct_declarator_list_1(p):
    '''struct_declarator_list : struct_declarator'''

def p_struct_declarator_list_2(p):
    '''struct_declarator_list : struct_declarator_list ',' struct_declarator'''

def p_struct_declarator_1(p):
    '''struct_declarator : declarator'''

def p_struct_declarator_2(p):
    '''struct_declarator : ':' constant_expression'''

def p_struct_declarator_3(p):
    '''struct_declarator : declarator ':' constant_expression'''

def p_enum_specifier_1(p):
    '''enum_specifier : ENUM OPENBRACK enumerator_list CLOSEBRACK'''

def p_enum_specifier_2(p):
    '''enum_specifier : ENUM IDENTIFIER OPENBRACK enumerator_list CLOSEBRACK'''

def p_enum_specifier_3(p):
    '''enum_specifier : ENUM IDENTIFIER'''

def p_enumerator_list_1(p):
    '''enumerator_list : enumerator'''

def p_enumerator_list_2(p):
    '''enumerator_list : enumerator_list ',' enumerator'''

def p_enumerator_1(p):
    '''enumerator : IDENTIFIER'''

def p_enumerator_2(p):
    '''enumerator : IDENTIFIER '=' constant_expression'''

def p_type_qualifier_1(p):
    '''type_qualifier : CONST'''

def p_type_qualifier_2(p):
    '''type_qualifier : VOLATILE'''

def p_declarator_1(p):
    '''declarator : pointer direct_declarator'''

def p_declarator_2(p):
    '''declarator : direct_declarator'''

def p_direct_declarator_1(p):
    '''direct_declarator : IDENTIFIER'''

def p_direct_declarator_2(p):
    '''direct_declarator : OPENPARAN declarator CLOSEPARAN'''

def p_direct_declarator_3(p):
    '''direct_declarator : direct_declarator '[' constant_expression ']'''

def p_direct_declarator_4(p):
    '''direct_declarator : direct_declarator '[' ']'''

def p_direct_declarator_5(p):
    '''direct_declarator : direct_declarator OPENPARAN parameter_type_list CLOSEPARAN'''

def p_direct_declarator_6(p):
    '''direct_declarator : direct_declarator OPENPARAN identifier_list CLOSEPARAN'''

def p_direct_declarator_7(p):
    '''direct_declarator : direct_declarator OPENPARAN CLOSEPARAN''

def p_pointer_1(p):
    '''pointer : '*'''

def p_pointer_2(p):
    '''pointer : '*' type_qualifier_list'''

def p_pointer_3(p):
    '''pointer : '*' pointer'''

def p_pointer_4(p):
    '''pointer : '*' type_qualifier_list pointer'''

def p_type_qualifier_list_1(p):
    '''type_qualifier_list : type_qualifier'''

def p_type_qualifier_list_2(p):
    '''type_qualifier_list : type_qualifier_list type_qualifier'''

def p_parameter_type_list_1(p):
    '''parameter_type_list : parameter_list'''

def p_parameter_type_list_2(p):
    '''parameter_type_list : parameter_list ',' ELLIPSIS'''

def p_parameter_list_1(p):
    '''parameter_list : parameter_declaration'''

def p_parameter_list_2(p):
    '''parameter_list : parameter_list ',' parameter_declaration'''

def p_parameter_declaration_1(p):
    '''parameter_declaration : declaration_specifiers declarator'''

def p_parameter_declaration_2(p):
    '''parameter_declaration : declaration_specifiers abstract_declarator'''

def p_parameter_declaration_3(p):
    '''parameter_declaration : declaration_specifiers'''

def p_identifier_list_1(p):
    '''identifier_list : IDENTIFIER'''

def p_identifier_list_2(p):
    '''identifier_list : identifier_list ',' IDENTIFIER'''

def p_type_name_1(p):
    '''type_name : specifier_qualifier_list'''

def p_type_name_2(p):
    '''type_name : specifier_qualifier_list abstract_declarator'''

def p_abstract_declarator_1(p):
    '''abstract_declarator : pointer'''

def p_abstract_declarator_2(p):
    '''abstract_declarator : direct_abstract_declarator'''

def p_abstract_declarator_3(p):
    '''abstract_declarator : pointer direct_abstract_declarator'''

def p_direct_abstract_declarator_1(p):
    '''direct_abstract_declarator : OPENPARAN abstract_declarator CLOSEPARAN''

def p_direct_abstract_declarator_2(p):
    '''direct_abstract_declarator : '[' ']'''

def p_direct_abstract_declarator_3(p):
    '''direct_abstract_declarator : '[' constant_expression ']'''

def p_direct_abstract_declarator_4(p):
    '''direct_abstract_declarator : direct_abstract_declarator '[' ']'''

def p_direct_abstract_declarator_5(p):
    '''direct_abstract_declarator : direct_abstract_declarator '[' constant_expression ']'''

def p_direct_abstract_declarator_6(p):
    '''direct_abstract_declarator : OPENPARAN CLOSEPARAN''

def p_direct_abstract_declarator_7(p):
    '''direct_abstract_declarator : OPENPARAN parameter_type_list CLOSEPARAN''

def p_direct_abstract_declarator_8(p):
    '''direct_abstract_declarator : direct_abstract_declarator OPENPARAN CLOSEPARAN''

def p_direct_abstract_declarator_9(p):
    '''direct_abstract_declarator : direct_abstract_declarator OPENPARAN parameter_type_list CLOSEPARAN''

def p_initializer_1(p):
    '''initializer : assignment_expression'''

def p_initializer_2(p):
    '''initializer : OPENBRACK initializer_list CLOSEBRACK''

def p_initializer_3(p):
    '''initializer : OPENBRACK initializer_list ',' CLOSEBRACK''

def p_initializer_list_1(p):
    '''initializer_list : initializer'''

def p_initializer_list_2(p):
    '''initializer_list : initializer_list ',' initializer'''

def p_statement_1(p):
    '''statement : labeled_statement'''

def p_statement_2(p):
    '''statement : compound_statement'''

def p_statement_3(p):
    '''statement : expression_statement'''

def p_statement_4(p):
    '''statement : selection_statement'''

def p_statement_5(p):
    '''statement : iteration_statement'''

def p_statement_6(p):
    '''statement : jump_statement'''

def p_labeled_statement_1(p):
    '''labeled_statement : IDENTIFIER ':' statement'''

def p_labeled_statement_2(p):
    '''labeled_statement : CASE constant_expression ':' statement'''

def p_labeled_statement_3(p):
    '''labeled_statement : DEFAULT ':' statement'''

def p_compound_statement_1(p):
    '''compound_statement : OPENBRACK CLOSEBRACK''

def p_compound_statement_2(p):
    '''compound_statement : OPENBRACK statement_list CLOSEBRACK''

def p_compound_statement_3(p):
    '''compound_statement : OPENBRACK declaration_list CLOSEBRACK''

def p_compound_statement_4(p):
    '''compound_statement : OPENBRACK declaration_list statement_list CLOSEBRACK''

def p_declaration_list_1(p):
    '''declaration_list : declaration'''

def p_declaration_list_2(p):
    '''declaration_list : declaration_list declaration'''

def p_statement_list_1(p):
    '''statement_list : statement'''

def p_statement_list_2(p):
    '''statement_list : statement_list statement'''

def p_expression_statement_1(p):
    '''expression_statement : SEMI''

def p_expression_statement_2(p):
    '''expression_statement : expression SEMI''

def p_selection_statement_1(p):
    '''selection_statement : IF OPENPARAN expression CLOSEPARAN statement'''

def p_selection_statement_2(p):
    '''selection_statement : IF OPENPARAN expression CLOSEPARAN statement ELSE statement'''

def p_selection_statement_3(p):
    '''selection_statement : SWITCH OPENPARAN expression CLOSEPARAN statement'''

def p_iteration_statement_1(p):
    '''iteration_statement : WHILE OPENPARAN expression CLOSEPARAN statement'''

def p_iteration_statement_2(p):
    '''iteration_statement : DO statement WHILE OPENPARAN expression CLOSEPARAN SEMI''

def p_iteration_statement_3(p):
    '''iteration_statement : FOR OPENPARAN expression_statement expression_statement CLOSEPARAN statement'''

def p_iteration_statement_4(p):
    '''iteration_statement : FOR OPENPARAN expression_statement expression_statement expression CLOSEPARAN statement'''

def p_jump_statement_1(p):
    '''jump_statement : GOTO IDENTIFIER SEMI''

def p_jump_statement_2(p):
    '''jump_statement : CONTINUE SEMI''

def p_jump_statement_3(p):
    '''jump_statement : BREAK SEMI''

def p_jump_statement_4(p):
    '''jump_statement : RETURN SEMI''

def p_jump_statement_5(p):
    '''jump_statement : RETURN expression SEMI''

def p_translation_unit_1(p):
    '''translation_unit : external_declaration'''

def p_translation_unit_2(p):
    '''translation_unit : translation_unit external_declaration'''

def p_external_declaration_1(p):
    '''external_declaration : function_definition'''

def p_external_declaration_2(p):
    '''external_declaration : declaration'''

def p_function_definition_1(p):
    '''function_definition : declaration_specifiers declarator declaration_list compound_statement'''

def p_function_definition_2(p):
    '''function_definition : declaration_specifiers declarator compound_statement'''

def p_function_definition_3(p):
    '''function_definition : declarator declaration_list compound_statement'''

def p_function_definition_4(p):
    '''function_definition : declarator compound_statement'''

# -------------- RULES END ----------------
# 
# #include <stdio.h>
# 
# extern char yytext[];
# extern int column;
# 
# yyerror(s)
# char *s;
# {
# 	fflush(stdout);
# 	printf("\n%*s\n%*s\n", column, "^", column, s);
# }

if __name__ == '__main__':
    from ply import *
    yacc.yacc()

