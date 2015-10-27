#Props to https://github.com/eliben/pycparser/blob/master/pycparser/_ast_gen.py
import sys
import re
import pprint
from string import Template

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
			slots += ", 'coord', '__weakref__'"
			arglist = '(self, %s, coord=None)' % args
		else:
			slots = "'coord', '__weakref__'"
			arglist = '(self, coord=None)'

		code += "	__slots__ = (%s)\n\n" % slots
		code += "	def __init__%s:\n" %arglist

		for name in self.entries + ['coord']:
			code += "        self.%s = %s\n" % (name, name)

		return code

	def makeBabies(self):
	    code = '    def children(self):\n'

	    if self.entries:
	        code += '        nodelist = []\n'

	        for child in self.child:
	            code += (
	                '        if self.%(child)s is not None:' +
	                ' nodelist.append(("%(child)s", self.%(child)s))\n') % (
	                    dict(child=child))

	        for seq in self.sequence:
	            code += (
	                '        for i, child in enumerate(self.%(child)s or []):\n'
	                '            nodelist.append(("%(child)s[%%d]" %% i, child))\n') % (
	                    dict(child=sequence))

	        code += '        return tuple(nodelist)\n'
	    else:
	        code += '        return ()\n'

	    return code

	def generateAttributes(self):
		code = "    attr_names = (" + ''.join("%r, " % nm for nm in self.attribute) + ')'
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

class Node(object):
    __slots__ = ()
    """ Base class for AST nodes. Auto-Generated.
    """

    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
        """ buf:
                Open IO buffer into which the Node is printed.
            offset:
                Initial offset (amount of leading spaces)
            attrnames:
                True if you want to see the attribute names in
                name=value pairs. False to only see the values.
            nodenames:
                True if you want to see the actual node names
                within their parents.
            showcoord:
                Do you want the coordinates of each Node to be
                displayed.
        """
        lead = ' ' * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
        else:
            buf.write(lead + self.__class__.__name__+ ': ')
        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self,n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)
        if showcoord:
            buf.write(' (at %s)' % self.coord)
        buf.write('\n')
        for (child_name, child) in self.children():
            child.show(
                buf,
                offset=offset + 2,
                attrnames=attrnames,
                nodenames=nodenames,
                showcoord=showcoord,
                _my_node_name=child_name)

'''


if __name__ == "__main__":
	astgen = Generator("ast.cfg")
	astgen.generate(open('ast.py', 'w'))