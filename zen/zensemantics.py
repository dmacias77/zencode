# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅] Semantic Tools

# ---Compiling Structures-----------------------------------------

# Custom Types Register
customReg = {}

# ---Static Structures

# Predefined Types
basic_types = { "int": int, "dec": float, "char": str, "bool": bool }

# Semantic Cube
# -- Key: int : 0 | dec : 1 | char : 2 | bool : 3 | err : -1
zenocube = [
  # <<, +, -, *, /, ^, %,CM,LG
  [[ 0, 0, 0, 0, 0, 0, 0, 3,-1],  # int  -  int
   [ 0, 1, 1, 1, 1, 1,-1, 3,-1],  #         dec
   [ 0, 0, 0,-1,-1,-1,-1,-1,-1],  #         char
   [ 0, 0, 0, 0, 0,-1,-1, 3,-1]], #         bool
  [[ 1, 1, 1, 1, 1, 1,-1, 3,-1],  # dec  -  int
   [ 1, 1, 1, 1, 1, 1,-1, 3,-1],  #         dec
   [-1,-1,-1,-1,-1,-1,-1,-1,-1],  #         char
   [ 1, 1, 1, 1, 1,-1,-1, 3,-1]], #         bool
  [[ 2, 2, 2, 0, 0,-1,-1,-1,-1],  # char -  int
   [-1, 1, 1,-1,-1,-1,-1,-1,-1],  #         dec
   [ 2,-1,-1,-1,-1,-1,-1, 3,-1],  #         char
   [-1,-1,-1,-1,-1,-1,-1,-1,-1]], #         bool
  [[ 1,-1,-1,-1,-1,-1,-1, 3,-1],  # bool -  int
   [-1,-1,-1,-1,-1,-1,-1, 3,-1],  #         dec
   [-1,-1,-1,-1,-1,-1,-1,-1,-1],  #         char
   [-1,-1,-1,-1,-1,-1,-1, 3, 3]]  #         bool
]

def check_compatible(left, operator, right):
  comp = -1
  if operator in range(0,7): comp = zenocube[left][right][operator]
  elif operator in range(7,13): comp = zenocube[left][right][7]
  elif operator in range(19,21): comp = zenocube[left][right][8]
  print("::zs.cc(", left, right, operator, ") : ", comp)
  return comp

# ---Error Classes------------------------------------------------
class ZenImportError(Exception):
  pass

class ZenInvalidType(Exception):
  pass

class ZenRedefinedID(Exception):
  pass

class ZenTypeMismatch(Exception):
  pass

class ZenUndefinedID(Exception):
  pass

# ---Auxiliary Functions------------------------------------------
def import_file(filename):
  try:
    with open(filename + '.zh', 'r') as file:
      header = file.read()
      exec(header, globals())
  except FileNotFoundError:
    raise ZenImportError(f"zen::cmp > import error: File {filename}.zh not found.")

def storef(origin: str): # next to define 21
  if len(origin) == 1:
    if origin == '+': return 1
    elif origin == '-': return 2
    elif origin == '*': return 3
    elif origin == '/': return 4
    elif origin == '%': return 5
    elif origin == '^': return 6
    elif origin == '>': return 7
    elif origin == '<': return 8
    elif origin == '=': return 9
  elif len(origin) == 2:
    if origin == '<<': return 0
    elif origin == '><': return 10
    elif origin == '>=': return 11
    elif origin == '<=': return 12
    elif origin == "or": return 19
  elif len(origin) == 3:
    if origin == "not": return 18
    elif origin == "and": return 20
  elif len(origin) == 4:
    if origin == "goto": return 13
  elif len(origin) == 5:
    if origin == "cread": return 16
  elif len(origin) == 6:
    if origin == "goto-t": return 14
    elif origin == "goto-f": return 15
    elif origin == "cwrite": return 17

def quad(operation, element_1, element_2, element_3):
  q1 = q2 = q3 = -1
  
  if element_1 != None:
    q1 = element_1
  if element_2 != None:
    q2 = element_2
  if element_3 != None:
    q3 = element_3
  if isinstance(operation, str):
    print((storef(operation), q1, q2, q3))
    return (storef(operation), q1, q2, q3)
  else:
    print((operation, q1, q2, q3))
    return (operation, q1, q2, q3)