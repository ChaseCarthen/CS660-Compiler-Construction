from astvisitor import *
from asttree import *
import math
import re
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
    saveticket = TicketCounter("save_")
    def __init__(self, code):
        self.local = False # If this this is true we are in a local scope
        #self.globals = {}
        self.locals = [] # pop off of this guy if leaving a scope
        self.arg = []
        self.done = ""
        self.localcount = 0
        self.CODE = code
        self.offset = {}
        
        # Build the offset dictionary from the file
        f = open("src/platform.info", "r")
        for line in f:
            item = line.replace("\n","").split("=")
            self.offset[item[0].strip()] = int(math.ceil(int(item[1].strip()) / 4.0))
        f.close()

    def searchForVariable(self,name):
        #if name in self.globals:
        #    return self.globals[name]
        for local in self.locals:
            if name in local:
                return self.compressedTAC("local",local[name])

        for arg in self.arg:
            if name in arg:
                return self.compressedTAC("arg",arg[name])

        return self.compressedTAC("glob",name)
    def InsertLocalScope(self):
        self.locals.append({})
        self.arg.append({})
    def PopLocalScope(self):
        self.locals.pop()
        self.arg.pop()
    def insertVariable(self,name,label):
        if len(self.locals):
            self.locals[-1][name] = label
    def commentify(self,string,lines=None): # lines will be a tupld
        if not self.CODE:
            return ""
        string2 = ""
        strings = string.split('\n')
        if lines != None:
            linestart = lines[0]
        for i in strings:

            string2 += ";\t\t" + i
            if lines != None: 
                string2 += " line number: " + str(linestart) + "\n"
                linestart += 1
            else:
                string2 += "\n"
        string2 = string2[0:len(string2)-1] 
        if string == "":
            return ""
        return string2 + "\n"

    def printTAC(self,name, one = '-', two = '-', three = '-', code = '',lines=None):
        coord = (name, one, two, three)
        if self.CODE:
            return self.commentify(code,lines) + '({0[0]:^30}, {0[1]:^30}, {0[2]:^30}, {0[3]:^30})\n'.format(coord)
        else:
            return '({0[0]:^30}, {0[1]:^30}, {0[2]:^30}, {0[3]:^30})\n'.format(coord)

    def compressedTAC(self,*strings):
        number = len(strings)
        string = '('
        for i in range(number):
            string += "{"
            string += "0[" + str(i) +"]}"
            if i != number - 1:
                string += " "
        string += ")"
        return string.format(strings)

    def visit_ID(self,node):
        pass
        
    #type,qualifier,storage
    def visit_Type(self,node):
        qualifier = ""
        Type = ""
        if node.qualifier:
            for i in node.qualifier:
                qualifier += i + " "

        for i in node.type:
            Type += i + " "

        t = ""
        for i in node.type:
            t += i + " "
        t = t.strip()
        return (Type,qualifier),t # The "" is for convention

    def visit_Decl(self,node):
        # No strings right now.
        # Floats and Ints need to be supported

        op = ""
        assignOP = ""
        string = ""
        name = node.name
        if not self.local:
            op = "glob"
            string += self.printTAC("global",name," ",str(4)) # hard codeness
            return string,self.compressedTAC(op,name)
        else:
            op = "local"
            # Create a local counter
            previousname = name
            name = str(self.localcount) #self.localticket.GetNextTicket()
            self.localcount += 1
            self.insertVariable(previousname,name)
        
        TypeOut,variable = self.visit(node.type)
        Type = TypeOut[0]
        Qual = TypeOut[1]
        if node.init != None:
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
            string += self.printTAC("assign",initvalue,"-",self.compressedTAC(op,name),node.text,node.lines) 
        # We need to add strings
        return string,self.compressedTAC(op,name)

    def visit_Constant(self,node):
        TypeOut,variable = self.visit(node.type)
        Type = TypeOut[0]
        Qual = TypeOut[1]
        if "int" in Type:
            op = "cons"
        elif "char" in Type:
            op = "char"
        else:# Add string check here when we get to it.
            op = "fcons"
        string = self.compressedTAC(op,node.value)
        return "",string

    def visit_Program(self,node):
        string = ""
        for n in node.NodeList:
            s,s2 = self.visit(n)
            string += s
        return string,""
        
    def visit_DeclList(self,node):
        string = ""
        for n in node.decls:
            declstring,declvariable = self.visit(n)
            string += declstring
        return string,""

    # FuncDef: [ParamList**,type*,name,expression*,numlocals]
    def visit_FuncDef(self,node):
        self.local = True
        self.InsertLocalScope()
        local = {}
        #raw_input()

        temp = self.arg.pop()
        index = 0
        for name in node.ParamList.params:
            temp[name.name] = "$a" + str(index)
            index += 1

        self.arg.append(temp)

        string2,s = self.visit(node.expression)
        string = "\n"+ self.commentify(node.text,node.lines)
        string += "procentry \n" + self.compressedTAC("glob",node.name) + "\n" + self.compressedTAC("cons",len(node.ParamList.params)) + "\n" + self.compressedTAC("cons",self.localcount) + "\n"
        string += string2
        string += "endproc" 
        # Search local variables first if found return
        # Search globals if not in locals
        self.PopLocalScope()
        self.localcount = 0
        return string,"" 

    def visit_VariableCall(self,node):
        variableName = self.searchForVariable(node.name)
        return "",variableName

    def GetTypeInformation(self,typenode):
        TypeOut,variable = self.visit(typenode)
        Type = TypeOut[0]
        Qual = TypeOut[1]
        return Type,Qual

    def GetTempLabel(self,Type):
        if "int" == Type:
            templabel = self.inttemp.GetNextTicket()
        elif "float" == Type:
            templabel = self.floattemp.GetNextTicket()
        return templabel

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
        string += self.printTAC(command,leftlabel,rightlabel,templabel,node.text,node.lines)
        return string,templabel

    #ArrDecl: [name,type*,init*,dim**] {}
    def visit_ArrDecl(self,node):
        op = ""
        assignOP = ""
        string = ""
        name = node.name

        TypeOut,variable = self.visit(node.type)
        if not self.local:
            op = "glob"
            #dims = map(int,node.dim)
            prod = 1
            for i in node.dim:
                prod *= int(i.value)

            string += self.printTAC("global",name,"_",str(prod*self.offset[variable])) # hard codeness
            return string,self.compressedTAC(op,name)
        else:
            op = "local"
            # Create a local counter
            previousname = name
            name = str(self.localcount) #self.localticket.GetNextTicket()
            self.localcount += 1
            self.insertVariable(previousname,name)
        

        #Type = TypeOut[0]
        #Qual = TypeOut[1]
        #string += TypeOut

        if node.init != None:
            strings,initvalue = self.visit(node.init)
            string += strings
        else:
            initvalue = "-"

        #lets get down to the meat
        dim = self.inttemp.GetNextTicket()
        string += self.printTAC("assign",self.compressedTAC("cons",self.offset[variable]),"_",dim)
        for i in node.dim:
            outstr, label = self.visit(i)
            string +=  outstr
            newlabel = self.inttemp.GetNextTicket()
            string += self.printTAC("mult",dim,label,newlabel)
            dim = newlabel
            
        string += self.printTAC("array",dim,"-",self.compressedTAC(op,name),node.text,node.lines) 
        #string += self.printTAC("assign",initvalue,"-",self.compressedTAC(op,name),node.text,node.lines) 

        # We need to add strings
        return string,self.compressedTAC(op,name)

    # ArrRef: [name,subscript**,type*,dim**]
    def visit_ArrRef(self, node):
        #print "ARRREF"
        variableName = self.searchForVariable(node.name)
        if "glob" in variableName:
            variableName = self.compressedTAC("arrglob",node.name)

        subscripts = []
        dims = []
        string = ""
        for i in node.subscript:
            temp, label = self.visit(i)
            string += temp
            print label
            subscripts.append(label)

        for i in node.dim:
            temp, label = self.visit(i)
            string += temp
            dims.append(label)

        # Gets the base address to a temp
        baseAddress = self.inttemp.GetNextTicket()
        string += self.printTAC("assign",variableName,"-",baseAddress)

        # Build types as a full string
        t = ''

        temp,t = self.visit(node.type)

        typeSize = self.offset[t]

        addTemps = []
        string += self.printTAC("bound",dims[len(subscripts)-1],self.compressedTAC("cons",0),subscripts[len(subscripts)-1])
        temp = self.inttemp.GetNextTicket()
        addTemps.append(temp)
        string += self.printTAC("mult", self.compressedTAC("cons",typeSize*4), subscripts[len(subscripts)-1], temp, "-")

        for i in reversed(range(len(subscripts)-1)):
            string += self.printTAC("bound",dims[i],self.compressedTAC("cons",0),subscripts[i])
            temp1 = self.inttemp.GetNextTicket()
            string += self.printTAC("mult", self.compressedTAC("cons",typeSize*4), subscripts[i], temp1, "-")

            final = ""
            current1 = temp1
            for j in range(i+1, len(subscripts)):
                final = self.inttemp.GetNextTicket()
                string += self.printTAC("mult", current1, dims[j], final, "-")
                current1 = final

            addTemps.append(final)

        assignment = self.inttemp.GetNextTicket()
        current1 = self.inttemp.GetNextTicket()
        final = self.inttemp.GetNextTicket()
        string += self.printTAC("add", baseAddress, addTemps[0], assignment, "-")
        for i in range(1, len(addTemps)):
            string += self.printTAC("add", addTemps[i], assignment, assignment, "-")
        #string += self.printTAC("assign",self.compressedTAC("indr",assignment),"-",assignment)
        return string, self.compressedTAC("indr",assignment)

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

        donestring = self.printTAC("br","_","_",self.done,"") + "\n"
        if node.falsecond != None:
            falsestring,flabel = self.visit(node.falsecond)

        string += self.printTAC("bre",conditional,'(cons 0)',falselabel,node.text) + "\n" 
        string += truestring
        string += donestring 
        string += self.printTAC("label",'-','-',falselabel) + "\n"
        string += falsestring
        
        
        if first:
            string += self.printTAC("label",'-','-',self.done) + "\n"
            self.done = ""
        return string, ""
    # IterStatement: [init*, cond*, next*, stmt*,isdowhile,name] {}
    def visit_IterStatement(self,node):
        string = ""
        if node.init:
            string, dummy = self.visit(node.init)
        top = self.labelticket.GetNextTicket()
        bottom = self.labelticket.GetNextTicket()
        if not node.isdowhile:
            string = string + self.printTAC("br",'-','-',top,node.text.replace("\n", "")) 
        string += self.printTAC("label",'-','-',top,"") 
        if (node.stmt != None):
            temp, dummy = self.visit(node.stmt)
            string += temp
        string += self.printTAC("label",'-','-',bottom,"")
        if(node.next != None):
            temp, label = self.visit(node.next)
            string += temp
        if(node.cond != None):
            temp, label = self.visit(node.cond)
            string += temp
        string += self.printTAC("bne",'(cons 0)',label,top,"") 
        return string, None

    def visit_AssignOp(self, node):
        string = ''
        temp, label_1 = self.visit(node.right)
        string += temp
        temp, label_2 = self.visit(node.left)
        string += temp

        #raw_input()
        return string + self.printTAC('assign', label_1, '-', label_2, node.text,node.lines), ""

    def visit_FuncCall(self,node):
        string = self.printTAC('args',"-","-",self.compressedTAC("cons",len(node.ParamList.params)))
        for i in node.ParamList.params:
            content, label = self.visit(i)
            string += content
            #raw_input()
            if type(i) == ArrRef or ( i == type(VariableCall) and i.isPtr):
                string += self.printTAC("refout", "_","_",label)
            else:
                string += self.printTAC("valout ", "_", "_", label) 
            
        string += self.printTAC("funccall","_","_",self.compressedTAC("glob",node.name)) 
        temp = "$v0"
        if "int" in node.type.type or "float" in node.type.type: 
            temp = self.saveticket.GetNextTicket()
            string += self.printTAC("assign","$v0","_",temp)
        return string, temp

    def visit_EmptyStatement(self,node):
        return "", ""

    def visit_Func(self,node):
        return None, None

    def visit_FuncDecl(self,node):
        return "", ""
        


    #PtrDecl: [name,type*,numindirections]
    def visit_PtrDecl(self,node):
        # No strings right now.
        # Floats and Ints need to be supported
        
        op = ""
        assignOP = ""
        string = ""
        name = node.name
        if not self.local:
            op = "glob"
            string += self.printTAC("global",name," ",str(4)) # hard codeness
            return string,self.compressedTAC(op,name)
        else:
            op = "local"
            # Create a local counter
            previousname = name
            name = str(self.localcount) #self.localticket.GetNextTicket()
            self.localcount += 1
            self.insertVariable(previousname,name)
        
        TypeOut,variable = self.visit(node.type)
        Type = TypeOut[0]
        Qual = TypeOut[1]
        if node.init != None:
            strings,initvalue = self.visit(node.init)
            string += strings
        else:
            initvalue = "-"
        
        if 'const' in Qual:
            #op = "const"
            # No idea here??
            pass
        else:
            finallabel = self.compressedTAC(op,name)
            #lets get down to the meat
            #for i in range(node.numindirections):
            #    nextlabel = self.GetTempLabel("int")
            #    string += self.printTAC("assign",self.compressedTAC("indr",finallabel),"-",nextlabel,node.text,node.lines)
            #    finallabel = nextlabel
            #raw_input()
            string += self.printTAC("assign",initvalue,"-",finallabel,node.text,node.lines) 
        # We need to add strings
        return string,self.compressedTAC(op,name)

    def visit_CompoundStatement(self,node):
        string = ""
        for i in node.stmts:
            if(i == None):
                continue
            cs, cl = self.visit(i)
            string += cs
        return string, ""


    # Return: [expr*]
    def visit_Return(self,node):
        string = ""

        if node.expr != None and node.expr != node:
            exprstring, exprlabel = self.visit(node.expr)
            string += exprstring
            string += self.printTAC("return","_","_",exprlabel,node.text,node.lines)
        else:
            string += self.printTAC("return","_","_","_",node.text,node.lines)
        #string += self.printTAC("return") + "\n"

        return string,""

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
        return self.OPCommand("Land",node)
    def visit_LorOp(self,node):
        return self.OPCommand("Lor",node)
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

    def visit_ModOp(self,node):                     # More Problems
        return self.OPCommand("mod",node)

    #[value*,type*]
    def UnaryOp(self,command,node):
        stringvalue,valuelabel = self.visit(node.value)
        Type,Qual = self.GetTypeInformation(node.type)
        if "int" in Type:
            templabel = self.inttemp.GetNextTicket()
        elif "float" in Type:
            templabel = self.floattemp.GetNextTicket()
        string = stringvalue 
        string += self.printTAC(command,valuelabel,"-",templabel,node.text,node.lines)
        return string,templabel

    # Unary Operators -- SMILE :D
    def visit_RefOp(self,node):
        return self.UnaryOp("addr",node)
    def visit_BitNotOp(self,node):
        return self.UnaryOp("bnot",node)
    def visit_LogNotOp(self,node):                  # This may be a problem in the future
        return self.UnaryOp("lnot",node)
    def visit_IndOp(self,node):
        return self.UnaryOp("indr",node)
    def visit_AbsOp(self,node):
        return self.UnaryOp("abs",node)
    def visit_NegOp(self,node):
        return self.UnaryOp("neg",node)

    def visit_Struct(self,node):
        op = ""
        assignOP = ""
        string = ""
        name = node.name
        if not self.local:
            op = "glob"
            string += self.printTAC("global",name,"_",node.size) # hard codeness
            return string,self.compressedTAC(op,name)
        else:
            op = "local"
            # Create a local counter
            previousname = name
            name = str(self.localcount) #self.localticket.GetNextTicket()
            self.localcount += 1
            self.insertVariable(previousname,name)
        

        #fieldstring,fieldlabel = self.visit(node.fields)

        
        #finallabel = self.compressedTAC(op,name)
        #lets get down to the meat

        string = self.printTAC("array",self.compressedTAC("cons",node.size),"-",self.compressedTAC(op,name),node.text,node.lines) 
        # We need to add strings
        return string,self.compressedTAC(op,name)
    def visit_StructDecl(self,node):
        self.offset[node.name] = node.size
        return "",node.name

    # StructRef: [name,field*,offset,type]
    def visit_StructRef(self,node):
        #print "STRUCT REF"
        op = ""
        assignOP = ""
        string = ""
        name = variableName = self.searchForVariable(node.name)
        if "glob" in name:
            name = variableName = self.compressedTAC("arrglob",node.name)

        fieldstring, fieldvalue = self.visit(node.field)
        #raw_input(fieldstring)
        #string += "MEOX\n"
        fieldstring = re.sub(";.*","",re.sub("arrglob " + node.field.name,"cons " +str(0),fieldstring),re.DOTALL)
        string += fieldstring
        #string += fieldstring
        #string += "BARK\n"
        templabel = self.GetTempLabel("int")
        string += self.printTAC("assign",name,"_",templabel,node.text,node.lines)
        string += self.printTAC("add",self.compressedTAC("cons",node.offset), templabel,templabel,"",None)

        if fieldstring != "":
            string += self.printTAC("add",re.sub('\)',"",re.sub('\(',"",re.sub("indr","",fieldvalue))),templabel,templabel,"",None)
        #string += self.printTAC("assign",self.compressedTAC("indr",templabel), "-", templabel,"",None)
        return string,self.compressedTAC("indr",templabel)

    #name,[name,type*,offset*]
    def visit_PtrRef(self,node):
        name = variableName = self.searchForVariable(node.name)
        offsetstring,offsetlabel = self.visit(node.offset)
        string = ""
        string += offsetstring
        templabel = self.GetTempLabel("int")
        string += self.printTAC("add",offsetlabel,name,templabel)
        string += self.printTAC("indr",templabel,"_",templabel)
        return string,templabel
    def visit_String(self,node):
        return "",""
