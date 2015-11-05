import bintrees
from CompilerExceptions import *
import sys

class SymbolTable(object):
  """docstring for SymbolTable"""

  def __init__(self):
    self.stack = []
    self.insert = True
    tree = bintrees.RBTree()
    tree["_type"] = {}
    self.stack.append(tree)
    self.pointer = None

  def Retrieve(self, name):
    self.pointer = None
    self._CheckStack(name, self.pointer)
    if not self.pointer:
      raise SymbolTableError("There is no value in the symbol table with name: " + str(name))

    return self.pointer

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

    tree = self.stack.pop()
    
    if self._CheckTree(tree, node.GetKey()):
        self.stack.append(tree)
        if not type(node) == type(FunctionNode()):
          raise SymbolTableError("The variable " + node.GetKey() +  " added to tree exists at this scope.")
        else:
          self.Retrieve(node.GetName())
          if not self.pointer.CheckParameters(node.parameters):
            raise SymbolTableError("Error function parameters do not match!")
          else:
            return
        

    self.pointer = None
    self._CheckStack(node.GetKey(), self.pointer)

    tree[node.GetKey()] = node
    self.stack.append(tree)

    if self.pointer:
      raise SymbolTableWarning("Overshadow of " + str(node.GetKey()) + " at line: " + str(self.pointer.GetLine()) + ".")

  def InsertNodePreviousStack(self, node):
    if node == None:
      raise SymbolTableError("The Insert did not have all required Values: \n" + str(node))

    if not node.CheckInsert():
      raise SymbolTableError("The Insert did not have all required Values: \n" + str(node))
    
    tree_holder = self.stack.pop()

    tree = self.stack.pop()
    
    if self._CheckTree(tree, node.GetKey()):
        self.stack.append(tree)
        self.stack.append(tree_holder)
        if not type(node) == type(FunctionNode()):
          raise SymbolTableWarning("Overshadow of " + str(node.GetKey()) + " at line: " + str(self.pointer.GetLine()) + ".")
        else:
          self.Retrieve(node.GetName())
          if not self.pointer.CheckParameters(node.parameters):
            raise SymbolTableError("Error function parameters do not match!")
          else:
            return


    self.pointer = None
    self._CheckStack(node.GetKey(), self.pointer)

    tree[node.GetKey()] = node
    self.stack.append(tree)
    self.stack.append(tree_holder)

    if self.pointer:
      raise SymbolTableWarning("Overshadow of value.")

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

  def CheckForType(self,name):
    if len(self.stack) == 0:
      return
    tree = self.stack.pop()
    typenode = self._CheckTree(tree, "_type")
    result = None

    if not typenode:
      result = self.CheckForType(name)
    else:
      if name in typenode:
        result = typenode[name]
      else:
        result = self.CheckForType(name)

    # check for stack overflow -- later
    self.stack.append(tree)
    return result

  def InsertNewType(self,name,typenode):
    self.stack[-1]["_type"][name] = typenode

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
    tree["_type"] = {}
    self.stack.append(tree)

  def StackDump(self):
    print "Stack Dump: "
    for treeIndex in range(len(self.stack)):
      print "Scope: " + str(treeIndex)
      print "========= Scope Contents ========"
      for info in self.stack[treeIndex]:
        print self.stack[treeIndex][info]
      print "========= End of Scope Contents ========="

  def __str__(self):
    string = ""
    for treeIndex in range(len(self.stack)):
      string = string + "Scope: " + str(treeIndex) + '\n'
      string = string + "========= Scope Contents ========\n"
      for info in self.stack[treeIndex]:
        string = string + str(self.stack[treeIndex][info]) + '\n'
      string = string + "========= End of Scope Contents =========\n"
    return string



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

  def SetType(self,Type):
    self.info["Type"] = Type

  def SetCharacterLocation(self,LineLoc):
    self.info["CharacterLocation"] = LineLoc

  def SetLine(self,Line):
    self.info["Line"] = Line

  def GetName(self):
    return self.info["Name"]

  def GetType(self):
    return self.info["Type"]

  def IsConstant(self):
    return False

  def GetCharacterLocation(self):
    return self.info["CharacterLocation"]

  def GetLine(self):
    return self.info["Line"]

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

  def __init__(self, tq = [], type_var = '', name = '', line = 0, line_loc = 0):
    super(PointerNode,self).__init__(type_var,name,line,line_loc) # Call base class of this guy which is SymbolTableNode
    #self.info["NumberOfIndirections"] = 1 
    self.numindirection = 1
    if tq == None:
      tq = []
    self.typequalifiers = tq # This could be a list!

  def AddIndirection(self):
    self.numindirection += 1

  def AddTypeQualifiers(self,tq):
    self.typequalifiers += tq

  def IsConstant(self):
    if 'const' in self.typequalifiers:
      return True
    return False

  def __str__(self):
    string = super(PointerNode,self).__str__() 
    string += "Number of Indirections: " + str(self.numindirection) + ", "
    string += "Type Qualifiers: " + str(self.typequalifiers)
    return string
    
  def SetQualifiers(self, tq):
    self.typequalifiers += tq

class FunctionNode(SymbolTreeNode):
  """A function node"""
  def __init__(self, parameters = [], type_var = '', name = '', line = 0, line_loc = 0):
    super(FunctionNode, self).__init__(type_var, name, line, line_loc)
    self.parameters = parameters

  def __str__(self):
    string = super(FunctionNode,self).__str__()
    string += "\n\tParameter List\n\t----------------\n"
    
    for i in self.parameters:
      string = string + '\t' + str(i) + '\n'

    return string

  def CheckParameters(self,params):
    good = True
    for i,j in zip(self.parameters,params):
      good = good and i.GetType() == j.GetType()
    if good:
      self.parameters = params
    return good
  def GetParameters(self):
    return self.parameters
  def SetQualifiers(self, tq):
    pass

class VariableNode(SymbolTreeNode):
  """A variable node"""
  def __init__(self, tq = [], type_var = '', name = '', line = 0, line_loc = 0):
    super(VariableNode, self).__init__(type_var, name, line, line_loc)
    self.typequalifiers = tq

  def __str__(self):
    string = super(VariableNode,self).__str__()
    string += " Type Qualifiers: " + str(self.typequalifiers)
    return string

  def SetQualifiers(self, tq):
    self.typequalifiers += tq

  def GetQualifiers(self):
    return self.typequalifiers

  def IsConstant(self):
    if 'const' in self.typequalifiers:
      return True
    return False

class ArrayNode(SymbolTreeNode):
  """An array node"""
  def __init__(self, tq = [], type_var = '', name = '', line = 0, line_loc = 0, dim = 0):
    super(ArrayNode, self).__init__(type_var, name, line, line_loc)
    self.dimensions = [dim]
    self.typequalifiers = tq

  def AddDimension(self,number):
    self.dimensions.append(number)

  def SetQualifiers(self, tq):
    self.typequalifiers += tq

  def GetQualifiers(self):
    return self.typequalifiers

  def __str__(self):
    string = super(ArrayNode, self).__str__()
    string = string + " Dimensions: " + str(self.dimensions) + ","
    string += " Type Qualifiers: " + str(self.typequalifiers)
    return string
