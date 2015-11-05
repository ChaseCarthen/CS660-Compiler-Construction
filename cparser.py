from cscanner import Scanner
from cscanner import reserved
import sys
from symboltable import *
from CompilerExceptions import *
from termcolor import colored
from node import *
from asttree import *
import strconv

def makeParserDict(symboltablenode,astnode):
    return {"symbolNode" : symboltablenode,"astNode" : astnode}
start = 'translation_unit'
class Parser(Scanner):
    start = 'translation_unit'
    def p_primary_expression_1(self, p):
        '''primary_expression : IDENTIFIER'''
        try:
            p[0] = self.symbol_table.Retrieve(p[1])
            p[0] = VariableCall( Type(p[0].GetType(), p[0].GetQualifiers(), None), p[0].GetName())
        except SymbolTableError, e:
            print("We need to fail(this output on line 14): " + str(e))
            sys.exit()

    def p_primary_expression_2(self, p):
        '''primary_expression : CONSTANT'''
        cType = strconv.infer(p[1])
        tNode = Type([cType],[],[])
        p[0] = Constant(tNode,p[1],None)
        #p[0] = p[1]

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
        p[0] = p[1] #array checking gos here

    def p_postfix_expression_3(self, p):
        '''postfix_expression : postfix_expression OPENPARAN CLOSEPARAN'''
        p[0] = p[1] #+ p[2] + p[3]

    def p_postfix_expression_4(self, p):
        '''postfix_expression : postfix_expression OPENPARAN argument_expression_list CLOSEPARAN'''
        p[0] = p[1] # do a type check in parameter

    def p_postfix_expression_5(self, p):
        '''postfix_expression : postfix_expression '.' IDENTIFIER'''
        #p[0] = p[1] + p[2] + p[3] # Do a look on identfier

    def p_postfix_expression_6(self, p):
        '''postfix_expression : postfix_expression PTR_OP IDENTIFIER'''
        #p[0] = p[1] + p[2] + p[3] # Do a look up

    def p_postfix_expression_7(self, p):
        '''postfix_expression : postfix_expression INC_OP'''
        #p[0] = p[1] + p[2]

    def p_postfix_expression_8(self, p):
        '''postfix_expression : postfix_expression DEC_OP'''
        #p[0] = p[1] + p[2]

    def p_argument_expression_list_1(self, p):
        '''argument_expression_list : assignment_expression'''
        p[0] = p[1]

    def p_argument_expression_list_2(self, p):
        '''argument_expression_list : argument_expression_list ',' assignment_expression'''
        p[0] = p[1]#+p[2]+p[3]

    def p_unary_expression_1(self, p):
        '''unary_expression : postfix_expression'''
        p[0] = p[1]

    def p_unary_expression_2(self, p):
        '''unary_expression : INC_OP unary_expression'''
        #p[0] = p[1] + p[2]

    def p_unary_expression_3(self, p):
        '''unary_expression : DEC_OP unary_expression'''
        #p[0] = p[1] + p[2]

    def p_unary_expression_4(self, p):
        '''unary_expression : unary_operator cast_expression'''
        #p[0] = p[1] + p[2]
    def p_unary_expression_5(self, p):
        '''unary_expression : SIZEOF unary_expression'''
        #p[0] = p[1] + p[2]
    def p_unary_expression_6(self, p):
        '''unary_expression : SIZEOF OPENPARAN type_name CLOSEPARAN'''
        #p[0] = p[1] + p[2] + p[3]

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
        #p[0] = p[1] + p[2] + p[3] + p[4]

    def p_multiplicative_expression_1(self, p):
        '''multiplicative_expression : cast_expression'''
        p[0] = p[1]

    def p_multiplicative_expression_2(self, p):
        '''multiplicative_expression : multiplicative_expression '*' cast_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't multiply these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak Upcast Warning"
            p[0]= Constant(rType,str(p[1].value * p[3].value))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = MultOp(one,two,Typed)


    def p_multiplicative_expression_3(self, p):
        '''multiplicative_expression : multiplicative_expression '/' cast_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't divide these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(p[1].value / p[3].value))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = DivOp(one,two,Typed)

    def p_multiplicative_expression_4(self, p):
        '''multiplicative_expression : multiplicative_expression '%' cast_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type) or self.TypeComparison("float",p[1].type) or self.TypeComparison("float",p[3].type):
            print "Error can't modulo these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)

            p[0]= Constant(rType,str(p[1].value % p[3].value))

        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = ModOp(one,two,Typed)

    def p_additive_expression_1(self, p):
        '''additive_expression : multiplicative_expression'''
        p[0] = p[1]

    def p_additive_expression_2(self, p):
        '''additive_expression : additive_expression '+' multiplicative_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't add these two types together!!"
            sys.exit(0)

        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(p[1].value + p[3].value))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = AddOp(one,two,Typed)

    def p_additive_expression_3(self, p):
        '''additive_expression : additive_expression '-' multiplicative_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(p[1].value - p[3].value))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = SubOp(one,two,Typed)

    def p_shift_expression_1(self, p):
        '''shift_expression : additive_expression'''
        p[0] = p[1]
    def p_shift_expression_2(self, p):
        '''shift_expression : shift_expression LEFT_OP additive_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(p[1].value << p[3].value))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = LeftOp(one,two,Typed) 
        #p[0] = p[1] + p[2] + p[3]
    def p_shift_expression_3(self, p):
        '''shift_expression : shift_expression RIGHT_OP additive_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(p[1].value >> p[3].value))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = RightOp(one,two,Typed) 
    def p_relational_expression_1(self, p):
        '''relational_expression : shift_expression'''
        p[0] = p[1]
    def p_relational_expression_2(self, p):
        '''relational_expression : relational_expression '<' shift_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(1 if p[1].value < p[3].value else 0))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = LessOp(one,two,Typed)  

    def p_relational_expression_3(self, p):
        '''relational_expression : relational_expression '>' shift_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(1 if p[1].value > p[3].value else 0))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = GreatOp(one,two,Typed) 
    def p_relational_expression_4(self, p):
        '''relational_expression : relational_expression LE_OP shift_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(1 if p[1].value <= p[3].value else 0))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = LEqualOp(one,two,Typed) 
    def p_relational_expression_5(self, p):
        '''relational_expression : relational_expression GE_OP shift_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(1 if p[1].value >= p[3].value else 0))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = GEqualOp(one,two,Typed) 
    def p_equality_expression_1(self, p):
        '''equality_expression : relational_expression'''
        p[0] = p[1]
    def p_equality_expression_2(self, p):
        '''equality_expression : equality_expression EQ_OP relational_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(1 if p[1].value == p[3].value else 0))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = EqualOp(one,two,Typed) 
    def p_equality_expression_3(self, p):
        '''equality_expression : equality_expression NE_OP relational_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(1 if p[1].value != p[3].value else 0))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = NEqualOp(one,two,Typed) 
    def p_and_expression_1(self, p):
        '''and_expression : equality_expression'''
        p[0] = p[1]
    def p_and_expression_2(self, p):
        '''and_expression : and_expression '&' equality_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(p[1].value & p[3].value))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = AndOp(one,two,Typed) 
    def p_exclusive_or_expression_1(self, p):
        '''exclusive_or_expression : and_expression'''
        p[0] = p[1]
    def p_exclusive_or_expression_2(self, p):
        '''exclusive_or_expression : exclusive_or_expression '^' and_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(p[1].value ^ p[3].value))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = XorOp(one,two,Typed) 
    def p_inclusive_or_expression_1(self, p):
        '''inclusive_or_expression : exclusive_or_expression'''
        p[0] = p[1]
    def p_inclusive_or_expression_2(self, p):
        '''inclusive_or_expression : inclusive_or_expression '|' exclusive_or_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(p[1].value | p[3].value))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = OrOp(one,two,Typed) 
    def p_logical_and_expression_1(self, p):
        '''logical_and_expression : inclusive_or_expression'''
        p[0] = p[1]
    def p_logical_and_expression_2(self, p):
        '''logical_and_expression : logical_and_expression AND_OP inclusive_or_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(1 if p[1].value != 0 and p[3].value != 0 else 0))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = LandOp(one,two,Typed) 
    def p_logical_or_expression_1(self, p):
        '''logical_or_expression : logical_and_expression'''
        p[0] = p[1]
    def p_logical_or_expression_2(self, p):
        '''logical_or_expression : logical_or_expression OR_OP logical_and_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant and type(p[3]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0]= Constant(rType,str(1 if p[1].value != 0 or p[3].value != 0 else 0))
        else:
            one,two,Typed = self.StrongestType(p[1],p[3])
            p[0] = LorOp(one,two,Typed) 
    def p_conditional_expression_1(self, p):
        '''conditional_expression : logical_or_expression'''
        #print("Conditional expression" + str(p[1]))
        p[0] = p[1]
    def p_conditional_expression_2(self, p):
        '''conditional_expression : logical_or_expression '?' expression ':' conditional_expression'''
        rType = ""
        if self.TypeComparison("char",p[1].type) or self.TypeComparison("char",p[3].type):
            print "Error can't subtract these two types together!!"
            sys.exit(0)
        if type(p[1]) == Constant:
            if self.WeakTypeComparisonWithType('int',p[1].type,p[3].type):
                rType = Type(['int'],[],[])
                p[1].value = int(p[1].value)
                p[3].value = int(p[3].value)
            else:
                rType = Type(['float'],[],[])
                p[1].value = float(p[1].value)
                p[3].value = float(p[3].value)
                if not self.WeakTypeComparison(p[1].type,p[3].type):
                    print "Weak upcast warning!"
            p[0] = p[3] if p[1].value != 0 else p[5]
        else:
            p[0] = TernaryOp(p[1],p[3],p[5]) 

    def p_assignment_expression_1(self, p):
        '''assignment_expression : conditional_expression'''
        p[0] = p[1]

    def p_assignment_expression_2(self, p):
        '''assignment_expression : unary_expression assignment_operator assignment_expression'''

        if 'const' in p[1].type.qualifier:
            print("This is not allowed since the variable is constant.")
            sys.exit()

        p[2].left = p[1]
        p[2].right = p[3]
        p[0] = p[2]

    def p_assignment_operator_1(self, p):
        '''assignment_operator : '=' '''
        p[0] = AssignOp(None, None)

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

    # Pushing a dictionary here.
    def p_declaration_1(self, p):
        '''declaration : declaration_specifiers SEMI'''
        p[0] = p[1]
        self.typelist.pop()
        #print(p[1])

    def p_declaration_2(self, p):
        '''declaration : declaration_specifiers init_declarator_list SEMI'''
        p[0] = p[2]
        astList = []

        # lookup and insert
        for declarator in p[2]:
            if declarator != None:
                declarator["symbolNode"].SetType(p[1].type) 
                declarator["symbolNode"].SetQualifiers(p[1].qualifier) # Dictionary ouch right here .. a potential bug to fix
                declarator["astNode"].type = p[1]
                astList.append(declarator["astNode"])

        p[0] = DeclList(astList)


    def p_declaration_specifiers_1(self, p):
        '''declaration_specifiers : storage_class_specifier'''
        p[0] = Type([],[],[p[1]]) 
        self.typelist.append(p[0])

    def p_declaration_specifiers_2(self, p):
        '''declaration_specifiers : storage_class_specifier declaration_specifiers'''
        #p[0] = p[1] + p[2]
        self.typelist[-1].storage.append(p[2])
        p[0] = p[2]

    def p_declaration_specifiers_3(self, p):
        '''declaration_specifiers : type_specifier'''
        p[0] = Type([p[1]],[],[]) #{"qualifiers" : [], "specifiers" : [p[1]],"storage" : []}
        self.typelist.append(p[0])

    def p_declaration_specifiers_4(self, p):
        '''declaration_specifiers : type_specifier declaration_specifiers'''
        #p[0] = [p[1]] + p[2]
        # specifiers is a list
        p[2].type = [p[1]] + p[2].type
        checkstring = ""
        for i in p[2].type:
            checkstring += i + " "
        checkstring = checkstring.strip()
        if not checkstring in self.supportedtypes:
            print "ERROR INVALID TYPE SPECIFIER: " + str(p.lineno(1)) + " starting at Character: "+ str(p.lexpos(1)) 
            sys.exit()
        p[0] = p[2]

    def p_declaration_specifiers_5(self, p):
        '''declaration_specifiers : type_qualifier'''
        #p[0] = p[1]
        p[0] = Type([],[p[1]],[]) #{"specifiers" : [], "qualifiers" : [p[1]],"storage" : []}

    def p_declaration_specifiers_6(self, p):
        '''declaration_specifiers : type_qualifier declaration_specifiers'''
        for qual in p[1]:
            p[2].qualifier.append(qual)
        p[0] = p[2] #{"qualifiers" : p[1] + p[2]["qualifiers"], "specifiers" : p[2]["specifiers"]}

    def p_init_declarator_list_1(self, p):
        '''init_declarator_list : init_declarator'''
        p[0] = [p[1]]

    def p_init_declarator_list_2(self, p):
        '''init_declarator_list : init_declarator_list ',' init_declarator'''
        p[1].append(p[3])
        p[0] = p[1]
        
    def p_init_declarator_1(self, p):
        '''init_declarator : declarator'''
        if not "typedef" in self.typelist[-1].storage:
            try:
                self.symbol_table.InsertNode(p[1])
            except SymbolTableWarning, e:
                print(e)
            except SymbolTableError, e:
                print(e)
            #p[0] = p[1],astnode
        else:
            self.symbol_table.InsertNewType(p[1].GetName(),self.typelist[-1][1:].type)
        if VariableNode == type(p[1]):
            p[0] = makeParserDict(p[1], Decl(p[1].GetName(),None,None) )
        elif ArrayNode == type(p[1]):
            p[0] = makeParserDict(p[1], ArrDecl(p[1].GetName(),None,None,p[1].dimensions) )
        elif FunctionNode == type(p[1]):
            paramlist = []
            for param in p[1].GetParameters():
                paramlist.append(Decl(param.GetName(),Type(param.GetType(),param.GetQualifiers(),[]), None,None))
            p[0] = makeParserDict(p[1], FuncDecl(ParamList(paramlist),Type(p[1].GetType(),[],[] ), p[1].GetName()) )
        

    def p_init_declarator_2(self, p):
        '''init_declarator : declarator '=' initializer'''
        try:
            self.symbol_table.InsertNode(p[1])
        except SymbolTableWarning, e:
            print(e)
        except SymbolTableError, e:
            print(e)
        p[0] = makeParserDict(p[1], Decl(p[1].GetName(),None,p[3],None))
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
        '''struct_or_union_specifier : struct_or_union IDENTIFIER OPENBRACE struct_declaration_list CLOSEBRACE'''
        p[0] = p[1] + p[2] + p[3] + p[4] + p[5] # insert this guy

    def p_struct_or_union_specifier_2(self, p):
        '''struct_or_union_specifier : struct_or_union OPENBRACE struct_declaration_list CLOSEBRACE'''
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
        '''enum_specifier : ENUM OPENBRACE enumerator_list CLOSEBRACE'''
        p[0] = p[1] + p[2] + p[3] + p[4]
    def p_enum_specifier_2(self, p):
        '''enum_specifier : ENUM IDENTIFIER OPENBRACE enumerator_list CLOSEBRACE'''
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
        p[0] = [p[1]]

    def p_type_qualifier_2(self, p):
        '''type_qualifier : VOLATILE'''
        p[0] = [p[1]]

    def p_declarator_1(self, p):
        '''declarator : pointer direct_declarator'''
        p[1]["symbolNode"].SetName(p[2]["symbolNode"].GetName())
        p[1]["symbolNode"].SetLine(p[2]["symbolNode"].GetLine())
        p[1]["symbolNode"].SetCharacterLocation(p[2]["symbolNode"].GetCharacterLocation())
        n = node(text="Declarator")
        n.SetChild(p[1]["astNode"])
        n.SetChild(p[2]["astNode"])
        p[1]["astNode"] = n
        p[0] = p[1]

    def p_declarator_2(self, p):
        '''declarator : direct_declarator'''
        p[0] = p[1] #VariableNode(name=p[1][0], type_var="", line=p[1][1], line_loc=p[1][2])

    def p_direct_declarator_1(self, p):
        '''direct_declarator : IDENTIFIER'''
        p[0] = VariableNode(name=p[1], type_var="", line=p.lineno(1), line_loc=p.lexpos(1) - self.lines[p.lineno(1)-1],tq=[])
        
    def p_direct_declarator_2(self, p):
        '''direct_declarator : OPENPARAN declarator CLOSEPARAN'''
        p[0] = p[2]

    def p_direct_declarator_3(self, p):
        '''direct_declarator : direct_declarator '[' constant_expression ']' '''
        if type(p[1]) == type(VariableNode()):
            p[1] = ArrayNode(type_var = p[1].GetType(), name = p[1].GetName(), line = p[1].GetLine(), line_loc = p[1].GetCharacterLocation(), dim = p[3])
        else:
            #p[1].IncrementDimensions()
            p[1].AddDimension(p[3])
        p[0] = p[1]

    def p_direct_declarator_4(self, p):
        '''direct_declarator : direct_declarator '[' ']' '''
        if type(p[1]) == type(VariableNode()):
            p[1] = ArrayNode(type_var = p[1].GetType(), name = p[1].GetName(), line = p[1].GetLine(), line_loc = p[1].GetCharacterLocation(), dim = 1)
        else:
            #p[1].IncrementDimensions()
            pass
        p[0] = p[1]

    def p_direct_declarator_5(self, p):
        '''direct_declarator : direct_declarator OPENPARAN parameter_type_list CLOSEPARAN'''
        params = []
        for param in p[3]:
            params.append(param)

        # This is where we create a ast with function parameters?
        p[1] = FunctionNode(parameters = params, type_var = self.typelist[-1].type, name = p[1].GetName(), line = p[1].GetLine(), line_loc = p[1].GetCharacterLocation())
        try:
            if len(self.symbol_table.stack) > 1:
                self.symbol_table.InsertNodePreviousStack(p[1])
            else:
                self.symbol_table.InsertNode(p[1])
        except SymbolTableWarning, e:
            print(e)
        except SymbolTableError, e:
            print(e)

        for i in p[3]:
            if len(self.symbol_table.stack) > 1:
                self.loginfo("INSERTING INTO STACK")
                try:
                    self.symbol_table.InsertNode(i)
                    #pass
                except SymbolTableWarning, e:
                    print(e)
                except SymbolTableError, e:
                    print(e)

        p[0] = p[1]

    def p_direct_declarator_6(self, p):
        '''direct_declarator : direct_declarator OPENPARAN identifier_list CLOSEPARAN'''
        p[0] = FunctionNode(parameters = p[3], type_var = self.typelist[-1]["specifiers"], name = p[1].GetName(), line = p[1].GetLine(), line_loc = p[1].GetCharacterLocation())

        try:
            if len(self.symbol_table.stack) > 1:
                self.symbol_table.InsertNodePreviousStack(p[0])
            else:
                self.symbol_table.InsertNode(p[0])
        except SymbolTableWarning, e:
            print(e)
        except SymbolTableError, e:
            print(e)

        p[0] = p[1]

    def p_direct_declarator_7(self, p):
        '''direct_declarator : direct_declarator OPENPARAN CLOSEPARAN'''

        p[1] = p[1]
        p[0] = FunctionNode(type_var = self.typelist[-1], name = p[1].GetName(), line = p[1].GetLine(), line_loc = p[1].GetCharacterLocation())

        try:
            if len(self.symbol_table.stack) > 1:
                self.symbol_table.InsertNodePreviousStack(p[0])
            else:
                self.symbol_table.InsertNode(p[0])
        except SymbolTableWarning, e:
            print(e)
        except SymbolTableError, e:
            print(e)

    def p_pointer_1(self, p):
        '''pointer : '*' '''
        p[0] = makeParserDict(PointerNode(None),node(text="*"))

    def p_pointer_2(self, p):
        '''pointer : '*' type_qualifier_list'''
        n = node(text="*")
        p[2]["astNode"].SetParent(n)
        p[0] = makeParserDict(PointerNode(p[2]),n)

    def p_pointer_3(self, p):
        '''pointer : '*' pointer'''
        p[2]["symbolNode"].AddIndirection()
        p[2]["astNode"].text = "*" + p[2]["astNode"].text
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
        #p[0] = p[1] + p[2] + p[3] # black magic warning...

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
        self.typelist.pop()
        p[2].SetType(p[1].type)
        p[2].SetQualifiers(p[1].qualifier)
        p[0] = p[2]

    def p_parameter_declaration_2(self, p):
        '''parameter_declaration : declaration_specifiers abstract_declarator'''
        self.typelist.pop()

    def p_parameter_declaration_3(self, p):
        '''parameter_declaration : declaration_specifiers'''
        self.typelist.pop()
        #print( "TYPE: " + str(p[1]))
        p[0] = VariableNode(type_var = p[1]['specifiers'], tq = p[1]['qualifiers'])

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
        #p[0] = p[1] + p[2]
    def p_abstract_declarator_1(self, p):
        '''abstract_declarator : pointer'''
        p[0] = p[1]
    def p_abstract_declarator_2(self, p):
        '''abstract_declarator : direct_abstract_declarator'''
        #p[0] = p[1] + p[2]
    def p_abstract_declarator_3(self, p):
        '''abstract_declarator : pointer direct_abstract_declarator'''
        #p[0] = p[1] + p[2]
    def p_direct_abstract_declarator_1(self, p):
        '''direct_abstract_declarator : OPENPARAN abstract_declarator CLOSEPARAN'''
        #p[0] = p[1] + p[2] + p[3]
    def p_direct_abstract_declarator_2(self, p):
        '''direct_abstract_declarator : '[' ']' '''
        #p[0] = p[1] + p[2]
    def p_direct_abstract_declarator_3(self, p):
        '''direct_abstract_declarator : '[' constant_expression ']' '''
        #p[0] = p[1] + p[2] + p[3]
    def p_direct_abstract_declarator_4(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator '[' ']' '''
        #p[0] = p[1] + p[2] + p[3]
    def p_direct_abstract_declarator_5(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator '[' constant_expression ']' '''
        #p[0] = p[1] + p[2] + p[3] + p[4]
    def p_direct_abstract_declarator_6(self, p):
        '''direct_abstract_declarator : OPENPARAN CLOSEPARAN'''
        #p[0] = p[1] + p[2]
    def p_direct_abstract_declarator_7(self, p):
        '''direct_abstract_declarator : OPENPARAN parameter_type_list CLOSEPARAN'''
        #p[0] = p[1] + p[2] + p[3]
    def p_direct_abstract_declarator_8(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator OPENPARAN CLOSEPARAN'''
        #p[0] = p[1] + p[2] + p[3]
    def p_direct_abstract_declarator_9(self, p):
        '''direct_abstract_declarator : direct_abstract_declarator OPENPARAN parameter_type_list CLOSEPARAN'''
        #p[0] = p[1] + p[2] + p[3] + p[4]
    def p_initializer_1(self, p):
        '''initializer : assignment_expression'''
        p[0] = p[1]
    def p_initializer_2(self, p):
        '''initializer : OPENBRACE initializer_list CLOSEBRACE'''
        #p[0] = p[1] + p[2] + p[3]
    def p_initializer_3(self, p):
        '''initializer : OPENBRACE initializer_list ',' CLOSEBRACE'''
        #p[0] = p[1] + p[2] + p[3] + p[4]
    def p_initializer_list_1(self, p):
        '''initializer_list : initializer'''
        p[0] = p[1]
    def p_initializer_list_2(self, p):
        '''initializer_list : initializer_list ',' initializer'''
        #p[0] = p[1] + p[2] + p[3]
    def p_statement_1(self, p):
        '''statement : labeled_statement'''
        p[0] = p[1]
    def p_statement_2(self, p):
        '''statement : compound_statement'''
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
        #p[0] = p[1] + p[2] + p[3]
    def p_labeled_statement_2(self, p):
        '''labeled_statement : CASE constant_expression ':' statement'''
        #p[0] = p[1] + p[2] + p[3]
    def p_labeled_statement_3(self, p):
        '''labeled_statement : DEFAULT ':' statement'''
        #p[0] = p[1] + p[2] + p[3]
    def p_compound_statement_1(self, p):
        '''compound_statement : OPENBRACE CLOSEBRACE'''
        self.symbol_table.EndScope()
        p[0] = [EmptyStatement()] #makeParserDict(None,EmptyStatement())
        #print ("Found a scope")
        #p[0] = p[1] + p[2]

    def p_compound_statement_2(self, p):
        '''compound_statement : OPENBRACE statement_list CLOSEBRACE'''
        self.symbol_table.EndScope()
        p[0] = p[2]

    def p_compound_statement_3(self, p):
        '''compound_statement : OPENBRACE declaration_list CLOSEBRACE'''
        p[0] = p[2]#makeParserDict(None,p[2])
        self.symbol_table.EndScope()

    def p_compound_statement_4(self, p):
        '''compound_statement : OPENBRACE declaration_list statement_list CLOSEBRACE'''
        self.symbol_table.EndScope()
        p[0] = p[2] + p[3]

    def p_declaration_list_1(self, p):
        '''declaration_list : declaration'''
        p[0] = [p[1]]

    def p_declaration_list_2(self, p):
        '''declaration_list : declaration_list declaration'''
        p[0] = p[1] + [p[2]]

    def p_statement_list_1(self, p):
        '''statement_list : statement'''
        p[0] = [p[1]]

    def p_statement_list_2(self, p):
        '''statement_list : statement_list statement'''
        p[0] = p[1] + [p[2]]

    def p_expression_statement_1(self, p):
        '''expression_statement : SEMI'''
        p[0] = p[1]

    def p_expression_statement_2(self, p):
        '''expression_statement : expression SEMI'''
        p[0] = p[1] 

    # This will do the last if first
    def p_selection_statement_1(self, p):
        '''selection_statement : IF OPENPARAN expression CLOSEPARAN statement'''
        p[0] = If(p[3], p[4],None) # May need to check types here 
    # Will iterate up through the ifs
    def p_selection_statement_2(self, p):
        '''selection_statement : IF OPENPARAN expression CLOSEPARAN statement ELSE statement'''
        p[0] = If(p[3],p[5],p[7]) # May need to check types

    def p_selection_statement_3(self, p):
        '''selection_statement : SWITCH OPENPARAN expression CLOSEPARAN statement'''
        pass

    def p_iteration_statement_1(self, p):
        '''iteration_statement : WHILE OPENPARAN expression CLOSEPARAN statement'''
        p[0] = IterStatement(None,p[3],None,p[5],False,"While")# IterStatement: [init*, cond*, next*, stmt*,isdowhile,name]

    def p_iteration_statement_2(self, p):
        '''iteration_statement : DO statement WHILE OPENPARAN expression CLOSEPARAN SEMI'''
        p[0] = IterStatement(None,p[5],None,p[1],True,"Do While")

    def p_iteration_statement_3(self, p):
        '''iteration_statement : FOR OPENPARAN expression_statement expression_statement CLOSEPARAN statement'''
        p[0] = IterStatement(p[3],p[4],None,p[6],False,"For")

    def p_iteration_statement_4(self, p):
        '''iteration_statement : FOR OPENPARAN expression_statement expression_statement expression CLOSEPARAN statement'''
        p[0] = IterStatement(p[3],p[4],p[5],p[7],False,"For")

    def p_jump_statement_1(self, p):
        '''jump_statement : GOTO IDENTIFIER SEMI'''
        #p[0] = p[1] + p[2] + p[3] # look up
    def p_jump_statement_2(self, p):
        '''jump_statement : CONTINUE SEMI'''
        p[0] = Continue()
        #p[0] = p[1] + p[2]
    def p_jump_statement_3(self, p):
        '''jump_statement : BREAK SEMI'''
        p[0] = Break()
        #p[0] = p[1] + p[2]
    def p_jump_statement_4(self, p):
        '''jump_statement : RETURN SEMI'''
        p[0] = Return(None)
        #p[0] = p[1] + p[2]
    def p_jump_statement_5(self, p):
        '''jump_statement : RETURN expression SEMI'''
        p[0] = Return(p[2])
        #p[0] = p[1] + p[2] + p[3]
    def p_translation_unit_1(self, p):
        '''translation_unit : external_declaration'''
        self.rootnode.append(p[1])
        p[0] = self.rootnode
        #print p.lineno(1)
        span = p.lexspan(1)
        print self.input_data[span[0]:span[1]+1]

    def p_translation_unit_2(self, p):
        '''translation_unit : translation_unit external_declaration'''
        self.rootnode.append(p[2])
        p[0] = self.rootnode
        #print p.lineno(2)
        span = p.lexspan(2)
        print self.input_data[span[0]:span[1]+1]

    def p_external_declaration_1(self, p):
        '''external_declaration : function_definition'''
        p[0] = p[1]

    def p_external_declaration_2(self, p):
        '''external_declaration : declaration'''
        p[0] = p[1]

    def p_function_definition_1(self, p):
        '''function_definition : declaration_specifiers declarator declaration_list compound_statement'''
        # int test(a,b) int a,b; {}
        self.typelist.pop()
        p[0] = p[2]

    def p_function_definition_2(self, p):
        '''function_definition : declaration_specifiers declarator compound_statement'''
        paramlist = []
        for param in p[2].GetParameters():
            paramlist.append(Decl(param.GetName(),Type(param.GetType(),param.GetQualifiers(),[]), None,None))
        p[0] = FuncDef(ParamList(paramlist), p[1], p[2].GetName(), p[3])
        self.typelist.pop()

    def p_function_definition_3(self, p):
        '''function_definition : declarator declaration_list compound_statement'''
        # Function implementation with no type but with params test(a,b)int a,b;{}
        p[0] = p[1]
    def p_function_definition_4(self, p):
        '''function_definition : declarator compound_statement'''
        # Funciton implementation with no type test(){}
        p[0] + p[1]

    def p_error(self,p):
        print("Syntax error in input at " + str(self.lexer.lexpos-self.lines[self.lexer.lineno-1]) + " on line: " + str(self.lexer.lineno))
        self.highlightstring(self.lexer.lineno,self.lexer.lexpos)
        sys.exit()


 
