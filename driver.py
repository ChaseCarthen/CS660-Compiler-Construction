from cparser import Parser
import sys
from symboltable import SymbolTable



# Read the file from command line
input_file = open(sys.argv[1], 'r')
data = input_file.read()
input_file.close()

# Build and Call the scanner
scan = Parser(data)
st = SymbolTable()
scan.set_symbol_table(st)
#scan.scan(data)
scan.run()

print
print
print
print
st.StackDump()
