# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅橋] Hashi
from zen.zenmind import MasterMind
import zen.zensemantics as zs

mastermind = [MasterMind(1), MasterMind(0)]
schema = []
zenmind = {}

def addr(address):
  if isinstance(address, str):
    return int(address[1:])
  else: return address

def interpret(instruction, state):
  # Assignment
  if instruction[0] == 0:
    print("> assigning ", zenmind[addr(instruction[1])], "in", zenmind[addr(instruction[3])])
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(zenmind[addr(instruction[1])])
      elif type == "dec": zenmind[addr(instruction[3])] = float(zenmind[addr(instruction[1])])
      elif type == "char": zenmind[addr(instruction[3])] = chr(zenmind[addr(instruction[1])])
      elif type == "bool": zenmind[addr(instruction[3])] = False if zenmind[addr(instruction[1])] == 0 else True
    else:
      zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])]
  # Sum
  elif instruction[0] == 1:
    print("> calc ", zenmind[addr(instruction[1])], " + ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(zenmind[addr(instruction[1])] + zenmind[addr(instruction[2])])
      elif type == "dec": zenmind[addr(instruction[3])] = float(zenmind[addr(instruction[1])] + zenmind[addr(instruction[2])])
      elif type == "char": zenmind[addr(instruction[3])] = chr(zenmind[addr(instruction[1])] + zenmind[addr(instruction[2])])
    else:
      zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] + zenmind[addr(instruction[2])]
  # Subtraction
  elif instruction[0] == 2:
    print("> calc ", zenmind[addr(instruction[1])], " - ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(zenmind[addr(instruction[1])] - zenmind[addr(instruction[2])])
      elif type == "dec": zenmind[addr(instruction[3])] = float(zenmind[addr(instruction[1])] - zenmind[addr(instruction[2])])
      elif type == "char": zenmind[addr(instruction[3])] = chr(zenmind[addr(instruction[1])] - zenmind[addr(instruction[2])])
    else:
      zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] - zenmind[addr(instruction[2])]
  # Multiplication
  elif instruction[0] == 3:
    print("> calc ", zenmind[addr(instruction[1])], " * ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(zenmind[addr(instruction[1])] * zenmind[addr(instruction[2])])
      elif type == "dec": zenmind[addr(instruction[3])] = float(zenmind[addr(instruction[1])] * zenmind[addr(instruction[2])])
    else:
      zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] * zenmind[addr(instruction[2])]
  # Division
  elif instruction[0] == 4:
    print("> calc ", zenmind[addr(instruction[1])], " / ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(zenmind[addr(instruction[1])] / zenmind[addr(instruction[2])])
      elif type == "dec": zenmind[addr(instruction[3])] = float(zenmind[addr(instruction[1])] / zenmind[addr(instruction[2])])
    else:
      zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] / zenmind[addr(instruction[2])]
  # Modulo
  elif instruction[0] == 5:
    print("> calc ", zenmind[addr(instruction[1])], " % ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    zenmind[addr(instruction[3])] = int(zenmind[addr(instruction[1])]) % int(zenmind[addr(instruction[2])])
  # Exponentiation
  elif instruction[0] == 6:
    print("> calc ", zenmind[addr(instruction[1])], " ^ ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(zenmind[addr(instruction[1])] ** zenmind[addr(instruction[2])])
      elif type == "dec": zenmind[addr(instruction[3])] = float(zenmind[addr(instruction[1])] ** zenmind[addr(instruction[2])])
    else:
      zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] ** zenmind[addr(instruction[2])]
  # Greater-Than Comparison
  elif instruction[0] == 7:
    print("> check if ", zenmind[addr(instruction[1])], " > ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] > zenmind[addr(instruction[2])]
  # Lesser-Than Comparison
  elif instruction[0] == 8:
    print("> check if ", zenmind[addr(instruction[1])], " < ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] < zenmind[addr(instruction[2])]
  # Equal-Than Comparison
  elif instruction[0] == 9:
    print("> check if ", zenmind[addr(instruction[1])], " = ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] == zenmind[addr(instruction[2])]
  # Different-Than Comparison
  elif instruction[0] == 10:
    print("> check if ", zenmind[addr(instruction[1])], " >< ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] != zenmind[addr(instruction[2])]
  # Greater-or-Equal-Than Comparison
  elif instruction[0] == 11:
    print("> check if ", zenmind[addr(instruction[1])], " >= ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] >= zenmind[addr(instruction[2])]
  # Lesser-or-Equal-Than Comparison
  elif instruction[0] == 12:
    print("> check if ", zenmind[addr(instruction[1])], " <= ", zenmind[addr(instruction[2])])
    print("  > value kept in: ", instruction[3])
    zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] <= zenmind[addr(instruction[2])]
  # GoTo
  elif instruction[0] == 13:
    print("> goto:", instruction[3])
    state = instruction[3]
    return interpret(schema[instruction[3]], instruction[3])
  # GoTo if True
  elif instruction[0] == 14:
    if instruction[1]:
      print("> T then goto:", instruction[3])
      return interpret(schema[instruction[3]], instruction[3])
    else:
      print("> F ignoring goto:", instruction[3])
  # GoTo if False
  elif instruction[0] == 15:
    if instruction[1]:
      print("> F then goto:", instruction[3])
      return interpret(schema[instruction[3]], instruction[3])
    else:
      print("> T ignoring goto:", instruction[3])
  # Console Read
  elif instruction[0] == 16:
    print("> read from console: ")
    type = mastermind[0].typeof(addr(instruction[3])) or mastermind[1].typeof(addr(instruction[3]))
    if len(type) < 5:
      if type == "int": zenmind[addr(instruction[3])] = int(input())
      elif type == "dec": zenmind[addr(instruction[3])] = float(input())
      elif type == "char":
        temp = str(input())
        zenmind[instruction[3]] = temp[0]
      elif type == "bool":
        temp = input()
        if temp == "True" or temp == "true" or temp == "1" or temp == "T" or temp == "t":
          zenmind[instruction[3]] = True
        elif temp == "False" or temp == "false" or temp == "0" or temp == "F" or temp == "f":
          zenmind[instruction[3]] = False
        else: zs.ZenRuntimeError("zen::run > invalid input for boolean variable.")
  # Console Write
  elif instruction[0] == 17:
    print("> write in console: ")
    print(zenmind[addr(instruction[3])])
  # Logical Not
  elif instruction[0] == 18:
    print("> negate value")
    zenmind[addr(instruction[3])] = not zenmind[addr(instruction[1])]
  # Logical Or
  elif instruction[0] == 19:
    print("> logical OR between", addr(instruction[1]), "and", addr(instruction[2]))
    zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] or zenmind[addr(instruction[1])]
  # Logical And
  elif instruction[0] == 20:
    print("> logical AND between", addr(instruction[1]), "and", addr(instruction[2]))
    zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])] and zenmind[addr(instruction[1])]
  # ARX (Activation Record Expansion)
  elif instruction[0] == 21:
    pass
  # Parameter Definition
  elif instruction[0] == 22:
    print("> assigning", addr(instruction[1]), "as parameter")
    zenmind[addr(instruction[3])] = zenmind[addr(instruction[1])]
  # GoTo Submethod
  elif instruction[0] == 23:
    pass
  # Return
  elif instruction[0] == 24:
    pass
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
  # End
  elif instruction[0] == 99:
    print("> done with function!")
    return 99
  # End
  elif instruction[0] == 999:
    print("> done!")
    return 999
  return interpret(schema[state+1], state+1)

def meditate(list, mind):
  global schema, zenmind
  schema = list
  zenmind = mind

  zenlogo()
  print(schema)
  program = interpret(schema[0], 0)
  if program != 999: raise OSError("zen::run > unexpected end.")

def zenlogo():
  print("\n          *%@@        %(                                                                  ")
  print("     @@@@@@@@@            @@@/                                                            ")
  print("  /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                          ")
  print(" @@@@@@@@@@@@@/    .//.       @@@        _____________      _______        ____   ____    ")
  print("*@@@@@@@@@@@                  @@@@       @@@@@@@@@@@@%    .@@@@@@@@@@      @@@@,@@@@@@@@  ")
  print("@@@@@@@@@@@@@& /@@@@@@@     ,@@@@@              &@@@@    @@@@(    #@@@%    @@@@@@   &@@@@ ")
  print("@@@@@@@@@@@@@@@@@@@@@     .@@@@@@@            &@@@@.    /@@@@      @@@@    @@@@      @@@@.")
  print("@@@@@@@@@@@@@@@@@@#     (@@@@@@@@@          #@@@@,      %@@@@@@@@@@@@@@    @@@@      @@@@.")
  print("@@@@@@@@@@@@@&                 @@@        /@@@@/        ,@@@@              @@@@      @@@@.")
  print("&@@@@@@                       *@@@      .@@@@/..../&@@   #@@@@%    @@@     @@@@      @@@@,")
  print(" @@@@@@@&       ./@@@,===@@@@@@@@(      .@@@@@@@@@@@@&     #@@@@@@@@@/     @@@@      @@@@@")
  print("  @@@@@@@@@@@@@@@@@@.    @@@@@@@(                                                         ")
  print("   ,@@@@@@@@@@@@@@@@     @@@@@&                                                           ")
  print("       @@@@@@@@@@@@@     @@,                                                              \n\n")