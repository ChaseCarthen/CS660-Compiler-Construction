class node(object):
	'''The basic node that is a text node at this point.'''
	def __init__(self,**kwargs):
		self.children = []
		if "text" in kwargs:
			self.text = kwargs["text"]
	def SetText(self,text):
		self.text = text
	def SetParent(self,node):
		self.parent = node
	def SetChild(self,node):
		self.children.append(node)
	def ParseTree(self):
		parent = self.text
		string = ""
		for i in self.children:
			string += parent + "->" + i.text + "\n"
			string += i.ParseTree()
		return string
