from astvisitor import *

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
        return "",""

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

