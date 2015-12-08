import sys
import re
from register_allocation import *
from stack_tracker import *

class Variable:
	def __init__(self,string):
		self.type = None
		self.name = None
		self.modifier = None
		if (len(string) == 1):
			self.name = string[0]
		elif(len(string) == 2):
			self.type = string[0]
			self.name = string[1]
		elif(len(string) == 3):
			self.type = string[1]
			self.modifier = string[0]
			self.name = string[2]
	def  __str__(self):
		string = ""
		if self.modifier != None:
			string += self.modifier + " "
		if self.type != None:
			string += self.type + " "
		if self.name != None:
			string += self.name
		return string

class Instruction:
	def __init__(self,string):
		self.name = string[0]
		self.one = Variable(self.Tuple(string[1]))
		self.two = Variable(self.Tuple(string[2]))
		self.three = Variable(self.Tuple(string[3]))

	def params(self):
		return [self.one, self.two, self.three]

	def Tuple(self,string):
		if " " in string:
			strlist = string.split(" ")
			return strlist
		else:
			string = [string] 
		return string
	def __str__(self):
		string = str(self.name)
		string += "," + str(self.one)
		string +=  "," + str(self.two)
		string +=  "," + str(self.three) + "\n"
		return string

class Function:
	def __init__(self,string):

		self.name = Variable(string[0][0].split(" ")).name

		# Getting arg count 
		self.argcount = int(Variable(string[1][0].split(" ")).name)

		# getting local word count
		self.localcount = int(Variable(string[2][0].split(" ")).name)

		del string[0]
		del string[0]
		del string[0]

		# parse the rest of everything else
		self.statements = map(Instruction,string)



class MipsGenerator:

	Frequency = []
	def __init__(self):
		# the local variable is for handling cases of global statements
		self.local = False
		self.registermap = RegisterAllocation()
		self.variableMap = {}
		self.removeList = []
		self.stackTracker = StackTracker()

	def MarkForRemove(self,parameters):
		self.removeList.append(parameters[0].name)
		self.removeList.append(parameters[1].name)
		self.removeList.append(parameters[2].name)

	def cleanUpVariableMap(self):
		for i in self.removeList:
			if i in self.variableMap:
				del self.variableMap[i]

	def call(self,funcname,parameters):
		method = funcname
		callfunc = getattr(self, method, None)

		if not callfunc:
			print("No Attribute of type " + funcname + " exists.")
			return "\t\tNot Implemented: " + funcname + "\n"
		return callfunc(parameters)

	def undef(self,parameters):
		print "UNDEFINED"
	def test(self,parameters):
		print "test"
	def assign(self,parameters):
		string = ""
		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = parameters[0]

		val = self.registerMap(value)

		# Loading constants
		if value.type == "cons":
			print reg
			string += "li " + reg + "," + str(val)  + "\n"
		else:
			string += "move " + reg + "," + str(val) + "\n"

		self.stackTracker.SetVariable(dest.name,4)
		# make the assignment happen
		string += "sw " + reg + ","+ str(self.stackTracker.GetVariable(dest.name)) + "($sp)"+ "\n"
		return string

	def registerMap(self,variable):
		if variable.name in self.variableMap:
			return self.variableMap[variable.name]
		if variable.type == "cons":
			return variable.name
		elif variable.type == "local":
			reg = self.registermap.getSavedRegister(variable.name)
			self.variableMap[variable.name] = reg
			return reg
		elif variable.type == "glob":
			pass
		reg = self.registermap.getTemporaryRegister(variable.name)
		self.variableMap[variable.name] = reg
		return reg

	def add(self,parameters):
		string = ""
		# figure out destination
		dest = parameters[2]
		
		reg = self.registerMap(dest)
		# Get value

		
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		if parameters[0].type == "cons":
			string += "addi " + reg + "," + value2 + "," + value + "\n"
		elif parameters[1].type == "cons":
			string += "addi " + reg + "," + value + "," + value2 + "\n"
		else:
			string += "add " + reg + "," + value + "," + value2 + "\n"
		return string  

	def label(self, parameters):
		return "\t" + parameters[2].name + ':\n'

	def br(self, parameters):
		return "\t\tj " + parameters[2].name + '\n'

	def Global(self,globals):
		self.local = False

	def function(self,function):
		self.local = True
		# Thank you https://courses.cs.washington.edu/courses/cse410/09sp/examples/MIPSCallingConventionsSummary.pdf
		string = function.name + ":\n"

		# handle stack stuff here
		# save registers from previous routine -- could save all 8
		savedregisters = 0

		# compute space for stack frame -- include space for return address
		stackspace = function.localcount + savedregisters + 1
		self.stackTracker.UpdateStackSize(stackspace*4)
		self.stackTracker.SetVariable("$ra",4)
		# store save registers

		# push stack frame 
		string += "\t\taddiu $sp,$sp,(-"+str(self.stackTracker.GetStackSize())+")\n"

		# store the return address
		string += "\t\tsw $ra," + str(self.stackTracker.GetVariable("$ra")) + "($sp)\n" 

		# Lets go through the statements
		for i in function.statements:
			string += self.call(i.name,i.params())
			self.MarkForRemove(i.params())

		# restore save registers

		# restore return address
		string += "\t\tlw $ra," + str(self.stackTracker.GetVariable("$ra")) + "($sp)\n" 
		string += "\t\taddiu $sp,$sp," + str(self.stackTracker.GetStackSize()) + "\n" # pop stack frame

 		# end of epilogue
 		string += "\t\tjr $ra" # return
 		print "============= Assembly ===================\n"
		print string
		print "\n============= Assembly ==================="
		self.cleanUpVariableMap()

	def Parse(self,string):
		Global,functions = self.TacSplit(string)
		Global,functions = self.ConstructData(functions,Global)
		for function in functions:
			self.call("function",function)
	def Intstructionize(self,li):
		return map(Instruction,li)
	def ConstructData(self,functions,Globals):
		self.Frequency.append({})
		Globals = map(Instruction,Globals)
		functions = map(Function,functions)
		return Globals,functions

	def TacSplit(self,string):
		string = re.sub(r'procentry','@',string)
		string = re.sub(r'endproc','@',string)

		functionstrings = re.findall(r"@[^\@]*@",string,re.DOTALL)

		string = re.sub(r'@[^\@]*@','',string,re.DOTALL)

		globalstatements = []
		for i in re.findall(r"\(.*\)",string):
			stmt = i.replace("(","")
			stmt = stmt.replace(")","")
			globalstatements.append(stmt)

		functionStmts = []
		for i in functionstrings:
			functionStmts.append(re.findall(r"\(.*\)",i))

		functions = []
		for function in functionStmts:
			functionlist = []
			for stmt in function:
				stringstmt = stmt.replace("(","")
				stringstmt = stringstmt.replace(")","")
				functionlist.append(map(str.strip,stringstmt.split(",")))
			functions.append(functionlist)

		Globals = []
		for i in globalstatements:
			b = i.split(",")
			Globals.append(map(str.strip,b))

		return Globals,functions

bas = open("log/3AC.tac",'r')
a = bas.read()

generator = MipsGenerator()
generator.Parse(a)
#generator.call("ttest","")
#generator.call("test","")

