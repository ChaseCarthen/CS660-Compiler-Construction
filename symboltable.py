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

  def STAccess(self, name):
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
      except:
        tree[node.GetKey()] = node
        self.stack.append(tree)

  def _CheckStack(self, name, pointer):
    tree = self.stack.pop()

    if not self._CheckTree(tree, name):
      self._CheckStack(name, pointer)

    self.stack.append(tree)


  def _CheckTree(self, tree, key):
    value = None
    try:
      value = tree[key]
    except:
      pass
    return value
 
  def _Retrieve(self, node):
    pass

  def EndInsert(self):
    self.insert = False

  def EndScope(self):
    self.insert = True
    self.stack.pop()

  def NewScope(self):
    self.insert = True
    tree = bintrees.RBTree()
    self.stack.append(tree)



class SymbolTreeNode(object):
  """docstring for symboltable"""

  def __init__(self, type_var = None, name = None, value = None, line = None, line_loc = None):
    self.info = { "Type" : type_var, "Name" : name, "Value" : value, 
                  "Line" : line, "CharacterLocation" : line_loc }

  def GetKey(self):
    return self.info["Name"]

  def CheckInsert(self):
    return (self.info["Type"] and self.info["Name"] and self.info["Value"] and self.info["Line"] and self.info["CharacterLocation"])

  def __str__(self):
    message = ""
    message = message + "Type: " + str(self.info["Type"]) + ", "
    message = message + "Name: " + str(self.info["Name"]) + ", "
    message = message + "Value: " + str(self.info["Value"]) + ", "
    message = message + "Line: " + str(self.info["Line"]) + ", "
    message = message + "CharacterLocation: " + str(self.info["CharacterLocation"]) + "."
    return message
    
