import sys
import re
from register_allocation import *
from stack_tracker import *

class Variable:
	def __init__(self,string):
		self.type = None
		self.name = None
		self.modifier = None
		self.Frequency = 0
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
		#print string
		#raw_input()
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

	
	def __init__(self):
		# the local variable is for handling cases of global statements
		self.local = False
		self.registermap = RegisterAllocation()
		self.variableMap = {}
		self.removeList = []
		self.stackTracker = StackTracker()
		self.arguments = []
		self.Frequency = {}
	def MarkForRemove(self,parameters):
		self.removeList.append(parameters[0].name)
		self.removeList.append(parameters[1].name)
		self.removeList.append(parameters[2].name)

	def cleanUpVariableMap(self):
		for i in self.removeList:
			if i in self.variableMap:
				del self.variableMap[i]
		self.Frequency.clear()

	def call(self,funcname,parameters):
		method = funcname.upper()
		callfunc = getattr(self, method, None)

		if not callfunc:
			print("No Attribute of type " + funcname + " exists.")
			return "\t\t#Not Implemented: " + funcname + "\n"
		return callfunc(parameters)


	def registerMap(self, variable, force_register = False):
		if variable.type == "cons" and not force_register:
			if variable.name == '0':
				return "$zero"
			return variable.name

		if variable.type == "char" and not force_register:
			return variable.name

		if variable.name in self.variableMap:
			self.Frequency[variable.name] -= 1
			value = self.variableMap[variable.name]
			if self.Frequency[variable.name] <= 0:
				del self.variableMap[variable.name]
				self.registermap.freeRegisterByName(variable.name)
			return value
		elif variable.type == "local":
			reg = self.registermap.getSavedRegister(variable.name)
			self.variableMap[variable.name] = reg
			return reg
		elif variable.type == "glob":
			pass
		reg = self.registermap.getTemporaryRegister(variable.name)
		self.variableMap[variable.name] = reg
		return reg

	def FUNCCALL(self,parameters):
		return "jal " + parameters[2].name + "\n"
	def undef(self,parameters):
		print "UNDEFINED"
	def test(self,parameters):
		print "test"

	def ASSIGN(self,parameters):
		string = ""
		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = parameters[0]

		val = self.registerMap(value)

		# Loading constants
		if value.type == "cons" and not val.startswith('$'):
			#print reg
			string += "\t\tli " + reg + "," + str(val)  + "\n"
		elif value.type == "char":
			#print reg
			string += "\t\tli " + reg + ',' + str(val)  + '\n'
		else:
			string += "\t\tmove " + reg + "," + str(val) + "\n"

		self.stackTracker.SetVariable(dest.name,4)
		# make the assignment happen
		string += "\t\tsw " + reg + ","+ str(self.stackTracker.GetVariable(dest.name)) + "($sp)"+ "\n"
		return string

	def VALOUT(self,parameters):
		string = ""
		reg = self.arguments[0]
		val = self.registerMap(parameters[2])

		if parameters[2].type == "cons" and not val.startswith('$'):
			print reg
			string += "\t\tli " + reg + "," + str(val)  + "\n"
		elif parameters[2].type == "char":
			print reg
			string += "\t\tli " + reg + ',' + str(val)  + '\n'	
		else:
			string += "\t\tmove " + reg + "," + str(val) + "\n"

		del self.arguments[0]
		return string
	def REFOUT(self,parameters):
		string = ""
		reg = self.arguments[0]
		val = self.registerMap(parameters[2])

		if parameters[2].type == "cons" and not val.startswith('$'):
			print reg
			string += "\t\tli " + reg + "," + str(val)  + "\n"
		elif parameters[2].type == "char":
			print reg
			string += "\t\tli " + reg + ',' + str(val)  + '\n'
		else:
			string += "\t\tmove " + reg + "," + str(val) + "\n"

		del self.arguments[0]
		return string
	def ARGS(self,parameters):
		if parameters[2] < 5:
			for i in range(int(parameters[2].name)):
				self.arguments.append("$a" + str(i))
		else:
			pass
		return ""

	# (bound,(cons 50),0,(cons 1))
	def BOUND(self,parameters):
		string = ""
		Max = self.registerMap(parameters[0])
		Min = self.registerMap(parameters[1])
		value = self.registerMap(parameters[2])
		if parameters[0].type == "cons" and not val.startswith('$'):
			Max = self.registermap.getTemporaryRegister(Max)
			string += "\t\tli " + Max + "," + parameters[0].name + "\n"
		if parameters[1].type == "cons" and not val.startswith('$'):
			Min = self.registermap.getTemporaryRegister(Max)
			string += "\t\tli " + Min + "," + parameters[1].name + "\n"
		if parameters[2].type == "cons" and not val.startswith('$'):
			value = self.registermap.getTemporaryRegister(Max)
			string += "\t\tli " + value + "," + parameters[2].name + "\n"

		string += "\t\tbgt " + value + "," + Max + ",Halt\n"
		string += "\t\tblt " + value + "," + Min + ",Halt\n"
		return string
	def ARRAY(self,parameters):
		string = ""
		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = parameters[0]

		val = self.registerMap(value)

		four = self.registermap.getTemporaryRegister(-4)
		string += "\t\tli " + four + "," + str(-4)

		# Loading constants
		string += "\t\tmult " + val + "," + val + "," + four + "\n"

		string += "\t\taddu $sp,$sp,"+val+"\n"

		# -1 
		string += "\t\tli " + four + "," + str(-1) + "\n"

		# Loading constants
		string += "\t\tmult " + val + "," + val + "," + four + "\n"

		# Handle here
		self.stackTracker.SetVariable(dest.name,val)

		return string

	def ADD(self,parameters):
		string = ""
		# figure out destination
		dest = parameters[2]
		
		reg = self.registerMap(dest)
		# Get value

		
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		if parameters[0].type == "cons":
			string += "\t\taddi " + reg + "," + value2 + "," + value + "\n"
		elif parameters[1].type == "cons":
			string += "\t\taddi " + reg + "," + value + "," + value2 + "\n"
		else:
			string += "\t\tadd " + reg + "," + value + "," + value2 + "\n"
		return string 

	def SUB(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])

		if parameters[0].type == "cons":
			string += "\t\taddi " + reg + "," + value2 + "," + -value + "\n"
		elif parameters[1].type == "cons":
			string += "\t\taddi " + reg + "," + value + "," + -value2 + "\n"
		else:
			string += "\t\tsub " + reg + "," + value + "," + value2 + "\n"
		return string  

	def MULT(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		
		if parameters[0].type == "cons":
			temp = self.registermap.getTemporaryRegister(parameters[0].name)
			string += "\t\tmult " + reg + "," + temp + "," + value2 + "\n"
		elif parameters[1].type == "cons":
			temp = self.registermap.getTemporaryRegister(parameters[1].name)
			print temp
			print reg
			print value
			raw_input("PRESS ENTER HERE")
			string += "\t\tmult " + reg + "," + value + "," + temp + "\n"
		else:
			string += "\t\tmult " + reg + "," + value + "," + value2 + "\n"
		return string  

	def DIV(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		if parameters[0].type == "cons":
			temp = self.registermap.getTemporaryRegister(parameters[0].name)
			string += "\t\tdiv " + reg + "," + temp + "," + value2 + "\n"
		elif parameters[1].type == "cons":
			temp = self.registermap.getTemporaryRegister(parameters[1].name)
			string += "\t\tdiv " + reg + "," + value + "," + temp + "\n"
		else:
			string += "\t\tdiv " + reg + "," + value + "," + value2 + "\n"
		return string  

	def BRE(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2].name

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		string += "beq " + value + "," + value2 + "," + dest + "\n"
		return string 

	def BRNE(self,parameters):
		string = ""
		
		# figure out destination
		dest = parameters[2].name

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		string += "\t\tbne " + value + "," + value2 + "," + dest + "\n"
		return string

	def BGEZ(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		string += "bgez " + value + "," + value2 + "," + dest + "\n"
		return string 

	def BLEZ(self,parameters):
		string = ""
		
		# figure out destination
		dest = parameters[2]

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		string += "blez " + value + "," + value2 + "," + dest + "\n"
		return string

	def BGTZ(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		string += "bgtz " + value + "," + value2 + "," + dest + "\n"
		return string 

	def BLTZ(self,parameters):
		string = ""
		
		# figure out destination
		dest = parameters[2]

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		string += "bltz " + value + "," + value2 + "," + dest + "\n"
		return string

	def BGT(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		string += "bgt " + value + "," + value2 + "," + dest + "\n"
		return string

	def GT(self,parameters):
		string = ""
		
		# figure out destination
		dest = self.registerMap(parameters[2])

		# Get value
		value = self.registerMap(parameters[0], True)
		value2 = self.registerMap(parameters[1], True)

		if parameters[0].type == 'cons':
			string += "\t\tli " + value1 + "," + parameters[0].name + "\n"

		if parameters[1].type == 'cons':
			string += "\t\tli " + value2 + "," + parameters[1].name + "\n"
		
		string += "\t\tslt " + dest + "," + value2 + "," + value + "\n"
		self.registermap.freeRegisterByName(parameters[0].name)
		self.registermap.freeRegisterByName(parameters[1].name)
		return string

	def BLT(self,parameters):
		string = ""
		
		# figure out destination
		dest = parameters[2]

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		string += "blt " + value + "," + value2 + "," + dest + "\n"
		return string

	def LT(self,parameters):
		string = ""
		
		# figure out destination
		dest = self.registerMap(parameters[2])

		# Get value
		value = self.registerMap(parameters[0], True)
		value2 = self.registerMap(parameters[1], True)

		if parameters[0].type == 'cons':
			string += "\t\tli " + value1 + "," + parameters[0].name + "\n"

		if parameters[1].type == 'cons':
			string += "\t\tli " + value2 + "," + parameters[1].name + "\n"

		string += "\t\tslt " + dest + "," + value + "," + value2 + "\n"
		self.registermap.freeRegisterByName(parameters[0].name)
		self.registermap.freeRegisterByName(parameters[1].name)
		return string

	def BGE(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		string += "bge " + value + "," + value2 + "," + dest + "\n"
		return string 

	def BLE(self,parameters):
		string = ""
		
		# figure out destination
		dest = parameters[2]

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		string += "ble " + value + "," + value2 + "," + dest + "\n"
		return string

	def AND(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		if parameters[0].type == "cons":
			string += "\t\tandi " + reg + "," + value2 + "," + value + "\n"
		elif parameters[1].type == "cons":
			string += "\t\tandi " + reg + "," + value + "," + value2 + "\n"
		else:
			string += "\t\tand " + reg + "," + value + "," + value2 + "\n"
		return string 

	def OR(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		if parameters[0].type == "cons":
			string += "\t\tori " + reg + "," + value2 + "," + value + "\n"
		elif parameters[1].type == "cons":
			string += "\t\tori " + reg + "," + value + "," + value2 + "\n"
		else:
			string += "\t\tor " + reg + "," + value + "," + value2 + "\n"
		return string 

	def NOR(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		if parameters[0].type == "cons":
			temp = self.registermap.getTemporaryRegister(parameters[0].name)
			string += "\t\tnor " + reg + "," + temp + "," + value2 + "\n"
		elif parameters[1].type == "cons":
			temp = self.registermap.getTemporaryRegister(parameters[1].name)
			string += "\t\tnor " + reg + "," + value + "," + temp + "\n"
		else:
			string += "\t\tnor " + reg + "," + value + "," + value2 + "\n"
		return string 

	def XOR(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		if parameters[0].type == "cons":
			string += "\t\txori " + reg + "," + value2 + "," + value + "\n"
		elif parameters[1].type == "cons":
			string += "\t\txori " + reg + "," + value + "," + value2 + "\n"
		else:
			string += "\t\txor " + reg + "," + value + "," + value2 + "\n"
		return string 

	def SLLV(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		if parameters[0].type == "cons":
			string += "\t\tsll " + reg + "," + value2 + "," + value + "\n"
		elif parameters[1].type == "cons":
			string += "\t\tsll " + reg + "," + value + "," + value2 + "\n"
		else:
			string += "\t\tsllv " + reg + "," + value + "," + value2 + "\n"
		return string

	def SRLV(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		if parameters[0].type == "cons":
			string += "\t\tsrl " + reg + "," + value2 + "," + value + "\n"
		elif parameters[1].type == "cons":
			string += "\t\tsrl " + reg + "," + value + "," + value2 + "\n"
		else:
			string += "\t\tsrlv " + reg + "," + value + "," + value2 + "\n"
		return string		

	def SRAV(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		# Get value
		value = self.registerMap(parameters[0])
		value2 = self.registerMap(parameters[1])
		if parameters[0].type == "cons":
			string += "\t\tsra " + reg + "," + value2 + "," + value + "\n"
		elif parameters[1].type == "cons":
			string += "\t\tsra " + reg + "," + value + "," + value2 + "\n"
		else:
			string += "\t\tsrav " + reg + "," + value + "," + value2 + "\n"
		return string


	def LABEL(self, parameters):
		return "\t" + parameters[2].name + ':\n'

	def BR(self, parameters):
		return "\t\tj " + parameters[2].name + '\n'

	def Global(self,globals):
		self.local = False

	def FUNCTION(self,function):

		self.CountFrequency(function.statements)

		self.local = True
		# Thank you https://courses.cs.washington.edu/courses/cse410/09sp/examples/MIPSCallingConventionsSummary.pdf
		string = function.name + ":\n"

		# handle stack stuff here
		# save registers from previous routine -- could save all 8
		savedregisters = 0

		# compute space for stack frame -- include space for return address
		stackspace = function.localcount + savedregisters + 8
		self.stackTracker.UpdateStackSize(stackspace*4)
		self.stackTracker.SetVariable("$ra",4)
		self.stackTracker.SetVariable("$s0",4)
		self.stackTracker.SetVariable("$s1",4)
		self.stackTracker.SetVariable("$s2",4)
		self.stackTracker.SetVariable("$s3",4)
		self.stackTracker.SetVariable("$s4",4)
		self.stackTracker.SetVariable("$s5",4)
		self.stackTracker.SetVariable("$s6",4)
		self.stackTracker.SetVariable("$s7",4)
		# store save registers

		# push stack frame 
		string += "\t\taddiu $sp,$sp,-"+str(self.stackTracker.GetStackSize())+"\n"

		# store the return address
		string += "\t\tsw $ra," + str(self.stackTracker.GetVariable("$ra")) + "($sp)\n"
		string += "\t\tsw $s0," + str(self.stackTracker.GetVariable("$s0")) + "($sp)\n" 
		string += "\t\tsw $s1," + str(self.stackTracker.GetVariable("$s1")) + "($sp)\n" 
		string += "\t\tsw $s2," + str(self.stackTracker.GetVariable("$s2")) + "($sp)\n" 
		string += "\t\tsw $s3," + str(self.stackTracker.GetVariable("$s3")) + "($sp)\n" 
		string += "\t\tsw $s4," + str(self.stackTracker.GetVariable("$s4")) + "($sp)\n" 
		string += "\t\tsw $s5," + str(self.stackTracker.GetVariable("$s5")) + "($sp)\n"
		string += "\t\tsw $s6," + str(self.stackTracker.GetVariable("$s6")) + "($sp)\n" 
		string += "\t\tsw $s7," + str(self.stackTracker.GetVariable("$s7")) + "($sp)\n"   
		
		# Lets go through the statements
		for i in function.statements:			
			string += self.call(i.name,i.params())
			self.MarkForRemove(i.params())

		# restore save registers

		# restore return address
		string += "\t\tlw $ra," + str(self.stackTracker.GetVariable("$ra")) + "($sp)\n" 
		string += "\t\tlw $s0," + str(self.stackTracker.GetVariable("$s0")) + "($sp)\n" 
		string += "\t\tlw $s1," + str(self.stackTracker.GetVariable("$s1")) + "($sp)\n" 
		string += "\t\tlw $s2," + str(self.stackTracker.GetVariable("$s2")) + "($sp)\n" 
		string += "\t\tlw $s3," + str(self.stackTracker.GetVariable("$s3")) + "($sp)\n" 
		string += "\t\tlw $s4," + str(self.stackTracker.GetVariable("$s4")) + "($sp)\n" 
		string += "\t\tlw $s5," + str(self.stackTracker.GetVariable("$s5")) + "($sp)\n" 
		string += "\t\tlw $s6," + str(self.stackTracker.GetVariable("$s6")) + "($sp)\n"
		string += "\t\tlw $s7," + str(self.stackTracker.GetVariable("$s7")) + "($sp)\n"

		result = self.stackTracker.GetStackSize()
		if type(result) == tuple:
			i = result[0]
			a = self.registermap.getTemporaryRegister("temp")
			string += "\t\tli " + a + "," + str(i) + "\n"
			temps = result[1]
			string += "\t\taddu $sp,$sp,"+a + "\n"
			for i in temps:
				string += "\t\taddu $sp,$sp,"+i +"\n"
		else:
			string += "\t\taddiu $sp,$sp," + str(self.stackTracker.GetStackSize()) + "\n" # pop stack frame

 		# end of epilogue
 		string += "\t\tjr $ra" # return

		self.cleanUpVariableMap()
		self.registermap.clear()
		return string

	def CountFrequency(self,instructions):
		for i in instructions:
			params = i.params()
			for param in params:
				if param.name in self.Frequency:
					self.Frequency[param.name] += 1
				else:
					self.Frequency[param.name] = 1
		print self.Frequency
		raw_input()
	def Parse(self,string):
		Global,functions = self.TacSplit(string)
		Global,functions = self.ConstructData(functions,Global)

		Funcs = {}
		for function in functions:
			Funcs[function.name] = self.call("function",function) + "\n"
		string = Funcs["main"]

		del Funcs["main"]

		for func in Funcs:
			string += Funcs[func]

		printdata = open("src/print.s", "r")
		string += "\n\n#Adding Generated print functions\n\n" + printdata.read()
		printdata.close()
		return string

	def Instructionize(self,li):
		return map(Instruction,li)
	def ConstructData(self,functions,Globals):
		if Globals[0][0] != '':
			Globals = map(Instruction,Globals)
		functions = map(Function,functions)
		return Globals,functions

	def TacSplit(self,string):
		string = re.sub(r'procentry','@',string)
		string = re.sub(r'endproc','@',string)

		functionstrings = re.findall(r"@[^\@]*@",string,re.DOTALL)

		string = re.sub(r'@[^\@]*@','',string,re.DOTALL)
		string = re.sub(r';.*','',string)
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

		Globals = [['']]
		for i in globalstatements:
			b = i.split(",")
			Globals.append(map(str.strip,b))

		if string == "":
			Globals = [['']]

		return Globals,functions
