from ticketcounter import *

# Node Visitor borrowed from https://github.acom/eliben/pycparser/blob/master/pycparser/_c_ast.cfg
class NodeVisitor(object):
    """ A base NodeVisitor class for visiting c_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.
        For example:
        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []
            def visit_Constant(self, node):
                self.values.append(node.value)
        Creates a list of values of all the constant nodes
        encountered below the given node. To use it:
        cv = ConstantVisitor()
        cv.visit(node)
        Notes:
        *   generic_visit() will be called for AST nodes for which
            no visit_XXX method was defined.
        *   The children of nodes for which a visit_XXX was
            defined will not be visited - if you need this, call
            generic_visit() on the node.
            You can use:
                NodeVisitor.generic_visit(self, node)
        *   Modeled after Python's own AST visiting facilities
            (the ast module of Python 3.0)
    """
    def visit(self, node):
        """ Visit a node.
        """
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        string = "Generic"
        print "Generic Visitor On Node: " + str(node)
        if type(node) == type(GraphVizVisitor):
            for c_name, c in node.children():
                string += self.visit(c)

        return string + ";\n"


class GraphVizVisitor(NodeVisitor):
    ''' GraphVizVisitor this will implement the output of the nodes to a GraphViz file.
        Return: All functions will output the graphviz text and the node name.
    '''
    ticket = TicketCounter("gv")

    def StringifyLabel(self,label,ticketlabel,braces=False):

        if braces:
            return "{"+ticketlabel + "["+"label=" + '"' + label + '"'+ "]"+"}"
        return ticketlabel + "["+"label=" + '"' + label + '"'+ "]"


    def AddBrackets(self, *strings):
        string = "{"
        for value in strings:
            string += value + " "
        return string.strip() + "}"


    def visit_Type(self,node):
        ticket = self.ticket.GetNextTicket()
        ticket2 = self.ticket.GetNextTicket()
        label = self.StringifyLabel("Type",ticket)
        string = ''
        for i in node.type:
            string += str(i) + " "
        string = string.strip()
        typelabel = self.StringifyLabel(string,ticket2)
        return self.AddBrackets(label) + "->" + self.AddBrackets(typelabel) + ";\n", label

    # IterStatement: [init*, cond*, next*, stmt*,isdowhile,name] {}
    def visit_IterStatement(self,node):
        IterStmt = self.StringifyLabel("Iteration Statement", self.ticket.GetNextTicket())
        string = ""
        if node.init != None:
            initstring,initlabel = self.visit(node.init)
            string = self.AddBrackets(IterStmt) + "->" + self.AddBrackets(initlabel) + ";\n"
            string += initstring
        if node.cond != None:
            condstring, condlabel = self.visit(node.cond)
            string += self.AddBrackets(IterStmt) + "->" + self.AddBrackets(condlabel) + ";\n"
            string += condstring
        if node.next != None:
            nextstring, nextlabel = self.visit(node.next)
            string += self.AddBrackets(IterStmt) + "->" + self.AddBrackets(nextlabel) + ";\n"
            string += nextstring
        if node.stmt != None:
            stmtstring, stmtlabel = self.visit(node.stmt)
            string += self.AddBrackets(IterStmt) + "->" + self.AddBrackets(stmtlabel) + ";\n"
            string += stmtstring
        string += self.AddBrackets(self.StringifyLabel("Iter Type",self.ticket.GetNextTicket())) + "->" + self.AddBrackets(self.StringifyLabel(node.name,self.ticket.GetNextTicket())) + "\n;"

        

        

        return string + typestring + paramstring + compoundlabel + compoundstring, FuncDefLabel
    def visit_Decl(self,node):
        initticket = self.ticket.GetNextTicket()
        declticket = self.ticket.GetNextTicket()
        init = self.StringifyLabel('Init',initticket)
        typestring,typelabel = self.visit(node.type)

        decllabel = self.StringifyLabel("Declaration",declticket,True) 
        string = decllabel + "->" + self.AddBrackets(self.StringifyLabel(node.name,self.ticket.GetNextTicket()), init, typelabel) + ';\n'

        if node.init:
            initstring,initlabel = self.visit(node.init)
            string += self.AddBrackets(init) + "->" + self.AddBrackets(initlabel) + ";\n"
            string += initstring
        else:
            string += self.AddBrackets(init) + "->" 
            string += self.AddBrackets(self.StringifyLabel("None",self.ticket.GetNextTicket())) + ";\n"

        return  string + typestring, decllabel

    def visit_AssignOp(self, node):
        label = self.StringifyLabel("Assignment Operation\n=", self.ticket.GetNextTicket())
        print(node.left)
        leftstring, leftlabel = self.visit(node.left)
        rightstring, rightlabel = self.visit(node.right)
        string = self.AddBrackets(label) + "->" + self.AddBrackets(leftlabel, rightlabel)

        return string + leftstring + rightstring, label

    def visit_DeclList(self,node):
        string = ""
        labels = ""
        for i in node.decls:
            value, label = self.visit(i)
            labels += label + " "
            string += value
        return string, labels.strip()

    def visit_EmptyStatement(self,node):
        emptyticket = self.ticket.GetNextTicket()
        emptylabel = self.StringifyLabel("Empty Statment",emptyticket)
        return "",emptylabel

    def visit_Func(self,node):
        self.visit(node.function)
        return ""

    def visit_FuncDecl(self,node):
        typestring,typelabel = self.visit(node.type)
        paramstring, paramlabel = self.visit(node.ParamList)

        FuncDeclLabel = self.StringifyLabel("Function Declaration", self.ticket.GetNextTicket())
        string = self.AddBrackets(FuncDeclLabel) + "->"

        string += self.AddBrackets(self.StringifyLabel(node.name, self.ticket.GetNextTicket()), typelabel, paramlabel) + ";\n"

        return string + typestring + paramstring, FuncDeclLabel
        
    def visit_If(self,node):
        return "",""

    def visit_FuncDef(self,node):
        typestring,typelabel = self.visit(node.type)
        paramstring, paramlabel = self.visit(node.ParamList)
        comlabel = self.StringifyLabel("Compound Statement", self.ticket.GetNextTicket())

        compoundstring = ""
        compoundlabel = self.AddBrackets(comlabel) + "->{"
        for i in node.expression:
            if(i == None):
                continue
            cs, cl = self.visit(i)
            compoundstring += cs
            compoundlabel += cl + " "

        compoundlabel = compoundlabel.strip() + "};\n"
        FuncDefLabel = self.StringifyLabel("Function Definition", self.ticket.GetNextTicket())
        string = self.AddBrackets(FuncDefLabel) + "->"

        string += self.AddBrackets(self.StringifyLabel(node.name, self.ticket.GetNextTicket()), typelabel, paramlabel, comlabel) + ";\n"

        return string + typestring + paramstring + compoundlabel + compoundstring, FuncDefLabel

    def visit_FuncCall(self,node):
        typestring,typelabel = self.visit(node.type)
        paramstring, paramlabel = self.visit(node.ParamList)

        FuncDeclLabel = self.StringifyLabel("Function Call", self.ticket.GetNextTicket())
        string = self.AddBrackets(FuncDeclLabel) + "->"

        string += self.AddBrackets(self.StringifyLabel(node.name, self.ticket.GetNextTicket()), typelabel, paramlabel) + ";\n"

        return string + typestring + paramstring, FuncDeclLabel

    def visit_Return(self,node):
        return ""

    def visit_ParamList(self,node):
        label = self.StringifyLabel("Parameter List", self.ticket.GetNextTicket())
        string = self.AddBrackets(label) + "->{"

        build_string = ""
        for param in node.params:
            typestring,typelabel = self.visit(param)

            string += typelabel
            build_string += typestring

        if not build_string:
            string += self.StringifyLabel("None", self.ticket.GetNextTicket())

        string += "};\n"

        return string + build_string, label

    def visit_VariableCall(self,node):

        name = self.StringifyLabel('Variable Call', self.ticket.GetNextTicket())
        varname = self.StringifyLabel(node.name, self.ticket.GetNextTicket())
        typestring, typelabel = self.visit(node.type)

        return self.AddBrackets(name) + "->" + self.AddBrackets(varname, typelabel) + ";\n" + typestring, name

    def visit_ArrDecl(self,node):

        init = self.StringifyLabel('Init', self.ticket.GetNextTicket())
        typestring, typelabel = self.visit(node.type)
        dimensionlabel = self.StringifyLabel('Dimensions', self.ticket.GetNextTicket())


        decllabel = self.StringifyLabel("Array Declaration", self.ticket.GetNextTicket())

        string = self.AddBrackets(decllabel) + "->" + self.AddBrackets(self.StringifyLabel(node.name,self.ticket.GetNextTicket()), init, typelabel, dimensionlabel) + ';\n'
        if node.init:
            initstring,initlabel = self.visit(node.init)
            string += self.AddBrackets(init) + "->" + self.AddBrackets(initlabel) + ";\n"
            string += initstring
        else:
            string += self.AddBrackets(init) + "->" 
            string += self.AddBrackets(self.StringifyLabel("None",self.ticket.GetNextTicket())) + ";\n"

        dimlabel = self.AddBrackets(dimensionlabel) + "->{"
        dimension = ""
        for dim in node.dim:
            dimstr, dimlab = self.visit(dim)
            dimension += dimstr
            dimlabel += dimlab + " "

        dimlabel += "};\n"

        return  string + typestring + dimension + dimlabel, decllabel

    def visit_ArrRef(self, node):
        name = self.StringifyLabel('Array Call', self.ticket.GetNextTicket())
        dimensionlabel = self.StringifyLabel('Dimensions', self.ticket.GetNextTicket())
        subscriptlabel = self.StringifyLabel('Subscripts', self.ticket.GetNextTicket())
        varname = self.StringifyLabel(node.name, self.ticket.GetNextTicket())
        typestring, typelabel = self.visit(node.type)

        string = self.AddBrackets(name) + "->" + self.AddBrackets(varname, typelabel, subscriptlabel, dimensionlabel) + ";\n"

        dimlabel = self.AddBrackets(dimensionlabel) + "->{"
        dimension = ""
        for dim in node.dim:
            dimstr, dimlab = self.visit(dim)
            dimension += dimstr
            dimlabel += dimlab + " "

        dimlabel += "};\n"

        sublabel = self.AddBrackets(subscriptlabel) + "->{"
        subscript = ""
        for sub in node.subscript:
            substr, sublab = self.visit(sub)
            subscript += substr
            sublabel += sublab + " "

        sublabel += "};\n"

        return string + typestring + dimension + dimlabel + subscript + sublabel, name

    def visit_Constant(self,node):
        constantticket = self.ticket.GetNextTicket()
        constantlabel = self.StringifyLabel("Constant",constantticket) 
        string = self.AddBrackets(constantlabel) + "->"+ self.AddBrackets(self.StringifyLabel(node.value,self.ticket.GetNextTicket())) + ";\n"
        TypeString,TypeLabel = self.visit(node.type)
        #string += TypeString
        string += self.AddBrackets(constantlabel) + "->"+self.AddBrackets(TypeLabel)
        string += TypeString
        return string, constantlabel

    def visit_Program(self,node):
        string = ""
        programticket = self.ticket.GetNextTicket()
        programlabel = self.StringifyLabel("Program",programticket)
        for nodes in node.NodeList:

            nodeString,nodeLabel = self.visit(nodes)
            string +=  self.AddBrackets(programlabel) + "->" + self.AddBrackets(nodeLabel)
            string += nodeString
        return string

    # &,|,<<,>>,^ 
    def visit_Cast(self,node):
        nodename = node.__class__.__name__
        castticket = self.ticket.GetNextTicket()
        castlabel = self.StringifyLabel(nodename,castticket)
        expr,exprlabel = self.visit(node.expr)
        Type,TypeLabel = self.visit(node.to_type)
        string = self.AddBrackets(castlabel) + "->" +  self.AddBrackets(exprlabel,TypeLabel) + "\n;"
        string += expr + Type
        return string,castlabel
    def generateOpOutput(self,node):
        nodename = node.__class__.__name__
        opticket = self.ticket.GetNextTicket()
        oplabel = self.StringifyLabel(nodename,opticket)
        left,leftlabel = self.visit(node.left)
        right,rightlabel = self.visit(node.right)
        Type,TypeLabel = self.visit(node.type)
        string = self.AddBrackets(oplabel) + "->" +  self.AddBrackets(leftlabel,rightlabel,TypeLabel) + "\n;"
        string += left + right + Type
        return string,oplabel
    def visit_AndOp(self,node):
        return self.generateOpOutput(node)
    def visit_OrOp(self,node):
        return self.generateOpOutput(node)
    def visit_LeftOp(self,node):
        return self.generateOpOutput(node)
    def visit_RightOp(self,node):
        return self.generateOpOutput(node)
    def visit_XorOp(self,node):
        return self.generateOpOutput(node)
    def visit_LandOp(self,node):
        return self.generateOpOutput(node)
    def visit_LorOp(self,node):
        return self.generateOpOutput(node)
    def visit_TernaryOp(self,node):
        return self.generateOpOutput(node)
    def visit_NEqualOp(self,node):
        return self.generateOpOutput(node)
    def visit_GEqualOp(self,node):
        return self.generateOpOutput(node)
    def visit_LEqualOp(self,node):
        return self.generateOpOutput(node)
    def visit_EqualOp(self,node):
        return self.generateOpOutput(node)
    def visit_GreatOp(self,node):
        return self.generateOpOutput(node)
    def visit_LessOp(self,node):
        return self.generateOpOutput(node)
    def visit_RefOp(self,node):
        return self.generateOpOutput(node)
    def visit_MultOp(self,node):
        return self.generateOpOutput(node)
    def visit_AddOp(self,node):
        return self.generateOpOutput(node)
    def visit_SubOp(self,node):
        return self.generateOpOutput(node)
    def visit_DivOp(self,node):
        return self.generateOpOutput(node)
    def visit_ModOp(self,node):
        return self.generateOpOutput(node)
    def visit_BitNotOp(self,node):
        return self.generateOpOutput(node)
    def visit_LogNotOp(self,node):
        return self.generateOpOutput(node)



class ThreeAddressCode(NodeVisitor):
    def visit_ID(self,node):
        pass
    def visit_DECL(self,node):
        pass
