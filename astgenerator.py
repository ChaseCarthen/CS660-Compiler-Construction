#Props to https://github.com/eliben/pycparser/blob/master/pycparser/_ast_gen.py
import sys
import re
import pprint
from string import Template
from ticketcounter import *

class Generator(object):
	def __init__(self,cfgfile):
		self.cfgfile = cfgfile
		self.data = [RawNode(node,params,tac) for(node,params,tac) in self.parse()]

	def parse(self):
		cfile = open(self.cfgfile,"r")
		string = cfile.read()
		string = re.sub(r'#.*','',string)
		l = re.findall(r'[a-zA-Z]+:.*\[.*\].*{[^{}]*}',string)
		for i in l:
			node = re.findall(r"[a-zA-Z]+:",i)[0].replace(':','')
			params = re.findall(r'\[.*\]',i)[0].replace(']','').replace('[','').split(',')
			tac = re.findall(r"{[^{}]*}",i)[0].replace('}','').replace('{','').split()
			yield node, params, tac

	def generate(self, file=None):
		""" Generates the code into file, an open file buffer.
		"""
		code = Template(_PROLOGUE_COMMENT).substitute(
		    cfg_filename=self.cfgfile)
		code += _PROLOGUE_CODE
		for node in self.data:
			code += str(node.generate()) + '\n\n\n'

		file.write(code)	

class RawNode(object):
	def __init__(self, name, params, tac):
		self.name = name
		self.entries = []
		self.attribute = []
		self.child = []
		self.sequence = []

		for i in params:
			clean = i.rstrip('*')
			clean = clean.strip(' ')
			if i is not '':
				self.entries.append(clean)

			if i.endswith('**'):
				self.sequence.append(clean)
			elif i.endswith('*'):
				self.child.append(clean)
			else:
				self.attribute.append(i)

	def generate(self):
		code = self.start()
		code += '\n' + self.makeBabies()
		#code += '\n' + self.generateTAC()
		code += '\n' + self.generateAttributes()
		return code

	def start(self):
		code = "class %s(Node):\n" % self.name

		if self.entries:
			args = ', '.join(self.entries)
			slots = ', '.join("'{0}'".format(e) for e in self.entries)
			slots += ",'text', 'coord', '__weakref__'"
			arglist = '(self, %s, coord=None,text="")' % args
		else:
			slots = "'coord', '__weakref__'"
			arglist = '(self, coord=None,text="")'

		code += "\t__slots__ = (%s)\n\n" % slots
		code += "\tdef __init__%s:\n" %arglist

		for name in self.entries + ['coord','text']:
			code += "\t\tself.%s = %s\n" % (name, name)

		return code

	def makeBabies(self):
	    code = '\tdef children(self):\n'

	    if self.entries:
	        code += '\t\tnodelist = []\n'

	        for child in self.child:
	            code += (
	                '\t\tif self.%(child)s is not None:\n' +
	                '\t\t\tnodelist.append(("%(child)s", self.%(child)s))\n') % (
	                    dict(child=child))

	        for seq in self.sequence:
	            code += (
	                '\t\tfor i, child in enumerate(self.%(child)s or []):\n'
	                '\t\t\tnodelist.append(("%(child)s[%%d]" %% i, child))\n') % (
	                    dict(child=seq))

	        code += '\t\treturn tuple(nodelist)\n'
	    else:
	        code += '\t\treturn ()\n'

	    return code

	def generateAttributes(self):
		code = "\tattr_names = (" + ''.join("%r, " % nm for nm in self.attribute) + ')'
		return code	

	def generateTAC(self, tac):
		stuff = tac
		return tac

_PROLOGUE_COMMENT = \
r'''#-----------------------------------------------------------------
# ** DISCLAIMER **
# This code was automatically generated from the file:
# $cfg_filename
#
# AST Node classes:
#  - Heavy Inspiration as drawn from the team developing pycparser
#  - Heavily altered to handle Three Address code
#  - Shut up Terence
#
#-----------------------------------------------------------------
'''

_PROLOGUE_CODE = r'''
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

'''


if __name__ == "__main__":
	astgen = Generator("ast.cfg")
	astgen.generate(open('asttree.py', 'w'))