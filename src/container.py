class container:
	def __init__(self):
		self.symbolNodeList = []
		self.astNode = None
		self.children = []
		self.passthrough = None

	def AddToNodeList(self,node):
		self.symbolNodeList += node

	def GetNodeList(self,node):
		return self.symbolNodeList

	def SetAstNode(self,node):
		self.astNode = node

	def GetAstNode(self,node):
		return self.astNode

	def SetChild(self,node):
		self.children += node

	def SetParent(self,node):
		self.astNode.SetParent(node)
		self.astNode = node

	def SetChildren(self,node):
		for i in self.children:
			self.astNode.SetParent(self.astNode)