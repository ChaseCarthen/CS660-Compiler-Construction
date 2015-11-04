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
        print "Generic Visitor"
        for c_name, c in node.children():
            self.visit(c)


class GraphVizVisitor(NodeVisitor):
    ''' GraphVizVisitor this will implement the output of the nodes to a GraphViz file.
        Return: All functions will output the graphviz text and the node name.
    '''
    ticket = TicketCounter("gv")
    def StringifyLabel(self,label,ticketlabel,braces=False):
        print ticketlabel
        print label
        if braces:
            print braces
            return "{"+ticketlabel + "["+"label=" + '"' + label + '"'+ "]"+"}"
        return ticketlabel + "["+"label=" + '"' + label + '"'+ "]"
    def AddBrackets(self,string):
        return "{" + string + "}"
    def visit_Type(self,node):
        ticket = self.ticket.GetNextTicket()
        ticket2 = self.ticket.GetNextTicket()
        label = self.StringifyLabel("Type",ticket)
        string = ''
        for i in node.type:
            string += str(i) + " "
        string = string.strip()
        typelabel = self.StringifyLabel(string,ticket2)
        return self.AddBrackets(label)+"->"+self.AddBrackets(typelabel)+";\n",label
    def visit_Decl(self,node):
        initticket = self.ticket.GetNextTicket()
        declticket = self.ticket.GetNextTicket()
        typeofdeclticket = self.ticket.GetNextTicket()
        init = self.StringifyLabel('Init',initticket)
        typeofdecl = self.StringifyLabel('Type of Decl',typeofdeclticket)
        typestring,typelabel = self.visit(node.type)

        string = self.StringifyLabel("Declaration",declticket,True) + "->"+ "{" + node.name + " " + init+ " " + typelabel  + " " + typeofdecl + '};\n'

        if node.init:
            string += '{' + init + "}->"+self.visit(node.init)
        else:
            string += '{' + init +"}->" + self.AddBrackets(self.StringifyLabel("None",self.ticket.GetNextTicket())) + ";\n"
        if node.typeofdecl:
            string += '{' + typeofdecl +'}->' + self.visit(node.typeofdecl)[1]
        else:
            string += '{' + typeofdecl+'}->' + self.StringifyLabel("Normal",self.ticket.GetNextTicket()) + ";\n"
        
        string += typestring
         
        return  string 
    def visit_DeclList(self,node):
        string = ""
        for i in node.decls:
            string += self.visit(i)
        return string
    def visit_Func(self,node):
        print "Func"
        self.visit(node.function)
        return ""
    def visit_FuncDecl(self,node):
        print "FuncDecl"
        return ""
    def visit_FuncDef(self,node):
        return ""
    def visit_FuncCall(self,node):
        return "" 
    def visit_Return(self,node):
        return ""
    def visit_ParamList(self,node):
        return ""
    def visit_ArrDecl(self,node):
        ticket = self.ticket.GetNextTicket()
        string = 'Array'
        for i in node.dim:
            string += "["+str(i) + "]"
        string = self.StringifyLabel(string,ticket,True)
        return string, string

class ThreeAddressCode(NodeVisitor):
    def visit_ID(self,node):
        pass
    def visit_DECL(self,node):
        pass