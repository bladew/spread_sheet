#!/usr/bin/env python
import re

class Node:
	"""
		Node in the expression tree

		args: 
			left, Node
			right, Node
			op, String/float 
	"""
	def __init__(self, left, right, op):
		self.left = left
		self.right = right
		self.op = op
		

class expTree:
	"""
		Expression tree

		args: 
			val, String, the corresponding expression
		"""
	simpleCal = {"+":lambda x,y:x + y,
				 "-":lambda x,y:x - y,
				 "*":lambda x,y:x * y,
				 "/":lambda x,y:x / y}

	def __init__(self, val):
		self.expression = val.split(' ')
		if '\n' in self.expression[-1]:
			self.expression[-1] = self.expression[-1][:-1]
		self.root = None
		self.dependency = []
		self.generateTree()

	def generateTree(self):
		"""
		Generate the tree with stack

		args: 
			None

		return:
			None
		"""
		nodeStack = []
		for c in self.expression:
			if c in expTree.simpleCal:
				right = nodeStack.pop(-1)
				left = nodeStack.pop(-1)
				nodeStack.append(Node(left,right,c))
			elif c in "++--":
				left = nodeStack.pop(-1)
				right = Node(None,None,float(1))
				nodeStack.append(Node(left,right,c[0]))
			else:
				match = re.match("[A-Z]\\d+", c)
				if match:
					nodeStack.append(Node(None,None, c))
					self.dependency.append(c)
				else:
					nodeStack.append(Node(None,None,float(c)))
		
		self.root = nodeStack.pop()


	def evaluate(self, cellBook):
		return self._evaluate(self.root, cellBook)

	def _evaluate(self, root, cellBook):
		"""
		Helper func for evaluating the tree

		args: 
			root, Node
			cellBook, Dictionary

		return:
			result of the this tree
		"""
		if root is None:
			return 0

		if root.left == None and root.right == None:
			if root.op in cellBook:
				return cellBook[root.op]
			else:
				return root.op
		else:
			left = self._evaluate(root.left, cellBook)
			right = self._evaluate(root.right, cellBook)
			return expTree.simpleCal[root.op](left,right)


	def getDependency(self):
		return self.dependency

if __name__ == '__main__':
	instance = expTree("4 5 * 2 /")
	print instance.evaluate({})
	instance = expTree("C1 B1 -")
	print instance.evaluate({"C1":2,"B1":2}),instance.getDependency()