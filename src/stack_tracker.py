# StackTracker class
class StackTracker:
	def __init__(self):
		self.size = 0
		self.variables = {}
		self.offset = 0
	def GetStackSize(self):
		return self.size
	def UpdateStackSize(self,size):
		self.size += size
	def SetVariable(self,variable,size=4):
		if not variable in self.variables:
			self.variables[variable] = self.offset
			self.offset += size
	def GetVariable(self,variable):
		return self.variables[variable]
	def Clear(self):
		self.variables.clear()
		self.size = 0
		self.offset = 0