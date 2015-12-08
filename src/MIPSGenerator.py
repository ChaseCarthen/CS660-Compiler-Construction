import sys
import re
bas = open("log/3AC.tac",'r')
a = bas.read()

class Instruction:
	def __init__(self,string):
		self.command = string[0]
		self.one = self.Tuple(string[1])
		self.two = self.Tuple(string[2])
		self.three = self.Tuple(string[3])
	def Tuple(self,string):
		if "cons" in string or "fcons" in string or "global" in string or "local" in string or "indr" in string or "addr" in string:
			strlist = string.split(" ")
			return strlist 
		return string
	def __str__(self):
		string = str(self.command)
		string += "," + str(self.one)
		string +=  "," + str(self.two)
		string +=  "," + str(self.three) + "\n"
		return string

class Variable:
	def __init__(self,string):
		if(len(string) == 2):
			pass
		elif(len(string) == 3):
			pass

class MipsGenerator:
	Frequency = []
	def __init__(self):
		pass
	def call(self,funcname,parameters):
		method = funcname
		callfunc = getattr(self, method, self.undef)
		return callfunc(parameters)
	def undef(self,parameters):
		print "UNDEFINED"
	def test(self,parameters):
		print "test"

	def Parse(self,string):
		Global,functions = self.TacSplit(string)
		self.CountFrequencies(functions,Global)
	def Intstructionize(self,li):
		return map(Instruction,li)
	def CountFrequencies(self,functions,Globals):
		self.Frequency.append({})
		#functions = map(self.Intstructionize,functions)
		Globals = map(Instruction,Globals)
		for i in Globals:
			print i
		#for i in Globals:
		#	print i
		#for function in functions:
		#	for stmt in function:
		#		pass

	def TacSplit(self,string):
		#string = string.replace(" ","")
		string = re.sub(r'procentry','@',string)
		string = re.sub(r'endproc','@',string)

		functionstrings = re.findall(r"@[^\@]*@",string,re.DOTALL)

		string = re.sub(r'@[^\@]*@','',string,re.DOTALL)

		globalstatements = []
		for i in re.findall(r"\(.*\)",string):
			stmt = i.replace("(","")
			stmt = stmt.replace(")","")
			#print stmt
			#raw_input()
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
				#print stringstmt
				#raw_input()
				functionlist.append(map(str.strip,stringstmt.split(",")))
			functions.append(functionlist)

		Globals = []
		for i in globalstatements:
			b = i.split(",")
			Globals.append(map(str.strip,b))


		return Globals,functions

#Globals,functions = TacSplit(a)
#print Globals
#print functions
generator = MipsGenerator()
generator.Parse(a)
generator.call("test","")



