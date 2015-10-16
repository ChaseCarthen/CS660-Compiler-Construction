import bintrees
from CompilerExceptions import SymbolTableError

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


  def Insert(self, var = None, name = None, value = None, line = None, line_loc = None):
    node = SymbolTreeNode(var, name, value, line, line_loc)
    if not node.CheckInsert():
      raise SymbolTableError("The Insert did not have all required Values: \n" + str(node))
    else:
      print("Inserting to the tree at stack location: " + str(len(self.stack)))
      tree = self.stack.pop()
      
      if self._CheckTree(tree, node.GetKey()):
        self.stack.append(tree)
        raise SymbolTableError("The variable added to tree exists at this scope.")
      else:
        tree[node.GetKey()] = node
        self.stack.append(tree)

  def _CheckStack(self, name, pointer):

    tree = self.stack.pop()
    pointer = self._CheckTree(tree, name)

    if not pointer:
      self._CheckStack(name, pointer)

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
        print info
      print "========= End of Scope Contents ========="



class SymbolTreeNode(object):
  """docstring for symboltable"""

  def __init__(self, type_var = None, name = None, value = None, line = None, line_loc = None):
    self.info = { "Type" : type_var, "Name" : name, "Value" : value, 
                  "Line" : line, "CharacterLocation" : line_loc }

  def GetKey(self):
    return self.info["Name"]

  def CheckInsert(self):
    return (self.info["Type"] and self.info["Name"] and self.info["Value"] != None and self.info["Line"] != None and self.info["CharacterLocation"] != None)

  def __str__(self):
    message = ""
    message = message + "Type: " + str(self.info["Type"]) + ", "
    message = message + "Name: " + str(self.info["Name"]) + ", "
    message = message + "Value: " + str(self.info["Value"]) + ", "
    message = message + "Line: " + str(self.info["Line"]) + ", "
    message = message + "CharacterLocation: " + str(self.info["CharacterLocation"]) + "."
    return message
    

