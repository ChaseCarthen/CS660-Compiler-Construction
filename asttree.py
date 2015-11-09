#-----------------------------------------------------------------
# ** DISCLAIMER **
# This code was automatically generated from the file:
# ast.cfg
#
# AST Node classes:
#  - Heavy Inspiration as drawn from the team developing pycparser
#  - Heavily altered to handle Three Address code
#  - Shut up Terence
#
#-----------------------------------------------------------------

import sys
from ticketcounter import *
class Node(object):
	__slots__ = ()

	""" Base class for AST nodes. Auto-Generated.
	"""
	text = ""
	floatTicketCounter = TicketCounter("float")
	intTicketCounter = TicketCounter("int")
	charTicketCounter = TicketCounter("char")
	def children(self):
		""" A sequence of all children that are Nodes
		"""
		pass

class CompoundStatement(Node):
	__slots__ = ('stmts','text', 'coord', '__weakref__')

	def __init__(self, stmts, coord=None,text=""):
		self.stmts = stmts
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.stmts or []):
			nodelist.append(("stmts[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class FuncDecl(Node):
	__slots__ = ('ParamList', 'type', 'name','text', 'coord', '__weakref__')

	def __init__(self, ParamList, type, name, coord=None,text=""):
		self.ParamList = ParamList
		self.type = type
		self.name = name
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		for i, child in enumerate(self.ParamList or []):
			nodelist.append(("ParamList[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class FuncDef(Node):
	__slots__ = ('ParamList', 'type', 'name', 'expression','text', 'coord', '__weakref__')

	def __init__(self, ParamList, type, name, expression, coord=None,text=""):
		self.ParamList = ParamList
		self.type = type
		self.name = name
		self.expression = expression
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		if self.expression is not None:
			nodelist.append(("expression", self.expression))
		for i, child in enumerate(self.ParamList or []):
			nodelist.append(("ParamList[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class FuncCall(Node):
	__slots__ = ('ParamList', 'type', 'name','text', 'coord', '__weakref__')

	def __init__(self, ParamList, type, name, coord=None,text=""):
		self.ParamList = ParamList
		self.type = type
		self.name = name
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		for i, child in enumerate(self.ParamList or []):
			nodelist.append(("ParamList[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class Program(Node):
	__slots__ = ('NodeList','text', 'coord', '__weakref__')

	def __init__(self, NodeList, coord=None,text=""):
		self.NodeList = NodeList
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.NodeList or []):
			nodelist.append(("NodeList[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Return(Node):
	__slots__ = ('expr','text', 'coord', '__weakref__')

	def __init__(self, expr, coord=None,text=""):
		self.expr = expr
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.expr is not None:
			nodelist.append(("expr", self.expr))
		return tuple(nodelist)

	attr_names = ()


class VariableCall(Node):
	__slots__ = ('type', 'name','text', 'coord', '__weakref__')

	def __init__(self, type, name, coord=None,text=""):
		self.type = type
		self.name = name
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = (' name', )


class ParamList(Node):
	__slots__ = ('params','text', 'coord', '__weakref__')

	def __init__(self, params, coord=None,text=""):
		self.params = params
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.params or []):
			nodelist.append(("params[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Decl(Node):
	__slots__ = ('name', 'type', 'init','text', 'coord', '__weakref__')

	def __init__(self, name, type, init, coord=None,text=""):
		self.name = name
		self.type = type
		self.init = init
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		if self.init is not None:
			nodelist.append(("init", self.init))
		return tuple(nodelist)

	attr_names = ('name', )


class DeclList(Node):
	__slots__ = ('decls','text', 'coord', '__weakref__')

	def __init__(self, decls, coord=None,text=""):
		self.decls = decls
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(("decls[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class IterStatement(Node):
	__slots__ = ('init', 'cond', 'next', 'stmt', 'isdowhile', 'name','text', 'coord', '__weakref__')

	def __init__(self, init, cond, next, stmt, isdowhile, name, coord=None,text=""):
		self.init = init
		self.cond = cond
		self.next = next
		self.stmt = stmt
		self.isdowhile = isdowhile
		self.name = name
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.init is not None:
			nodelist.append(("init", self.init))
		if self.cond is not None:
			nodelist.append(("cond", self.cond))
		if self.next is not None:
			nodelist.append(("next", self.next))
		if self.stmt is not None:
			nodelist.append(("stmt", self.stmt))
		return tuple(nodelist)

	attr_names = ('isdowhile', 'name', )


class Break(Node):
	__slots__ = ('coord', '__weakref__')

	def __init__(self, coord=None,text=""):
		self.coord = coord
		self.text = text

	def children(self):
		return ()

	attr_names = ('', )


class Continue(Node):
	__slots__ = ('coord', '__weakref__')

	def __init__(self, coord=None,text=""):
		self.coord = coord
		self.text = text

	def children(self):
		return ()

	attr_names = ('', )


class ArrDecl(Node):
	__slots__ = ('name', 'type', 'init', 'dim','text', 'coord', '__weakref__')

	def __init__(self, name, type, init, dim, coord=None,text=""):
		self.name = name
		self.type = type
		self.init = init
		self.dim = dim
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		if self.init is not None:
			nodelist.append(("init", self.init))
		for i, child in enumerate(self.dim or []):
			nodelist.append(("dim[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class ArrRef(Node):
	__slots__ = ('name', 'subscript', 'type', 'dim','text', 'coord', '__weakref__')

	def __init__(self, name, subscript, type, dim, coord=None,text=""):
		self.name = name
		self.subscript = subscript
		self.type = type
		self.dim = dim
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		for i, child in enumerate(self.subscript or []):
			nodelist.append(("subscript[%d]" % i, child))
		for i, child in enumerate(self.dim or []):
			nodelist.append(("dim[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class PtrDecl(Node):
	__slots__ = ('name', 'type', 'numindirections','text', 'coord', '__weakref__')

	def __init__(self, name, type, numindirections, coord=None,text=""):
		self.name = name
		self.type = type
		self.numindirections = numindirections
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ('name', 'numindirections', )


class Assignment(Node):
	__slots__ = ('op', 'lvalue', 'rvalue','text', 'coord', '__weakref__')

	def __init__(self, op, lvalue, rvalue, coord=None,text=""):
		self.op = op
		self.lvalue = lvalue
		self.rvalue = rvalue
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.lvalue is not None:
			nodelist.append(("lvalue", self.lvalue))
		if self.rvalue is not None:
			nodelist.append(("rvalue", self.rvalue))
		return tuple(nodelist)

	attr_names = ('op', )


class AndOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class OrOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class LeftOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class RightOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class XorOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class LandOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class LorOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class TernaryOp(Node):
	__slots__ = ('cond', 'truecond', 'falsecond','text', 'coord', '__weakref__')

	def __init__(self, cond, truecond, falsecond, coord=None,text=""):
		self.cond = cond
		self.truecond = truecond
		self.falsecond = falsecond
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.cond is not None:
			nodelist.append(("cond", self.cond))
		if self.truecond is not None:
			nodelist.append(("truecond", self.truecond))
		if self.falsecond is not None:
			nodelist.append(("falsecond", self.falsecond))
		return tuple(nodelist)

	attr_names = ()


class If(Node):
	__slots__ = ('cond', 'truecond', 'falsecond','text', 'coord', '__weakref__')

	def __init__(self, cond, truecond, falsecond, coord=None,text=""):
		self.cond = cond
		self.truecond = truecond
		self.falsecond = falsecond
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.cond is not None:
			nodelist.append(("cond", self.cond))
		if self.truecond is not None:
			nodelist.append(("truecond", self.truecond))
		if self.falsecond is not None:
			nodelist.append(("falsecond", self.falsecond))
		return tuple(nodelist)

	attr_names = ()


class NEqualOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class GEqualOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class LEqualOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class EqualOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class GreatOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class LessOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class RefOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class MultOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class AddOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class SubOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class DivOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class ModOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class BitNotOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class LogNotOp(Node):
	__slots__ = ('left', 'right', 'type','text', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class AssignOp(Node):
	__slots__ = ('left', 'right','text', 'coord', '__weakref__')

	def __init__(self, left, right, coord=None,text=""):
		self.left = left
		self.right = right
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		return tuple(nodelist)

	attr_names = ()


class Goto(Node):
	__slots__ = ('name','text', 'coord', '__weakref__')

	def __init__(self, name, coord=None,text=""):
		self.name = name
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('name', )


class Cast(Node):
	__slots__ = ('to_type', 'expr','text', 'coord', '__weakref__')

	def __init__(self, to_type, expr, coord=None,text=""):
		self.to_type = to_type
		self.expr = expr
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.to_type is not None:
			nodelist.append(("to_type", self.to_type))
		if self.expr is not None:
			nodelist.append(("expr", self.expr))
		return tuple(nodelist)

	attr_names = ()


class Constant(Node):
	__slots__ = ('type', 'value','text', 'coord', '__weakref__')

	def __init__(self, type, value, coord=None,text=""):
		self.type = type
		self.value = value
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('type', 'value', )


class ExprList(Node):
	__slots__ = ('exprs','text', 'coord', '__weakref__')

	def __init__(self, exprs, coord=None,text=""):
		self.exprs = exprs
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.exprs or []):
			nodelist.append(("exprs[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class EmptyStatement(Node):
	__slots__ = ('coord', '__weakref__')

	def __init__(self, coord=None,text=""):
		self.coord = coord
		self.text = text

	def children(self):
		return ()

	attr_names = ('', )


class InitList(Node):
	__slots__ = ('exprs','text', 'coord', '__weakref__')

	def __init__(self, exprs, coord=None,text=""):
		self.exprs = exprs
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.exprs or []):
			nodelist.append(("exprs[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Label(Node):
	__slots__ = ('name', 'stmt','text', 'coord', '__weakref__')

	def __init__(self, name, stmt, coord=None,text=""):
		self.name = name
		self.stmt = stmt
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.stmt is not None:
			nodelist.append(("stmt", self.stmt))
		return tuple(nodelist)

	attr_names = ('name', )


class Type(Node):
	__slots__ = ('type', 'qualifier', 'storage','text', 'coord', '__weakref__')

	def __init__(self, type, qualifier, storage, coord=None,text=""):
		self.type = type
		self.qualifier = qualifier
		self.storage = storage
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('type', 'qualifier', 'storage', )


class ID(Node):
	__slots__ = ('name','text', 'coord', '__weakref__')

	def __init__(self, name, coord=None,text=""):
		self.name = name
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('name', )


class Struct(Node):
	__slots__ = ('name', 'decls','text', 'coord', '__weakref__')

	def __init__(self, name, decls, coord=None,text=""):
		self.name = name
		self.decls = decls
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(("decls[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class Union(Node):
	__slots__ = ('name', 'decls','text', 'coord', '__weakref__')

	def __init__(self, name, decls, coord=None,text=""):
		self.name = name
		self.decls = decls
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(("decls[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class StructRef(Node):
	__slots__ = ('name', 'type', 'field','text', 'coord', '__weakref__')

	def __init__(self, name, type, field, coord=None,text=""):
		self.name = name
		self.type = type
		self.field = field
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.name is not None:
			nodelist.append(("name", self.name))
		if self.field is not None:
			nodelist.append(("field", self.field))
		return tuple(nodelist)

	attr_names = ('type', )


class Case(Node):
	__slots__ = ('expr', 'stmts','text', 'coord', '__weakref__')

	def __init__(self, expr, stmts, coord=None,text=""):
		self.expr = expr
		self.stmts = stmts
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.expr is not None:
			nodelist.append(("expr", self.expr))
		for i, child in enumerate(self.stmts or []):
			nodelist.append(("stmts[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Default(Node):
	__slots__ = ('stmts','text', 'coord', '__weakref__')

	def __init__(self, stmts, coord=None,text=""):
		self.stmts = stmts
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.stmts or []):
			nodelist.append(("stmts[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Switch(Node):
	__slots__ = ('cond', 'stmt','text', 'coord', '__weakref__')

	def __init__(self, cond, stmt, coord=None,text=""):
		self.cond = cond
		self.stmt = stmt
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		if self.cond is not None:
			nodelist.append(("cond", self.cond))
		if self.stmt is not None:
			nodelist.append(("stmt", self.stmt))
		return tuple(nodelist)

	attr_names = ()


class Example(Node):
	__slots__ = ('a', 'b','text', 'coord', '__weakref__')

	def __init__(self, a, b, coord=None,text=""):
		self.a = a
		self.b = b
		self.coord = coord
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.a or []):
			nodelist.append(("a[%d]" % i, child))
		for i, child in enumerate(self.b or []):
			nodelist.append(("b[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


