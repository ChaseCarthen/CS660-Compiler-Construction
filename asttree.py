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

class FuncDecl(Node):
	__slots__ = ('ParamList', 'type', 'name', 'coord', '__weakref__')

	def __init__(self, ParamList, type, name, coord=None):
		self.ParamList = ParamList
		self.type = type
		self.name = name
		self.coord = coord

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		for i, child in enumerate(self.ParamList or []):
			nodelist.append(("ParamList[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class FuncDef(Node):
	__slots__ = ('ParamList', 'type', 'name', 'expression', 'coord', '__weakref__')

	def __init__(self, ParamList, type, name, expression, coord=None):
		self.ParamList = ParamList
		self.type = type
		self.name = name
		self.expression = expression
		self.coord = coord

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
	__slots__ = ('ParamList', 'type', 'name', 'coord', '__weakref__')

	def __init__(self, ParamList, type, name, coord=None):
		self.ParamList = ParamList
		self.type = type
		self.name = name
		self.coord = coord

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		for i, child in enumerate(self.ParamList or []):
			nodelist.append(("ParamList[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class Program(Node):
	__slots__ = ('NodeList', 'coord', '__weakref__')

	def __init__(self, NodeList, coord=None):
		self.NodeList = NodeList
		self.coord = coord

	def children(self):
		nodelist = []
		for i, child in enumerate(self.NodeList or []):
			nodelist.append(("NodeList[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Return(Node):
	__slots__ = ('expr', 'coord', '__weakref__')

	def __init__(self, expr, coord=None):
		self.expr = expr
		self.coord = coord

	def children(self):
		nodelist = []
		if self.expr is not None:
			nodelist.append(("expr", self.expr))
		return tuple(nodelist)

	attr_names = ()


class VariableCall(Node):
	__slots__ = ('type', 'name', 'coord', '__weakref__')

	def __init__(self, type, name, coord=None):
		self.type = type
		self.name = name
		self.coord = coord

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = (' name', )


class ParamList(Node):
	__slots__ = ('params', 'coord', '__weakref__')

	def __init__(self, params, coord=None):
		self.params = params
		self.coord = coord

	def children(self):
		nodelist = []
		for i, child in enumerate(self.params or []):
			nodelist.append(("params[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Decl(Node):
	__slots__ = ('name', 'type', 'init', 'coord', '__weakref__')

	def __init__(self, name, type, init, coord=None):
		self.name = name
		self.type = type
		self.init = init
		self.coord = coord

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		if self.init is not None:
			nodelist.append(("init", self.init))
		return tuple(nodelist)

	attr_names = ('name', )


class DeclList(Node):
	__slots__ = ('decls', 'coord', '__weakref__')

	def __init__(self, decls, coord=None):
		self.decls = decls
		self.coord = coord

	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(("decls[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class IterStatement(Node):
	__slots__ = ('init', 'cond', 'next', 'stmt', 'isdowhile', 'name', 'coord', '__weakref__')

	def __init__(self, init, cond, next, stmt, isdowhile, name, coord=None):
		self.init = init
		self.cond = cond
		self.next = next
		self.stmt = stmt
		self.isdowhile = isdowhile
		self.name = name
		self.coord = coord

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

	def __init__(self, coord=None):
		self.coord = coord

	def children(self):
		return ()

	attr_names = ('', )


class Continue(Node):
	__slots__ = ('coord', '__weakref__')

	def __init__(self, coord=None):
		self.coord = coord

	def children(self):
		return ()

	attr_names = ('', )


class ArrDecl(Node):
	__slots__ = ('name', 'type', 'init', 'dim', 'coord', '__weakref__')

	def __init__(self, name, type, init, dim, coord=None):
		self.name = name
		self.type = type
		self.init = init
		self.dim = dim
		self.coord = coord

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
	__slots__ = ('name', 'subscript', 'type', 'dim', 'coord', '__weakref__')

	def __init__(self, name, subscript, type, dim, coord=None):
		self.name = name
		self.subscript = subscript
		self.type = type
		self.dim = dim
		self.coord = coord

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
	__slots__ = ('quals', 'type', 'coord', '__weakref__')

	def __init__(self, quals, type, coord=None):
		self.quals = quals
		self.type = type
		self.coord = coord

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ('quals', )


class Assignment(Node):
	__slots__ = ('op', 'lvalue', 'rvalue', 'coord', '__weakref__')

	def __init__(self, op, lvalue, rvalue, coord=None):
		self.op = op
		self.lvalue = lvalue
		self.rvalue = rvalue
		self.coord = coord

	def children(self):
		nodelist = []
		if self.lvalue is not None:
			nodelist.append(("lvalue", self.lvalue))
		if self.rvalue is not None:
			nodelist.append(("rvalue", self.rvalue))
		return tuple(nodelist)

	attr_names = ('op', )


class AndOp(Node):
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('cond', 'truecond', 'falsecond', 'coord', '__weakref__')

	def __init__(self, cond, truecond, falsecond, coord=None):
		self.cond = cond
		self.truecond = truecond
		self.falsecond = falsecond
		self.coord = coord

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
	__slots__ = ('cond', 'truecond', 'falsecond', 'coord', '__weakref__')

	def __init__(self, cond, truecond, falsecond, coord=None):
		self.cond = cond
		self.truecond = truecond
		self.falsecond = falsecond
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'type', 'coord', '__weakref__')

	def __init__(self, left, right, type, coord=None):
		self.left = left
		self.right = right
		self.type = type
		self.coord = coord

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
	__slots__ = ('left', 'right', 'coord', '__weakref__')

	def __init__(self, left, right, coord=None):
		self.left = left
		self.right = right
		self.coord = coord

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		return tuple(nodelist)

	attr_names = ()


class Goto(Node):
	__slots__ = ('name', 'coord', '__weakref__')

	def __init__(self, name, coord=None):
		self.name = name
		self.coord = coord

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('name', )


class Cast(Node):
	__slots__ = ('to_type', 'expr', 'coord', '__weakref__')

	def __init__(self, to_type, expr, coord=None):
		self.to_type = to_type
		self.expr = expr
		self.coord = coord

	def children(self):
		nodelist = []
		if self.to_type is not None:
			nodelist.append(("to_type", self.to_type))
		if self.expr is not None:
			nodelist.append(("expr", self.expr))
		return tuple(nodelist)

	attr_names = ()


class Constant(Node):
	__slots__ = ('type', 'value', 'coord', '__weakref__')

	def __init__(self, type, value, coord=None):
		self.type = type
		self.value = value
		self.coord = coord

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('type', 'value', )


class ExprList(Node):
	__slots__ = ('exprs', 'coord', '__weakref__')

	def __init__(self, exprs, coord=None):
		self.exprs = exprs
		self.coord = coord

	def children(self):
		nodelist = []
		for i, child in enumerate(self.exprs or []):
			nodelist.append(("exprs[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class EmptyStatement(Node):
	__slots__ = ('coord', '__weakref__')

	def __init__(self, coord=None):
		self.coord = coord

	def children(self):
		return ()

	attr_names = ('', )


class InitList(Node):
	__slots__ = ('exprs', 'coord', '__weakref__')

	def __init__(self, exprs, coord=None):
		self.exprs = exprs
		self.coord = coord

	def children(self):
		nodelist = []
		for i, child in enumerate(self.exprs or []):
			nodelist.append(("exprs[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Label(Node):
	__slots__ = ('name', 'stmt', 'coord', '__weakref__')

	def __init__(self, name, stmt, coord=None):
		self.name = name
		self.stmt = stmt
		self.coord = coord

	def children(self):
		nodelist = []
		if self.stmt is not None:
			nodelist.append(("stmt", self.stmt))
		return tuple(nodelist)

	attr_names = ('name', )


class Type(Node):
	__slots__ = ('type', 'qualifier', 'storage', 'coord', '__weakref__')

	def __init__(self, type, qualifier, storage, coord=None):
		self.type = type
		self.qualifier = qualifier
		self.storage = storage
		self.coord = coord

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('type', 'qualifier', 'storage', )


class ID(Node):
	__slots__ = ('name', 'coord', '__weakref__')

	def __init__(self, name, coord=None):
		self.name = name
		self.coord = coord

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('name', )


class Struct(Node):
	__slots__ = ('name', 'decls', 'coord', '__weakref__')

	def __init__(self, name, decls, coord=None):
		self.name = name
		self.decls = decls
		self.coord = coord

	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(("decls[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class Union(Node):
	__slots__ = ('name', 'decls', 'coord', '__weakref__')

	def __init__(self, name, decls, coord=None):
		self.name = name
		self.decls = decls
		self.coord = coord

	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(("decls[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class StructRef(Node):
	__slots__ = ('name', 'type', 'field', 'coord', '__weakref__')

	def __init__(self, name, type, field, coord=None):
		self.name = name
		self.type = type
		self.field = field
		self.coord = coord

	def children(self):
		nodelist = []
		if self.name is not None:
			nodelist.append(("name", self.name))
		if self.field is not None:
			nodelist.append(("field", self.field))
		return tuple(nodelist)

	attr_names = ('type', )


class Case(Node):
	__slots__ = ('expr', 'stmts', 'coord', '__weakref__')

	def __init__(self, expr, stmts, coord=None):
		self.expr = expr
		self.stmts = stmts
		self.coord = coord

	def children(self):
		nodelist = []
		if self.expr is not None:
			nodelist.append(("expr", self.expr))
		for i, child in enumerate(self.stmts or []):
			nodelist.append(("stmts[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Default(Node):
	__slots__ = ('stmts', 'coord', '__weakref__')

	def __init__(self, stmts, coord=None):
		self.stmts = stmts
		self.coord = coord

	def children(self):
		nodelist = []
		for i, child in enumerate(self.stmts or []):
			nodelist.append(("stmts[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Switch(Node):
	__slots__ = ('cond', 'stmt', 'coord', '__weakref__')

	def __init__(self, cond, stmt, coord=None):
		self.cond = cond
		self.stmt = stmt
		self.coord = coord

	def children(self):
		nodelist = []
		if self.cond is not None:
			nodelist.append(("cond", self.cond))
		if self.stmt is not None:
			nodelist.append(("stmt", self.stmt))
		return tuple(nodelist)

	attr_names = ()


class Example(Node):
	__slots__ = ('a', 'b', 'coord', '__weakref__')

	def __init__(self, a, b, coord=None):
		self.a = a
		self.b = b
		self.coord = coord

	def children(self):
		nodelist = []
		for i, child in enumerate(self.a or []):
			nodelist.append(("a[%d]" % i, child))
		for i, child in enumerate(self.b or []):
			nodelist.append(("b[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


