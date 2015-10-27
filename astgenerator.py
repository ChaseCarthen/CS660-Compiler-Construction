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


if __name__ == "__main__":
	astgen = Generator("ast.cfg")
	astgen.generate()