


class RegisterAllocation(object):

  def __init__(self):
    # Init all registers to empty
    # TODO: exempt the reserved registers from the list
    self.registers = {}
    for i in range(2,32):
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
