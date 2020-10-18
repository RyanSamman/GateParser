import functools

class Node:
	def __init__(self, value, nextValue=None):
		self.value = value
		self.next = nextValue
	
	def __repr__(self):
		return f"Node({repr(self.value)}, {repr(self.next)})"

class Stack:
	def __init__(self, *args):
		self.head = None
		self.size = 0

		[self.push(i) for i in args]

	def push(self, item):
		newNode = Node(item)

		# Add value to the head if empty
		if self.size == 0:
			self.head = newNode
			self.size = 1
			return
		
		# Assign next to old head
		newNode.next = self.head

		# Set new head to the new node (Last value)
		self.head = newNode

		self.size += 1
	
	def pop(self):
		if self.size == 0:
			return None
		
		# Get last value from the stack
		lastNode = self.head

		# Set the last value to the size
		self.head = lastNode.next
		self.size -= 1
		
		return lastNode.value

	def size(self):
		return self.size

	def isEmpty(self):
		return self.size == 0

	def peek(self):
		return None if self.head is None else self.head.value

	def emptyContents(self):
		self.head = None

	def __repr__(self):
		def getValue(node: Node):
			while True:
				yield node.value

				if node.next is None:
					break

				node = node.next
		values = ', '.join([repr(v) for v in getValue(self.head)][::-1])
		return f"Stack({values})"

if __name__ == "__main__":
	s = Stack(1,2,3,4,5,6,7,8)
	print(s)
