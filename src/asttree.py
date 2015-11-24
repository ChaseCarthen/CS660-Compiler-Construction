#-----------------------------------------------------------------
# ** DISCLAIMER **
# This code was automatically generated from the file:
# src/ast.cfg
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
	__slots__ = ('stmts','text', 'lines', '__weakref__')

	def __init__(self, stmts, lines=None,text=""):
		self.stmts = stmts
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.stmts or []):
			nodelist.append(("stmts[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class FuncDecl(Node):
	__slots__ = ('ParamList', 'type', 'name','text', 'lines', '__weakref__')

	def __init__(self, ParamList, type, name, lines=None,text=""):
		self.ParamList = ParamList
		self.type = type
		self.name = name
		self.lines = lines
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
	__slots__ = ('ParamList', 'type', 'name', 'expression', 'numlocals','text', 'lines', '__weakref__')

	def __init__(self, ParamList, type, name, expression, numlocals, lines=None,text=""):
		self.ParamList = ParamList
		self.type = type
		self.name = name
		self.expression = expression
		self.numlocals = numlocals
		self.lines = lines
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

	attr_names = ('name', 'numlocals', )


class FuncCall(Node):
	__slots__ = ('ParamList', 'type', 'name','text', 'lines', '__weakref__')

	def __init__(self, ParamList, type, name, lines=None,text=""):
		self.ParamList = ParamList
		self.type = type
		self.name = name
		self.lines = lines
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
	__slots__ = ('NodeList','text', 'lines', '__weakref__')

	def __init__(self, NodeList, lines=None,text=""):
		self.NodeList = NodeList
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.NodeList or []):
			nodelist.append(("NodeList[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Return(Node):
	__slots__ = ('expr','text', 'lines', '__weakref__')

	def __init__(self, expr, lines=None,text=""):
		self.expr = expr
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.expr is not None:
			nodelist.append(("expr", self.expr))
		return tuple(nodelist)

	attr_names = ()


class VariableCall(Node):
	__slots__ = ('type', 'name', 'isPtr','text', 'lines', '__weakref__')

	def __init__(self, type, name, isPtr, lines=None,text=""):
		self.type = type
		self.name = name
		self.isPtr = isPtr
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = (' name', 'isPtr', )


class ParamList(Node):
	__slots__ = ('params','text', 'lines', '__weakref__')

	def __init__(self, params, lines=None,text=""):
		self.params = params
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.params or []):
			nodelist.append(("params[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class StructDecl(Node):
	__slots__ = ('name', 'decls','text', 'lines', '__weakref__')

	def __init__(self, name, decls, lines=None,text=""):
		self.name = name
		self.decls = decls
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(("decls[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class StructCall(Node):
	__slots__ = ('name', 'field','text', 'lines', '__weakref__')

	def __init__(self, name, field, lines=None,text=""):
		self.name = name
		self.field = field
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('name', 'field', )


class Decl(Node):
	__slots__ = ('name', 'type', 'init', 'wordsize','text', 'lines', '__weakref__')

	def __init__(self, name, type, init, wordsize, lines=None,text=""):
		self.name = name
		self.type = type
		self.init = init
		self.wordsize = wordsize
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		if self.init is not None:
			nodelist.append(("init", self.init))
		return tuple(nodelist)

	attr_names = ('name', 'wordsize', )


class DeclList(Node):
	__slots__ = ('decls','text', 'lines', '__weakref__')

	def __init__(self, decls, lines=None,text=""):
		self.decls = decls
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(("decls[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class IterStatement(Node):
	__slots__ = ('init', 'cond', 'next', 'stmt', 'isdowhile', 'name','text', 'lines', '__weakref__')

	def __init__(self, init, cond, next, stmt, isdowhile, name, lines=None,text=""):
		self.init = init
		self.cond = cond
		self.next = next
		self.stmt = stmt
		self.isdowhile = isdowhile
		self.name = name
		self.lines = lines
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
	__slots__ = ('lines', '__weakref__', 'text')

	def __init__(self, lines=None,text=""):
		self.lines = lines
		self.text = text

	def children(self):
		return ()

	attr_names = ('', )


class Continue(Node):
	__slots__ = ('lines', '__weakref__', 'text')

	def __init__(self, lines=None,text=""):
		self.lines = lines
		self.text = text

	def children(self):
		return ()

	attr_names = ('', )


class ArrDecl(Node):
	__slots__ = ('name', 'type', 'init', 'dim', 'wordsize','text', 'lines', '__weakref__')

	def __init__(self, name, type, init, dim, wordsize, lines=None,text=""):
		self.name = name
		self.type = type
		self.init = init
		self.dim = dim
		self.wordsize = wordsize
		self.lines = lines
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

	attr_names = ('name', 'wordsize', )


class ArrRef(Node):
	__slots__ = ('name', 'subscript', 'type', 'dim','text', 'lines', '__weakref__')

	def __init__(self, name, subscript, type, dim, lines=None,text=""):
		self.name = name
		self.subscript = subscript
		self.type = type
		self.dim = dim
		self.lines = lines
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
	__slots__ = ('name', 'type', 'numindirections', 'wordsize', 'init','text', 'lines', '__weakref__')

	def __init__(self, name, type, numindirections, wordsize, init, lines=None,text=""):
		self.name = name
		self.type = type
		self.numindirections = numindirections
		self.wordsize = wordsize
		self.init = init
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ('name', 'numindirections', 'wordsize', 'init', )


class PtrRef(Node):
	__slots__ = ('name', 'type', 'offset','text', 'lines', '__weakref__')

	def __init__(self, name, type, offset, lines=None,text=""):
		self.name = name
		self.type = type
		self.offset = offset
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.type is not None:
			nodelist.append(("type", self.type))
		if self.offset is not None:
			nodelist.append(("offset", self.offset))
		return tuple(nodelist)

	attr_names = ('name', )


class Assignment(Node):
	__slots__ = ('op', 'lvalue', 'rvalue','text', 'lines', '__weakref__')

	def __init__(self, op, lvalue, rvalue, lines=None,text=""):
		self.op = op
		self.lvalue = lvalue
		self.rvalue = rvalue
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('cond', 'truecond', 'falsecond','text', 'lines', '__weakref__')

	def __init__(self, cond, truecond, falsecond, lines=None,text=""):
		self.cond = cond
		self.truecond = truecond
		self.falsecond = falsecond
		self.lines = lines
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
	__slots__ = ('cond', 'truecond', 'falsecond','text', 'lines', '__weakref__')

	def __init__(self, cond, truecond, falsecond, lines=None,text=""):
		self.cond = cond
		self.truecond = truecond
		self.falsecond = falsecond
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right', 'type','text', 'lines', '__weakref__')

	def __init__(self, left, right, type, lines=None,text=""):
		self.left = left
		self.right = right
		self.type = type
		self.lines = lines
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
	__slots__ = ('left', 'right','text', 'lines', '__weakref__')

	def __init__(self, left, right, lines=None,text=""):
		self.left = left
		self.right = right
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.left is not None:
			nodelist.append(("left", self.left))
		if self.right is not None:
			nodelist.append(("right", self.right))
		return tuple(nodelist)

	attr_names = ()


class IndOp(Node):
	__slots__ = ('value', 'type','text', 'lines', '__weakref__')

	def __init__(self, value, type, lines=None,text=""):
		self.value = value
		self.type = type
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.value is not None:
			nodelist.append(("value", self.value))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class RefOp(Node):
	__slots__ = ('value', 'type','text', 'lines', '__weakref__')

	def __init__(self, value, type, lines=None,text=""):
		self.value = value
		self.type = type
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.value is not None:
			nodelist.append(("value", self.value))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class BitNotOp(Node):
	__slots__ = ('value', 'type','text', 'lines', '__weakref__')

	def __init__(self, value, type, lines=None,text=""):
		self.value = value
		self.type = type
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.value is not None:
			nodelist.append(("value", self.value))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class AbsOp(Node):
	__slots__ = ('value', 'type','text', 'lines', '__weakref__')

	def __init__(self, value, type, lines=None,text=""):
		self.value = value
		self.type = type
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.value is not None:
			nodelist.append(("value", self.value))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class NegOp(Node):
	__slots__ = ('value', 'type','text', 'lines', '__weakref__')

	def __init__(self, value, type, lines=None,text=""):
		self.value = value
		self.type = type
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.value is not None:
			nodelist.append(("value", self.value))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class LogNotOp(Node):
	__slots__ = ('value', 'type','text', 'lines', '__weakref__')

	def __init__(self, value, type, lines=None,text=""):
		self.value = value
		self.type = type
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.value is not None:
			nodelist.append(("value", self.value))
		if self.type is not None:
			nodelist.append(("type", self.type))
		return tuple(nodelist)

	attr_names = ()


class Goto(Node):
	__slots__ = ('name','text', 'lines', '__weakref__')

	def __init__(self, name, lines=None,text=""):
		self.name = name
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('name', )


class Cast(Node):
	__slots__ = ('to_type', 'expr','text', 'lines', '__weakref__')

	def __init__(self, to_type, expr, lines=None,text=""):
		self.to_type = to_type
		self.expr = expr
		self.lines = lines
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
	__slots__ = ('type', 'value','text', 'lines', '__weakref__')

	def __init__(self, type, value, lines=None,text=""):
		self.type = type
		self.value = value
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('type', 'value', )


class String(Node):
	__slots__ = ('type', 'value','text', 'lines', '__weakref__')

	def __init__(self, type, value, lines=None,text=""):
		self.type = type
		self.value = value
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('type', 'value', )


class ExprList(Node):
	__slots__ = ('exprs','text', 'lines', '__weakref__')

	def __init__(self, exprs, lines=None,text=""):
		self.exprs = exprs
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.exprs or []):
			nodelist.append(("exprs[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class EmptyStatement(Node):
	__slots__ = ('lines', '__weakref__', 'text')

	def __init__(self, lines=None,text=""):
		self.lines = lines
		self.text = text

	def children(self):
		return ()

	attr_names = ('', )


class InitList(Node):
	__slots__ = ('exprs','text', 'lines', '__weakref__')

	def __init__(self, exprs, lines=None,text=""):
		self.exprs = exprs
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.exprs or []):
			nodelist.append(("exprs[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Label(Node):
	__slots__ = ('name', 'stmt','text', 'lines', '__weakref__')

	def __init__(self, name, stmt, lines=None,text=""):
		self.name = name
		self.stmt = stmt
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.stmt is not None:
			nodelist.append(("stmt", self.stmt))
		return tuple(nodelist)

	attr_names = ('name', )


class Type(Node):
	__slots__ = ('type', 'qualifier', 'storage','text', 'lines', '__weakref__')

	def __init__(self, type, qualifier, storage, lines=None,text=""):
		self.type = type
		self.qualifier = qualifier
		self.storage = storage
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('type', 'qualifier', 'storage', )


class ID(Node):
	__slots__ = ('name','text', 'lines', '__weakref__')

	def __init__(self, name, lines=None,text=""):
		self.name = name
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		return tuple(nodelist)

	attr_names = ('name', )


class StructDecl(Node):
	__slots__ = ('name', 'fields', 'size','text', 'lines', '__weakref__')

	def __init__(self, name, fields, size, lines=None,text=""):
		self.name = name
		self.fields = fields
		self.size = size
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.fields or []):
			nodelist.append(("fields[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', 'size', )


class Struct(Node):
	__slots__ = ('name', 'fields', 'size','text', 'lines', '__weakref__')

	def __init__(self, name, fields, size, lines=None,text=""):
		self.name = name
		self.fields = fields
		self.size = size
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.fields or []):
			nodelist.append(("fields[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', 'size', )


class StructRef(Node):
	__slots__ = ('name', 'field', 'offset', 'type','text', 'lines', '__weakref__')

	def __init__(self, name, field, offset, type, lines=None,text=""):
		self.name = name
		self.field = field
		self.offset = offset
		self.type = type
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		if self.field is not None:
			nodelist.append(("field", self.field))
		return tuple(nodelist)

	attr_names = ('name', 'offset', 'type', )


class Union(Node):
	__slots__ = ('name', 'decls','text', 'lines', '__weakref__')

	def __init__(self, name, decls, lines=None,text=""):
		self.name = name
		self.decls = decls
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.decls or []):
			nodelist.append(("decls[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ('name', )


class Case(Node):
	__slots__ = ('expr', 'stmts','text', 'lines', '__weakref__')

	def __init__(self, expr, stmts, lines=None,text=""):
		self.expr = expr
		self.stmts = stmts
		self.lines = lines
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
	__slots__ = ('stmts','text', 'lines', '__weakref__')

	def __init__(self, stmts, lines=None,text=""):
		self.stmts = stmts
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.stmts or []):
			nodelist.append(("stmts[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


class Switch(Node):
	__slots__ = ('cond', 'stmt','text', 'lines', '__weakref__')

	def __init__(self, cond, stmt, lines=None,text=""):
		self.cond = cond
		self.stmt = stmt
		self.lines = lines
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
	__slots__ = ('a', 'b','text', 'lines', '__weakref__')

	def __init__(self, a, b, lines=None,text=""):
		self.a = a
		self.b = b
		self.lines = lines
		self.text = text

	def children(self):
		nodelist = []
		for i, child in enumerate(self.a or []):
			nodelist.append(("a[%d]" % i, child))
		for i, child in enumerate(self.b or []):
			nodelist.append(("b[%d]" % i, child))
		return tuple(nodelist)

	attr_names = ()


