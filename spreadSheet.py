#!/usr/bin/env python
import sys
import copy
from Cell import Cell

class CycleException(Exception):
	"""Exception for cyclic dependencies"""
	def __init__(self, cyclePart):
		self.arg = ", ".join(s for s in cyclePart)

	def __str__(self):
		return "There is cycle in the dependency graph among " + self.arg

class SpreadsheetCal:
	"""
		Spreadsheet calculator class 
	"""
	def __init__(self):
		init_line = sys.stdin.readline()
		self.col,self.row = map(int,init_line.split())
		self.dependencyGraph = {}
		self.cellBook = {}
		self.cellsWithDepen = []
		self.cells = {}

	def initialRead(self):
		"""
		initialize the calculator with size of the spreadsheet

		args: 
			None

		return:
			cells with 0 in-degree
		"""
		for row in xrange(self.row):
			for col in xrange(self.col):
				value = sys.stdin.readline()
				new_cell = Cell(self.calId(row,col), value)
				new_cell.evaluate(self.cellBook)
				if not new_cell.evaluated:
					self.dependencyGraph[new_cell.getId()] = new_cell.getDependency()
					self.cellsWithDepen.append(new_cell.getId())
					self.cells[new_cell.getId()] = new_cell
				
	def calculate(self):
		"""
		Calculate the cell value

		args: 
			None

		return:
			None
		"""
		try:
			while True:
				sourceCell = self.inDegree()
				if sourceCell:
					for source in sourceCell: 
						self.cells[source].setDependency([])
						self.cells[source].evaluate(self.cellBook)
						del self.dependencyGraph[source]
						self.cellsWithDepen.remove(source)
				else:
					if not self.cellsWithDepen:
						break
					else:
						# if there is no source cells while there are still uncalculated cells, cycles exist 
						raise CycleException(self.cellsWithDepen)
		except CycleException as e:
			print e
			sys.exit(1)


	def inDegree(self):
		"""
		Calculate the cells with 0 in-degree

		args: 
			None

		return:
			cells with 0 in-degree
		"""
		if not self.cellsWithDepen:
			return []

		temp = copy.copy(self.cellsWithDepen)
		for cell in self.cellsWithDepen:
			depen = self.dependencyGraph[cell]
			count = len(depen)
			for depenCell in depen:
				if depenCell in self.cellBook:
					count -= 1
			if count != 0:
				temp.remove(cell)
		return temp 

	def formattedPrint(self):
		"""
		Print the result in the required format
		"""
		print "%d %d"%(self.col, self.row)
		for row in xrange(self.row):
			for col in xrange(self.col):
				print "%.5f"%self.cellBook[self.calId(row,col)]

	def calId(self, row, col):
		"""
		Transfer row and col into form of "A1", "A2"

		args: 
			row, int
			col, int

		return:
			id, string
		"""
		return chr(row + 65) + str(col + 1)

	def main(self):
		"""
		Interface with user
		"""
		self.initialRead()
		self.calculate()
		self.formattedPrint()


if __name__ == '__main__':
	instance = SpreadsheetCal()
	instance.main()
