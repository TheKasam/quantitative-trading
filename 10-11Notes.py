
#Oct 11th Notes


ans = (7 + (12+3) * 3) # infix notataion

#later 7 12 3 + 2 * + #takes previous two -> RPN: reverse polish notation aka post fix notataion

 #how it worked
  #if you entered a number: push it on a stack
  #if you enter an opertaor: pop the stack twice and apply the operator and push result on stack
  #code on website

#also have prefix: * 5 2 #not very useful #operator operand operand #good exercise



#########

#Queues: an ordered collection of elements where the addition of new items only takes place at one end (called the back) and the removal of existing items only takes place at the other end (called the front)

  #ex: any lines , one way street
  #FIFO: first in first out

#functions

  #Create new empty Queue: q = Queue()
    #args: none returns: pointer to Queue

  #Get the num of elements: q.size()
    #args: none, returns: int

  #Check empty: q.isEmpty()
    #args: none, retuns: bool

  #Add an element: q.enqueue()
    #args; item to add, returns; none

  #remove an element: q.dequeue()
    #args: none, return item removed

  #Look at item in front of queue without changing it: q.peek()
    #args: none, returns: front element
