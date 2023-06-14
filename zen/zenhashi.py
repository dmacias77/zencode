# David Macías (1283419)
# ZENCODE [禅橋] Hashi
from zen.zenmind import MasterMind
import zen.zensemantics as zs

import numpy
import statistics

# ---Memory----------------------------------------------------------
zenmind = {}

# ---Directories and Stacks------------------------------------------
const_list = []
function = []
mastermind = [MasterMind(1), MasterMind(0)]
param_pusher = []
pipe = []
return_stack = []
schema = []
tesseract = []

# ---Pins------------------------------------------------------------
nextface = -1
part_one = True
show_vb = False
to_main = True

# ---Helper Functions------------------------------------------------

# -*-Addr-
# -----Returns the real address based on their meimei and the Tesseract's
# -----current rotation.
def addr(element):
  if isinstance(element, str):
    if element[0] == "&":
      me, im, ei = element[1:].split(".")
      if int(me) == 0: return zenmind[tesseract[0][int(im)][int(ei)-1]]
      else: return zenmind[tesseract[-1][int(im)][int(ei)-1]]
    else:
      me, im, ei = element.split(".")
      if int(me) == 0: return tesseract[0][int(im)][int(ei)-1]
      else:
        return tesseract[-1][int(im)][int(ei)-1]
  else:
    return element

# -*-DropFace-
# -----Drops the current face of the Tesseract, and returns to the last one.
def dropface():
  for x in tesseract[-1]:
    for y in x:
      zenmind.pop(y)
  tesseract.pop()

# -*-NewFace-
# -----Adds a new face to the Tesseract, and shifts to it.
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

# -*-PassConstants-
# -----Allocs the constant list into the memory.
# -----Tip: Direction 1500000 is only used for statistical results of
# -----datatables.
def pass_constants():
  zenmind[1500000] = 0
  for i in range(len(const_list)):
    zenmind[1500001+i] = const_list[i]

# -*-Value-
# -----Returns the real value based on their meimei and the Tesseract's
# -----current rotation.
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

# -*-Verbose-
# -----Prints only if show_vb is True.
def verbose(text):
  if show_vb: print(text)

