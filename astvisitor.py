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
            #print braces
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

    def visit_Decl(self,node):
        initticket = self.ticket.GetNextTicket()
        declticket = self.ticket.GetNextTicket()
        init = self.StringifyLabel('Init',initticket)
        typestring,typelabel = self.visit(node.type)

        decllabel = self.StringifyLabel("Declaration",declticket,True) 
        string = decllabel + "->" + self.AddBrackets(node.name, init, typelabel) + ';\n'

        if node.init:
            string += self.AddBrackets(init) + "->"+self.visit(node.init)
        else:
            string += self.AddBrackets(init) + "->" 
            string += self.AddBrackets(self.StringifyLabel("None",self.ticket.GetNextTicket())) + ";\n"

        return  string + typestring, decllabel

    def visit_AssignOp(self, node):
        label = self.StringifyLabel("Assignment Operation\n=", self.ticket.GetNextTicket())
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

    def visit_Func(self,node):
        #print "Func"
        self.visit(node.function)
        return ""

    def visit_FuncDecl(self,node):
        #print "FuncDecl!!!!!!!!!!!!!!!"
        return ""

    def visit_FuncDef(self,node):
        typestring,typelabel = self.visit(node.type)
        paramstring, paramlabel = self.visit(node.ParamList)
        comlabel = self.StringifyLabel("Compound Statement", self.ticket.GetNextTicket())

        compoundstring = ""
        compoundlabel = self.AddBrackets(comlabel) + "->{"
        for i in node.expression:
            cs, cl = self.visit(i)
            compoundstring += cs
            compoundlabel += cl + " "

        compoundlabel = compoundlabel.strip() + "};\n"
        string = self.AddBrackets(self.StringifyLabel("Function Definition", self.ticket.GetNextTicket())) + "->"

        string += self.AddBrackets(self.StringifyLabel(node.name, self.ticket.GetNextTicket()), typelabel, paramlabel, comlabel) + ";\n"

        return string + typestring + paramstring + compoundlabel + compoundstring, None

    def visit_FuncCall(self,node):
        return "" 
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
        ticket = self.ticket.GetNextTicket()
        string = 'Array'
        for i in node.dim:
            string += "["+str(i) + "]"
        string = self.StringifyLabel(string,ticket,True)
        return string, string

    def visit_Constant(self,node):
        string = "Constant->"+ node.value + ",Type;\n"
        string += self.visit(node.type)[1]
        return string


class ThreeAddressCode(NodeVisitor):
    def visit_ID(self,node):
        pass
    def visit_DECL(self,node):
        pass
