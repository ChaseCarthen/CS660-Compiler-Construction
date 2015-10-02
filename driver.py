from cparser import Parser
import sys

# Read the file from command line
input_file = open(sys.argv[1], 'r')
data = input_file.read()
input_file.close()

# Build and Call the scanner
scan = Parser(data)
scan.scan(data)
