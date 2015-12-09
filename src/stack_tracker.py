# StackTracker class
class StackTracker:
	def __init__(self):
		self.size = 0
		self.variables = {}
		self.offset = 0
		self.extra = []
	def GetStackSize(self):
		if len(self.extra) == 0:
			return self.size
		else:
			return self.size,self.extra
	def UpdateStackSize(self,size):
		self.size += size
	def SetVariable(self,variable,size):
		if not variable in self.variables:
			self.variables[variable] = self.offset
			if type(size) == int:
				self.offset += size
			else:
				self.extra.append(size)
	def GetVariable(self,variable):
		return self.variables[variable]
	def Clear(self):
		self.variables.clear()
		self.size = 0
		self.offset = 0