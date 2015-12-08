ignored = [0,1,26,27]
results = [2,3]
arguments = [4,5,6,7]
temporary = [8,9,10,11,12,13,14,15,24,25]
saved = [16,17,18,19,20,21,22,23,24]

class RegisterAllocation(object):
  '''
  2-3 results $v0 - $v1
  4-7 arguments $a0-$a3
  8-15,24-25 temporaries $t0-$t9
  16-24 saved $s0-$s7
  28 global pointer $gp
  29 stack pointer $sp
  30 frame pointer $fp
  31 return address $ra
  '''

  def __init__(self):
    # Init all registers to empty
    # TODO: exempt the reserved registers from the list
    self.registers = {}
    self.saved = {}
    self.temporary = {}
    for i in range(0,32):
      if not i in ignored:
        self.registers[i] = None
    for i in range(0,8):
      self.saved["$s"+str(i)] = None
    for i in range(0,10):
      self.temporary["$t" + str(i)] = None 

  # Get the next temporary register
  def getTemporaryRegister(self, name):
    for index in self.temporary:
      if not self.temporary[index]:
        self.temporary[index] = name
        return index

    return 0
  # Get the next saved register
  def getSavedRegister(self, name):
    for index in self.saved:
      if not self.saved[index]:
        self.saved[index] = name
        return index

    # Register spilling happens yall
    return 0

  def getResultRegister(self, name):
    for index in results:
      if not self.registers[index]:
        self.registers[index] = name
        return index

    return 0

  def getArgumentRegister(self, name):
    for index in arguments:
      if not self.registers[index]:
        self.registers[index] = name
        return index

    return 0

  def freeRegisterByValue(self, item):
    for index, value in self.registers.items():
      if value == item:
        self.registers[index] = None
        return True

    return False

  def freeRegisterByName(self, name):
    self.registers[name] = None

  def findRegisterByName(self, name):
    return self.registers[name]

  def findRegisterByValue(self, item):
    for index, value in self.registers.items():
      if value == item:
        return self.registers[index]

    return False
