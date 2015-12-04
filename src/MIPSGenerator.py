import sys
import re
bas = open("log/3AC.tac",'r')
a = bas.read()

class MipsGenerator:
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
		print self.TacSplit(string)
	def TacSplit(self,string):
		string = string.replace(" ","")
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
				functionlist.append(stringstmt.split(","))
			functions.append(functionlist)

		Globals = []
		for i in globalstatements:
			b = i.split(",")
			Globals.append(b)


		return Globals,functions

#Globals,functions = TacSplit(a)
#print Globals
#print functions
generator = MipsGenerator()
generator.Parse(a)
generator.call("test","")



