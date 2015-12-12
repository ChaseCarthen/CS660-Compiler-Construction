import sys
import re
from register_allocation import *
from stack_tracker import *

class Variable:
	def __init__(self,string):
		self.type = ""
		self.name = ""
		self.modifier = ""
		self.Frequency = 0
		if (len(string) == 1):
			self.name = string[0]
		elif(len(string) == 2):
			if string[0] == "indr" or string[0] == "addr":
				self.modifier = string[0]
			else:
				self.type = string[0]
			self.name = string[1]
		elif(len(string) == 3):
			self.type = string[1]
			self.modifier = string[0]
			self.name = string[2]
	def  __str__(self):
		string = ""
		if self.modifier != "":
			string += self.modifier + " "
		if self.type != "":
			string += self.type + " "
		if self.name != "":
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

	
	def __init__(self):
		# the local variable is for handling cases of global statements
		self.local = False
		self.registermap = RegisterAllocation()
		self.variableMap = {}
		self.removeList = []
		self.stackTracker = StackTracker()
		self.arguments = []
		self.Frequency = {}
	# Get a stack variable and return a register that contain the address for the variable
	def GetStackVariable(self,variablename):
		# generate a string
		string = ""
		offset = str(self.stackTracker.GetVariable(variablename))
		fixedsize = str(self.stackTracker.GetFixedStackSize())
		stacksymbol = self.stackTracker.GetStackSymbol()

		plist, temp = self.MagicFunction([(Variable(["tempor"]),True)])
		string += temp
		string += "\t\taddiu " + plist[0] + "," + stacksymbol + ",-" + fixedsize + "\n"
		string += "\t\taddiu " + plist[0] + "," + plist[0] + "," + offset + "\n"
		string += "\t\taddu " + plist[0] + ",$sp,"+plist[0] + "\n"
		return plist[0],string
		# addi temp reg, stack symbol, -size
		# addi temp reg, temp reg, -offset
		# add temp reg, $sp, temp reg
	def MarkForRemove(self,parameters):
		if parameters[0].type == "local" or parameters[0].type == "glob":
			self.removeList.append(parameters[0].type + "_" + parameters[0].name)
		else:
			self.removeList.append(parameters[0].name)
		if parameters[1].type == "local" or parameters[1].type == "glob":
			self.removeList.append(parameters[1].type + "_" + parameters[1].name)
		else:
			self.removeList.append(parameters[0].name)
		if parameters[2].type == "local" or parameters[2].type == "glob":
			self.removeList.append(parameters[2].type + "_" + parameters[2].name)
		else:
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
				variable.type = "reg"
				return "$zero"
			
			return variable.name

		if variable.type == "char" and not force_register:
			return variable.name

		if variable.type == "arg":
			return variable.name

		check = variable.type + "_" + variable.name
		if check in self.variableMap:
			if check in self.Frequency:
				self.Frequency[check] -= 1
			value = self.variableMap[check]
			if check in self.Frequency and self.Frequency[check] <= 0:
				del self.variableMap[check]
				self.registermap.freeRegisterByName(check)
			variable.type = "reg"
			if "i_" in variable.name:
				self.registermap.InsertIntoRecentMap(value)
			return value
		elif variable.type == "local":
			reg = self.registermap.getSavedRegister(check)
			self.variableMap["local_" + variable.name] = reg
			return reg
		elif variable.type == "glob":
			pass
		reg = self.registermap.getTemporaryRegister(check)
		if "i_" in variable.name or variable.type == "cons":
			self.registermap.InsertIntoRecentMap(reg)
		

		if variable.type != "cons":
			self.variableMap[check] = reg
		variable.type = "reg"
		#print self.Frequency
		if check in self.Frequency:
			#print check
			#print self.Frequency[check]
			#raw_input("DEC")
			self.Frequency[check] -= 1
		return reg

	def FUNCCALL(self,parameters):
		return "\t\tjal " + parameters[2].name + "\n"
	def undef(self,parameters):
		print "UNDEFINED"
	def test(self,parameters):
		print "test"

	def ASSIGN(self,parameters):
		string = "#assign \n"
		# figure out destination
		dest = parameters[2]

		#reg = self.registerMap(dest)

		# Get value
		value = parameters[0]

		#val = self.registerMap(value)

		plist, temp = self.MagicFunction(  [(parameters[0],False), (parameters[2],False) ],False )

		reg = plist[1]
		val = plist[0]


		string += temp

		tempor,temp = self.MagicFunction([( Variable(["temp"]), True) ])
		tempor = tempor[0]
		string += temp

		# Loading constants
		if value.type == "" or value.type == "cons" or value.type == "char":
			#print reg
			string += "\t\tli " + tempor + "," + str(val)  + "\n"
		else:
			string += "\t\tmove " + tempor + "," + str(val) + "#assig\n"

		#self.stackTracker.SetVariable(dest.type+"_"+dest.name,4)
		if parameters[2].type == "local" and not parameters[2].type == "indr":
			#raw_input(reg)
			string += self.StoreOntoStack(tempor,reg)
			string += "\t\tmove " + reg + "," + tempor + "\n" 
		elif parameters[2].modifier == "indr":
			string += "\t\tsw " + tempor + "," + "(" + reg + ")# indr here" + "\n"
			string += "\t\tmove " + reg + "," + tempor + "\n"
		else:
			string += "\t\tmove " + reg + "," + tempor + "\n"

		# make the assignment happen
		#string += "\t\tsw " + reg + ","+ str(self.stackTracker.GetVariable(dest.type+"_"+dest.name)) + "($sp)"+ "\n"

		return string

	def VALOUT(self,parameters):
		string = ""
		string = ""
		plist,string = self.MagicFunction( [ ( parameters[2] ,True)  ] )
		reg = self.arguments[0]
		val = plist[0]
		#val = self.registerMap(parameters[2])

		if parameters[2].type == "cons" and not val.startswith('$'):
			#print reg
			string += "\t\tli " + reg + "," + str(val)  + "\n"
		elif parameters[2].type == "char":
			#print reg
			string += "\t\tli " + reg + ',' + str(val)  + '\n'	
		else:
			string += "\t\tmove " + reg + "," + str(val) + "\n"

		del self.arguments[0]
		return string
	def REFOUT(self,parameters):
		string = ""
		plist,string = self.MagicFunction( [ ( parameters[2] ,False)  ] )
		reg = self.arguments[0]
		val = plist[0]#self.registerMap(parameters[2])

		if parameters[2].type == "cons" and not val.startswith('$'):
			#print reg
			string += "\t\tli " + reg + "," + str(val)  + "\n"
		elif parameters[2].type == "char":
			#print reg
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
		#Max = self.registerMap(parameters[0])
		#Min = self.registerMap(parameters[1])
		#val = self.registerMap(parameters[2])
		force1 = parameters[0].type == "cons" or parameters[2].type == "char"
		force2 = parameters[1].type == "cons" or parameters[2].type == "char"
		force3 = parameters[2].type == "cons" or parameters[2].type == "char"

		plist,temp = self.MagicFunction([(parameters[0],force1),(parameters[1],force2),(parameters[2],force3)])
		Max = plist[0]
		Min = plist[1]
		value = plist[2]
		string += temp
		#if parameters[0].type == "cons":
		#	string += "\t\tli " + Max + "," + parameters[0].name + "\n"
		#if parameters[1].type == "cons":
		#	string += "\t\tli " + Min + "," + parameters[1].name + "\n"
		#if parameters[2].type == "cons":
		#	string += "\t\tli " + str(value) + "," + str(parameters[2].name) + "\n"

		string += "\t\tbgt " + str(value) + "," + str(Max) + ",Halt\n"
		string += "\t\tblt " + str(value) + "," + str(Min) + ",Halt\n"
		self.registermap.freeRegisterByName(Max)
		return string
	def ARRAY(self,parameters):
		string = ""

		plist,temp = self.MagicFunction([(parameters[0],True), (parameters[2],True)])

		string += temp

		# figure out destination
		dest = parameters[2]

		reg = plist[1]#self.registerMap(dest)

		# Get value
		#value = parameters[0]

		val = plist[0]#self.registerMap(value)

		four = self.registermap.getTemporaryRegister(4)
		self.registermap.freeRegisterByName(4)

		#self.stackTracker.SetVariable(dest.type+"_"+dest.name,4)

		string += "\t\tli " + four + "," + str(4) + "\n"

		# Loading constants

		#string += "\t\tmul " + plist[0] + "," + val + "," + four + "\n"
		string += "\t\tmult " + val + "," + four + "\n"
		string += "\t\tmflo " + plist[0] + "\n"

		#string += "\t\tsubu $sp,$sp,"+plist[0]+"\n"
		string += self.stackTracker.AddToStack(plist[0])

		r,temp = self.GetStackVariable(reg)
		string += temp

		string += "\t\tsw $sp," + "(" + r + ")" + "# Here\n"
		string += "\t\tmove " + plist[1] + ",$sp# FLLLLLL\n"
		# -1 
		#string += "\t\tli " + four + "," + str(-1) + "\n"

		# Loading constants
		#string += "\t\tmult " + plist[0] + "," + plist[0] + "," + four + "\n"

		
		# Handle here
		#self.stackTracker.SetVariable(dest.name,plist[1])

		return string

	def ADD(self,parameters):
		string = ""
		plist,s = self.MagicFunction( ((parameters[0],False),(parameters[1],False), (parameters[2],False)) )
		string += s
		if parameters[0].type == "cons":
			string += "\t\taddi " + str(plist[2]) + "," + str(plist[1]) + "," + str(plist[0]) + "\n"
		elif parameters[1].type == "cons":
			string += "\t\taddi " + str(plist[2]) + "," + str(plist[0]) + "," + str(plist[1]) + "\n"
		else:
			string += "\t\tadd " + str(plist[2]) + "," + str(plist[1]) + "," + str(plist[0]) + "\n"
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
			string += "\t\taddi " + reg + "," + value2 + "," + '-' + value + "\n"
		elif parameters[1].type == "cons":
			string += "\t\taddi " + reg + "," + value + "," + '-' + value2 + "\n"
		else:
			string += "\t\tsub " + reg + "," + value + "," + value2 + "\n"
		return string

	def MagicFunction(self,parameters,indr=True):
		string = ""
		parameterlist = []
		freelist = []
		for params in parameters:
			force = params[1]
			i = params[0]
			if i.name == "$v0":
				parameterlist.append(i.name)
				continue
			if i.name == "-" or i.name == " " or i.name == "_":
				#parameterlist.append('0')
				i.name = '0'
				#i.type = 'cons'
				freelist.append(i.type + "_" + '0')
			if (i.type == "cons" or i.type == "fcons" or i.type == "char") and force: # Luke use the force
				freelist.append(i.type + "_" + i.name)
				reg = self.registerMap(i,force)
				string += "\t\tli " + reg + "," + i.name + "\n"

				parameterlist.append(reg)
			else:
				#freelist.append(i.type + "_" + i.name)
				#i.type = 'reg'
				reg = self.registerMap(i)
				if i.modifier == "indr" and indr:
					string += "\t\tlw " + reg + "," + "(" + reg + ")# load indr here" + "\n"
					#raw_input("LOADING")
				parameterlist.append(reg)
		for free in freelist:
			self.registermap.freeRegisterByName(free)
		#print freelist
		#print parameterlist
		self.registermap.ClearRecentMap()
		return parameterlist,string

	def MULT(self,parameters):
		string = ""

		# figure out destination
		#dest = parameters[2]
		#reg = self.registerMap(dest)
		plist,s = self.MagicFunction( ((parameters[0],True),(parameters[1],True), (parameters[2],False)) )
		string += s

		string += "\t\tmult " +  plist[0] + "," + plist[1] + "\n"
		string += "\t\tmflo " + plist[2] + "\n"
		return string  

	def DIV(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2]
		reg = self.registerMap(dest)

		if parameters[0].type == "cons":
			plist,s = self.MagicFunction( ((parameters[0],True),(parameters[1],False), (parameters[2],False)) )
			string += s
			string += "\t\tdiv " + plist[0] + "," + plist[1] + "," + plist[2] + "\n"
		elif parameters[1].type == "cons":
			plist,s = self.MagicFunction( ((parameters[0],False),(parameters[1],True), (parameters[2],False)) )
			string += s
			string += "\t\tdiv " + plist[0] + "," + plist[1] + "," + plist[2] + "\n"
		else:
			plist,s = self.MagicFunction( ((parameters[0],False),(parameters[1],False), (parameters[2],False)) )
			string += s
			string += "\t\tdiv " + plist[0] + "," + plist[1] + "," + plist[2] + "\n"
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

		reglist, temp = self.MagicFunction([(parameters[0], True), (parameters[1], True), (parameters[2], False)])
		
		string += temp
		string += "\t\tslt " + reglist[2] + "," + reglist[1] + "," + reglist[0] + "\n"

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

		reglist, temp = self.MagicFunction([(parameters[0], True), (parameters[1], True), (parameters[2], False)])
		
		string += temp
		string += "\t\tslt " + reglist[2] + "," + reglist[0] + "," + reglist[1] + "\n"
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
			self.registermap.freeRegisterByName(parameters[0].name)
			string += "\t\tnor " + reg + "," + temp + "," + value2 + "\n"
		elif parameters[1].type == "cons":
			temp = self.registermap.getTemporaryRegister(parameters[1].name)
			self.registermap.freeRegisterByName(parameters[1].name)
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

	def RETURN(self, parameters):
		string = ""

		reg, temp = self.MagicFunction([(parameters[2],True)])

		string += temp
		string += "\t\tmove " + "$v0, " + reg[0] + "\n"

		# restore return address
		string += "#Restoring Stack\n"
		string += self.LoadOntoStack("$ra","$ra") 
		string += self.LoadOntoStack("$s0","$s0")
		string += self.LoadOntoStack("$s1","$s1")
		string += self.LoadOntoStack("$s2","$s2")
		string += self.LoadOntoStack("$s3","$s3")
		string += self.LoadOntoStack("$s4","$s4")
		string += self.LoadOntoStack("$s5","$s5")
		string += self.LoadOntoStack("$s6","$s6")
		string += self.LoadOntoStack("$s7","$s7")

 		# end of epilogue
 		string += "\t\tjr $ra" # return
		return string

	def Global(self,globals):
		self.local = False

	def StoreOntoStack(self,register,stackregister):
		string = ""
		reg,temp = self.GetStackVariable(stackregister)
		string += temp
		string += "\t\tsw " + register + ",(" + reg +")\n"
		return string

	def LoadOntoStack(self,register,stackregister):
		string = ""
		reg,temp = self.GetStackVariable(stackregister)
		string += temp
		string += "\t\tlw " + register + ",(" + reg +")\n"
		return string 

	def FUNCTION(self,function):
		reg = self.registermap.getTemporaryRegister("stack")
		self.stackTracker.SetStackSymbol(reg)
		self.CountFrequency(function.statements)

		self.local = True
		# Thank you https://courses.cs.washington.edu/courses/cse410/09sp/examples/MIPSCallingConventionsSummary.pdf
		string = function.name + ":\n"

		# handle stack stuff here
		# save registers from previous routine -- could save all 8
		savedregisters = 0

		# compute space for stack frame -- include space for return address
		stackspace = function.localcount + savedregisters + 9
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
		#string += "\t\taddiu $sp,$sp,-"+str(self.stackTracker.GetStackSize())+"\n"
		v = Variable(["cons",str(self.stackTracker.GetStackSize())])
		reg, temp = self.MagicFunction([(v,True)])
		string += temp
		string += self.stackTracker.AddToStack(reg[0],True)

		# store the return address
		string += "#Setting Stack\n"
		string += self.StoreOntoStack("$ra","$ra")
		string += self.StoreOntoStack("$s0","$s0")
		string += self.StoreOntoStack("$s1","$s1")
		string += self.StoreOntoStack("$s2","$s2")
		string += self.StoreOntoStack("$s3","$s3")
		string += self.StoreOntoStack("$s4","$s4")
		string += self.StoreOntoStack("$s5","$s5")
		string += self.StoreOntoStack("$s6","$s6")
		string += self.StoreOntoStack("$s7","$s7")
		sreg = self.registermap.getSavedRegister("stack")
		string += self.stackTracker.updateStackSymbol(sreg)
		self.registermap.freeRegisterByName("stack")
		

		# Lets go through the statements
		for i in function.statements:			
			string += self.call(i.name,i.params())
			self.MarkForRemove(i.params())

		# restore save registers

		# restore return address
		string += "#Restoring Stack\n"
		string += self.LoadOntoStack("$ra","$ra") 
		string += self.LoadOntoStack("$s0","$s0")
		string += self.LoadOntoStack("$s1","$s1")
		string += self.LoadOntoStack("$s2","$s2")
		string += self.LoadOntoStack("$s3","$s3")
		string += self.LoadOntoStack("$s4","$s4")
		string += self.LoadOntoStack("$s5","$s5")
		string += self.LoadOntoStack("$s6","$s6")
		string += self.LoadOntoStack("$s7","$s7")

		string += self.stackTracker.ResetStack()
 		# end of epilogue
 		string += "\t\tjr $ra" # return

		self.cleanUpVariableMap()
		self.registermap.clear()
		self.stackTracker.Clear()
		return string

	def CountFrequency(self,instructions):
		for i in instructions:
			params = i.params()
			for param in params:
				if param.type+"_"+param.name in self.Frequency:
					self.Frequency[param.type+"_"+param.name] += 1
				else:
					self.Frequency[param.type+"_"+param.name] = 1
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
		string += "Halt: " + "\n"
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
		string = re.sub(r';.*','',string)
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

		Globals = [['']]
		for i in globalstatements:
			b = i.split(",")
			Globals.append(map(str.strip,b))

		if string == "":
			Globals = [['']]

		return Globals,functions