# ---Schema Interpreter----------------------------------------------
def interpret():
  state = 0
  while state != 999:
    instruction = schema[state]
    # Assignment
    if instruction[0] == 0:
      verbose("> assigning " + str(value(instruction[1])) + " in " + str(instruction[3]))
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
      verbose("> check if " + str(value(instruction[1])) + " > " + str(value(instruction[2])))
      verbose("  > value kept in: " + str(addr(instruction[3])))
      zenmind[addr(instruction[3])] = value(instruction[1]) > value(instruction[2])
    # Lesser-Than Comparison
    elif instruction[0] == 8:
      verbose("> check if " + str(value(instruction[1])) + " < " + str(value(instruction[2])))
      verbose("  > value kept in: " + str(addr(instruction[3])))
      zenmind[addr(instruction[3])] = value(instruction[1]) < value(instruction[2])
    # Equal-Than Comparison
    elif instruction[0] == 9:
      verbose("> check if " + str(value(instruction[1])) + " = " + str(value(instruction[2])))
      verbose("  > value kept in: " + str(addr(instruction[3])))
      zenmind[addr(instruction[3])] = value(instruction[1]) == value(instruction[2])
    # Different-Than Comparison
    elif instruction[0] == 10:
      verbose("> check if " + str(value(instruction[1])) + " >< " + str(value(instruction[2])))
      verbose("  > value kept in: " + str(addr(instruction[3])))
      zenmind[addr(instruction[3])] = value(instruction[1]) != value(instruction[2])
    # Greater-or-Equal-Than Comparison
    elif instruction[0] == 11:
      verbose("> check if " + str(value(instruction[1])) + " >= " + str(value(instruction[2])))
      verbose("  > value kept in: " + str(addr(instruction[3])))
      zenmind[addr(instruction[3])] = value(instruction[1]) >= value(instruction[2])
    # Lesser-or-Equal-Than Comparison
    elif instruction[0] == 12:
      verbose("> check if " + str(value(instruction[1])) + " <= " + str(value(instruction[2])))
      verbose("  > value kept in: " + str(addr(instruction[3])))
      zenmind[addr(instruction[3])] = value(instruction[1]) <= value(instruction[2])
    # GoTo
    elif instruction[0] == 13:
      global to_main
      verbose("> goto:" + str(instruction[3]))
      if to_main:
        newface(len(function)-1)
        to_main = False
      state = instruction[3]
      continue
    # GoTo if True
    elif instruction[0] == 14:
      if value(instruction[1]):
        verbose("> T then goto:" + str(instruction[3]))
        state = instruction[3]
        continue
      else:
        verbose("> F ignoring goto:" + str(instruction[3]))
    # GoTo if False
    elif instruction[0] == 15:
      if not value(instruction[1]):
        verbose("> F then goto:" + str(instruction[3]))
        state = instruction[3]
        continue
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
          if temp == "True" or temp == True or temp == "1" or temp == "T":
            zenmind[addr(instruction[3])] = True
          elif temp == "False" or temp == False or temp == "0" or temp == "F":
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
      verbose("> logical OR between " + str(addr(instruction[1])) + " and " + str(addr(instruction[2])))
      zenmind[addr(instruction[3])] = value(instruction[1]) or value(instruction[2])
    # Logical And
    elif instruction[0] == 20:
      verbose("> logical AND between " + str(addr(instruction[1])) + " and " + str(addr(instruction[2])))
      zenmind[addr(instruction[3])] = value(instruction[1]) and value(instruction[2])
    # ARX (Activation Record Expansion)
    elif instruction[0] == 21:
      global nextface
      verbose("> allocate function: " + str(instruction[3]))
      nextface = instruction[3]
    # Parameter Definition
    elif instruction[0] == 22:
      verbose("> assigning " + str(instruction[1]) + " as parameter")
      param_pusher.append((instruction[1], instruction[3]))
    # GoTo Subroutine
    elif instruction[0] == 23:
      verbose("> going to subroutine in state " + str(instruction[3]))
      sender = []
      for x in param_pusher:
        sender.append(value(x[0]))
      newface(nextface)
      sender.reverse()
      for x in param_pusher:
        zenmind[addr(x[1])] = sender[-1]
        sender.pop()
      param_pusher.clear()
      return_stack.append(state+1)
      state = instruction[3]
      continue
    # Return
    elif instruction[0] == 24:
      verbose("> returning " + str(value(instruction[3])))
      zenmind[addr(schema[return_stack[-1]][1])] = value(instruction[3])
      state = return_stack[-1]
      return_stack.pop()
      dropface()
      continue
    # Check Index
    elif instruction[0] == 25:
      verbose("> check if " + str(value(instruction[1])) + " is between " + str(instruction[2]) + " and " +  str(instruction[3]))
      if instruction[2] > value(instruction[1]) or value(instruction[1]) >= instruction[3]:
        raise OverflowError(f"zen::run > value out of bounds; {value(instruction[1])} is not between {instruction[2]} and {instruction[3]}")
    # Datatable Check Row
    elif instruction[0] == 26:
      verbose("> check if datatable has row " + str(instruction[1]))
      if instruction[2] > instruction[1] or instruction[1] >= instruction[3]:
        raise OverflowError(f"zen::run > value out of bounds; {value(instruction[1])} is not between {instruction[2]} and {instruction[3]}")
    # Datatable Check Length
    elif instruction[0] == 27:
      verbose("> check if " + str(instruction[1]) + " is exactly " + str(instruction[3]))
      if int(instruction[1]) != int(instruction[3]):
        raise zs.ZenTypeMismatch(f"zen::run > datatable update requires exactly {value(instruction[1])} values; got {instruction[3]}.")
    # Datatable Max
    elif instruction[0] == 28:
      verbose("> finding datatable's column " + str(instruction[1] + 1) + " max value")
      aux = []
      base = addr(tesseract[-1][8][0]) + instruction[1]
      for _ in range(instruction[2]):
        aux.append(value(base))
        base += instruction[3]
      zenmind[1500000] = max(aux)
    # Datatable Min
    elif instruction[0] == 29:
      verbose("> finding datatable's column " + str(instruction[1] + 1) + " min value")
      aux = []
      base = addr(tesseract[-1][8][0]) + instruction[1]
      for _ in range(instruction[2]):
        aux.append(value(base))
        base += instruction[3]
      zenmind[1500000] = min(aux)
    # Datatable Sum
    elif instruction[0] == 30:
      verbose("> finding datatable's column " + str(instruction[1] + 1) + " sum of values")
      aux = []
      base = addr(tesseract[-1][8][0]) + instruction[1]
      for _ in range(instruction[2]):
        aux.append(value(base))
        base += instruction[3]
      zenmind[1500000] = sum(aux)
    # Datatable Mean
    elif instruction[0] == 31:
      verbose("> finding datatable's column " + str(instruction[1] + 1) + " mean")
      aux = []
      base = addr(tesseract[-1][8][0]) + instruction[1]
      for _ in range(instruction[2]):
        aux.append(value(base))
        base += instruction[3]
      zenmind[1500000] = statistics.mean(aux)  
    # Datatable Variance
    elif instruction[0] == 32:
      verbose("> finding datatable's column " + str(instruction[1] + 1) + " variance")
      aux = []
      base = addr(tesseract[-1][8][0]) + instruction[1]
      for _ in range(instruction[2]):
        aux.append(value(base))
        base += instruction[3]
      zenmind[1500000] = statistics.variance(aux) 
    # Datatable Standard Deviation
    elif instruction[0] == 33:
      verbose("> finding datatable's column " + str(instruction[1] + 1) + " standard deviation")
      aux = []
      base = addr(tesseract[-1][8][0]) + instruction[1]
      for _ in range(instruction[2]):
        aux.append(value(base))
        base += instruction[3]
      zenmind[1500000] = statistics.stdev(aux)
    # Datatable Correlation
    elif instruction[0] == 34:
      global part_one
      aux = []
      base = addr(tesseract[-1][8][0]) + instruction[1]
      for _ in range(instruction[2]):
        aux.append(value(base))
        base += instruction[3]
      if part_one:
        global pipe
        verbose("> finding datatable's two columns correlation")
        verbose("  > part one")
        pipe = aux.copy()
        part_one = False
      else:
        verbose("  > part two")
        zenmind[1500000] = numpy.corrcoef(pipe, aux)[0,1]
        part_one = True
    # Datatable Prepare for Distribution Fitting
    elif instruction[0] == 35:
      if schema[state-1][0] == 27:
        verbose("> setting data for update")
        pipe.append(instruction[1])
        pipe.append(instruction[2])
      else:
        verbose("> setting data for distribution fitting")
        pipe.append(value(instruction[1]))
        pipe.append(value(instruction[2]))
    # Datatable Normal Distribution Fitting
    elif instruction[0] == 36:
      verbose("> fitting datatable column " + str(instruction[1] + 1) + " into normal dist")
      sd = pipe[-1]
      pipe.pop()
      mean = pipe[-1]
      pipe.pop()
      aux = numpy.random.normal(mean, sd, instruction[2])
      base = addr(tesseract[-1][8][0]) + instruction[1]
      for _ in range(instruction[2]):
        zenmind[addr(base)] = aux[-1]
        base += instruction[3]
        aux = aux[:-1]
    # Datatable Binomial Distribution Fitting
    elif instruction[0] == 37:
      verbose("> fitting datatable column " + str(instruction[1] + 1) + " into binomial dist")
      prob = pipe[-1]
      pipe.pop()
      tests = pipe[-1]
      pipe.pop()
      aux = numpy.random.binomial(tests, prob, instruction[2])
      base = addr(tesseract[-1][8][0]) + instruction[1]
      for _ in range(instruction[2]):
        zenmind[addr(base)] = aux[-1]
        base += instruction[3]
        aux = aux[:-1]  
    # Update End
    elif instruction[0] == 49:
      verbose("> done updating")
    # Function End
    elif instruction[0] == 99:
      verbose("> done with function!")
      state = return_stack[-1]
      return_stack.pop()
      dropface()
      continue
    # End
    elif instruction[0] == 999:
      verbose("> done!")
      return 999
    state += 1

# ---Starter Function------------------------------------------------
def meditate(list1, list2, list3):
  global const_list, function, schema
  schema = list1
  function = list2
  const_list = list3

  # Verbose-shows current schema.
  if show_vb:
    for i in range(len(schema)):
      print(i, ": ", schema[i])
    print("\n")
      
  pass_constants()     # Initializes the memory with the constants.
  newface(0)           # Initializes the Tesseract

  # Runs the interpretation.
  program = interpret()

  # Fallback
  if program != 999:
    raise OSError("zen::run > unexpected end.")