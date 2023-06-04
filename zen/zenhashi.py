# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅橋] Hashi
from zen.zenmind import MasterMind
import zen.zensemantics as zs

# ---Memory----------------------------------------------------------
zenmind = {}

# ---Directories and Stacks------------------------------------------
const_list = []
function = []
mastermind = [MasterMind(1), MasterMind(0)]
param_pusher = []
return_stack = []
schema = []
tesseract = []

# ---Pins------------------------------------------------------------
nextface = -1
show_vb = False
to_main = True

# ---Helper Functions------------------------------------------------
def addr(element):
  if isinstance(element, str):
    if element[0] == "&":
      me, im, ei = element[1:].split(".")
      if int(me) == 0: return zenmind[tesseract[0][int(im)][int(ei)-1]]
      else: return zenmind[tesseract[-1][int(im)][int(ei)-1]]
    else:
      me, im, ei = element.split(".")
      if int(me) == 0: return tesseract[0][int(im)][int(ei)-1]
      else: return tesseract[-1][int(im)][int(ei)-1]
  else:
    return element

def dropface():
  for x in tesseract[-1]:
    for y in x:
      zenmind.pop(y)
  tesseract.pop()

def newface(template):
  types = []
  indexes = []
  if template == 0: mmi = 0
  else:
    mastermind[1].alloc_func()
    mmi = 1
  for x in range(9):
    for y in range(function[template][1][x]):
      auxmei = str(template)+"." + str(x) + "." + str(y+1)
      addr = mastermind[mmi].alloc(auxmei)
      indexes.append(addr)
      zenmind[addr] = None
    types.append(indexes)
    indexes = []
  tesseract.append(types)

def pass_constants():
  zenmind[1500000] = 0
  for i in range(len(const_list)):
    zenmind[1500001+i] = const_list[i]

def value(element):
  if isinstance(element, str):
    if element[0] == "*":
      me, im, ei = element[1:].split(".")
      if int(me) == 0: return tesseract[0][int(im)][int(ei)-1]
      else: return tesseract[-1][int(im)][int(ei)-1]
    elif element[0] == "&":
      me, im, ei = element[1:].split(".")
      if int(me) == 0: return zenmind[zenmind[tesseract[0][int(im)][int(ei)-1]]]
      else: return zenmind[zenmind[tesseract[-1][int(im)][int(ei)-1]]]
    else:
      me, im, ei = element.split(".")
      if int(me) == 0: return zenmind[tesseract[0][int(im)][int(ei)-1]]
      else: return zenmind[tesseract[-1][int(im)][int(ei)-1]]
  else:
    return zenmind[element]

def verbose(text):
  if show_vb: print(text)
# -------------------------------------------------------------------

