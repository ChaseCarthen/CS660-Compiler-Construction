import bintrees
from CompilerExceptions import SymbolTableError
import sys

class SymbolTable(object):
  """docstring for SymbolTable"""

  def __init__(self):
    self.stack = []
    self.insert = True
    tree = bintrees.RBTree()
    self.stack.append(tree)
    self.pointer = None

  def Retrieve(self, name):
    self.pointer = None
    self._CheckStack(name, self.pointer)
    if not self.pointer:
      raise SymbolTableError("There is no value in the symbol table of that type.")

  def Insert(self, var = None, name = None,  line = None, line_loc = None):
    node = SymbolTreeNode(var, name, line, line_loc)
    try:
      InsertNode(self, node)
    except SymbolTableError,e:
      raise SymbolTableError(str(e))

  def InsertNode(self, node):
    if node == None:
      raise SymbolTableError("The Insert did not have all required Values: \n" + str(node))

    if not node.CheckInsert():
      raise SymbolTableError("The Insert did not have all required Values: \n" + str(node))
    
    print("Inserting to the tree at stack location: " + str(len(self.stack)))
    tree = self.stack.pop()
    
    if self._CheckTree(tree, node.GetKey()):
        self.stack.append(tree)
        raise SymbolTableError("The variable added to tree exists at this scope.")
    else:
      tree[node.GetKey()] = node
      self.stack.append(tree)

  def _CheckStack(self, name, pointer):
    if len(self.stack) == 0:
        return
    tree = self.stack.pop()
    pointer = self._CheckTree(tree, name)

    if not pointer:
      self._CheckStack(name, pointer)
    else:
      self.pointer = pointer

    # check for stack overflow -- later
    self.stack.append(tree)


  def _CheckTree(self, tree, key):
    value = None
    try:
      value = tree[key]
    except:
      pass
    return value

  def GetValue(self):
    return self.pointer.info["Value"]

  def GetType(self):
    return self.pointer.info["Type"]

  def GetLineNumber(self):
    return self.pointer.info["Line"]

  def GetCharPos(self):
    return self.pointer.info["CharacterLocation"]

  def SetValue(self,val):
    # Check for type conflicts int to float conversions here
    self.pointer.info["Value"] = val
  def SetType(self,typed):
    self.pointer.info["Type"] = typed 

  def EndInsert(self):
    self.insert = False

  def EndScope(self):
    self.insert = True
    self.stack.pop()

  def NewScope(self):
    self.insert = True
    tree = bintrees.RBTree()
    self.stack.append(tree)

  def StackDump(self):
    print "Stack Dump: "
    for treeIndex in range(len(self.stack)):
      print "Scope: " + str(treeIndex)
      print "========= Scope Contents ========"
      for info in self.stack[treeIndex]:
        print self.stack[treeIndex][info]
      print "========= End of Scope Contents ========="



class SymbolTreeNode(object):
  """docstring for symboltable"""

  def __init__(self, type_var = None, name = None, line = None, line_loc = None):
    self.info = { "Type" : type_var, "Name" : name, "Line" : line, "CharacterLocation" : line_loc}

  def GetKey(self):
    return self.info["Name"]

  def CheckInsert(self):
    return (self.info["Type"] != None and self.info["Name"] and self.info["Line"] != None and self.info["CharacterLocation"] != None)
  
  def SetName(self,name):
    self.info["Name"] = name
    print name

  def SetType(self,Type):
    self.info["Type"] = Type

  def __str__(self):
    message = ""
    message = message + "Type: " + str(self.info["Type"]) + ", "
    message = message + "Name: " + str(self.info["Name"]) + ", "
    message = message + "Line: " + str(self.info["Line"]) + ", "
    message = message + "CharacterLocation: " + str(self.info["CharacterLocation"]) +"."
    return message
    
# A pointer node to be propagated around the pointer grammar symbol
class PointerNode(SymbolTreeNode):
  """A pointer node to be place into the symbol table?"""

  def __init__(self, tq=None, type_var = '', name = '', line = 0, line_loc = 0):
    super(PointerNode,self).__init__(type_var,name,value,line,line_loc) # Call base class of this guy which is SymbolTableNode
    #self.info["NumberOfIndirections"] = 1 
    self.numindirection = 1
    if tq != None:
      self.typequalifiers = tq # This could be a list!
    else:
      self.typequalifiers = [] # Empty list means we have no type qualifiers

  def AddIndirection(self):
    self.numindirection += 1

  def AddTypeQualifiers(self,tq):
    self.typequalifiers += tq

  def __str__(self):
    string = super(PointerNode,self).__str__() 
    string += "Number of Indirections: " + str(self.numindirection) + ", "
    string += "Type Qualifiers: " + str(self.typequalifiers)
    return string

class FunctionNode(SymbolTreeNode):
  """A function node"""
  def __init__(self, parameters = [], type_var = '', name = '', line = 0, line_loc = 0):
    super(FunctionNode, self).__init__(type_var, name, line, line_loc)
    self.parameters = parameters

  def __str__(self):
    string = super(PointerNode,self).__str__()
    string += "\nParameter List\n----------------\n"
    
    for i in self.parameters:
      string = string + str(i) + '\n'

    return string

class VariableNode(SymbolTreeNode):
  """A function node"""
  def __init__(self, type_var = '', name = '', line = 0, line_loc = 0):
    super(VariableNode, self).__init__(type_var, name, line, line_loc)

  def __str__(self):
    string = super(PointerNode,self).__str__()
    return string
