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
  #  +, -, *, /, ^, %,COM
  [[ 0, 0, 0, 0, 0, 0, 3 ],  # int  -  int
   [ 1, 1, 1, 1, 1,-1, 3 ],  #         dec
   [ 0, 0,-1,-1,-1,-1,-1 ],  #         char
   [ 0, 0, 0, 0,-1,-1, 3 ]], #         bool
  [[ 1, 1, 1, 1, 1,-1, 3 ],  # dec  -  int
   [ 1, 1, 1, 1, 1,-1, 3 ],  #         dec
   [-1,-1,-1,-1,-1,-1,-1 ],  #         char
   [ 1, 1, 1, 1,-1,-1, 3 ]], #         bool
  [[ 2, 2, 0, 0,-1,-1,-1 ],  # char -  int
   [ 1, 1,-1,-1,-1,-1,-1 ],  #         dec
   [-1,-1,-1,-1,-1,-1, 3 ],  #         char
   [-1,-1,-1,-1,-1,-1,-1 ]], #         bool
  [[-1,-1,-1,-1,-1,-1, 3 ],  # bool -  int
   [-1,-1,-1,-1,-1,-1, 3 ],  #         dec
   [-1,-1,-1,-1,-1,-1,-1 ],  #         char
   [-1,-1,-1,-1,-1,-1, 3 ]]  #         bool
]

def check_compatible(left, operator, right):
  if operator == '+': return zenocube[left][right][0]
  elif operator == '-': return zenocube[left][right][1]
  elif operator == '*': return zenocube[left][right][2]
  elif operator == '/': return zenocube[left][right][3]
  elif operator == '^': return zenocube[left][right][4]
  elif operator == '%': return zenocube[left][right][5]
  else:
    compop = ['<', '>', '<=', '>=', '=', '><']
    if operator in compop: return zenocube[left][right][6]

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

def storef(origin: str):
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
  elif len(origin) == 4:
    if origin == "goto": return 13
  elif len(origin) == 6:
    if origin == "goto-t": return 14
    elif origin == "goto-f": return 15

def to_quad(operation, element_1, element_2, element_3):
  if isinstance(operation, str):
    return (storef(operation), element_1, element_2, element_3)
  else:
    return (operation, element_1, element_2, element_3)