ignored = [0,1,26,27]


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


  def getRegister(self, name):
    index = 2
    while index < 32 and self.registers[index]:
      index += 1

    if index == 32:
      return 0

    self.registers[index] = name
    return index

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
