# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅] Semantic Tools

# ---Compiling Structures-----------------------------------------

# Function Directory
fnDir = []

# Custom Types Register
customReg = {}

# ---Static Structures

# Predefined Types
basic_types = { "int": int, "dec": float, "char": str, "bool": bool }

# Semantic Cube
# -- Key: int : 0 | dec : 1 | char : 2 | bool : 3 | err : -1
sCube = [
  #  +, -, *, /, ^, %
  [[ 0, 0, 0, 0, 0, 0 ],  # int  -  int
   [ 1, 1, 1, 1, 1,-1 ],  #         dec
   [ 0, 0,-1,-1,-1,-1 ],  #         char
   [ 0, 0, 0, 0,-1,-1 ]]  #         bool
  [[ 1, 1, 1, 1, 1,-1 ],  # dec  -  int
   [ 1, 1, 1, 1, 1,-1 ],  #         dec
   [-1,-1,-1,-1,-1,-1 ],  #         char
   [ 1, 1, 1, 1,-1,-1 ]]  #         bool
  [[ 2, 2, 0, 0,-1,-1 ],  # char -  int
   [ 1, 1,-1,-1,-1,-1 ],  #         dec
   [-1,-1,-1,-1,-1,-1 ],  #         char
   [-1,-1,-1,-1,-1,-1 ]]  #         bool
  [[-1,-1,-1,-1,-1,-1 ],  # bool -  int
   [-1,-1,-1,-1,-1,-1 ],  #         dec
   [-1,-1,-1,-1,-1,-1 ],  #         char
   [-1,-1,-1,-1,-1, 3 ]]  #         bool
]

# ---Error Classes------------------------------------------------
class ZenImportError(Exception):
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