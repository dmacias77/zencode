# David Macías (1283419)
# ZENCODE [禅] ZenMind Administrators
CONST_BOTTOM = 1500001
MALLOCMAX = 999
SUB_BOTTOM = 100000

def ecapsdnim(sector: int):
  slist = ["int", "dec", "char", "bool", "t.int", "t.dec", "t.char", "t.bool", "data"]
  return slist[sector]

def mindspace(type: str, kind):
  x = -1
  if type == "int": x = 0
  elif type == "dec": x = 1
  elif type == "char": x = 2
  elif type == "bool": x = 3
  elif type == "data": x = 8
  if kind == "temporal": x += 4
  return x

# ---Koan: Variable Renamer------------------------------------------
# -----Assigns an identifier (meimei) to variables declared to be
# -----found in a Tesseract template.
class Koan:
  def __init__(self):
    self.ck = -1
    self.fnk = [[1,1,1,1,1,1,1,1,1,1]]

  def add_func(self):
    self.fnk.append([1,1,1,1,1,1,1,1,1,1])

  def constant(self, value):
    self.ck += 1
    return CONST_BOTTOM + self.ck

  # Meimei (from Japanese '命名', 'naming')
  # --Transitional name for variables. Consist of three sections
  # --separated by points: 'Function.Type.ID'. The last two elements
  # --are the row and column of the Tesseract's face.
  def meimei(self, function, type, kind):
    if isinstance(type, str):
      sector = mindspace(type, kind)
    else: sector = mindspace(ecapsdnim(type), kind)
    if sector != -1:
      if self.fnk[function][sector] < MALLOCMAX:
        ID = str(1000 + self.fnk[function][sector])
        name = str(function) + "." + str(sector) + "." + ID[1:]
        self.fnk[function][sector] += 1
        return name
      else:
        raise OverflowError()
    else:
      raise IOError()

  def resources(self, function):
    if function < len(self.fnk):
      rlist = self.fnk[function].copy()
      for i in range(len(rlist)):
        rlist[i] -= 1
      return rlist
    else:
      raise OverflowError()

  def rest(self):
    self.ck = -1
    self.fnk = []

# ---MasterMind: Memory Administrator--------------------------------
# -----Administrates memory locations, allocates Tesseract templates
# -----in the memory, and translates meimei into directions.
class MasterMind:
  def __init__(self, is_main: bool):
    self.next_free = []
    self.limit = []
    self.func_boundary = [(0,0,0,0,0,0,0,0,0)]
    self.main = is_main
    global MALLOCMAX, SUB_BOTTOM
    
    if is_main:
      self.next_free.append(0)
    else:
      self.next_free.append(SUB_BOTTOM)
      MALLOCMAX += 99000
    self.limit.append(self.next_free[0]+MALLOCMAX) # integers : 0
    self.next_free.append(self.limit[0]+1)
    self.limit.append(self.next_free[1]+MALLOCMAX) # decimals : 1
    self.next_free.append(self.limit[1]+1)
    self.limit.append(self.next_free[2]+MALLOCMAX) # chars    : 2
    self.next_free.append(self.limit[2]+1)
    self.limit.append(self.next_free[3]+MALLOCMAX) # booleans : 3
    self.next_free.append(self.limit[3]+1)
    self.limit.append(self.next_free[4]+MALLOCMAX) # temp_int : 4
    self.next_free.append(self.limit[4]+1)
    self.limit.append(self.next_free[5]+MALLOCMAX) # temp_dec : 5
    self.next_free.append(self.limit[5]+1)
    self.limit.append(self.next_free[6]+MALLOCMAX) # temp_char: 6
    self.next_free.append(self.limit[6]+1)
    self.limit.append(self.next_free[7]+MALLOCMAX) # temp_bool: 7
    self.next_free.append(self.limit[7]+1)
    self.limit.append(self.next_free[8]+(MALLOCMAX * 4 + 4)) # datatable: 8

  def alloc(self, meimei):
    me, im, ei = meimei.split(".")
    type = int(im)
    if self.next_free[type] < self.limit[type]:
      cell = self.next_free[type]
      self.next_free[type] += 1
      return cell
    else:
      raise OverflowError()

  def alloc_func(self):
    self.func_boundary.append((self.next_free[0], self.next_free[1],
                               self.next_free[2], self.next_free[3],
                               self.next_free[4], self.next_free[5],
                               self.next_free[6], self.next_free[7],
                               self.next_free[8]))

  def dir_range(self, type: int):
    if type != -1:
      bottom = self.limit[type-1]+1
      top = self.next_free[type]-1
      return bottom, top
    else:
      return self.resources(self)

  def drop_func(self):
    self.func_boundary.pop()
  
  def func_range(self, type: int):
    if self.main:
      raise SyntaxError("zen::mind > func_range method is not available for main memory.")
    else:
      if type != -1:
        bottom = self.func_boundary[-1][type]
        top = self.next_free[type]
        return bottom, top
      else: return self.func_boundary[-1]
  
  def typeof(self, addr):
    for i in range(9):
      if addr < self.limit[i]:
        return ecapsdnim(i)
    else:
      return None