def interpret(instruction, state):
  # Assignment
  if instruction[0] == 0:
    verbose("> assigning " + str(value(instruction[1])) + "in" + str(instruction[3]))
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(value(instruction[1]))
      elif type == "dec": zenmind[addr(instruction[3])] = float(value(instruction[1]))
      elif type == "char": zenmind[addr(instruction[3])] = chr(value(instruction[1]))
      elif type == "bool": zenmind[addr(instruction[3])] = False if value(instruction[1]) == 0 else True
    else:
      zenmind[addr(instruction[3])] = value(instruction[1])
  # Sum
  elif instruction[0] == 1:
    verbose("> calc " + str(value(instruction[1])) + " + " + str(value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(value(instruction[1]) + value(instruction[2]))
      elif type == "dec": zenmind[addr(instruction[3])] = float(value(instruction[1]) + value(instruction[2]))
      elif type == "char": zenmind[addr(instruction[3])] = chr(value(instruction[1]) + value(instruction[2]))
    else:
      zenmind[addr(instruction[3])] = value(instruction[1]) + value(instruction[2])
  # Subtraction
  elif instruction[0] == 2:
    verbose("> calc " + str(value(instruction[1])) + " - " + str(value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(value(instruction[1]) - value(instruction[2]))
      elif type == "dec": zenmind[addr(instruction[3])] = float(value(instruction[1]) - value(instruction[2]))
      elif type == "char": zenmind[addr(instruction[3])] = chr(value(instruction[1]) - value(instruction[2]))
    else:
      zenmind[addr(instruction[3])] = value(instruction[1]) - value(instruction[2])
  # Multiplication
  elif instruction[0] == 3:
    verbose("> calc " + str(value(instruction[1])) + " * " + str(value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(value(instruction[1]) * value(instruction[2]))
      elif type == "dec": zenmind[addr(instruction[3])] = float(value(instruction[1]) * value(instruction[2]))
    else:
      zenmind[addr(instruction[3])] = value(instruction[1]) * value(instruction[2])
  # Division
  elif instruction[0] == 4:
    verbose("> calc " + str(value(instruction[1])) + " / " + str(value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(value(instruction[1]) / value(instruction[2]))
      elif type == "dec": zenmind[addr(instruction[3])] = float(value(instruction[1]) / value(instruction[2]))
    else:
      zenmind[addr(instruction[3])] = value(instruction[1]) / value(instruction[2])
  # Modulo
  elif instruction[0] == 5:
    verbose("> calc " + str(value(instruction[1])) + " % " + str(value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    zenmind[addr(instruction[3])] = value(instruction[1]) % value(instruction[2])
  # Exponentiation
  elif instruction[0] == 6:
    verbose("> calc " + str(value(instruction[1])) + " ^ " + str(value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(value(instruction[1]) ** value(instruction[2]))
      elif type == "dec": zenmind[addr(instruction[3])] = float(value(instruction[1]) ** value(instruction[2]))
    else:
      zenmind[addr(instruction[3])] = value(instruction[1]) ** value(instruction[2])
  # Greater-Than Comparison
  elif instruction[0] == 7:
    verbose("> check if " + str(value(instruction[1])) + " > " + (value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    zenmind[addr(instruction[3])] = value(instruction[1]) > value(instruction[2])
  # Lesser-Than Comparison
  elif instruction[0] == 8:
    verbose("> check if " + str(value(instruction[1])) + " < " + (value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    zenmind[addr(instruction[3])] = value(instruction[1]) < value(instruction[2])
  # Equal-Than Comparison
  elif instruction[0] == 9:
    verbose("> check if " + str(value(instruction[1])) + " = " + (value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    zenmind[addr(instruction[3])] = value(instruction[1]) == value(instruction[2])
  # Different-Than Comparison
  elif instruction[0] == 10:
    verbose("> check if " + str(value(instruction[1])) + " >< " + (value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    zenmind[addr(instruction[3])] = value(instruction[1]) != value(instruction[2])
  # Greater-or-Equal-Than Comparison
  elif instruction[0] == 11:
    verbose("> check if " + str(value(instruction[1])) + " >= " + (value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    zenmind[addr(instruction[3])] = value(instruction[1]) >= value(instruction[2])
  # Lesser-or-Equal-Than Comparison
  elif instruction[0] == 12:
    verbose("> check if " + str(value(instruction[1])) + " <= " + (value(instruction[2])))
    verbose("  > value kept in: " + str(addr(instruction[3])))
    zenmind[addr(instruction[3])] = value(instruction[1]) <= value(instruction[2])
  # GoTo
  elif instruction[0] == 13:
    global to_main
    verbose("> goto:" + str(instruction[3]))
    if to_main:
      newface(len(function)-1)
      to_main = False
    return interpret(schema[instruction[3]], instruction[3])
  # GoTo if True
  elif instruction[0] == 14:
    if value(instruction[1]):
      verbose("> T then goto:" + str(instruction[3]))
      return interpret(schema[instruction[3]], instruction[3])
    else:
      verbose("> F ignoring goto:" + str(instruction[3]))
  # GoTo if False
  elif instruction[0] == 15:
    if value(instruction[1]):
      verbose("> F then goto:" + str(instruction[3]))
      return interpret(schema[instruction[3]], instruction[3])
    else:
      verbose("> T ignoring goto:" + str(instruction[3]))
  # Console Read
  elif instruction[0] == 16:
    verbose("> read from console: ")
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(input())
      elif type == "dec": zenmind[addr(instruction[3])] = float(input())
      elif type == "char":
        temp = str(input())
        zenmind[addr(instruction[3])] = temp[0]
      elif type == "bool":
        temp = input()
        if temp == "True" or temp == "true" or temp == "1" or temp == "T" or temp == "t":
          zenmind[addr(instruction[3])] = True
        elif temp == "False" or temp == "false" or temp == "0" or temp == "F" or temp == "f":
          zenmind[addr(instruction[3])] = False
        else: zs.ZenRuntimeError("zen::run > invalid input for boolean variable.")
  # Console Write
  elif instruction[0] == 17:
    verbose("> write in console: ")
    print(zenmind[addr(instruction[3])])
  # Logical Not
  elif instruction[0] == 18:
    verbose("> negate value")
    zenmind[addr(instruction[3])] = not value(instruction[1])
  # Logical Or
  elif instruction[0] == 19:
    verbose("> logical OR between" + str(addr(instruction[1])) + "and" + str(addr(instruction[2])))
    zenmind[addr(instruction[3])] = value(instruction[1]) or value(instruction[2])
  # Logical And
  elif instruction[0] == 20:
    verbose("> logical AND between" + str(addr(instruction[1])) + "and" + str(addr(instruction[2])))
    zenmind[addr(instruction[3])] = value(instruction[1]) and value(instruction[2])
  # ARX (Activation Record Expansion)
  elif instruction[0] == 21:
    nextface = instruction[3]
  # Parameter Definition
  elif instruction[0] == 22:
    verbose("> assigning" + str(instruction[1]) + "as parameter")
    param_pusher.append((instruction[1], instruction[3]))
  # GoTo Subroutine
  elif instruction[0] == 23:
    verbose("> going to subroutine in state " + str(instruction[3]))
    newface(nextface)
    for x in param_pusher:
      a, b = x
      zenmind[addr(b)] = value(a)
    param_pusher.clear()
    return_stack.append(state+1)
    _status_ = interpret(schema[instruction[3]], instruction[3])
    if _status_ != 0:
      raise OSError("zen::run > how the heck did we end up here?")
  # Return
  elif instruction[0] == 24:
    verbose("> returning " + str(value(instruction[3])))
    zenmind[addr(schema[return_stack[-1]][1])] = value(instruction[3])
    return_stack.pop()
    dropface()
    return 0
  # Check Index
  elif instruction[0] == 25:
    pass
  # Datatable Check Row
  elif instruction[0] == 26:
    pass
  # Datatable Check Length
  elif instruction[0] == 27:
    pass
  # Datatable Max
  elif instruction[0] == 28:
    pass
  # Datatable Min
  elif instruction[0] == 29:
    pass
  # Datatable Sum
  elif instruction[0] == 30:
    pass
  # Datatable Mean
  elif instruction[0] == 31:
    pass
  # Datatable Variance
  elif instruction[0] == 32:
    pass
  # Datatable Standard Deviation
  elif instruction[0] == 33:
    pass
  # Datatable Correlation
  elif instruction[0] == 34:
    pass
  # Datatable Prepare for Distribution Filling
  elif instruction[0] == 35:
    pass
  # Datatable Normal Distribution Fitting
  elif instruction[0] == 36:
    pass
  # Datatable Binomial Distribution Fitting
  elif instruction[0] == 37:
    pass
  # Update End
  elif instruction[0] == 49:
    verbose("> done updating")
    return 49
  # End
  elif instruction[0] == 99:
    verbose("> done with function!")
    return 99
  # End
  elif instruction[0] == 999:
    verbose("> done!")
    return 999
  return interpret(schema[state+1], state+1)

def meditate(list1, list2, list3):
  global const_list, function, schema
  schema = list1
  function = list2
  const_list = list3

  pass_constants()
  newface(0)
  
  program = interpret(schema[0], 0)
  
  if program != 999:
    raise OSError("zen::run > unexpected end.")