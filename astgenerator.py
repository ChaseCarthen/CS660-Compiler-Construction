#Props to https://github.com/eliben/pycparser/blob/master/pycparser/_ast_gen.py
import sys
import re

class Generator(object):
	def __init__(self,cfgfile):
		print "The cake is a lie"
		self.cfgfile = cfgfile
		self.data = [(node,params,tac) for(node,params,tac) in self.generate() ]

	def generate(self):
		print "HERE"
		cfile = open(self.cfgfile,"r")
		string = cfile.read()
		string = re.sub(r'#.*','',string)
		l = re.findall(r'[a-zA-Z]+:.*\[.*\].*{[^{}]*}',string)
		for i in l:
			node = re.findall(r"[a-zA-Z]+:",i)[0].replace(':','')
			params = re.findall(r'\[.*\]',i)[0].replace(']','').replace('[','').split(',')
			tac = re.findall(r"{[^{}]*}",i)[0].replace('}','').replace('{','').split()
			yield node, params, tac

class RawNode(object):
	def __init__(self, name, params, tac):
		self.name = name
		self.entries = []
		self.attribute = []
		self.child = []
		self.sequence = []

		for i in params:
			clean = i.rstrip('*')
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
		code += '\n' + self.generateAttributes()

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

		code += "	__slots__ = (%s)\n" % slots
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

    def _gen_attr_names(self):
        code = "    attr_names = (" + ''.join("%r, " % nm for nm in self.attribute) + ')'
        return code	



if __name__ == "__main__":
	astgen = Generator("ast.cfg")
	astgen.generate()