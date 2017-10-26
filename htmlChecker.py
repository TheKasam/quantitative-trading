#Description: Using Stacks to check html tags
#  Student's Name: Sai Kasam
#  Student's UT EID: spk585
#  Course Name: CS 313E
#  Unique Number:
#
#  Date Created: Oct 7th
#  Date Last Modified: Oct 11th


#defining class Stack
class Stack:

  #stack methods and structure

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



def main():
  # openingfile
  htmlCode = open('htmlfile.txt','r')
  #list of all tags
  valid_words = []
  #list of invalid words
  invalid_words = ['meta','br','hr']

  #getting one character
  char = htmlCode.read(1)
  #know when to stop adding char to a word
  add = False
  word = ""
  while char:
#logic to get tags
    if char ==">":
      add = False
      valid_words.append(word)
      word = ''

    if add:
      word += char

    if char == "<":
      add = True


    char = htmlCode.read(1)

  #printing output
  print("Get tags list", valid_words)
  VALIDTAGS =  check_tags(valid_words, invalid_words)

  print("Validtags " + str(VALIDTAGS))

  print("Invalidtags " + str(invalid_words))

def check_tags(validTags, invalidTags):

  #creating Stack
  tags_stack = Stack()
  #unique list of tags
  VALIDTAGS = []

  error = False

  for x in range(0,len(validTags)):

    #skip tag if invalid
    if validTags[x].split()[0] in invalidTags:
      print("Tag: "+validTags[x] +" is skipped because it is not an invalid tag.")
      continue

    #pushing tag to stack 

    if validTags[x][0] != "/":
      tags_stack.push(validTags[x])
      print("Tag "+ validTags[x]+ " pushed:  stack is now "+str(tags_stack.items))

      #adding to tag is unique      
      if validTags[x] not in VALIDTAGS:
        VALIDTAGS.append(validTags[x]) 


    #checking is peek matched top of stack
    elif validTags[x][1:] == tags_stack.peek():

      print("Tag " + str(validTags[x]) +" matches top of stack:  stack is now [html, body]")
      tags_stack.pop()

    else:
      error = True
      return print("Error:  tag is " + validTags[x][1:] + " but top of stack is " + tags_stack.peek())

  #printing if errror was true
  if not error:
    print("Processing complete. No mismatches found")
  print()

  #returns valid list
  return VALIDTAGS

main()
