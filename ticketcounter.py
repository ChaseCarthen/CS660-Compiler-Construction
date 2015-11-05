class TicketCounter(object):
	def __init__(self,name):
		self.count = 100000 - 1
		self.name = name
	def GetNextTicket(self):
		self.count += 1
		return self.name + str(self.count)
	def GetCurrentTicket(self):
		return self.name + str(self.count)