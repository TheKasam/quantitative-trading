
class Stack:

  def __init__(self):
    self.items = []

  def peek(self):
    return self.items[-1]

  def push(self,item):
    self.items.append(item)

  def pop(self):
    return self.items.pop(-1)

  def isEmpty(self):
    return self.items == []

  def size(self):
    return len(self.items)


def parChecker (symbolString):

  s = Stack()

  balanced = True
  index =0

  while index < len(symbolString) and balanced:

    symbol = symbolString[index]

    if symbol in  "([{":

      s.push(symbol)
    else:
      #there had better be a matching open paren on the stack
      if s.isEmpty():
        Balanced = False
      else:
        top = s.pop()
        if not matches (top,symbol
