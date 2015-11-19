from ticketcounter import *
import sys

CODE = False

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
        print "Generic Visitor On Node: " + node.__class__.__name__ + " " + str(node)
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
            init = self.AddBrackets(self.StringifyLabel("Initialization",self.ticket.GetNextTicket()))
            string += self.AddBrackets(IterStmt) + "->" + init + ";\n"
            string += init + "->" + self.AddBrackets(initlabel) + ";\n"
            string += initstring
        if node.cond != None:
            condstring, condlabel = self.visit(node.cond)
            cond = self.AddBrackets(self.StringifyLabel("Conditional",self.ticket.GetNextTicket()))
            string += self.AddBrackets(IterStmt) + "->" + cond + ";\n"
            string += cond + "->" + self.AddBrackets(condlabel) + ";\n"
            string += condstring
        if node.next != None:
            nextstring, nextlabel = self.visit(node.next)
            next = self.AddBrackets(self.StringifyLabel("Next Step",self.ticket.GetNextTicket()))
            string += self.AddBrackets(IterStmt) + "->" + next + ";\n"
            string += next + "->" + self.AddBrackets(nextlabel) + ";\n"
            string += nextstring
        if node.stmt != None:
            comstring,comlabel = self.visit(node.stmt)

            string += comstring
            string += self.AddBrackets(IterStmt) + "->" + self.AddBrackets(comlabel) + ";\n"
        itertype = self.AddBrackets(self.StringifyLabel("Iter Type",self.ticket.GetNextTicket()))
        string += self.AddBrackets(IterStmt) + "->" + self.AddBrackets(itertype) + ";\n" 
        string += itertype
        string += "->" + self.AddBrackets(self.StringifyLabel(node.name,self.ticket.GetNextTicket())) + "\n;"    
        return string, IterStmt

        
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
        
    # If: [cond*,truecond*,falsecond*] {}
    def visit_If(self,node):
        string = ""
        iflabel = self.StringifyLabel("If Statement", self.ticket.GetNextTicket())
        if node.truecond != None:

            truecond, truecondlabel = self.visit(node.truecond)
            TrueCondition = self.StringifyLabel("True Condition", self.ticket.GetNextTicket())
            string += self.AddBrackets(iflabel) + "->" + self.AddBrackets(TrueCondition) + ";\n" 
            string += self.AddBrackets(TrueCondition) + "->" + self.AddBrackets(truecondlabel)
            string += truecond

        if node.falsecond != None:
            falsecond, falsecondlabel = self.visit(node.falsecond)
            FalseCondition = self.StringifyLabel("False Condition", self.ticket.GetNextTicket())
            string += self.AddBrackets(iflabel) + "->" + self.AddBrackets(FalseCondition) + ";\n" 
            string += self.AddBrackets(FalseCondition) + "->" + self.AddBrackets(falsecondlabel) + ";\n" 
            string += falsecond

        if node.cond != None:
            cond,condlabel = self.visit(node.cond)
            Conditional = self.StringifyLabel("Conditional", self.ticket.GetNextTicket())
            string += self.AddBrackets(iflabel) + "->" + self.AddBrackets(Conditional) + ";\n" 
            string += self.AddBrackets(Conditional) + "->" + self.AddBrackets(condlabel) + ";\n" 
            string += cond

        return string,iflabel
    #PtrDecl: [name,type*,numindirections]
    def visit_PtrDecl(self,node):
        Pointer = self.StringifyLabel("Pointer", self.ticket.GetNextTicket())
        name = self.StringifyLabel(node.name, self.ticket.GetNextTicket())
        TypeString,TypeLabel = self.visit(node.type)
        NumIndirections = self.StringifyLabel(str(node.numindirections), self.ticket.GetNextTicket())
        NumIndirectionsLabel = self.StringifyLabel("Pointer Dimension", self.ticket.GetNextTicket())
        string = ""
        string += self.AddBrackets(Pointer) + "->" + self.AddBrackets(TypeLabel,name,NumIndirectionsLabel)
        string += self.AddBrackets(NumIndirectionsLabel) + "->" + self.AddBrackets(NumIndirections)
        string += TypeString
        return string,Pointer
    def visit_CompoundStatement(self,node):
        comlabel = self.StringifyLabel("Compound Statement", self.ticket.GetNextTicket())
        compoundstring = ""
        compoundlabel = self.AddBrackets(comlabel) + "->{"
        for i in node.stmts:

            if(i == None):
                continue
            cs, cl = self.visit(i)
            compoundstring += cs
            compoundlabel += cl + " "

        compoundlabel = compoundlabel.strip() + "};\n"
        return compoundlabel+compoundstring, comlabel

    def visit_FuncDef(self,node):
        typestring,typelabel = self.visit(node.type)
        paramstring, paramlabel = self.visit(node.ParamList)

        comstring,comlabel = self.visit(node.expression)
        FuncDefLabel = self.StringifyLabel("Function Definition", self.ticket.GetNextTicket())
        string = self.AddBrackets(FuncDefLabel) + "->"

        string += self.AddBrackets(self.StringifyLabel(node.name, self.ticket.GetNextTicket()), typelabel, paramlabel, comlabel) + ";\n"

        return string + typestring + paramstring + comstring, FuncDefLabel

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

        if build_string == "":
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
    # Add a shadow variable handing
    '''
    ThreeAddressCode our visitor for making three address code.
    I think we should keep a similar goal to the one above where we return the string
    on the first and a variable label that is needed.
    exp: return string,relevant_glob_local_temp
    '''
    floattemp = TicketCounter("f_")
    inttemp = TicketCounter("i_")
    localticket = TicketCounter("l_")
    labelticket = TicketCounter("label_")
    def __init__(self):
        self.local = False # If this this is true we are in a local scope
        #self.globals = {}
        self.locals = [] # pop off of this guy if leaving a scope
        self.done = ""
    def searchForVariable(self,name):
        #if name in self.globals:
        #    return self.globals[name]
        for local in self.locals:
            if name in local:
                return self.compressedTAC("local",local[name])
        return self.compressedTAC("glob",name)
    def InsertLocalScope(self):
        self.locals.append({})
    def PopLocalScope(self):
        self.locals.pop()
    def insertVariable(self,name,label):
        if len(self.locals):
            self.locals[-1][name] = label
        else:
            self.globals[name] = label
    def commentify(self,string):
        return "//" + string

    def printTAC(self,name, one = '-', two = '-', three = '-', code = 'No Code Given'):
        coord = (name, one, two, three, self.commentify(code))
        if code:
            return '({0[0]:^30}, {0[1]:^30}, {0[2]:^30}, {0[3]:^30}); {0[4]:<40}\n'.format(coord)
        else:
            return '({0[0]:^30}, {0[1]:^30}, {0[2]:^30}, {0[3]:^30});\n'.format(coord)

    def compressedTAC(self,*strings):
        number = len(strings)
        string = '('
        for i in range(number):
            string += "{"
            string += "0[" + str(i) +"]}"
            if i != number - 1:
                string += ", "
        string += ")"
        return string.format(strings)

    def visit_ID(self,node):
        pass
        
    #type,qualifier,storage
    def visit_Type(self,node):
        qualifier = ""
        Type = ""
        for i in node.qualifier:
            qualifier += i + " "
        for i in node.type:
            Type += i + " "
        return (Type,qualifier),"" # The "" is for convention

    def visit_Decl(self,node):
        # No strings right now.
        # Floats and Ints need to be supported

        op = ""
        assignOP = ""
        string = ""
        name = node.name
        if not self.local:
            op = "glob"
            string += self.printTAC("global",name,str(4)) # hard codeness
        else:
            op = "local"
            # Create a local counter
            previousname = name
            name = self.localticket.GetNextTicket()
            self.insertVariable(previousname,name)
        
        TypeOut,variable = self.visit(node.type)
        Type = TypeOut[0]
        Qual = TypeOut[1]
        if node.init != None:
            #print (node.init)
            strings,initvalue = self.visit(node.init)
            string += strings
        else:
            initvalue = "-"
        
        if 'const' in Qual:
            #op = "const"
            # No idea here??
            pass
        else:
            #lets get down to the meat
            string += self.printTAC("assign",initvalue,"-",self.compressedTAC(op,name),node.text) 
        # We need to add strings
        return string,self.compressedTAC(op,name)

    def visit_Constant(self,node):
        TypeOut,variable = self.visit(node.type)
        Type = TypeOut[0]
        Qual = TypeOut[1]
        if "int" in Type:
            op = "cons"
        else:# Add string check here when we get to it.
            op = "fcons"

        string = self.compressedTAC(op,node.value)
        return "",string
    def visit_Program(self,node):
        #print ("Program")
        string = ""
        for n in node.NodeList:
            s,s2 = self.visit(n)
            string += s
        print (string)
        
    def visit_DeclList(self,node):
        #print "DeclList"
        string = ""
        for n in node.decls:
            declstring,declvariable = self.visit(n)
            string += declstring
        #print string
        return string,""
    # FuncDef: [ParamList**,type*,name,expression*,numlocals]
    def visit_FuncDef(self,node):
        self.local = True
        self.InsertLocalScope()
        local = {}
        string = "procentry \n" + self.compressedTAC("glob",node.name) + "\n" + self.compressedTAC("cons",len(node.ParamList.params)) + "\n" + self.compressedTAC("cons",node.numlocals) + "\n"
        string2,s = self.visit(node.expression)
        string += string2
        string += "endproc" 
        # Search local variables first if found return
        # Search globals if not in locals
        #print string
        self.PopLocalScope()
        return string,"" 

    def visit_VariableCall(self,node):
        variableName = self.searchForVariable(node.name)
        return "",variableName

    def GetTypeInformation(self,typenode):
        TypeOut,variable = self.visit(typenode)
        Type = TypeOut[0]
        Qual = TypeOut[1]
        return Type,Qual

    def OPCommand(self,command,node):
        stringleft,leftlabel = self.visit(node.left)
        stringright,rightlabel = self.visit(node.right)
        Type,Qual = self.GetTypeInformation(node.type)
        if "int" in Type:
            templabel = self.inttemp.GetNextTicket()
        elif "float" in Type:
            templabel = self.floattemp.GetNextTicket()
        string = stringleft 
        string += stringright
        string += self.printTAC(command,leftlabel,rightlabel,templabel,node.text)
        return string,templabel
    #ArrDecl: [name,type*,init*,dim**] {}
    def visit_ArrDecl(self,node):
        op = ""
        assignOP = ""
        string = ""
        name = node.name
        if not self.local:
            op = "glob"
            string += self.printTAC("global",name,str(4)) # hard codeness
        else:
            op = "local"
            # Create a local counter
            previousname = name
            name = self.localticket.GetNextTicket()
            self.insertVariable(previousname,name)
        
        TypeOut,variable = self.visit(node.type)
        Type = TypeOut[0]
        Qual = TypeOut[1]
        if node.init != None:
            print (node.init)
            strings,initvalue = self.visit(node.init)
            string += strings
        else:
            initvalue = "-"

        #lets get down to the meat
        dim = 1
        for i in node.dim:
            dim *= int(i.value)
        string += self.printTAC("array",dim,"-",self.compressedTAC(op,name),node.text) 
        string += self.printTAC("assign",initvalue,"-",self.compressedTAC(op,name),node.text) 

        # We need to add strings
        return string,self.compressedTAC(op,name)

    # ArrRef: [name,subscript**,type*,dim**]
    def visit_ArrRef(self, node):
        variableName = self.searchForVariable(node.name)
        subscripts = []
        dims = []
        string = ""
        for i in node.subscript:
            subscripts.append(int(i.value))

        for i in node.dim:
            dims.append(int(i.value))
        for i in range(len(subscripts)):
            string += self.printTAC("bound",dims[i],0,subscripts[i]) 
            temp = self.inttemp.GetNextTicket()
            string += self.printTAC("assign",self.compressedTAC("indr",variableName),"-",temp) 
            variableName = temp
        return string,temp

    def visit_AddOp(self,node):
        return self.OPCommand("add",node)
    def visit_MultOp(self,node):
        return self.OPCommand("mult",node)
    def visit_SubOp(self,node):
        return self.OPCommand("sub",node)
    def visit_DivOp(self,node):
        return self.OPCommand("div",node)
    def visit_LessOp(self,node):
        return self.OPCommand("lt",node)

        # If: [cond*,truecond*,falsecond*] {}
    def visit_If(self,node):
        string,conditional = self.visit(node.cond)
        falsestring = ""
        truestring = ""
        falselabel = self.labelticket.GetNextTicket()
        truestring,tlabel = self.visit(node.truecond)
        first = False
        if self.done == "":
            self.done = self.labelticket.GetNextTicket()
            first = True

        donestring = self.printTAC("br","_","_",self.compressedTAC("label",self.done),"") + "\n"
        if node.falsecond != None:
            falsestring,flabel = self.visit(node.falsecond)

        string += self.printTAC("brne",conditional,0,falselabel,node.text) + "\n" 
        string += truestring
        string += donestring 
        string += self.compressedTAC("label",falselabel) + "\n"
        string += falsestring
        
        
        if first:
            string += self.compressedTAC("label",self.done) + "\n"
            self.done = ""
        return string, ""
    # IterStatement: [init*, cond*, next*, stmt*,isdowhile,name] {}
    def visit_IterStatement(self,node):
        string, dummy = self.visit(node.init)
        top = self.labelticket.GetNextTicket()
        bottom = self.labelticket.GetNextTicket()
        if not node.isdowhile:
            string = string + self.printTAC("br",'-','-',top,node.text.replace("\n", "")) 
        string += self.printTAC("label",'-','-',top,"") 
        temp, dummy = self.visit(node.stmt)
        string += temp
        string += self.printTAC("label",'-','-',bottom,"") 
        temp, label = self.visit(node.cond)
        string += temp
        string += self.printTAC("brne",'0',label,top,"") 
        return string, None

    def visit_AssignOp(self, node):
        string = ''
        temp, label_1 = self.visit(node.left)
        string += temp
        temp, label_2 = self.visit(node.left)
        string += temp
        return string + self.printTAC('assign', label_1, '-', label_2, node.text), None

    def visit_EmptyStatement(self,node):
        return "", ""

    def visit_Func(self,node):
        return None, None

    def visit_FuncDecl(self,node):
        return None, None
        


    #PtrDecl: [name,type*,numindirections]
    def visit_PtrDecl(self,node):
        return None, None

    def visit_CompoundStatement(self,node):
        string = ""
        for i in node.stmts:
            if(i == None):
                continue
            cs, cl = self.visit(i)
            string += cs
        return string, ""

    def visit_FuncCall(self,node):
        return None, None

    def visit_Return(self,node):
        return None, None

    def visit_ParamList(self,node):
        return None, None

    # &,|,<<,>>,^ 
    def visit_Cast(self,node):
        return None, None

    def generateOpOutput(self,node):
        return None, None

    def visit_AndOp(self,node):
        return self.OPCommand("and",node)
    def visit_OrOp(self,node):
        return self.OPCommand("or",node)
    def visit_LeftOp(self,node):
        return self.OPCommand("sll",node)
    def visit_RightOp(self,node):
        return self.OPCommand("srl",node)
    def visit_XorOp(self,node):
        return self.OPCommand("xor",node)
    def visit_LandOp(self,node):
        return self.OPCommand("andi",node)
    def visit_LorOp(self,node):
        return self.OPCommand("ori",node)
    def visit_TernaryOp(self,node):
        return None, None
    def visit_NEqualOp(self,node):
        return self.OPCommand("ne",node)
    def visit_GEqualOp(self,node):
        return self.OPCommand("ge",node)
    def visit_LEqualOp(self,node):
        return self.OPCommand("le",node)
    def visit_EqualOp(self,node):
        return self.OPCommand("eq",node)
    def visit_GreatOp(self,node):
        return self.OPCommand("gt",node)
    def visit_LessOp(self,node):
        return self.OPCommand("lt",node)
    def visit_RefOp(self,node):
        return self.OPCommand("addr",node)
    def visit_ModOp(self,node):                     # More Problems
        return self.OPCommand("mod",node)
    def visit_BitNotOp(self,node):
        return self.OPCommand("not",node)
    def visit_LogNotOp(self,node):                  # This may be a problem in the future
        return self.OPCommand("noti",node)

