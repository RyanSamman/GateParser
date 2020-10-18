import re
from stack import Stack
from typing import List

def tokenize(expression: str):
	'''
		Takes an expression, ex abc+(b*c)
		and parses it into an array of 'tokens'
		['abc', '+', 'b', '+', 'c']
	'''
	# Escape regex special characters
	operatorRegex = "".join(["+", "\-", "*", "\/","\(", "\)", "^", "="])
	tokenRegex = f"[^{operatorRegex}\s]+|[{operatorRegex}]"

	return re.findall(tokenRegex, expression)
def generatePostfixTokens(expression: List[str], operators: List[str] = []):
	# Reference:
	# https://www.geeksforgeeks.org/stack-set-2-infix-to-postfix/
	precidence = {"^": 3, "*": 2, "/": 2, "+": 1, "-": 1, "=": 0}
	stack = Stack()
	postfix = []

	for token in expression:
		if token not in ["^", "*", "/", "+", "-", "(", ")", '='] + operators:
			# If it's an operand, add it into the postfix
			postfix.append(token)

		elif token == '(':
			# If it's an opening parenthesis, add it to the stack
			stack.push('(')

		elif token == ')':
			# If it's a closing parenthesis, add operators to postfix
			# Until a '(' is found or the stack is empty
			while not stack.isEmpty() and stack.peek() != '(':
				postfix.append(stack.pop())
			
			# Remove closing parenthesis from stack
			if stack.peek() == '(':
				stack.pop()

		else: # It's an operator
			# If the current token's 'precidence' (Eg, * is evaluated before +)
			# is less than or equal to the one in the stack, 
			while not stack.isEmpty() and stack.peek() != '(' and precidence.get(token, 1) <= precidence.get(stack.peek(), 1):
				postfix.append(stack.pop())

			stack.push(token)

	while not stack.isEmpty():
		postfix.append(stack.pop())

	return postfix

def parseExpression(expression: List[str], operators: List[str] = []):
	tokens = tokenize(expression)
	postfix = generatePostfixTokens(tokens, operators)
	return postfix

if __name__ == "__main__":
	
	def test():
		exp = "a+b*(c^d-e)^(f+g*h)-i"
		tokens = tokenize(exp)
		postfix = generatePostfixTokens(tokens)
		assert ''.join(postfix) == 'abcd^e-fgh*+^*+i-'
	test()

	expressions = [
		"result = (input1 AND (NOT input2)) OR ((NOT input1) AND input2)", 
		"v=a AND (b OR c)"
	]

	for e in expressions:
		postfix = parseExpression(e, ["AND", "OR", "XOR", "NOT"])
		print(postfix)


