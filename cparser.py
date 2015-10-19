from cscanner import Scanner
import sys
from symboltable import *
start = 'translation_unit'
class Parser(Scanner):
    start = 'translation_unit'
    def p_primary_expression_1(self, p):
        '''primary_expression : IDENTIFIER'''
        print "IDENTIFER"
        p[0] = p[1] # Do a lookup

    def p_primary_expression_2(self, p):
        '''primary_expression : CONSTANT'''
        p[0] = p[1]

    def p_primary_expression_3(self, p):
        '''primary_expression : STRING_LITERAL'''
        p[0] = p[1]

    def p_primary_expression_4(self, p):
        '''primary_expression : OPENPARAN expression CLOSEPARAN''' 
        p[0] = p[1] + p[2] + p[3]

    def p_postfix_expression_1(self, p):
        '''postfix_expression : primary_expression'''
        p[0] = p[1]

    def p_postfix_expression_2(self, p):
        '''postfix_expression : postfix_expression '[' expression ']' '''
        p[0] = p[1] + p[2] + p[3] + p[4]

    def p_postfix_expression_3(self, p):
        '''postfix_expression : postfix_expression OPENPARAN CLOSEPARAN'''
        p[0] = p[1] + p[2] + p[3]

    def p_postfix_expression_4(self, p):
        '''postfix_expression : postfix_expression OPENPARAN argument_expression_list CLOSEPARAN'''
        p[0] = p[1] + p[2] + p[3] + p[4]

    def p_postfix_expression_5(self, p):
        '''postfix_expression : postfix_expression '.' IDENTIFIER'''
        p[0] = p[1] + p[2] + p[3] # Do a look on identfier

    def p_postfix_expression_6(self, p):
        '''postfix_expression : postfix_expression PTR_OP IDENTIFIER'''
        p[0] = p[1] + p[2] + p[3] # Do a look up

    def p_postfix_expression_7(self, p):
        '''postfix_expression : postfix_expression INC_OP'''
        p[0] = p[1] + p[2]

    def p_postfix_expression_8(self, p):
        '''postfix_expression : postfix_expression DEC_OP'''
        p[0] = p[1] + p[2]

    def p_argument_expression_list_1(self, p):
        '''argument_expression_list : assignment_expression'''
        p[0] = p[1]

    def p_argument_expression_list_2(self, p):
        '''argument_expression_list : argument_expression_list ',' assignment_expression'''
        p[0] = p[1]+p[2]+p[3]

    def p_unary_expression_1(self, p):
        '''unary_expression : postfix_expression'''
        p[0] = p[1]

    def p_unary_expression_2(self, p):
        '''unary_expression : INC_OP unary_expression'''
        p[0] = p[1] + p[2]

    def p_unary_expression_3(self, p):
        '''unary_expression : DEC_OP unary_expression'''
        p[0] = p[1] + p[2]

    def p_unary_expression_4(self, p):
        '''unary_expression : unary_operator cast_expression'''
        p[0] = p[1] + p[2]
    def p_unary_expression_5(self, p):
        '''unary_expression : SIZEOF unary_expression'''
        p[0] = p[1] + p[2]
    def p_unary_expression_6(self, p):
        '''unary_expression : SIZEOF OPENPARAN type_name CLOSEPARAN'''
        p[0] = p[1] + p[2] + p[3]

    def p_unary_operator_1(self, p):
        '''unary_operator : '&' '''
        p[0] = p[1]

    def p_unary_operator_2(self, p):
        '''unary_operator : '*' '''
        p[0] = p[1]
    def p_unary_operator_3(self, p):
        '''unary_operator : '+' '''
        p[0] = p[1]
    def p_unary_operator_4(self, p):
        '''unary_operator : '-' '''
        p[0] = p[1]
    def p_unary_operator_5(self, p):
        '''unary_operator : '~' '''
        p[0] = p[1]
    def p_unary_operator_6(self, p):
        '''unary_operator : '!' '''
        p[0] = p[1]
    def p_cast_expression_1(self, p):
        '''cast_expression : unary_expression'''
        p[0] = p[1]
    def p_cast_expression_2(self, p):
        '''cast_expression : OPENPARAN type_name CLOSEPARAN cast_expression'''
        p[0] = p[1] + p[2] + p[3] + p[4]

    def p_multiplicative_expression_1(self, p):
        '''multiplicative_expression : cast_expression'''
        p[0] = p[1]

    def p_multiplicative_expression_2(self, p):
        '''multiplicative_expression : multiplicative_expression '*' cast_expression'''
        p[0] = p[1] + p[2] + p[3]

    def p_multiplicative_expression_3(self, p):
        '''multiplicative_expression : multiplicative_expression '/' cast_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_multiplicative_expression_4(self, p):
        '''multiplicative_expression : multiplicative_expression '%' cast_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_additive_expression_1(self, p):
        '''additive_expression : multiplicative_expression'''
        p[0] = p[1]
    def p_additive_expression_2(self, p):
        '''additive_expression : additive_expression '+' multiplicative_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_additive_expression_3(self, p):
        '''additive_expression : additive_expression '-' multiplicative_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_shift_expression_1(self, p):
        '''shift_expression : additive_expression'''
        p[0] = p[1]
    def p_shift_expression_2(self, p):
        '''shift_expression : shift_expression LEFT_OP additive_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_shift_expression_3(self, p):
        '''shift_expression : shift_expression RIGHT_OP additive_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_relational_expression_1(self, p):
        '''relational_expression : shift_expression'''
        p[0] = p[1]
    def p_relational_expression_2(self, p):
        '''relational_expression : relational_expression '<' shift_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_relational_expression_3(self, p):
        '''relational_expression : relational_expression '>' shift_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_relational_expression_4(self, p):
        '''relational_expression : relational_expression LE_OP shift_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_relational_expression_5(self, p):
        '''relational_expression : relational_expression GE_OP shift_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_equality_expression_1(self, p):
        '''equality_expression : relational_expression'''
        p[0] = p[1]
    def p_equality_expression_2(self, p):
        '''equality_expression : equality_expression EQ_OP relational_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_equality_expression_3(self, p):
        '''equality_expression : equality_expression NE_OP relational_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_and_expression_1(self, p):
        '''and_expression : equality_expression'''
        p[0] = p[1]
    def p_and_expression_2(self, p):
        '''and_expression : and_expression '&' equality_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_exclusive_or_expression_1(self, p):
        '''exclusive_or_expression : and_expression'''
        p[0] = p[1]
    def p_exclusive_or_expression_2(self, p):
        '''exclusive_or_expression : exclusive_or_expression '^' and_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_inclusive_or_expression_1(self, p):
        '''inclusive_or_expression : exclusive_or_expression'''
        p[0] = p[1]
    def p_inclusive_or_expression_2(self, p):
        '''inclusive_or_expression : inclusive_or_expression '|' exclusive_or_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_logical_and_expression_1(self, p):
        '''logical_and_expression : inclusive_or_expression'''
        p[0] = p[1]
    def p_logical_and_expression_2(self, p):
        '''logical_and_expression : logical_and_expression AND_OP inclusive_or_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_logical_or_expression_1(self, p):
        '''logical_or_expression : logical_and_expression'''
        p[0] = p[1]
    def p_logical_or_expression_2(self, p):
        '''logical_or_expression : logical_or_expression OR_OP logical_and_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_conditional_expression_1(self, p):
        '''conditional_expression : logical_or_expression'''
        p[0] = p[1]
    def p_conditional_expression_2(self, p):
        '''conditional_expression : logical_or_expression '?' expression ':' conditional_expression'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
    def p_assignment_expression_1(self, p):
        '''assignment_expression : conditional_expression'''
        p[0] = p[1]

    def p_assignment_expression_2(self, p):
        '''assignment_expression : unary_expression assignment_operator assignment_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_assignment_operator_1(self, p):
        '''assignment_operator : '=' '''
        p[0] = p[1]
    def p_assignment_operator_2(self, p):
        '''assignment_operator : MUL_ASSIGN'''
        p[0] = p[1]
    def p_assignment_operator_3(self, p):
        '''assignment_operator : DIV_ASSIGN'''
        p[0] = p[1]
    def p_assignment_operator_4(self, p):
        '''assignment_operator : MOD_ASSIGN'''
        p[0] = p[1]
    def p_assignment_operator_5(self, p):
        '''assignment_operator : ADD_ASSIGN'''
        p[0] = p[1]
    def p_assignment_operator_6(self, p):
        '''assignment_operator : SUB_ASSIGN'''
        p[0] = p[1]
    def p_assignment_operator_7(self, p):
        '''assignment_operator : LEFT_ASSIGN'''
        p[0] = p[1]
    def p_assignment_operator_8(self, p):
        '''assignment_operator : RIGHT_ASSIGN'''
        p[0] = p[1]
    def p_assignment_operator_9(self, p):
        '''assignment_operator : AND_ASSIGN'''
        p[0] = p[1]
    def p_assignment_operator_10(self, p):
        '''assignment_operator : XOR_ASSIGN'''
        p[0] = p[1]
    def p_assignment_operator_11(self, p):
        '''assignment_operator : OR_ASSIGN'''
        p[0] = p[1]
    def p_expression_1(self, p):
        '''expression : assignment_expression'''
        p[0] = p[1]
    def p_expression_2(self, p):
        '''expression : expression ',' assignment_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_constant_expression_1(self, p):
        '''constant_expression : conditional_expression'''
        p[0] = p[1]

    def p_declaration_1(self, p):
        '''declaration : declaration_specifiers SEMI'''
        p[0] = p[1] + p[2]
        #print(p[1])

    def p_declaration_2(self, p):
        '''declaration : declaration_specifiers init_declarator_list SEMI'''
        p[0] = p[2]
        # lookup and insert
        #for i in p[2]:
        #    self.symbol_table.Retrieve(i[0])
        #    self.symbol_table.SetType(p[1])
        #   self.symbol_table.SetValue(i[1])
        #    #self.symbol_table.Insert(name=i[0],var=p[1],value=i[1],line=0,line_loc=0) 
        #print(p[2])

    def p_declaration_specifiers_1(self, p):
        '''declaration_specifiers : storage_class_specifier'''
        p[0] = p[1]
    def p_declaration_specifiers_2(self, p):
        '''declaration_specifiers : storage_class_specifier declaration_specifiers'''
        p[0] = p[1] + p[2]
    def p_declaration_specifiers_3(self, p):
        '''declaration_specifiers : type_specifier'''
        p[0] = p[1]

    def p_declaration_specifiers_4(self, p):
        '''declaration_specifiers : type_specifier declaration_specifiers'''
        p[0] = p[1] + p[2]
    def p_declaration_specifiers_5(self, p):
        '''declaration_specifiers : type_qualifier'''
        p[0] = p[1]
    def p_declaration_specifiers_6(self, p):
        '''declaration_specifiers : type_qualifier declaration_specifiers'''
        p[0] = p[1] + p[2]
    def p_init_declarator_list_1(self, p):
        '''init_declarator_list : init_declarator'''
        p[0] = [p[1]]
    def p_init_declarator_list_2(self, p):
        '''init_declarator_list : init_declarator_list ',' init_declarator'''
        p[1].append(p[3])
        p[0] = p[1]
        
    def p_init_declarator_1(self, p):
        '''init_declarator : declarator'''
        #self.symbol_table.Insert(name=p[1],var=0,line=0,line_loc=0)
        p[0] = (p[1],"")

    def p_init_declarator_2(self, p):
        '''init_declarator : declarator '=' initializer'''
        print p[1]
        #self.symbol_table.Insert(name=p[1],var=" ",line=0,line_loc=0) # we need to do something with p[3]
        p[0] = (p[1],  p[3])

    def p_storage_class_specifier_1(self, p):
        '''storage_class_specifier : TYPEDEF'''
        p[0] = p[1]
    def p_storage_class_specifier_2(self, p):
        '''storage_class_specifier : EXTERN'''
        p[0] = p[1]
    def p_storage_class_specifier_3(self, p):
        '''storage_class_specifier : STATIC'''
        p[0] = p[1]
    def p_storage_class_specifier_4(self, p):
        '''storage_class_specifier : AUTO'''
        p[0] = p[1]
    def p_storage_class_specifier_5(self, p):
        '''storage_class_specifier : REGISTER'''
        p[0] = p[1]
    def p_type_specifier_1(self, p):
        '''type_specifier : VOID'''
        p[0] = p[1]

    def p_type_specifier_2(self, p):
        '''type_specifier : CHAR'''
        p[0] = p[1]
    def p_type_specifier_3(self, p):
        '''type_specifier : SHORT'''
        p[0] = p[1]
    def p_type_specifier_4(self, p):
        '''type_specifier : INT'''
        p[0] = p[1]
    def p_type_specifier_5(self, p):
        '''type_specifier : LONG'''
        p[0] = p[1]
    def p_type_specifier_6(self, p):
        '''type_specifier : FLOAT'''
        p[0] = p[1]
    def p_type_specifier_7(self, p):
        '''type_specifier : DOUBLE'''
        p[0] = p[1]
    def p_type_specifier_8(self, p):
        '''type_specifier : SIGNED'''
        p[0] = p[1]
    def p_type_specifier_9(self, p):
        '''type_specifier : UNSIGNED'''
        p[0] = p[1]
    def p_type_specifier_10(self, p):
        '''type_specifier : struct_or_union_specifier'''
        p[0] = p[1]
    def p_type_specifier_11(self, p):
        '''type_specifier : enum_specifier'''
        p[0] = p[1]
    def p_struct_or_union_specifier_1(self, p):
        '''struct_or_union_specifier : struct_or_union IDENTIFIER OPENBRACK struct_declaration_list CLOSEBRACK'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] # insert this guy

    def p_struct_or_union_specifier_2(self, p):
        '''struct_or_union_specifier : struct_or_union OPENBRACK struct_declaration_list CLOSEBRACK'''
        p[0] = p[1] + p[2] + p[3] + p[4] # insert this guy???

    def p_struct_or_union_specifier_3(self, p):
        '''struct_or_union_specifier : struct_or_union IDENTIFIER'''
        p[0] = p[1] + p[2] # insert this guy

    def p_struct_or_union_1(self, p):
        '''struct_or_union : STRUCT'''
        p[0] = p[1]

    def p_struct_or_union_2(self, p):
        '''struct_or_union : UNION'''
        p[0] = p[1]

    def p_struct_declaration_list_1(self, p):
        '''struct_declaration_list : struct_declaration'''
        p[0] = p[1]

    def p_struct_declaration_list_2(self, p):
        '''struct_declaration_list : struct_declaration_list struct_declaration'''
        p[0] = p[1] + p[2]

    def p_struct_declaration_1(self, p):
        '''struct_declaration : specifier_qualifier_list struct_declarator_list SEMI'''
        p[0] = p[1] + p[2] + p[3] # insert

    def p_specifier_qualifier_list_1(self, p):
        '''specifier_qualifier_list : type_specifier specifier_qualifier_list'''
        p[0] = p[1] + p[2]

    def p_specifier_qualifier_list_2(self, p):
        '''specifier_qualifier_list : type_specifier'''
        p[0] = p[1]
    def p_specifier_qualifier_list_3(self, p):
        '''specifier_qualifier_list : type_qualifier specifier_qualifier_list'''
        p[0] = p[1] + p[2]
    def p_specifier_qualifier_list_4(self, p):
        '''specifier_qualifier_list : type_qualifier'''
        p[0] = p[1]
    def p_struct_declarator_list_1(self, p):
        '''struct_declarator_list : struct_declarator'''
        p[0] = p[1] 
    def p_struct_declarator_list_2(self, p):
        '''struct_declarator_list : struct_declarator_list ',' struct_declarator'''
        p[0] = p[1] + p[2] + p[3]
    def p_struct_declarator_1(self, p):
        '''struct_declarator : declarator'''
        p[0] = p[1]
    def p_struct_declarator_2(self, p):
        '''struct_declarator : ':' constant_expression'''
        p[0] = p[1]
    def p_struct_declarator_3(self, p):
        '''struct_declarator : declarator ':' constant_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_enum_specifier_1(self, p):
        '''enum_specifier : ENUM OPENBRACK enumerator_list CLOSEBRACK'''
        p[0] = p[1] + p[2] + p[3] + p[4]
    def p_enum_specifier_2(self, p):
        '''enum_specifier : ENUM IDENTIFIER OPENBRACK enumerator_list CLOSEBRACK'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] # lookup
    def p_enum_specifier_3(self, p):
        '''enum_specifier : ENUM IDENTIFIER'''
        p[0] = p[1]
    def p_enumerator_list_1(self, p):
        '''enumerator_list : enumerator'''
        p[0] = p[1]
    def p_enumerator_list_2(self, p):
        '''enumerator_list : enumerator_list ',' enumerator'''
        p[0] = p[1] + p[2] + p[3]
    def p_enumerator_1(self, p):
        '''enumerator : IDENTIFIER'''
        p[0] = p[1]
    def p_enumerator_2(self, p):
        '''enumerator : IDENTIFIER '=' constant_expression'''
        p[0] = p[1] + p[2] + p[3]
    def p_type_qualifier_1(self, p):
        '''type_qualifier : CONST'''
        p[0] = p[1]
    def p_type_qualifier_2(self, p):
        '''type_qualifier : VOLATILE'''
        p[0] = p[1]

    def p_declarator_1(self, p):
        '''declarator : pointer direct_declarator'''
        p[1].SetName(p[2])
        p[0] = p[1]

    def p_declarator_2(self, p):
        '''declarator : direct_declarator'''
        p[0] = SymbolTreeNode(name=p[1],type_var="",line=0,line_loc=0)
        print p[1]
        #self.symbol_table.Insert(name=p[1],var=" ",value=" ",line=0,line_loc=0)

    def p_direct_declarator_1(self, p):
        '''direct_declarator : IDENTIFIER'''
        p[0] = p[1]
        


    def p_direct_declarator_2(self, p):
        '''direct_declarator : OPENPARAN declarator CLOSEPARAN'''
        p[0] = p[1] + p[2] + p[3]
    def p_direct_declarator_3(self, p):
        '''direct_declarator : direct_declarator '[' constant_expression ']' '''
        p[0] = p[1] + p[2] + p[3] + p[4]
    def p_direct_declarator_4(self, p):
        '''direct_declarator : direct_declarator '[' ']' '''
        p[0] = p[1] + p[2] + p[3]
    def p_direct_declarator_5(self, p):
        '''direct_declarator : direct_declarator OPENPARAN parameter_type_list CLOSEPARAN'''
        # This is where we create a ast with function parameters?
        print "Function: " + p[1]
        print "Parameters: " + str(p[3])
        
        for i in p[3]:
            self.symbol_table.InsertNode(i)
        #self.symbol_table.NewScope()
        #for i in p[3]:
        #    pass
        #    self.symbol_table.Insert(name=i[1],var=i[0],value=0,line=0,line_loc=0)
        p[0] = p[1]
    def p_direct_declarator_6(self, p):
        '''direct_declarator : direct_declarator OPENPARAN identifier_list CLOSEPARAN'''
        print "IDENTIFIER LIST"
        p[0] = p[1]
    def p_direct_declarator_7(self, p):
        '''direct_declarator : direct_declarator OPENPARAN CLOSEPARAN'''
        p[0] = p[1] # push onto stack?
        #self.symbol_table.NewScope();

    def p_pointer_1(self, p):
        '''pointer : '*' '''
        p[0] = PointerNode(None)

    def p_pointer_2(self, p):
        '''pointer : '*' type_qualifier_list'''
        p[0] = PointerNode(p[2])

    def p_pointer_3(self, p):
        '''pointer : '*' pointer'''
        p[2].AddIndirection()
        p[0] = p[2]

    def p_pointer_4(self, p):
        '''pointer : '*' type_qualifier_list pointer'''
        p[3].AddIndirection() 
        p[3].AddTypeQualifiers(p[2])
        p[0] = p[3]

    def p_type_qualifier_list_1(self, p):
        '''type_qualifier_list : type_qualifier'''
        p[0] = p[1]
    def p_type_qualifier_list_2(self, p):
        '''type_qualifier_list : type_qualifier_list type_qualifier'''
        p[0] = p[1] + p[2]
    def p_parameter_type_list_1(self, p):
        '''parameter_type_list : parameter_list'''
        p[0] = p[1]

    def p_parameter_type_list_2(self, p):
        '''parameter_type_list : parameter_list ',' ELLIPSIS'''
        p[0] = p[1] + p[2] + p[3] # black magic warning...

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
        #print(p[1])
        #self.symbol_table.Retrieve(p[2])
        #self.symbol_table.SetType(p[1])
        p[2].SetType(p[1])
        p[0] = p[2]

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
        p[0] = p[1]
    def p_type_name_2(self, p):
        '''type_name : specifier_qualifier_list abstract_declarator'''
        p[0] = p[1] + p[2]
    def p_abstract_declarator_1(self, p):
        '''abstract_declarator : pointer'''
        p[0] = p[1]
    def p_abstract_declarator_2(self, p):
        '''abstract_declarator : direct_abstract_declarator'''
        p[0] = p[1] + p[2]
    def p_abstract_declarator_3(self, p):
        '''abstract_declarator : pointer direct_abstract_declarator'''
        p[0] = p[1] + p[2]
    def p_direct_abstract_declarator_1(self, p):
        '''direct_abstract_declarator : OPENPARAN abstract_declarator CLOSEPARAN'''
        p[0] = p[1] + p[2] + p[3]
    def p_direct_abstract_declarator_2(self, p):
        '''direct_abstract_declarator : '[' ']' '''
        p[0] = p[1] + p[2]
    def p_direct_abstract_declarator_3(self, p):
        '''direct_abstract_declarator : '[' constant_expression ']' '''
        p[0] = p[1] + p[2] + p[3]
    def p_direct_abstract_declarator_4(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator '[' ']' '''
        p[0] = p[1] + p[2] + p[3]
    def p_direct_abstract_declarator_5(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator '[' constant_expression ']' '''
        p[0] = p[1] + p[2] + p[3] + p[4]
    def p_direct_abstract_declarator_6(self, p):
        '''direct_abstract_declarator : OPENPARAN CLOSEPARAN'''
        p[0] = p[1] + p[2]
    def p_direct_abstract_declarator_7(self, p):
        '''direct_abstract_declarator : OPENPARAN parameter_type_list CLOSEPARAN'''
        p[0] = p[1] + p[2] + p[3]
    def p_direct_abstract_declarator_8(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator OPENPARAN CLOSEPARAN'''
        p[0] = p[1] + p[2] + p[3]
    def p_direct_abstract_declarator_9(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator OPENPARAN parameter_type_list CLOSEPARAN'''
        p[0] = p[1] + p[2] + p[3] + p[4]
    def p_initializer_1(self, p):
        '''initializer : assignment_expression'''
        p[0] = p[1]
    def p_initializer_2(self, p):
        '''initializer : OPENBRACK initializer_list CLOSEBRACK'''
        p[0] = p[1] + p[2] + p[3]
    def p_initializer_3(self, p):
        '''initializer : OPENBRACK initializer_list ',' CLOSEBRACK'''
        p[0] = p[1] + p[2] + p[3] + p[4]
    def p_initializer_list_1(self, p):
        '''initializer_list : initializer'''
        p[0] = p[1]
    def p_initializer_list_2(self, p):
        '''initializer_list : initializer_list ',' initializer'''
        p[0] = p[1] + p[2] + p[3]
    def p_statement_1(self, p):
        '''statement : labeled_statement'''
        p[0] = p[1]
    def p_statement_2(self, p):
        '''statement : compound_statement'''
        print "COMPOUND"
        p[0] = p[1]
    def p_statement_3(self, p):
        '''statement : expression_statement'''
        p[0] = p[1]
    def p_statement_4(self, p):
        '''statement : selection_statement'''
        p[0] = p[1]
    def p_statement_5(self, p):
        '''statement : iteration_statement'''
        p[0] = p[1]
    def p_statement_6(self, p):
        '''statement : jump_statement'''
        p[0] = p[1]
    def p_labeled_statement_1(self, p):
        '''labeled_statement : IDENTIFIER ':' statement'''
        p[0] = p[1] + p[2] + p[3]
    def p_labeled_statement_2(self, p):
        '''labeled_statement : CASE constant_expression ':' statement'''
        p[0] = p[1] + p[2] + p[3]
    def p_labeled_statement_3(self, p):
        '''labeled_statement : DEFAULT ':' statement'''
        p[0] = p[1] + p[2] + p[3]
    def p_compound_statement_1(self, p):
        '''compound_statement : OPENBRACK CLOSEBRACK'''
        #self.symbol_table.EndScope()
        #print ("Found a scope")
        #p[0] = p[1] + p[2]
    def p_compound_statement_2(self, p):
        '''compound_statement : OPENBRACK statement_list CLOSEBRACK'''
        #self.symbol_table.EndScope()
        #print ("Found a scope")
        #p[0] = p[1] + p[2] + p[3]
    def p_compound_statement_3(self, p):
        '''compound_statement : OPENBRACK declaration_list CLOSEBRACK'''
        #self.symbol_table.EndScope()
        print ("Found a scope")
        #p[0] = p[1] + p[2] + p[3]
    def p_compound_statement_4(self, p):
        '''compound_statement : OPENBRACK declaration_list statement_list CLOSEBRACK'''
        #self.symbol_table.EndScope()
        #print ("Found a scope")
        #p[0] = p[1] + p[2] + p[3] + p[4]
    #def p_compound_statement_error(self,p):
    #    '''compound_statement : error compound_statement '''
    #    print p[1]
    #    print "COMPOUND ERROR"

    def p_declaration_list_1(self, p):
        '''declaration_list : declaration'''
        p[0] = p[1]
    def p_declaration_list_2(self, p):
        '''declaration_list : declaration_list declaration'''
        p[0] = p[1] + p[2]
    def p_statement_list_1(self, p):
        '''statement_list : statement'''
        p[0] = p[1]
    def p_statement_list_2(self, p):
        '''statement_list : statement_list statement'''
        #p[0] = p[1] + p[2]
    def p_expression_statement_1(self, p):
        '''expression_statement : SEMI'''
        p[0] = p[1]
    def p_expression_statement_2(self, p):
        '''expression_statement : expression SEMI'''
        p[0] = p[1] + p[2]

    def p_selection_statement_1(self, p):
        '''selection_statement : IF OPENPARAN expression CLOSEPARAN statement'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
    def p_selection_statement_2(self, p):
        '''selection_statement : IF OPENPARAN expression CLOSEPARAN statement ELSE statement'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]
    def p_selection_statement_3(self, p):
        '''selection_statement : SWITCH OPENPARAN expression CLOSEPARAN statement'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
    def p_iteration_statement_1(self, p):
        '''iteration_statement : WHILE OPENPARAN expression CLOSEPARAN statement'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
    def p_iteration_statement_2(self, p):
        '''iteration_statement : DO statement WHILE OPENPARAN expression CLOSEPARAN SEMI'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]
    def p_iteration_statement_3(self, p):
        '''iteration_statement : FOR OPENPARAN expression_statement expression_statement CLOSEPARAN statement'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
    def p_iteration_statement_4(self, p):
        '''iteration_statement : FOR OPENPARAN expression_statement expression_statement expression CLOSEPARAN statement'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]
    def p_jump_statement_1(self, p):
        '''jump_statement : GOTO IDENTIFIER SEMI'''
        p[0] = p[1] + p[2] + p[3] # look up
    def p_jump_statement_2(self, p):
        '''jump_statement : CONTINUE SEMI'''
        p[0] = p[1] + p[2]
    def p_jump_statement_3(self, p):
        '''jump_statement : BREAK SEMI'''
        p[0] = p[1] + p[2]
    def p_jump_statement_4(self, p):
        '''jump_statement : RETURN SEMI'''
        p[0] = p[1] + p[2]
    def p_jump_statement_5(self, p):
        '''jump_statement : RETURN expression SEMI'''
        p[0] = p[1] + p[2] + p[3]
    def p_translation_unit_1(self, p):
        '''translation_unit : external_declaration'''
        p[0] = p[1]
    def p_translation_unit_2(self, p):
        '''translation_unit : translation_unit external_declaration'''
        p[0] = p[1] + p[2]
    def p_external_declaration_1(self, p):
        '''external_declaration : function_definition'''
        p[0] = p[1]
    def p_external_declaration_2(self, p):
        '''external_declaration : declaration'''
        p[0] = p[1]
    def p_function_definition_1(self, p):
        '''function_definition : declaration_specifiers declarator declaration_list compound_statement'''
        # int test(a,b) int a,b; {}
        print "==================================!!!!!!!!!!!!!!!!"
        p[0] = p[2]
    def p_function_definition_2(self, p):
        '''function_definition : declaration_specifiers declarator compound_statement'''
        #elf.symbol_table.StackDump()
        #self.symbol_table.EndScope()
        p[0] = p[2]

    #def p_function_definition_error(self,p):
    #    '''function_definition : declarator declaration_specifiers declarator'''
    #    print "ERROR IDENTIFIER: " + p[1] + " BEFORE TYPE SPECIFIER!!!!!!"
    def p_function_definition_3(self, p):
        '''function_definition : declarator declaration_list compound_statement'''
        # Function implementation with no type but with params test(a,b)int a,b;{}
        print "BONKERS"
        p[0] = p[1]
    def p_function_definition_4(self, p):
        '''function_definition : declarator compound_statement'''
        # Funciton implementation with no type test(){}
        print "BONKERSSSS2"
        p[0] + p[1]

    def p_error(self,p):
        print("Syntax error in input at " + str(self.lexer.lexpos-self.lines[-1]) + " on line: " + str(self.lexer.lineno))
        self.highlightstring(self.lexer.lexdata.split('\n')[self.lexer.lineno-1],self.lexer.lexpos-self.lines[self.lexer.lineno-1])
        sys.exit()


 
