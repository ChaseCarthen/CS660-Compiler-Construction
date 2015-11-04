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
    def visit_Type(self,node):
        string = '"'
        for i in node.type:
            string += str(i) + " "
        string = string.strip() + '"' 
        return "Type->"+string+";\n"
    def visit_Decl(self,node):
        string = "Declaration->"+ node.name + ",Init,Type;\n"
        if node.init:
            string += "Init->"+self.visit(node.init)
        else:
            string += "Init->None;\n"
        string += self.visit(node.type)
        return string 
    def visit_DeclList(self,node):
        string = ""
        for i in node.decls:
            string += self.visit(i)
        return string
    def visit_FuncDecl(self,node):
        return 
    def visit_FuncDef(self,node):
        return
    def visit_FuncCall(self,node):
        return  
    def visit_Return(self,node):
        return
    def visit_ParamList(self,node):
        return 
    def visit_Constant(self,node):
        string = "Constant->"+ node.value + ",Type;\n"
        string += self.visit(node.type)
        return string

class ThreeAddressCode(NodeVisitor):
    def visit_ID(self,node):
        pass
    def visit_DECL(self,node):
        pass