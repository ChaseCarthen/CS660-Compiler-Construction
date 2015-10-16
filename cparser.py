from cscanner import Scanner
import sys
start = 'translation_unit'
class Parser(Scanner):
    start = 'translation_unit'
    def p_primary_expression_1(self, p):
        '''primary_expression : IDENTIFIER'''
        print "IDENTIFER"
        p[0] = p[1]
    def p_primary_expression_2(self, p):
        '''primary_expression : CONSTANT'''
        p[0] = p[1]
    def p_primary_expression_3(self, p):
        '''primary_expression : STRING_LITERAL'''

    def p_primary_expression_4(self, p):
        '''primary_expression : OPENPARAN expression CLOSEPARAN'''

    def p_postfix_expression_1(self, p):
        '''postfix_expression : primary_expression'''
        p[0] = p[1]
    def p_postfix_expression_2(self, p):
        '''postfix_expression : postfix_expression '[' expression ']' '''

    def p_postfix_expression_3(self, p):
        '''postfix_expression : postfix_expression OPENPARAN CLOSEPARAN'''

    def p_postfix_expression_4(self, p):
        '''postfix_expression : postfix_expression OPENPARAN argument_expression_list CLOSEPARAN'''

    def p_postfix_expression_5(self, p):
        '''postfix_expression : postfix_expression '.' IDENTIFIER'''

    def p_postfix_expression_6(self, p):
        '''postfix_expression : postfix_expression PTR_OP IDENTIFIER'''

    def p_postfix_expression_7(self, p):
        '''postfix_expression : postfix_expression INC_OP'''

    def p_postfix_expression_8(self, p):
        '''postfix_expression : postfix_expression DEC_OP'''

    def p_argument_expression_list_1(self, p):
        '''argument_expression_list : assignment_expression'''

    def p_argument_expression_list_2(self, p):
        '''argument_expression_list : argument_expression_list ',' assignment_expression'''

    def p_unary_expression_1(self, p):
        '''unary_expression : postfix_expression'''

    def p_unary_expression_2(self, p):
        '''unary_expression : INC_OP unary_expression'''

    def p_unary_expression_3(self, p):
        '''unary_expression : DEC_OP unary_expression'''

    def p_unary_expression_4(self, p):
        '''unary_expression : unary_operator cast_expression'''

    def p_unary_expression_5(self, p):
        '''unary_expression : SIZEOF unary_expression'''

    def p_unary_expression_6(self, p):
        '''unary_expression : SIZEOF OPENPARAN type_name CLOSEPARAN'''

    def p_unary_operator_1(self, p):
        '''unary_operator : '&' '''

    def p_unary_operator_2(self, p):
        '''unary_operator : '*' '''

    def p_unary_operator_3(self, p):
        '''unary_operator : '+' '''

    def p_unary_operator_4(self, p):
        '''unary_operator : '-' '''

    def p_unary_operator_5(self, p):
        '''unary_operator : '~' '''

    def p_unary_operator_6(self, p):
        '''unary_operator : '!' '''

    def p_cast_expression_1(self, p):
        '''cast_expression : unary_expression'''
        print  "Cast expression"
    def p_cast_expression_2(self, p):
        '''cast_expression : OPENPARAN type_name CLOSEPARAN cast_expression'''
        print "Cast expression"
    def p_multiplicative_expression_1(self, p):
        '''multiplicative_expression : cast_expression'''

    def p_multiplicative_expression_2(self, p):
        '''multiplicative_expression : multiplicative_expression '*' cast_expression'''

    def p_multiplicative_expression_3(self, p):
        '''multiplicative_expression : multiplicative_expression '/' cast_expression'''

    def p_multiplicative_expression_4(self, p):
        '''multiplicative_expression : multiplicative_expression '%' cast_expression'''

    def p_additive_expression_1(self, p):
        '''additive_expression : multiplicative_expression'''

    def p_additive_expression_2(self, p):
        '''additive_expression : additive_expression '+' multiplicative_expression'''

    def p_additive_expression_3(self, p):
        '''additive_expression : additive_expression '-' multiplicative_expression'''

    def p_shift_expression_1(self, p):
        '''shift_expression : additive_expression'''

    def p_shift_expression_2(self, p):
        '''shift_expression : shift_expression LEFT_OP additive_expression'''

    def p_shift_expression_3(self, p):
        '''shift_expression : shift_expression RIGHT_OP additive_expression'''

    def p_relational_expression_1(self, p):
        '''relational_expression : shift_expression'''

    def p_relational_expression_2(self, p):
        '''relational_expression : relational_expression '<' shift_expression'''

    def p_relational_expression_3(self, p):
        '''relational_expression : relational_expression '>' shift_expression'''

    def p_relational_expression_4(self, p):
        '''relational_expression : relational_expression LE_OP shift_expression'''

    def p_relational_expression_5(self, p):
        '''relational_expression : relational_expression GE_OP shift_expression'''

    def p_equality_expression_1(self, p):
        '''equality_expression : relational_expression'''

    def p_equality_expression_2(self, p):
        '''equality_expression : equality_expression EQ_OP relational_expression'''

    def p_equality_expression_3(self, p):
        '''equality_expression : equality_expression NE_OP relational_expression'''

    def p_and_expression_1(self, p):
        '''and_expression : equality_expression'''

    def p_and_expression_2(self, p):
        '''and_expression : and_expression '&' equality_expression'''

    def p_exclusive_or_expression_1(self, p):
        '''exclusive_or_expression : and_expression'''

    def p_exclusive_or_expression_2(self, p):
        '''exclusive_or_expression : exclusive_or_expression '^' and_expression'''

    def p_inclusive_or_expression_1(self, p):
        '''inclusive_or_expression : exclusive_or_expression'''

    def p_inclusive_or_expression_2(self, p):
        '''inclusive_or_expression : inclusive_or_expression '|' exclusive_or_expression'''

    def p_logical_and_expression_1(self, p):
        '''logical_and_expression : inclusive_or_expression'''

    def p_logical_and_expression_2(self, p):
        '''logical_and_expression : logical_and_expression AND_OP inclusive_or_expression'''

    def p_logical_or_expression_1(self, p):
        '''logical_or_expression : logical_and_expression'''

    def p_logical_or_expression_2(self, p):
        '''logical_or_expression : logical_or_expression OR_OP logical_and_expression'''

    def p_conditional_expression_1(self, p):
        '''conditional_expression : logical_or_expression'''

    def p_conditional_expression_2(self, p):
        '''conditional_expression : logical_or_expression '?' expression ':' conditional_expression'''

    def p_assignment_expression_1(self, p):
        '''assignment_expression : conditional_expression'''

    def p_assignment_expression_2(self, p):
        '''assignment_expression : unary_expression assignment_operator assignment_expression'''

    def p_assignment_operator_1(self, p):
        '''assignment_operator : '=' '''

    def p_assignment_operator_2(self, p):
        '''assignment_operator : MUL_ASSIGN'''

    def p_assignment_operator_3(self, p):
        '''assignment_operator : DIV_ASSIGN'''

    def p_assignment_operator_4(self, p):
        '''assignment_operator : MOD_ASSIGN'''

    def p_assignment_operator_5(self, p):
        '''assignment_operator : ADD_ASSIGN'''

    def p_assignment_operator_6(self, p):
        '''assignment_operator : SUB_ASSIGN'''

    def p_assignment_operator_7(self, p):
        '''assignment_operator : LEFT_ASSIGN'''

    def p_assignment_operator_8(self, p):
        '''assignment_operator : RIGHT_ASSIGN'''

    def p_assignment_operator_9(self, p):
        '''assignment_operator : AND_ASSIGN'''

    def p_assignment_operator_10(self, p):
        '''assignment_operator : XOR_ASSIGN'''

    def p_assignment_operator_11(self, p):
        '''assignment_operator : OR_ASSIGN'''

    def p_expression_1(self, p):
        '''expression : assignment_expression'''

    def p_expression_2(self, p):
        '''expression : expression ',' assignment_expression'''

    def p_constant_expression_1(self, p):
        '''constant_expression : conditional_expression'''

    def p_declaration_1(self, p):
        '''declaration : declaration_specifiers SEMI'''

    def p_declaration_2(self, p):
        '''declaration : declaration_specifiers init_declarator_list SEMI'''
        
    def p_declaration_specifiers_1(self, p):
        '''declaration_specifiers : storage_class_specifier'''

    def p_declaration_specifiers_2(self, p):
        '''declaration_specifiers : storage_class_specifier declaration_specifiers'''

    def p_declaration_specifiers_3(self, p):
        '''declaration_specifiers : type_specifier'''
        p[0] = p[1]

    def p_declaration_specifiers_4(self, p):
        '''declaration_specifiers : type_specifier declaration_specifiers'''

    def p_declaration_specifiers_5(self, p):
        '''declaration_specifiers : type_qualifier'''

    def p_declaration_specifiers_6(self, p):
        '''declaration_specifiers : type_qualifier declaration_specifiers'''

    def p_init_declarator_list_1(self, p):
        '''init_declarator_list : init_declarator'''

    def p_init_declarator_list_2(self, p):
        '''init_declarator_list : init_declarator_list ',' init_declarator'''

    def p_init_declarator_1(self, p):
        '''init_declarator : declarator'''

    def p_init_declarator_2(self, p):
        '''init_declarator : declarator '=' initializer'''

    def p_storage_class_specifier_1(self, p):
        '''storage_class_specifier : TYPEDEF'''

    def p_storage_class_specifier_2(self, p):
        '''storage_class_specifier : EXTERN'''

    def p_storage_class_specifier_3(self, p):
        '''storage_class_specifier : STATIC'''

    def p_storage_class_specifier_4(self, p):
        '''storage_class_specifier : AUTO'''

    def p_storage_class_specifier_5(self, p):
        '''storage_class_specifier : REGISTER'''

    def p_type_specifier_1(self, p):
        '''type_specifier : VOID'''
        p[0] = p[1]

    def p_type_specifier_2(self, p):
        '''type_specifier : CHAR'''
        p[0] = p[1]
    def p_type_specifier_3(self, p):
        '''type_specifier : SHORT'''

    def p_type_specifier_4(self, p):
        '''type_specifier : INT'''
        p[0] = p[1]
    def p_type_specifier_5(self, p):
        '''type_specifier : LONG'''

    def p_type_specifier_6(self, p):
        '''type_specifier : FLOAT'''

    def p_type_specifier_7(self, p):
        '''type_specifier : DOUBLE'''

    def p_type_specifier_8(self, p):
        '''type_specifier : SIGNED'''

    def p_type_specifier_9(self, p):
        '''type_specifier : UNSIGNED'''

    def p_type_specifier_10(self, p):
        '''type_specifier : struct_or_union_specifier'''

    def p_type_specifier_11(self, p):
        '''type_specifier : enum_specifier'''

    def p_struct_or_union_specifier_1(self, p):
        '''struct_or_union_specifier : struct_or_union IDENTIFIER OPENBRACK struct_declaration_list CLOSEBRACK'''

    def p_struct_or_union_specifier_2(self, p):
        '''struct_or_union_specifier : struct_or_union OPENBRACK struct_declaration_list CLOSEBRACK'''

    def p_struct_or_union_specifier_3(self, p):
        '''struct_or_union_specifier : struct_or_union IDENTIFIER'''

    def p_struct_or_union_1(self, p):
        '''struct_or_union : STRUCT'''

    def p_struct_or_union_2(self, p):
        '''struct_or_union : UNION'''

    def p_struct_declaration_list_1(self, p):
        '''struct_declaration_list : struct_declaration'''

    def p_struct_declaration_list_2(self, p):
        '''struct_declaration_list : struct_declaration_list struct_declaration'''

    def p_struct_declaration_1(self, p):
        '''struct_declaration : specifier_qualifier_list struct_declarator_list SEMI'''

    def p_specifier_qualifier_list_1(self, p):
        '''specifier_qualifier_list : type_specifier specifier_qualifier_list'''

    def p_specifier_qualifier_list_2(self, p):
        '''specifier_qualifier_list : type_specifier'''

    def p_specifier_qualifier_list_3(self, p):
        '''specifier_qualifier_list : type_qualifier specifier_qualifier_list'''

    def p_specifier_qualifier_list_4(self, p):
        '''specifier_qualifier_list : type_qualifier'''

    def p_struct_declarator_list_1(self, p):
        '''struct_declarator_list : struct_declarator'''

    def p_struct_declarator_list_2(self, p):
        '''struct_declarator_list : struct_declarator_list ',' struct_declarator'''

    def p_struct_declarator_1(self, p):
        '''struct_declarator : declarator'''

    def p_struct_declarator_2(self, p):
        '''struct_declarator : ':' constant_expression'''

    def p_struct_declarator_3(self, p):
        '''struct_declarator : declarator ':' constant_expression'''

    def p_enum_specifier_1(self, p):
        '''enum_specifier : ENUM OPENBRACK enumerator_list CLOSEBRACK'''

    def p_enum_specifier_2(self, p):
        '''enum_specifier : ENUM IDENTIFIER OPENBRACK enumerator_list CLOSEBRACK'''

    def p_enum_specifier_3(self, p):
        '''enum_specifier : ENUM IDENTIFIER'''

    def p_enumerator_list_1(self, p):
        '''enumerator_list : enumerator'''

    def p_enumerator_list_2(self, p):
        '''enumerator_list : enumerator_list ',' enumerator'''

    def p_enumerator_1(self, p):
        '''enumerator : IDENTIFIER'''

    def p_enumerator_2(self, p):
        '''enumerator : IDENTIFIER '=' constant_expression'''

    def p_type_qualifier_1(self, p):
        '''type_qualifier : CONST'''

    def p_type_qualifier_2(self, p):
        '''type_qualifier : VOLATILE'''

    def p_declarator_1(self, p):
        '''declarator : pointer direct_declarator'''

    def p_declarator_2(self, p):
        '''declarator : direct_declarator'''
        p[0] = p[1]

    def p_direct_declarator_1(self, p):
        '''direct_declarator : IDENTIFIER'''
        p[0] = p[1]
        


    def p_direct_declarator_2(self, p):
        '''direct_declarator : OPENPARAN declarator CLOSEPARAN'''

    def p_direct_declarator_3(self, p):
        '''direct_declarator : direct_declarator '[' constant_expression ']' '''

    def p_direct_declarator_4(self, p):
        '''direct_declarator : direct_declarator '[' ']' '''

    def p_direct_declarator_5(self, p):
        '''direct_declarator : direct_declarator OPENPARAN parameter_type_list CLOSEPARAN'''
        # This is where we create a ast with function parameters?
        print "Function: " + p[1]
        print "Parameters: " + str(p[3])
        self.symbol_table.NewScope()
        for i in p[3]:
            pass
            #self.symbol_table.Insert(name=i[1],var=i[0],value=0,line=0,line_loc=0)
        p[0] = p[1]
    def p_direct_declarator_6(self, p):
        '''direct_declarator : direct_declarator OPENPARAN identifier_list CLOSEPARAN'''
        p[0] = p[1]
    def p_direct_declarator_7(self, p):
        '''direct_declarator : direct_declarator OPENPARAN CLOSEPARAN'''
        p[0] = p[1] # push onto stack?
        self.symbol_table.NewScope();

    def p_pointer_1(self, p):
        '''pointer : '*' '''

    def p_pointer_2(self, p):
        '''pointer : '*' type_qualifier_list'''

    def p_pointer_3(self, p):
        '''pointer : '*' pointer'''

    def p_pointer_4(self, p):
        '''pointer : '*' type_qualifier_list pointer'''

    def p_type_qualifier_list_1(self, p):
        '''type_qualifier_list : type_qualifier'''

    def p_type_qualifier_list_2(self, p):
        '''type_qualifier_list : type_qualifier_list type_qualifier'''

    def p_parameter_type_list_1(self, p):
        '''parameter_type_list : parameter_list'''
        p[0] = p[1]

    def p_parameter_type_list_2(self, p):
        '''parameter_type_list : parameter_list ',' ELLIPSIS'''

    def p_parameter_list_1(self, p):
        '''parameter_list : parameter_declaration'''
        if p[0] == None:
            p[0] = []
        p[0].append(p[1])
    def p_parameter_list_2(self, p):
        '''parameter_list : parameter_list ',' parameter_declaration'''

        if p[1] != None:
            p[1].append(p[3])
            p[0] = p[1]
    def p_parameter_declaration_1(self, p):
        '''parameter_declaration : declaration_specifiers declarator'''
        #self.symbol_table.Insert(var = p[1],name=p[2],value=0,line=0,line_loc=0 )
        p[0] = (p[1],p[2])

    def p_parameter_declaration_2(self, p):
        '''parameter_declaration : declaration_specifiers abstract_declarator'''

    def p_parameter_declaration_3(self, p):
        '''parameter_declaration : declaration_specifiers'''

    def p_identifier_list_1(self, p):
        '''identifier_list : IDENTIFIER'''
        if p[0] == None:
            p[0] = []
        p[0].append(p[1])

    def p_identifier_list_2(self, p):
        '''identifier_list : identifier_list ',' IDENTIFIER'''
        if p[1] != None:
            p[1].append(p[3])
        p[0] = p[1]

    def p_type_name_1(self, p):
        '''type_name : specifier_qualifier_list'''

    def p_type_name_2(self, p):
        '''type_name : specifier_qualifier_list abstract_declarator'''

    def p_abstract_declarator_1(self, p):
        '''abstract_declarator : pointer'''

    def p_abstract_declarator_2(self, p):
        '''abstract_declarator : direct_abstract_declarator'''

    def p_abstract_declarator_3(self, p):
        '''abstract_declarator : pointer direct_abstract_declarator'''

    def p_direct_abstract_declarator_1(self, p):
        '''direct_abstract_declarator : OPENPARAN abstract_declarator CLOSEPARAN'''

    def p_direct_abstract_declarator_2(self, p):
        '''direct_abstract_declarator : '[' ']' '''

    def p_direct_abstract_declarator_3(self, p):
        '''direct_abstract_declarator : '[' constant_expression ']' '''

    def p_direct_abstract_declarator_4(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator '[' ']' '''

    def p_direct_abstract_declarator_5(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator '[' constant_expression ']' '''

    def p_direct_abstract_declarator_6(self, p):
        '''direct_abstract_declarator : OPENPARAN CLOSEPARAN'''

    def p_direct_abstract_declarator_7(self, p):
        '''direct_abstract_declarator : OPENPARAN parameter_type_list CLOSEPARAN'''

    def p_direct_abstract_declarator_8(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator OPENPARAN CLOSEPARAN'''

    def p_direct_abstract_declarator_9(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator OPENPARAN parameter_type_list CLOSEPARAN'''

    def p_initializer_1(self, p):
        '''initializer : assignment_expression'''

    def p_initializer_2(self, p):
        '''initializer : OPENBRACK initializer_list CLOSEBRACK'''

    def p_initializer_3(self, p):
        '''initializer : OPENBRACK initializer_list ',' CLOSEBRACK'''

    def p_initializer_list_1(self, p):
        '''initializer_list : initializer'''

    def p_initializer_list_2(self, p):
        '''initializer_list : initializer_list ',' initializer'''

    def p_statement_1(self, p):
        '''statement : labeled_statement'''

    def p_statement_2(self, p):
        '''statement : compound_statement'''

    def p_statement_3(self, p):
        '''statement : expression_statement'''

    def p_statement_4(self, p):
        '''statement : selection_statement'''

    def p_statement_5(self, p):
        '''statement : iteration_statement'''

    def p_statement_6(self, p):
        '''statement : jump_statement'''

    def p_labeled_statement_1(self, p):
        '''labeled_statement : IDENTIFIER ':' statement'''

    def p_labeled_statement_2(self, p):
        '''labeled_statement : CASE constant_expression ':' statement'''

    def p_labeled_statement_3(self, p):
        '''labeled_statement : DEFAULT ':' statement'''

    def p_compound_statement_1(self, p):
        '''compound_statement : OPENBRACK CLOSEBRACK'''
        print ("Found a scope")
        p[0] = p[1]
    def p_compound_statement_2(self, p):
        '''compound_statement : OPENBRACK statement_list CLOSEBRACK'''
        print ("Found a scope")

    def p_compound_statement_3(self, p):
        '''compound_statement : OPENBRACK declaration_list CLOSEBRACK'''
        print ("Found a scope")

    def p_compound_statement_4(self, p):
        '''compound_statement : OPENBRACK declaration_list statement_list CLOSEBRACK'''
        print ("Found a scope")
    def p_compound_statement_error(self,p):
        '''compound_statement : error compound_statement '''
        print p[1]
        print "COMPOUND ERROR"

    def p_declaration_list_1(self, p):
        '''declaration_list : declaration'''

    def p_declaration_list_2(self, p):
        '''declaration_list : declaration_list declaration'''

    def p_statement_list_1(self, p):
        '''statement_list : statement'''

    def p_statement_list_2(self, p):
        '''statement_list : statement_list statement'''

    def p_expression_statement_1(self, p):
        '''expression_statement : SEMI'''
        p[0] = p[1]
    def p_expression_statement_2(self, p):
        '''expression_statement : expression SEMI'''


    def p_selection_statement_1(self, p):
        '''selection_statement : IF OPENPARAN expression CLOSEPARAN statement'''

    def p_selection_statement_2(self, p):
        '''selection_statement : IF OPENPARAN expression CLOSEPARAN statement ELSE statement'''

    def p_selection_statement_3(self, p):
        '''selection_statement : SWITCH OPENPARAN expression CLOSEPARAN statement'''

    def p_iteration_statement_1(self, p):
        '''iteration_statement : WHILE OPENPARAN expression CLOSEPARAN statement'''

    def p_iteration_statement_2(self, p):
        '''iteration_statement : DO statement WHILE OPENPARAN expression CLOSEPARAN SEMI'''

    def p_iteration_statement_3(self, p):
        '''iteration_statement : FOR OPENPARAN expression_statement expression_statement CLOSEPARAN statement'''

    def p_iteration_statement_4(self, p):
        '''iteration_statement : FOR OPENPARAN expression_statement expression_statement expression CLOSEPARAN statement'''

    def p_jump_statement_1(self, p):
        '''jump_statement : GOTO IDENTIFIER SEMI'''

    def p_jump_statement_2(self, p):
        '''jump_statement : CONTINUE SEMI'''

    def p_jump_statement_3(self, p):
        '''jump_statement : BREAK SEMI'''

    def p_jump_statement_4(self, p):
        '''jump_statement : RETURN SEMI'''

    def p_jump_statement_5(self, p):
        '''jump_statement : RETURN expression SEMI'''

    def p_translation_unit_1(self, p):
        '''translation_unit : external_declaration'''

    def p_translation_unit_2(self, p):
        '''translation_unit : translation_unit external_declaration'''

    def p_external_declaration_1(self, p):
        '''external_declaration : function_definition'''

    def p_external_declaration_2(self, p):
        '''external_declaration : declaration'''

    def p_function_definition_1(self, p):
        '''function_definition : declaration_specifiers declarator declaration_list compound_statement'''
        # int test(a,b) int a,b; {}
        print "==================================!!!!!!!!!!!!!!!!"
    def p_function_definition_2(self, p):
        '''function_definition : declaration_specifiers declarator compound_statement'''
        self.symbol_table.StackDump()
        self.symbol_table.EndScope()
        print("FUNCITON NAME: " + p[2])
        p[0] = p[1]
    def p_function_definition_error(self,p):
        '''function_definition : declarator declaration_specifiers declarator'''
        print "ERROR IDENTIFIER: " + p[1] + " BEFORE TYPE SPECIFIER!!!!!!"
    def p_function_definition_3(self, p):
        '''function_definition : declarator declaration_list compound_statement'''
        # Function implementation with no type but with params test(a,b)int a,b;{}
        print "BONKERS"
    def p_function_definition_4(self, p):
        '''function_definition : declarator compound_statement'''
        # Funciton implementation with no type test(){}
        print "BONKERSSSS2"

    def p_error(self,p):
        print("Syntax error in input at " + str(self.lexer.lexpos-self.lines[-1]) + " on line: " + str(self.lexer.lineno))
        self.highlightstring(self.lexer.lexdata.split('\n')[self.lexer.lineno-1],self.lexer.lexpos-self.lines[self.lexer.lineno-1])
        sys.exit()


 