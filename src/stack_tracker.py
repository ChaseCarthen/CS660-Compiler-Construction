# StackTracker class
class StackTracker:
	def __init__(self):
		self.size = 0
		self.variables = {}
		self.offset = 0
		self.extra = []
		self.stacksymbol = "$s0"
		self.saved = False
		self.savename = ""
	def SetSaved(self,save):
		self.saved = save
	def GetSaveName(self):
		return self.savename
	def SetSaveName(self,name):
		self.savename = name
	def SetStackSymbol(self,symbol):
		self.stacksymbol = symbol
	def AddToStack(self,reg,beginning=False):
		string = ""
		#raw_input(type(reg))
		if not beginning:
			string = "\t\taddu " + self.stacksymbol + "," + self.stacksymbol + "," + reg + "\n"
		else:
			string = "\t\tmove " + self.stacksymbol + "," + reg + "\n"
		string += "\t\tsubu $sp,$sp,"+reg+"\n"
		return string
	def ResetStack(self):
		return "\t\taddu " + "$sp,$sp," + self.stacksymbol + "\n" 
	def GetStackSize(self):
		if len(self.extra) == 0:
			return self.size
		else:
			return self.size,self.extra
	def UpdateStackSize(self,size):
		if type(size) == int:
			self.size += size

	# This will remain the same.
	def SetVariable(self,variable,size):
		if not variable in self.variables:
			self.variables[variable] = self.offset
			if type(size) == int:
				self.offset += size
			else:
				self.extra.append(size)

	def GetStackSymbol(self):
		return self.stacksymbol
	def GetFixedStackSize(self):
		return self.size
	def GetVariable(self,variable):
		return self.variables[variable]
	def updateStackSymbol(self,sreg):
		string = "\t\tmove " + sreg + "," + self.stacksymbol + "\n"
		self.stacksymbol = sreg
		return string
	def Clear(self):
		self.variables.clear()
		self.size = 0
		self.offset = 0
		del self.extra[:]
	# This will always be $v0 -- This could be used for arrays in the future
	def PushOntoStack(self):
		string = "\t\taddiu $sp,$sp,-4\n"
		string += "\t\tsw $v0,($sp)\n"
		return string
	def PopOffStack(self):
		string = "\t\taddiu $sp,$sp,4\n"
		return string