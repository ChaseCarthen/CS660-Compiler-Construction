import sys
sys.path.insert(0, 'src/')

from cparser import Parser
from symboltable import SymbolTable
from MIPSGenerator import MipsGenerator
import argparse

# for more information goto https://docs.python.org/2/library/argparse.html
parser = argparse.ArgumentParser(description='Compiler for cs660.')
parser.add_argument("source",nargs='?',type=str,help="Specifies the input source file.")
parser.add_argument("-p",nargs=1,default=" ",type=str,dest="parselogfile",metavar='Parse Log Output', help="Specifies the parse log output file for production shifts and reduces.")
parser.add_argument("-t",nargs=1,default="tokenfile.log",type=str,dest="tokenfile", metavar='Token Log Output', help="The token log output file specifier.")
parser.add_argument("-v",default="Version 1.0.0",type=str,metavar='Version information.')
parser.add_argument("-g",default="tree.png",metavar="The graph picture file.",dest="graphfile")
parser.add_argument("-i",default="3AC.tac",metavar="The name of the .tac file.",dest="tacfile")
parser.add_argument("-c",action='store_true',dest="codeout",help="If exists then write the code to file.")

args = parser.parse_args()


if args.source != None:
	#print args.source
	# Read the file from command line
	input_file = open(args.source, 'r')
	data = input_file.read()
	input_file.close()

	# Build and Call the scanner
	if type(args.tokenfile) != str:
		args.tokenfile = args.tokenfile[0]

	scan = Parser(data, args.parselogfile != " ", args.parselogfile[0], args.tokenfile, args.graphfile, args.tacfile, args.codeout)
	st = SymbolTable()
	scan.set_symbol_table(st)
	#scan.scan(data)
	scan.run()

	bas = open("log/3AC.tac",'r')
	a = bas.read()
	bas.close()
	generator = MipsGenerator()
	assembly = generator.Parse(a)
	temp = args.source.split(".")
	filename = ""
	for i in temp[:len(temp)-1]:
		filename += i
		filename += "."
	filename += "asm"
	asm = open(filename, "w")
	asm.write(assembly)
	asm.close()
