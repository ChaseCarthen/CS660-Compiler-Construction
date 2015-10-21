from symboltable import *
from CompilerExceptions import *

def StackDump(table, f, number):
  f.write("============================ Begin Stack Dump " + str(number) + " ============================\n\n")
  f.write(str(table))
  f.write("\n\n============================ End Stack Dump " + str(number) + " ============================\n\n")


# Open file to dump the stack
stack_file = open("symboltable_dump.txt", 'w')
st = SymbolTable()

import os
os.system('clear')

print("Check File symboltable_dump.txt to view all the stack dumps.")

print("\nBuilding Function int foo with parameters int a, char b.")
tq = []
var1 = VariableNode(tq, ['int'], 'a', 1, 1)
var2 = VariableNode(tq, ['char'], 'b', 1, 1)
foo = FunctionNode([var1, var2], ['int'], 'foo', 1, 1)
print(foo)

print("\nAdding foo to the stack, and printing stack dump Number 1.")
st.InsertNode(foo)
StackDump(st, stack_file, 1)

print("\nInserting Variable int c to the scope 0 and dump stack Number 2.")
var3 = VariableNode(tq, ['int'], 'c', 2, 1)
st.InsertNode(var3)
StackDump(st, stack_file, 2)

print("\nWill Attempt to add in char c to the scope 0 and dump stack Number 3.")
var4 = VariableNode(tq, ['char'], 'c', 2, 1)

try:
  st.InsertNode(var4)
except SymbolTableError, e:
  print("SymbolTableError Caught.")
  print(e)

StackDump(st, stack_file, 3)

print("\nSwitch scope and overshadow int c and dump stack Number 4.")
st.NewScope()
try:
  st.InsertNode(var4)
except SymbolTableWarning, e:
  print("SymbolTableWarning Caught.")
  print(e)

StackDump(st, stack_file, 4)

print("\nSwitch scope and add int e and dump stack Number 5.")
var1 = VariableNode(tq, ['int'], 'e', 3, 1)
st.NewScope()
st.InsertNode(var1)
StackDump(st, stack_file, 5)

print("\nDo a check to see if the itentifier c Exists.")
st.Retrieve('c')
print("Successfully found Identifier c.")

print("\nDo a check to see if the itentifier d Exists.")
try:
  st.Retrieve('d')
except SymbolTableError, e:
  print("SymbolTableError Caught.")
  print(e)

print("\nTake off two scopes, dump stack Number 6, and check for the int e.")

st.EndScope()
st.EndScope()
StackDump(st, stack_file, 6)

try:
  st.Retrieve('e')
except SymbolTableError, e:
  print("SymbolTableError Caught.")
  print(e)


stack_file.close()
