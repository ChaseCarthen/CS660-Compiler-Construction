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

		#plist, temp = self.MagicFunction([(Variable(["tempor"]),True)])
		treg = self.registermap.getTemporaryRegister("ss")
		#raw_input(stacksymbol + "_" + treg)
		#string += temp
		string += "\t\taddiu " + treg + "," + stacksymbol + ",-" + fixedsize + "\n"
		string += "\t\taddiu " + treg + "," + treg + "," + offset + "\n"
		string += "\t\taddu " + treg + ",$sp,"+treg + "\n"
		self.registermap.freeRegisterByName("ss")
		return treg,string
		# addi temp reg, stack symbol, -size
		# addi temp reg, temp reg, -offset
		# add temp reg, $sp, temp reg
	def MarkForRemove(self,parameters):
		if parameters[0].type == "local" or parameters[0].type == "glob" or parameters[0].type == "arrglob":
			self.removeList.append(parameters[0].type + "_" + parameters[0].name)
		else:
			self.removeList.append(parameters[0].name)
		if parameters[1].type == "local" or parameters[1].type == "glob" or parameters[1].type == "arrglob":
			self.removeList.append(parameters[1].type + "_" + parameters[1].name)
		else:
			self.removeList.append(parameters[0].name)
		if parameters[2].type == "local" or parameters[2].type == "glob" or parameters[2].type == "arrglob":
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
			if variable.type != "local" and variable.type != "glob" and variable.type != "arrglob":
				variable.type = "reg"
			if "i_" in variable.name:
				self.registermap.InsertIntoRecentMap(value)
			return value
		elif variable.type == "local":
			reg = self.registermap.getSavedRegister(check)
			if reg == 0:
				# shot one of the saved registers
				name = self.registermap.freeASavedRegister()
				del self.variableMap[name]
				reg = self.registermap.getSavedRegister(check)
			self.registermap.InsertIntoRecentMap(reg)
			self.variableMap["local_" + variable.name] = reg
			return reg
		elif variable.type == "glob":
			reg = self.registermap.getSavedRegister(check)
			if reg == 0:
				# shot one of the saved registers
				name = self.registermap.freeASavedRegister()
				del self.variableMap[name]
				reg = self.registermap.getSavedRegister(check)
			self.registermap.InsertIntoRecentMap(reg)
			self.variableMap["glob_" + variable.name] = reg
			return reg
		elif variable.type == "arrglob":
			reg = self.registermap.getSavedRegister(check)
			if reg == 0:
				# shot one of the saved registers
				name = self.registermap.freeASavedRegister()
				del self.variableMap[name]
				reg = self.registermap.getSavedRegister(check)
			self.registermap.InsertIntoRecentMap(reg)
			self.variableMap["arrglob_" + variable.name] = reg
			return reg
		reg = self.registermap.getTemporaryRegister(check)
		if "i_" in variable.name or variable.type == "cons" or "save_" in variable.name:
			self.registermap.InsertIntoRecentMap(reg)
		

		if variable.type != "cons":
			self.variableMap[check] = reg
		if variable.type != "local" and variable.type != "glob" and variable.type != "arrglob":
			variable.type = "reg"
		#print self.Frequency
		if check in self.Frequency:
			#print check
			#print self.Frequency[check]
			#raw_input("DEC")
			self.Frequency[check] -= 1
		return reg

	def FUNCCALL(self,parameters):
		string = ""
		string += "\t\tjal " + parameters[2].name + "\n"
		string += "# Resetting arguments\n"
		string += self.LoadFromStack("$a0","$a0")
		string += self.LoadFromStack("$a1","$a1")
		string += self.LoadFromStack("$a2","$a2")
		string += self.LoadFromStack("$a3","$a3")
		string += "# Done Resetting arguments\n"
		return string

	def undef(self,parameters):
		print "UNDEFINED"
	def test(self,parameters):
		print "test"

	def ASSIGN(self,parameters):
		string = "# Assign Began\n"
		# figure out destination
		dest = parameters[2]

		#reg = self.registerMap(dest)

		# Get value
		value = parameters[0]

		#val = self.registerMap(value)
		ty = parameters[2].type
		ty2 = parameters[0].type
		tempor = self.registermap.getTemporaryRegister("test")
		plist, temp = self.MagicFunction(  [(parameters[0],False), (parameters[2],False) ],False )

		reg = plist[1]
		val = plist[0]


		if parameters[0].modifier == "indr":
			string += "\t\tlw " + val + "," + "(" + val + ")# load indr here" + "\n"

		string += temp


		
		if tempor == reg:
			print "SCARY"
		#tempor = tempor[0]
		#string += temp



		# Loading constants
		if value.type == "" or value.type == "cons" or value.type == "char":
			#print reg
			string += "\t\tli " + tempor + "," + str(val)  + "\n"
		else:
			string += "\t\tmove " + tempor + "," + str(val) + "\n"

		#self.stackTracker.SetVariable(dest.type+"_"+dest.name,4)
		if parameters[2].type == "local" and not parameters[2].type == "indr":
			string += self.StoreOntoStack(tempor, parameters[2].type + "_" +parameters[2].name)
			string += "\t\tmove " + reg + "," + tempor + "\n"
		elif parameters[2].type == "glob" and not parameters[2].type == "indr":
			string += "\t\tmove " + reg + "," + tempor + "\n"
			string += "\t\t" 
		elif parameters[2].modifier == "indr":
			string += "\t\tsw " + tempor + "," + "(" + reg + ")# indr here" + "\n"
			string += "\t\tmove " + reg + "," + tempor + "\n"
		else:
			string += "\t\tmove " + reg + "," + tempor + "\n"

		# make the assignment happen
		if ty == "glob":
			#raw_input("HERE")
			regs = self.registermap.getTemporaryRegister("ss")
			string += "\t\tla " + regs + ", GLOBAL_" + parameters[2].name + " # glob \n" 
			string += "\t\tsw " + reg + ",(" + regs + ") # glob\n"
			self.registermap.freeRegisterByName("ss")
		self.registermap.freeRegisterByName("test")

		string += "# Assign Ends\n"
		return string

	def VALOUT(self,parameters):
		string = "# VALOUT Began\n"
		plist,temp = self.MagicFunction( [ ( parameters[2] ,True)  ] )
		string += temp
		reg = self.arguments[0]
		val = plist[0]
		#val = self.registerMap(parameters[2])
		if parameters[2].type == "local":
			string += self.LoadFromStack(reg,parameters[2].type+ "_" + parameters[2].name)
		elif parameters[2].type == "cons" and not val.startswith('$'):
			#print reg
			string += "\t\tli " + reg + "," + str(val)  + "\n"
		elif parameters[2].type == "char":
			#print reg
			string += "\t\tli " + reg + ',' + str(val)  + '\n'	
		else:
			string += "\t\tmove " + reg + "," + str(val) + "\n"

		del self.arguments[0]

		string += "# VALOUT End\n"
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
		plist,s = self.MagicFunction( ((parameters[0],True),(parameters[1],True), (parameters[2],True)) )
		string += s
		string += "\t\tsub " + str(plist[2]) + "," + str(plist[0]) + "," + str(plist[1]) + "\n"
		return string 

	def MagicFunction(self,parameters,indr=True):
		string = ""
		parameterlist = []
		freelist = []

		for params in parameters:

			force = params[1]
			i = params[0]

			#if self.stackTracker.saved and self.stackTracker.GetSaveName() == i.name:
			#	reg = self.registerMap(i)
			#	string += "\t\tlw " +reg + "," + "($sp) # BLAD\n"
			#	string += self.stackTracker.PopOffStack()
			#	parameterlist.append(reg)
			#	raw_input("HERE")
			#	self.stackTracker.SetSaved(False)

			# Got to love this patch that uses a save_ keyword for storing stuff onto stack temporaily
			if not indr and "save_" in i.name:
				if self.Frequency["_"+i.name] > 1:
					string += self.stackTracker.PushOntoStack()
					
					reg = self.registerMap(i,True)

					parameterlist.append(reg)
				else:
					#i.type = "reg"
					parameterlist.append("$v0")
				continue
			elif "save_" in i.name:
				reg = self.registerMap(i,True)
				#reg = self.registermap.getTemporaryRegister("$test")
				string += "\t\tlw " +reg + "," + "($sp)\n"
				if self.Frequency["_"+i.name] == 0:
					string += self.stackTracker.PopOffStack()
				#self.registermap.freeRegisterByName("$test")
				parameterlist.append(reg)
				continue

			if i.name == "$v0":
				i.type = "reg"
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
				ty = i.type
				reg = self.registerMap(i)
				if ty == "glob" and i.modifier != "indr":
					#raw_input("HERE")
					string += "\t\tla " + reg + ",GLOBAL_" + i.name + "\n"
					string += "\t\tlw " + reg + ",(" + reg + ")\n"
				elif ty == "arrglob":
					string += "\t\tla " + reg + ",GLOBAL_" + i.name + "#ARRGLOB\n"
				if i.modifier == "indr" and indr and ty != "glob" and ty != "arrglob":
					string += "\t\tlw " + reg + "," + "(" + reg + ")# load indr here" + "\n"

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
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True) ])
		string += temp
		string += "\t\tbeq " + plist[0] + "," + plist[1] + "," + dest + "\n"
		return string 

	def EQ(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		string += "\t\txor " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
		string += "\t\tslti " + plist[2] + "," + plist[2] + "," + "1" + "\n"
		return string 

	def BNE(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2].name

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True) ])
		string += temp
		string += "\t\tbne " + plist[0] + "," + plist[1] + "," + dest + "\n"
		return string 

	def NE(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		string += "\t\txor " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
		return string 

	def BGEZ(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2].name

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True) ])
		string += temp
		string += "\t\tbgez " + plist[0] + "," + plist[1] + "," + dest + "\n"
		return string 
	def BLEZ(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2].name

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True) ])
		string += temp
		string += "\t\tblez " + plist[0] + "," + plist[1] + "," + dest + "\n"
		return string 

	def BGTZ(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2].name

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True) ])
		string += temp
		string += "\t\tbgtz " + plist[0] + "," + plist[1] + "," + dest + "\n"
		return string 

	def BLTZ(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2].name

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True) ])
		string += temp
		string += "\t\tbltz " + plist[0] + "," + plist[1] + "," + dest + "\n"
		return string 

	def BGT(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2].name

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True) ])
		string += temp
		string += "\t\tbgt " + plist[0] + "," + plist[1] + "," + dest + "\n"
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
		dest = parameters[2].name

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True) ])
		string += temp
		string += "\t\tblt " + plist[0] + "," + plist[1] + "," + dest + "\n"
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
		dest = parameters[2].name

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True) ])
		string += temp
		string += "\t\tbge " + plist[0] + "," + plist[1] + "," + dest + "\n"
		return string 

	def GE(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		string += "\t\txor " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
		string += "\t\tslti " + plist[2] + "," + plist[2] + "," + "1" + "\n"
		treg = self.registermap.getTemporaryRegister("GETemp")
		string += "\t\tslt " + treg + "," + plist[1] + "," + plist[0] + "#GETEMP\n"
		string += "\t\tor " + plist[2] + "," + plist[2] + "," + treg + "\n"
		self.registermap.freeRegisterByName("GETemp")
		return string 

	def BLE(self,parameters):
		string = ""

		# figure out destination
		dest = parameters[2].name

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True) ])
		string += temp
		string += "\t\tble " + plist[0] + "," + plist[1] + "," + dest + "\n"
		return string 

	def LE(self,parameters):
		string = ""
		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		string += "\t\txor " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
		string += "\t\tslti " + plist[2] + "," + plist[2] + "," + "1" + "\n"
		treg = self.registermap.getTemporaryRegister("GETemp")
		string += "\t\tslt " + treg + "," + plist[0] + "," + plist[1] + "\n"
		string += "\t\tor " + plist[2] + "," + plist[2] + "," + treg + "#LETEMP\n"
		self.registermap.freeRegisterByName("GETemp")
		return string 

	def LAND(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		string += "\t\tand " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		string += "\t\tslti " + plist[2] + "," + plist[2] + "," + "1" + "\n"
		string += "\t\txori " + plist[2] + "," + plist[2] + "," + "1\n"
		return string 

	def LOR(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		string += "\t\tor " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		string += "\t\tslti " + plist[2] + "," + plist[2] + "," + "1" + "\n"
		string += "\t\txori " + plist[2] + "," + plist[2] + "," + "1\n"
		return string 

	def AND(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp

		if parameters[0].type == "cons":
			string += "\t\tandi " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
		elif parameters[1].type == "cons":
			string += "\t\tandi " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		else:
			string += "\t\tand " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		return string 

	def OR(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp

		if parameters[0].type == "cons":
			string += "\t\tori " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
		elif parameters[1].type == "cons":
			string += "\t\tori " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		else:
			string += "\t\tor " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		return string 

	def NOR(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		string += "\t\tnor " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		return string 

	def XOR(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp

		if parameters[0].type == "cons":
			string += "\t\txori " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
		elif parameters[1].type == "cons":
			string += "\t\txori " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		else:
			string += "\t\txor " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		return string 

	def SLLV(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		
		if parameters[0].type == "cons":
			string += "\t\tsll " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
		elif parameters[1].type == "cons":
			string += "\t\tsll " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		else:
			string += "\t\tsllv " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		return string

	def SRLV(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		
		if parameters[0].type == "cons":
			string += "\t\tsrl " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
		elif parameters[1].type == "cons":
			string += "\t\tsrl " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		else:
			string += "\t\tsrlv " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		return string		

	def SRAV(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		
		if parameters[0].type == "cons":
			string += "\t\tsra " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
		elif parameters[1].type == "cons":
			string += "\t\tsra " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		else:
			string += "\t\tsrav " + plist[2] + "," + plist[0] + "," + plist[1] + "\n"
		return string

	def MOD(self,parameters):
		string = ""

		# Get value
		plist,temp = self.MagicFunction([ (parameters[0],True), (parameters[1],True), (parameters[2],True) ])
		string += temp
		string += "\t\trem " + plist[2] + "," + plist[1] + "," + plist[0] + "\n"
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

		treg = self.registermap.getTemporaryRegister("stack")
		#print self.stackTracker.GetStackSymbol()
		#print treg
		#raw_input("a")
		oldstacksymbol = self.stackTracker.GetStackSymbol()
		string += "\t\tmove " + treg + "," + self.stackTracker.GetStackSymbol() + "\n"

		self.stackTracker.SetStackSymbol(treg)

		# restore return address
		string += "\n#Restoring Stack\n"
		string += self.LoadFromStack("$ra","$ra") 
		string += self.LoadFromStack("$s0","$s0")
		string += self.LoadFromStack("$s1","$s1")
		string += self.LoadFromStack("$s2","$s2")
		string += self.LoadFromStack("$s3","$s3")
		string += self.LoadFromStack("$s4","$s4")
		string += self.LoadFromStack("$s5","$s5")
		string += self.LoadFromStack("$s6","$s6")
		string += self.LoadFromStack("$s7","$s7")
		string += self.LoadFromStack("$a0","$a0")
		string += self.LoadFromStack("$a1","$a1")
		string += self.LoadFromStack("$a2","$a2")
		string += self.LoadFromStack("$a3","$a3")
		string += self.stackTracker.ResetStack()
		self.registermap.freeRegisterByName("stack")
		self.stackTracker.SetStackSymbol(oldstacksymbol)
		string += "#Restoring Stack Complete\n\n"
 		# end of epilogue
 		string += "\t\tjr $ra\n" # return
		return string

	def Global(self,globals):
		self.local = False

	def StoreOntoStack(self,register,stackregister):
		string = ""
		reg,temp = self.GetStackVariable(stackregister)
		string += temp
		string += "\t\tsw " + register + ",(" + reg +")\n"
		return string

	def LoadFromStack(self,register,stackregister):
		string = ""
		reg,temp = self.GetStackVariable(stackregister)
		string += temp
		string += "\t\tlw " + register + ",(" + reg +")\n"
		return string 

	def ADDR(self,parameters):
		string = "# ADDR Began\n"

		'''
		# WHAT CHASE HAD BEFORE MERGE
		reg,temp = self.GetStackVariable(parameters[0].type+"_"+parameters[0].name)
		string += temp
		plist, temp = self.MagicFunction([(parameters[2],False)])
		string += temp
		string += "\t\tmove " + plist[0] + "," + reg + "\n"
		#raw_input(reg)
		#parameters[0].modifier = "indr"
		#plist,string = self.MagicFunction([ (parameters[0],True),(parameters[2],True)  ])
		#string += "\t\tmove " + plist[1] + "," + plist[0] + "# ADDR HERE\n"
		'''

		if parameters[0].type == "local":
			reg, temp = self.GetStackVariable(parameters[0].type + "_" + parameters[0].name)
			string += temp
			plist,temp = self.MagicFunction([ (parameters[2],True)  ])
			string += temp
			string += "\t\tmove " + plist[0] + "," + reg + "# ADDR HERE\n"

		else:
			parameters[0].modifier = ""
			plist,string = self.MagicFunction([ (parameters[0],True),(parameters[2],True)  ])
			string += "\t\tmove " + plist[1] + "," + plist[0] + "# ADDR HERE\n"

		return string

	def INDR(self, parameters):
		string = ""
		if parameters[0].type == "local":
			reg, temp = self.GetStackVariable(parameters[0].type + "_" + parameters[0].name)
			string += temp
			plist,temp = self.MagicFunction([ (parameters[2],True)  ])
			string += temp
			string += "\t\tlw " + plist[0] + ",(" + reg + ")# INDR HERE\n"
			string += "\t\tlw " + plist[0] + ",(" + plist[0] + ")# INDR HERE\n"

		elif parameters[0].type == "arg":
			reg, temp = self.GetStackVariable(parameters[0].name)
			string += temp
			plist,temp = self.MagicFunction([ (parameters[2],True)  ])
			string += temp
			string += "\t\tlw " + plist[0] + ",(" + reg + ")# INDR HERE\n"
			string += "\t\tlw " + plist[0] + ",(" + plist[0] + ")# INDR HERE\n"

		string += "# ADDR End\n"
		return string

	def CheckSave(self,params):
		string = ""
		if "save_" in params[0].name and "save_" in params[1].name:
			# Store onto stack
			self.stackTracker.SetSaveName(params[2].name)
			string += self.stackTracker.PushOntoStack()
			self.stackTracker.SetSaved(True)
			#print "\t\tsw " + self.variableMap["_"+params[2].name] + ",($sp)\n"
			string += "\t\tsw " + self.variableMap["_"+params[2].name] + ",($sp)# APPLE HERE\n"
			return string
		return ""

	def GLOBAL(self,params):
		string = ""
		string  += "\t\tGLOBAL_" + params[0].name + ": .space " + params[2].name + "\n"
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
		stackspace = function.localcount + savedregisters + 13
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
		self.stackTracker.SetVariable("$a0",4)
		self.stackTracker.SetVariable("$a1",4)
		self.stackTracker.SetVariable("$a2",4)
		self.stackTracker.SetVariable("$a3",4)

		for i in range(function.localcount):
			self.stackTracker.SetVariable("local_" + str(i),4)
		# store save registers

		# push stack frame 
		#string += "\t\taddiu $sp,$sp,-"+str(self.stackTracker.GetStackSize())+"\n"
		v = Variable(["cons",str(self.stackTracker.GetStackSize())])
		reg, temp = self.MagicFunction([(v,True)])
		string += temp
		string += self.stackTracker.AddToStack(reg[0],True)

		# store the return address
		string += "\n#Setting Stack\n"
		string += self.StoreOntoStack("$ra","$ra")
		string += self.StoreOntoStack("$s0","$s0")
		string += self.StoreOntoStack("$s1","$s1")
		string += self.StoreOntoStack("$s2","$s2")
		string += self.StoreOntoStack("$s3","$s3")
		string += self.StoreOntoStack("$s4","$s4")
		string += self.StoreOntoStack("$s5","$s5")
		string += self.StoreOntoStack("$s6","$s6")
		string += self.StoreOntoStack("$s7","$s7")
		string += self.StoreOntoStack("$a0","$a0")
		string += self.StoreOntoStack("$a1","$a1")
		string += self.StoreOntoStack("$a2","$a2")
		string += self.StoreOntoStack("$a3","$a3")
		sreg = self.registermap.getSavedRegister("stack1")
		string += self.stackTracker.updateStackSymbol(sreg)
		self.registermap.freeRegisterByName("stack")
		string += "#Setting Stack Complete\n\n"
		


		# Lets go through the statements
		for i in function.statements:
			string += self.call(i.name,i.params())
			#string += self.CheckSave(i.params())
			self.MarkForRemove(i.params())

		# restore save registers
		treg = self.registermap.getTemporaryRegister("stack")

		string += "\t\tmove " + treg + "," + self.stackTracker.GetStackSymbol() + "\n"

		self.stackTracker.SetStackSymbol(treg)
		# restore return address
		string += "\n#Restoring Stack\n"
		string += self.LoadFromStack("$ra","$ra") 
		string += self.LoadFromStack("$s0","$s0")
		string += self.LoadFromStack("$s1","$s1")
		string += self.LoadFromStack("$s2","$s2")
		string += self.LoadFromStack("$s3","$s3")
		string += self.LoadFromStack("$s4","$s4")
		string += self.LoadFromStack("$s5","$s5")
		string += self.LoadFromStack("$s6","$s6")
		string += self.LoadFromStack("$s7","$s7")
		string += self.LoadFromStack("$a0","$a0")
		string += self.LoadFromStack("$a1","$a1")
		string += self.LoadFromStack("$a2","$a2")
		string += self.LoadFromStack("$a3","$a3")
		self.registermap.freeRegisterByName("stack1")
		self.registermap.freeRegisterByName("stack")
		string += "#Restoring Stack Complete\n\n"

		string += self.stackTracker.ResetStack()
 		# end of epilogue
 		string += "\t\tjr $ra\n" # return

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
		string = ".data\n"
		after = ""

		for i in Global:
			if i.name == "global":
				string += self.call(i.name,i.params())
			else:
				after += self.call(i.name,i.params())
		string += "\n.text\n"
		string += after

		Funcs = {}
		for function in functions:
			Funcs[function.name] = self.call("function",function) + "\n"
		string += Funcs["main"]

		del Funcs["main"]

		for func in Funcs:
			string += Funcs[func]
		printdata = open("src/print.s", "r")
		string += "\n\n#Adding Generated print functions\n\n" + printdata.read()
		string += "\nHalt: " + "\n"
		printdata.close()
		return string

	def Instructionize(self,li):
		return map(Instruction,li)
	def ConstructData(self,functions,Globals):
		if len(Globals) != 0:
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

		Globals = []
		for i in globalstatements:
			b = i.split(",")
			Globals.append(map(str.strip,b))

		if string == "":
			Globals = [['']]

		return Globals,functions



