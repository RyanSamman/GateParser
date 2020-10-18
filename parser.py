import re
import inspect
from sys import argv
from os import stat
from tokenizer import parseExpression
from stack import Stack

# No idea what to call this, so Interpreter it is
class Interpreter:
	def __init__(self, filename):
		self.memory = {
			# Predefined Functions
			"AND": lambda i1, i2: i1 & i2,
			"OR":  lambda i1, i2: i1 | i2,
			"XOR": lambda i1, i2: i1 ^ i2,
			"NOT": lambda i1: i1 ^ -1,
			"OUT": lambda i: print(i),
			"OUTBIN": lambda i: print(bin(i)),
			"=": lambda key, value: self.addVariableToMemory(key, value),
		}

		# TODO: Update operators dynamically & at runtime
		self.operators = ["AND", "OR", "XOR", "NOT", "OUT", "OUTBIN"]

		expressions = self.retrieveFileContents(filename)

		for expression in expressions:
			self.evaluateExpression(expression)


	def evaluateExpression(self, expression):
		stack = Stack()
		postfix = parseExpression(expression, self.operators)

		for token in postfix:
			if not self.isTokenFunction(token):
				stack.push(token)
			else:
				argumentCount = self.getArguments(token)
				arguments = [stack.pop() for _ in range(argumentCount)]
				arguments = [self.memory.get(a, a) for a in arguments]
				result = self.memory[token](*arguments)
				stack.push(result)

		
	def addVariableToMemory(self, value, key):
		try:
			self.memory[key] = eval(value)
		except TypeError:
			self.memory[key] = value

	def isTokenFunction(self, token):
		if token not in self.memory:
			return False

		return inspect.isfunction(self.memory[token])

	@staticmethod
	def retrieveFileContents(filename):
		with open(filename, "r") as file:
			# Support lines ending in .
			return [re.sub('\.$', '', l) for l in file if not re.match("^\s*\/\/.*$", l)]

	def getArguments(self, token):
		function = self.memory[token]
		args = inspect.getfullargspec(function)[0]
		return len(args)


if __name__ == "__main__":
	codeToRun = argv[1] or "code3.txt"
	Interpreter(codeToRun)
