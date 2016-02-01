#!/usr/bin/env python
from expressionTree import expTree

class Cell:
	"""
	Class for each cell in the spreadsheet
	"""
	def __init__(self, Id, val):
		self.id = Id
		self.evaluated = False
		self.expTree = expTree(val)
		self.dependency = self.expTree.getDependency()
		self.result = None

	def evaluate(self,cellBook):
		"""
		Evaluate the tree related to this cell

		args: 
			cellBook, dictionary with currently available cell values

		return:
			None
		"""
		if not self.dependency:
			self.result = self.expTree.evaluate(cellBook)
			cellBook[self.id] = self.result
			self.evaluated = True

	def setDependency(self, newDepen):
		self.dependency = newDepen

	def getDependency(self):
		return self.dependency

	def getId(self):
		return self.id

	def getResult(self):
		return self.result

if __name__ == '__main__':
	instance = Cell("A","1","C1 B1 -")
	instance.evaluate({})
	if instance.evaluated:
		print instance.getResult()
	else:
		print instance.dependency
