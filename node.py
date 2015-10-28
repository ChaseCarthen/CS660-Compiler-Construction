class node(object):
	'''The basic node that is a text node at this point.'''
	def __init__(self,**kwargs):
		self.children = []
		if "text" in kwargs:
			self.text = kwargs["text"]
	def SetText(self,text):
		self.text = text
	def SetChild(self,node):
		self.children.append(node)
	def ParseTree(self):
		parent = self.text
		string = ""
		for i in self.children:
			string += '"'+ parent + '"' + "->" + '"'+ i.text + '"' + "\n"
			string += i.ParseTree()
		return string

class FuncDecl(node):
	def __init__(self,**kwargs):
		super(FuncDecl,self).__init__(**kwargs)

class FuncDef(node):
	def __init__(self,**kwargs):
		pass


# This will be for for,while,do-while
class IterStatement(node):
	def __init__(self,**kwargs):
		pass

class ArrDecl(node):
	def __init__(self,**kwargs):
		pass

class ArrRef(node):
	def __init__(self,**kwargs):
		pass

class Assignment(node):
	def __init__(self,**kwargs):
		pass

class BinOp(node):
	def __init__(self,**kwargs):
		pass

class Break(node):
	def __init__(self,**kwargs):
		pass

class Case(node):
	def __init__(self,**kwargs):
		pass

class Cast(node):
	def __init__(self,**kwargs):
		pass

class Compound(node):
	def __init__(self,**kwargs):
		pass

class CompoundLiteral(node):
	def __init__(self,**kwargs):
		pass

class Constant(node):
	def __init__(self,**kwargs):
		pass

class Continue(node):
	def __init__(self,**kwargs):
		pass

class Decl(node):
	def __init__(self,**kwargs):
		pass

class DeclList(node):
	def __init__(self,**kwargs):
		pass

class Default(node):
	def __init__(self,**kwargs):
		pass

class DoWhile(node):
	def __init__(self,**kwargs):
		pass

class EllipsisParam(node):
	def __init__(self,**kwargs):
		pass

class EmptyStatement(node):
	def __init__(self,**kwargs):
		pass

class Enum(node):
	def __init__(self,**kwargs):
		pass

class Enumerator(node):
	def __init__(self,**kwargs):
		pass

class EnumeratorList(node):
	def __init__(self,**kwargs):
		pass

class ExprList(node):
	def __init__(self,**kwargs):
		pass

class FileAST(node):
	def __init__(self,**kwargs):
		pass

class For(node):
	def __init__(self,**kwargs):
		pass

class FuncCall(node):
	def __init__(self,**kwargs):
		pass

class Goto(node):
	def __init__(self,**kwargs):
		pass

class ID(node):
	def __init__(self,**kwargs):
		pass

class IdenType(node):
	def __init__(self,**kwargs):
		pass

class If(node):
	def __init__(self,**kwargs):
		pass

class InitList(node):
	def __init__(self,**kwargs):
		pass

class Label(node):
	def __init__(self,**kwargs):
		pass

class NamedInitializer(node):
	def __init__(self,**kwargs):
		pass

class ParamList(node):
	def __init__(self,**kwargs):
		pass

class PtrDecl(node):
	def __init__(self,**kwargs):
		pass
		
class Return(node):
	def __init__(self,**kwargs):
		pass
		
class Struct(node):
	def __init__(self,**kwargs):
		pass
		
class StructRef(node):
	def __init__(self,**kwargs):
		pass
		
class Switch(node):
	def __init__(self,**kwargs):
		pass
		
class TernaryOp(node):
	def __init__(self,**kwargs):
		pass
		
class TypeDecl(node):
	def __init__(self,**kwargs):
		pass
		
class TypeName(node):
	def __init__(self,**kwargs):
		pass
		
class UnaryOp(node):
	def __init__(self,**kwargs):
		pass
		
class Union(node):
	def __init__(self,**kwargs):
		pass
		
class While(node):
	def __init__(self,**kwargs):
		pass