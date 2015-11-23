import argparse

# for more information goto https://docs.python.org/2/library/argparse.html
parser = argparse.ArgumentParser(description='Compiler for cs660.')
parser.add_argument("source",nargs='?',type=str,help="Specifies the input source file.")
parser.add_argument("-p",nargs=1,default="",type=str,dest="parselogfile",metavar='Parse Log Output', help="Specifies the parse log output file for production shifts and reduces.")
parser.add_argument("-t",nargs=1,default="tokenfile.txt",type=str,dest="tokenfile", metavar='Token Log Output', help="The token log output file specifier.")
parser.add_argument("-v",default="Version 1.0.0",type=str,metavar='Version information.')
args = parser.parse_args()
if args.parselogfile != '':
	print "Enable parse log"

print args
