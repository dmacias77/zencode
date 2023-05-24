# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅] Grammar and Semantics

# To Do:
# • Funciones pendientes en zzen.txt
# • Revisar administración de constantes... porque los int se duplican
# • Testing... mucho testing
import zen.ply.yacc as yacc

from zen.zenlexicon import tokens, tokenizer
from zen.zenmind import MasterMind
import zen.zensemantics as zs

# ---ZenMind (Memory)---------------------------------------------
zenmind = {}
mastermind = []

# ---Directories--------------------------------------------------
function_dir = []
custom_dir = []

# ---Pins---------------------------------------------------------
const_temporal = None
current_custom = -1
current_function = 0
current_type = -1
custom_declaration = False
invert_result = 0
read_write = -1

# ---Auxiliary Functions------------------------------------------
def searchconst(mmind_index, value):
  bottom, top = mastermind[mmind_index].dir_range(8)
  for key in range(bottom, top):
    if zenmind[key] == value:
      return key
      break
  else: return -1

def evaluate(left_arg, right_arg, operator):
  if operator == 7: return bool(left_arg > right_arg)
  elif operator == 8: return bool(left_arg < right_arg)
  elif operator == 9: return bool(left_arg = right_arg)
  elif operator == 10: return bool(left_arg != right_arg)
  elif operator == 11: return bool(left_arg >= right_arg)
  elif operator == 12: return bool(left_arg <= right_arg)
  elif operator == 19: return bool(left_arg or right_arg)
  elif operator == 20: return bool(left_arg and right_arg)
  else: raise IOError(f"Invalid operator: {operator}")

def function_end():
  pass

def update(quad_ID, element, new_value):
  temp = list(schema[quad_ID])
  temp[element] = new_value
  schema[quad_ID] = tuple(temp)

# ---Generate Functional Stacks-----------------------------------
dimensional_stack = []
jump_stack = []
operand_stack = []
operator_stack = []

# ---Program's Schema---------------------------------------------
# -----Contains the program in quadruples-------------------------
schema = []

# ---Grammar Definitions & Semantics------------------------------

# Program
def p_program(p):
  '''program : n0101 auxa auxb vars auxc mains'''
  pass

def p_n0101(p):
  '''n0101 : '''
  schema.append(zs.quad("goto",None,None,None))
  jump_stack.append(0)
  function_dir.append(("#", None, 0, 0, [], []))
  mastermind.append(MasterMind(1))
  mastermind.append(MasterMind(0))

def p_auxa(p):
  '''auxa : imports auxa
          | '''
  pass

def p_auxb(p):
  '''auxb : customdef auxb
          | '''
  pass

def p_auxc(p):
  '''auxc : functiondef auxc
          | '''
  pass

# File import statement
def p_imports(p):
  '''imports : IMPORT COLON STRING'''
  try:
    zs.import_file(p[3].strip('"'))
  except zs.ZenImportError:
    print(zs.ZenImportError)

# Statements
def p_statement(p):
  '''statement : assign
               | conds
               | whiles
               | dowhiles
               | loops
               | foreachs
               | switchs
               | jumps
               | funccall
               | applys
               | folds
               | console'''
  pass

# Variable definition
def p_vars(p):
  '''vars : SET type var SMCLN vars
          | '''
  pass

# Type definition
def p_type(p):
  '''type : INT
          | CHAR
          | DEC
          | BOOL
          | customkey'''
  global current_type
  if p[1] == r'int':
    current_type = 0
  elif p[1] == r'dec':
    current_type = 1
  elif p[1] == r'char':
    current_type = 2
  elif p[1] == r'bool':
    current_type = 3
  else: pass

# Custom variable name
def p_customkey(p):
  '''customkey : ID'''
  global current_type
  i = 0
  for x in custom_dir:
    if p[-1] == x[0]:
      current_type = i + 4
      break
    else:
      i += 1
  else:
    raise zs.ZenInvalidType(f"zen::cmp > custom type {p[-1]} is not defined.")

# Variable naming
def p_var(p):
  '''var : auxd
         | auxf
         | auxh'''
  pass

def p_auxd(p):
  '''auxd : ID auxe'''
  for x in function_dir[current_function][5]:
    if x[0] == p[1]:
      raise zs.ZenRedefinedID(f"zen::cmp > {p[1]} is already defined.")
      break
  else:
    mm = 0 if current_function == 0 else 1
    addr = mastermind[mm].alloc(current_type, "variable")
    zenmind.update({addr: 0})
    function_dir[current_function][5].append((p[1], current_type, addr))

def p_auxe(p):
  '''auxe : COMMA ID auxe
          | '''
  if len(p) > 2:
    for x in function_dir[current_function][5]:
      if x[0] == p[2]:
        raise zs.ZenRedefinedVariable(f"zen::cmp > {p[2]} is already defined.")
        break
    else:
      mm = 0 if current_function == 0 else 1
      addr = mastermind[mm].alloc(current_type, "variable")
      zenmind.update({addr: 0})
      function_dir[current_function][5].append((p[2], current_type, addr))

def p_auxf(p):
  '''auxf : LIST ID BOX_L INTEGER BOX_R auxg'''
  pass

def p_auxg(p):
  '''auxg : COMMA ID BOX_L INTEGER BOX_R auxg
          | '''
  pass

def p_auxh(p):
  '''auxh : MATRIX ID BOX_L INTEGER COMMA INTEGER BOX_R auxi'''
  pass

def p_auxi(p):
  '''auxi : COMMA ID BOX_L INTEGER COMMA INTEGER BOX_R auxi
          | '''
  pass

# Assignation
def p_assign(p):
  '''assign : ID n0801 ASSIGN n0802 auxk SMCLN
            | direction ASSIGN n0802 auxk SMCLN'''
  if operator_stack[-1] == 0:
    operator_stack.pop()
    for x in function_dir[current_function][5]:
      if p[1] == x[0]:
        if zs.check_compatible(x[1], 0, operand_stack[-1][1]) != -1:
          if x[1] == 0: zenmind[x[2]] = int(zenmind[operand_stack[-1][0]])
          elif x[1] == 1: zenmind[x[2]] = float(zenmind[operand_stack[-1][0]])
          elif x[1] == 2: zenmind[x[2]] = chr(zenmind[operand_stack[-1][0]])
          else: zenmind[x[2]] = False if p[5] == 0 else True
          schema.append(zs.quad(0,operand_stack[-1][0],None,x[2]))
          operand_stack.pop()
          break
        else:
          raise zs.ZenTypeMismatch(f"zen::cmp > couldn't cast assign to '{p[1]}'")
    else:
      if current_function != 0:
        for x in function_dir[0][5]:
          if p[1] == x[0]:
            if zs.check_compatible(x[1], 0, operand_stack[-1][1]) != -1:
              if x[1] == 0: zenmind[x[2]] = int(zenmind[operand_stack[-1][0]])
              elif x[1] == 1: zenmind[x[2]] = float(zenmind[operand_stack[-1][0]])
              elif x[1] == 2: zenmind[x[2]] = chr(zenmind[operand_stack[-1][0]])
              else: zenmind[x[2]] = False if p[5] == 0 else True
              schema.append(zs.quad(0,operand_stack[-1][0],None,x[2]))
              operand_stack.pop()
              break
        else:
          raise zs.ZenUndefinedID(f"zen::cmp > '{p[1]}' is never defined.")
      else:
        raise zs.ZenUndefinedID(f"zen::cmp > '{p[1]}' is never defined.")
  else:
    raise OSError()

def p_n0801(p):
  '''n0801 : '''
  print(p[-1])

def p_n0802(p):
  '''n0802 : '''
  operator_stack.append(0)

#def p_auxj(p):
#  '''auxj : ID ASSIGN auxj
#          | direction ASSIGN auxj
#          | '''
#  pass

def p_auxk(p):
  '''auxk : ID n6001
          | constant n6002
          | direction n6003
          | expression
          | funccall'''
  pass

def p_n6001(p):
  '''n6001 : '''
  for x in function_dir[current_function][5]:
    if p[-1] == x[0]:
      operand_stack.append((x[2], x[1]))
      break
  else:
    if current_function != 0:
      for x in function_dir[0][5]:
        if p[-1] == x[0]:
          operand_stack.append((x[2], x[1]))
        break
      else:
        raise zs.ZenUndefinedID(f"zen::cmp > '{p[-1]}' is never defined.")
    else:
      raise zs.ZenUndefinedID(f"zen::cmp > '{p[-1]}' is never defined.")

def p_n6002(p):
  '''n6002 : '''
  global const_temporal
  const, ctype = const_temporal
  const_temporal = None
  addr = searchconst(current_function, const)
  if addr != -1:
    operand_stack.append((addr, ctype))
  else:
    mm = 0 if current_function == 0 else 1
    addr = mastermind[mm].alloc(ctype, "constant")
    zenmind.update({addr: const})
    operand_stack.append((addr, ctype))

def p_n6003(p):
  '''n6003 : '''
  # Tristes arreglos...

# Conditional statement (if-else)
def p_conds(p):
  '''conds : IF PARNT_L condition PARNT_R n0901 auxl n0902
           | IF PARNT_L condition PARNT_R n0901 auxl ELSE n0903 auxl n0902'''
  pass

def p_n0901(p):
  '''n0901 : '''
  cond, ctype = operand_stack[-1]
  operand_stack.pop()
  if ctype != 3:
    if ctype > 3: wrong_type = custom_dir[ctype-4][0]
    elif ctype == 2: wrong_type = "char"
    elif ctype == 1: wrong_type = "dec"
    elif ctype == 0: wrong_type = "int"
    raise zs.ZenTypeMismatch(f"zen::cmp > if-statement expected boolean, received {wrong_type}")
  else:
    schema.append(zs.quad("goto-f", cond, None, None))
    jump_stack.append(len(schema)-1)

def p_n0902(p):
  '''n0902 : '''
  update(jump_stack[-1], 3, len(schema))
  jump_stack.pop()

def p_n0903(p):
  '''n0903 : '''
  schema.append(zs.quad("goto", None, None, None))
  update(jump_stack[-1], 3, len(schema))
  jump_stack.pop()
  jump_stack.append(len(schema)-1)

def p_auxl(p):
  '''auxl : statement
          | BRACE_L statement auxm BRACE_R'''
  pass

def p_auxm(p):
  '''auxm : statement auxm
          | '''
  pass

# Condition defining
def p_condition(p):
  '''condition : auxo comparison n1001 logicop condition
               | auxo comparison n1001'''
  pass

def p_n1001(p):
  '''n1001 : '''
  if len(operator_stack) > 0:
    if operator_stack[-1] == 19 or operator_stack[-1] == 20:
      right, rtype = operand_stack[-1]
      operand_stack.pop()
      left, ltype = operand_stack[-1]
      operand_stack.pop()
      operator = operator_stack[-1]
      operator_stack.pop()

      otype = zs.check_compatible(ltype, operator, rtype)
      if otype == 3:
        if current_function != 0:
          temp = mastermind[1].alloc(otype, "temporal")
        else:
          temp = mastermind[0].alloc(otype, "temporal")
        schema.append(zs.quad(operator,left,right,temp))
        value = evaluate(zenmind[left], zenmind[right], operator)
        if len(operator_stack) > 0:
          if operator_stack[-1] == 18:
            value = not value
            operator_stack.pop()
        zenmind.update({temp: value})
        operand_stack.append((temp, otype))
      else:
        raise zs.ZenTypeMismatch("zen::cmp > type mismatch: condition expected boolean result")
    elif operator_stack[-1] == 18:
      operator_stack.pop()
      bit, btype = operand_stack[-1]
      operand_stack.pop()
      if btype == 3:
        if current_function != 0:
          temp = mastermind[1].alloc(otype, "temporal")
        else:
          temp = mastermind[0].alloc(otype, "temporal")
        schema.append(zs.quad(operator,bit,None,temp))
        bit = not bit
        zenmind.update({temp: bit})
        operand_stack.append((temp, btype))

def p_auxo(p):
  '''auxo : TILDE
          | '''
  if len(p) > 1: operator_stack.append(18)

# Comparisons in condition
def p_comparison(p):
  '''comparison : auxk compop auxk'''
  right, rtype = operand_stack[-1]
  operand_stack.pop()
  left, ltype = operand_stack[-1]
  operand_stack.pop()
  operator = operator_stack[-1]
  operator_stack.pop()

  otype = zs.check_compatible(ltype, operator, rtype)
  if otype == 3:
    if current_function != 0:
      temp = mastermind[1].alloc(otype, "temporal")
    else:
      temp = mastermind[0].alloc(otype, "temporal")
    schema.append(zs.quad(operator,left,right,temp))
    value = evaluate(zenmind[left], zenmind[right], operator)
    zenmind.update({temp: value})
    operand_stack.append((temp, otype))
  else:
    raise zs.ZenTypeMismatch("zen::cmp > type mismatch: condition expected boolean result")

# While statement
def p_whiles(p):
  '''whiles : WHILE n1201 PARNT_L condition PARNT_R n1202 auxl'''
  temp = jump_stack[-1]
  jump_stack.pop()
  schema.append(zs.quad("goto", None, None, jump_stack[-1]))
  jump_stack.pop()
  update(temp, 3, len(schema))

def p_n1201(p):
  '''n1201 : '''
  jump_stack.append(len(schema))

def p_n1202(p):
  '''n1202 : '''
  cond, ctype = operand_stack[-1]
  operand_stack.pop()
  if ctype != 3:
    if ctype > 3: wrong_type = custom_dir[ctype-4][0]
    elif ctype == 2: wrong_type = "char"
    elif ctype == 1: wrong_type = "dec"
    elif ctype == 0: wrong_type = "int"
    raise zs.ZenTypeMismatch(f"zen::cmp > while-statement expected boolean, received {wrong_type}")
  else:
    schema.append(zs.quad("goto-f", cond, None, None))
    jump_stack.append(len(schema)-1)

# Do-while statement
def p_dowhiles(p):
  '''dowhiles : DO n1301 BRACE_L statement auxm BRACE_R WHILE PARNT_L condition PARNT_R'''
  cond, ctype = operand_stack[-1]
  operand_stack.pop()
  if ctype != 3:
    if ctype > 3: wrong_type = custom_dir[ctype-4][0]
    elif ctype == 2: wrong_type = "char"
    elif ctype == 1: wrong_type = "dec"
    elif ctype == 0: wrong_type = "int"
    raise zs.ZenTypeMismatch(f"zen::cmp > do-while-statement expected boolean, received {wrong_type}")
  else:
    schema.append(zs.quad("goto-t", cond, None, jump_stack[-1]))
    jump_stack.pop()

def p_n1301(p):
  '''n1301 : '''
  jump_stack.append(len(schema))

# Loop statement
def p_loops(p):
  '''loops : LOOP ID n1401 FROM auxk n1402 UNTIL PARNT_L condition PARNT_R auxl'''
  pass

def p_n1401(p):
  '''n1401 : '''
  if current_function != 0:
    for x in function_dir[current_function][5]:
      if x[0] == p[-1]:
        if x[1] == 0: 
          operand_stack.append((x[2], x[1]))
        else:
          if x[1] > 3: wrong_type = custom_dir[x[1]-4][0]
          elif x[1] == 3: wrong_type = "bool"
          elif x[1] == 2: wrong_type = "char"
          elif x[1] == 1: wrong_type = "dec"
          raise zs.ZenTypeMismatch(f"zen::cmp > for-statement expected int iterator, received {wrong_type}")
        break
  else:
    for x in function_dir[0][5]:
      if x[0] == p[-1]:
        if x[1] == 0: 
          operand_stack.append((x[2], x[1]))
        else:
          if x[1] > 3: wrong_type = custom_dir[x[1]-4][0]
          elif x[1] == 3: wrong_type = "bool"
          elif x[1] == 2: wrong_type = "char"
          elif x[1] == 1: wrong_type = "dec"
          raise zs.ZenTypeMismatch(f"zen::cmp > for-statement expected int iterator, received {wrong_type}")
        break
    else:
      raise zs.ZenUndefinedID(f"zen::cmp > {p[-1]} is not defined.")

def p_n1402(p):
  '''n1402 : '''
  begin, bgtype = operand_stack[-1]
  operand_stack.pop()
  if bgtype != 0:
    raise zs.ZenTypeMismatch("zen::cmp > for-statement start expected int.")

  iter, itype = operand_stack[-1]
  if zs.check_compatible(bgtype, 0, itype) != -1:
    schema.append(zs.quad(0, begin, None, iter))
    
  else:
    raise zs.ZenTypeMismatch(f"zen::cmp > type mismatch: can't operate {ltype} {operator} {rtype}")

# Foreach statement
def p_foreachs(p):
  '''foreachs : FOREACH AS ID IN ID auxl'''
  pass

# Switch statement
def p_switchs(p):
  '''switchs : SWITCH PARNT_L auxq PARNT_R BRACE_L cases auxr BRACE_R'''
  pass

def p_auxq(p):
  '''auxq : ID
          | expression'''
  pass

def p_auxr(p):
  '''auxr : cases auxr
          | '''
  pass

# Case statement
def p_cases(p):
  '''cases : CASE COLON auxs BREAK SMCLN
           | DEFAULT COLON auxs BREAK SMCLN'''
  pass

def p_auxs(p):
  '''auxs : statement auxs
          | '''
  pass

# Jump statement (next/break/return)
def p_jumps(p):
  '''jumps : NEXT SMCLN
           | BREAK SMCLN
           | RETURN auxk SMCLN'''
  pass

# Function call as statement
def p_funccall(p):
  '''funccall : function SMCLN'''
  pass

# Function call as part of an expression
def p_function(p):
  '''function : auxt ID PARNT_L args PARNT_R'''
  pass

def p_auxt(p):
  '''auxt : ID DOT
          | '''
  pass

# HOF apply statement
def p_applys(p):
  '''applys : APPLY auxu INTO ID SMCLN'''
  pass

def p_auxu(p):
  '''auxu : function
          | lambdacall'''
  pass

# HOF fold statement
def p_folds(p):
  '''folds : FOLDL ID INTO ID USING auxu SMCLN
           | FOLDR ID INTO ID USING auxu SMCLN'''
  pass

# Lambda function call
def p_lambdacall(p):
  '''lambdacall : LAMBDA PARNT_L args PARNT_R BRACE_L vars auxs RETURN auxk BRACE_R'''
  pass

# Console interaction statement
def p_console(p):
  '''console : CREAD n2401 ASSIGN auxw auxv SMCLN
             | CWRITE n2401 ASSIGN auxw auxv SMCLN'''
  global read_write
  schema.append(zs.quad(16 + read_write, None, None, operand_stack[-1][0]))
  operand_stack.pop()
  read_write = -1

def p_n2401(p):
  '''n2401 : '''
  global read_write
  if p[-1] == r'cread': read_write = 0
  else: read_write = 1
  
def p_auxv(p):
  '''auxv : ASSIGN auxw auxv
          | '''
  pass

def p_auxw(p):
  '''auxw : ID n7201
          | constant n7202
          | direction n7203
          | expression'''
  pass

def p_n7201(p):
  '''n7201 : '''
  for x in function_dir[current_function][5]:
    if p[-1] == x[0]:
      operand_stack.append((x[2], x[1]))
      break
  else:
    if current_function != 0:
      for x in function_dir[0][5]:
        if p[-1] == x[0]:
          operand_stack.append((x[2], x[1]))
        break
      else:
        raise zs.ZenUndefinedID(f"zen::cmp > {p[-1]} is never defined.")
    else:
      raise zs.ZenUndefinedID(f"zen::cmp > {p[-1]} is never defined.")

def p_n7202(p):
  '''n7202 : '''
  if isinstance(p[-1], str):
    mm = 0 if current_function == 0 else 1
    addr = mastermind[mm].alloc("string", "constant")
    zenmind.update({addr: p[-1]})
    operand_stack.append((addr, current_type))
  else:
    constant, type = const_temporal
    addr = searchconst(current_function, constant)
    if addr == -1:
      mm = 0 if current_function == 0 else 1
      addr = mastermind[mm].alloc(type, "constant")
      zenmind.update({addr: p[-1]})
      operand_stack.append((addr, type))
    else:
      operand_stack.append((addr, type))      

def p_n7203(p):
  '''n7203 : '''
  # Aquí va toda la wea de arreglos

# Constant usage
def p_constant(p):
  '''constant : INTEGER
              | DECIMAL
              | CHARACTER
              | TRUE
              | FALSE
              | NULL'''
  global const_temporal
  this_type = None
  if type(p[1]) is int: this_type = 0
  elif type(p[1]) is float: this_type = 1
  elif type(p[1]) is str and len(p[-1]) == 1: this_type = 2
  elif p[1] == "True" or p[1] == "False": this_type = 3
  else: this_type = -1
  const_temporal = (p[1], this_type)
  print("new: ", const_temporal)

def p_direction(p):
  '''direction : ID BOX_L auxk auxx BOX_R'''
  pass

def p_auxx(p):
  '''auxx : COMMA auxk
          | '''
  pass

# Function definition    
def p_functiondef(p):
  '''functiondef : FUNCTION type ID n2801 PARNT_L args PARNT_R BRACE_L auxs RETURN auxk BRACE_R n2802
                 | voidfdef'''
  pass

def p_n2801(p):
  '''n2801 : '''
  global current_function
  for x in function_dir:
    if x[0] == p[-1]:
      raise zs.ZenRedefinedID(f"zen::cmp > a function named {p[-1]} is already defined.")
      break
  else:
    function_dir.append((p[-1], current_type, len(schema) + 1, current_function, [], []))
    addr = mastermind[0].alloc(current_type, "function")
    zenmind.update({addr: 0})
    function_dir[0][5].append((f"zf#{p[-1]}", current_type, addr))
    current_function = len(function_dir) - 1

def p_n2802(p):
  '''n2802 : '''
  function_dir[current_function][5].clear()

# Void function definition
def p_voidfdef(p):
  '''voidfdef : FUNCTION VOID ID n2901 PARNT_L args PARNT_R BRACE_L vars statement auxs BRACE_R'''
  function_dir[current_function][5].clear()

def p_n2901(p):
  '''n2901 : '''
  global current_function, current_type
  current_type = -1
  for x in function_dir:
    if x[0] == p[-1]:
      raise zs.ZenRedefinedID(f"zen::cmp > a function named {p[-1]} is already defined.")
      break
  else:
    function_dir.append((p[-1], -1, len(schema) + 1, current_function, [], []))
    current_function = len(function_dir) - 1

# Custom variable type definition
def p_customdef(p):
  '''customdef : CUSTOM ID n3001 BRACE_L auxy BRACE_R SMCLN'''
  global custom_declaration
  custom_declaration = False

def p_n3001(p):
  '''n3001 : '''
  for x in custom_dir:
    if x[0] == p[-1]:
      raise zs.ZenRedefinedID(f"zen::cmp > class {p[-1]} is already defined.")
      break
  else:
    global current_custom, custom_declaration
    custom_declaration = True
    custom_dir.append((p[-1], [], [], [], [])) # name
    current_custom = len(custom_dir) - 1

def p_auxy(p):
  '''auxy : priv pub
          | pub priv'''
  pass

# Private section of custom variable definition
def p_priv(p):
  '''priv : PRIVATE COLON structstat auxz
          | '''
  pass

# Public section of custom variable definition
def p_pub(p):
  '''pub : PUBLIC COLON structstat auxz
         | '''
  pass

def p_auxz(p):
  '''auxz : structstat auxz
          | '''
  pass

# Custom variable's structure statement
def p_structstat(p):
  '''structstat : vars
                | functiondef
                | cnstrdef'''
  pass

# Custom variable's constructor definition
def p_cnstrdef(p):
  '''cnstrdef : CONSTR PARNT_L args PARNT_R BRACE_L statement auxt BRACE_R'''
  pass

# Arguments definition statement
def p_args(p):
  '''args : type var n3501 args
          | '''
  pass

def p_n3501(p):
  '''n3501 : '''
  function_dir[current_function][4].append(current_type)
  mm = 0 if current_function == 0 else 1
  addr = mastermind[mm].alloc(current_type, "variable")
  zenmind.update({addr: 0})
  function_dir[current_function][5].append((p[-1], current_type, addr))

# Arithmetic expression
def p_expression(p):
  '''expression : term n3601 PLUS n3602 expression
                | term n3601 NDASH n3602 expression
                | term n3601'''
  pass

def p_n3601(p):
  '''n3601 : '''
  if len(operator_stack) > 0:
    if operator_stack[-1] == 1 or operator_stack[-1] == 2:
      right, rtype = operand_stack[-1]
      operand_stack.pop()
      left, ltype = operand_stack[-1]
      operand_stack.pop()
      operator = operator_stack[-1]
      operator_stack.pop()
  
      otype = zs.check_compatible(ltype, operator, rtype)
      if otype != -1:
        if current_function != 0:
          temp = mastermind[1].alloc(otype, "temporal")
        else:
          temp = mastermind[0].alloc(otype, "temporal")
        schema.append(zs.quad(operator,left,right,temp))
        value = zenmind[left] + zenmind[right] if operator == 1 else zenmind[left] - zenmind[right]
        if otype == 0: value = int(value)
        elif otype == 2: value = chr(value)
        zenmind.update({temp: value})
        operand_stack.append((temp, otype))
      else:
        raise zs.ZenTypeMismatch(f"zen::cmp > type mismatch: can't operate {ltype} {operator} {rtype}")
      
def p_n3602(p):
  '''n3602 : '''
  if p[-1] == '+': operator_stack.append(1)
  elif p[-1] == '-': operator_stack.append(2)

# Arithmetic term
def p_term(p):
  '''term : base n3701 ASTRK n3702 term
          | base n3701 SLASH n3702 term
          | base n3701'''
  pass

def p_n3701(p):
  '''n3701 : '''
  if len(operator_stack) > 0:
    if operator_stack[-1] == 3 or operator_stack[-1] == 4:
      right, rtype = operand_stack[-1]
      operand_stack.pop()
      left, ltype = operand_stack[-1]
      operand_stack.pop()
      operator = operator_stack[-1]
      operator_stack.pop()
  
      otype = zs.check_compatible(ltype, operator, rtype)
      print(otype)
      if otype != -1:
        if current_function != 0:
          temp = mastermind[1].alloc(otype, "temporal")
        else:
          temp = mastermind[0].alloc(otype, "temporal")
        schema.append(zs.quad(operator,left,right,temp))
        value = zenmind[left] * zenmind[right] if operator == 3 else zenmind[left] / zenmind[right]
        if otype == 0: value = int(value)
        zenmind.update({temp: value})
        operand_stack.append((temp, otype))
      else:
        raise zs.ZenTypeMismatch(f"zen::cmp > type mismatch: can't operate {ltype} {operator} {rtype}")
        
def p_n3702(p):
  '''n3702 : '''
  if p[-1] == '*': operator_stack.append(3)
  elif p[-1] == '/': operator_stack.append(4)

# Numerical base
def p_base(p):
  '''base : factor MODULO factor
          | factor CARET factor
          | factor'''
  if len(p) > 2:
    op = None
    if p[2] == '%': op = 5
    elif p[2] == '^': op = 6
    relation, rtype = operand_stack[-1]
    operand_stack.pop()
    base, btype = operand_stack[-1]
    operand_stack.pop()
    otype = zs.check_compatible(btype, op, rtype)
    if otype != -1:
      mm = 0 if current_function == 0 else 1
      temp = mastermind[mm].alloc(current_type, "temporal")
      operand_stack.append((temp, current_type))
      term = (zenmind[base] % zenmind[relation]) if op == 5 else (zenmind[base] ** zenmind[relation])
      zenmind.update({temp: term})
      schema.append(zs.quad(op, base, relation, temp))

# Arithmetic factor
def p_factor(p):
  '''factor : ID n3901
            | constant n3902
            | NDASH constant n3903
            | direction n3904
            | funccall
            | PARNT_L expression PARNT_R'''
  pass

def p_3901(p):
  '''n3901 : '''
  for x in function_dir[current_function][5]:
    if p[-1] == x[0]:
      operand_stack.append((x[2], x[1]))
      break
  else:
    if current_function != 0:
      for x in function_dir[0][5]:
        if p[-1] == x[0]:
          operand_stack.append((x[2], x[1]))
        break
      else:
        raise zs.ZenUndefinedID(f"zen::cmp > '{p[-1]}' is never defined.")
    else:
      raise zs.ZenUndefinedID(f"zen::cmp > '{p[-1]}' is never defined.")

def p_n3902(p):
  '''n3902 : '''
  global const_temporal
  const, ctype = const_temporal
  const_temporal = None
  addr = searchconst(current_function, const)
  if addr != -1:
    operand_stack.append((addr, ctype))
  else:
    mm = 0 if current_function == 0 else 1
    addr = mastermind[mm].alloc(ctype, "constant")
    zenmind.update({addr: const})
    operand_stack.append((addr, ctype))

def p_n3903(p):
  '''n3903 : '''
  global const_temporal
  const, ctype = const_temporal
  const_temporal = None
  const = -const
  addr = searchconst(current_function, const)
  if addr != -1:
    operand_stack.append((addr, ctype))
  else:
    mm = 0 if current_function == 0 else 1
    addr = mastermind[mm].alloc(ctype, "constant")
    zenmind.update({addr: const})
    operand_stack.append((addr, ctype))

def p_n3904(p):
  '''n3904 : '''
  # Tristes arreglos...

# Logical operator appearance
def p_logicop(p):
  '''logicop : AND
             | OR'''
  if p[1] == '||':
    operator_stack.append(zs.storef("or"))
  else: operator_stack.append(zs.storef("and"))

# Comparative operator appearance
def p_compop(p):
  '''compop : ANG_L n4101
            | ANG_R n4102
            | EQUAL
            | NEQUAL'''
  if len(p) == 2:
    operator_stack.append(zs.storef(p[1]))

def p_n4101(p):
  '''n4101 : EQUAL
           | '''
  if len(p) > 1:
    operator_stack.append(12)
  else: operator_stack.append(8)

def p_n4102(p):
  '''n4102 : EQUAL
           | '''
  if len(p) > 1:
    operator_stack.append(11)
  else: operator_stack.append(7)

# Main section
def p_mains(p):
  '''mains : MAIN BRACE_L n4201 vars statement auxs END n4202 BRACE_R'''
  pass

def p_n4201(p):
  '''n4201 : '''
  global current_function
  update(jump_stack[-1], 3, len(schema))
  jump_stack.pop()
  function_dir.append(("main", None, len(schema), 0, None, []))
  current_function = len(function_dir) - 1

def p_n4202(p):
  '''n4202 : '''
  schema.append((999,-1,-1,-1))
  # Temporal instructions------------
  for x in function_dir:
    print(x)
  print("\nJS: ", jump_stack)
  print("OTS:", operand_stack)
  print("OS: ", operator_stack, "\n")
  i = 0
  for x in schema:
    print(i, ".: ", x)
    i += 1
  print("\n")
  for x, y in zenmind.items():
    print(x,":",y)
  # ----------------------------------
  function_dir.clear()

# YACC required error function
def p_error(p):
  if p:
    if p.type != 'COMMENT':
      print(f"zen::grm > syntax error at token {p.type} ({p.value}) at line {p.lineno} : {p.lexpos}\n")
      for x in function_dir:
        print(x)
      print("\nJS: ", jump_stack)
      print("DS: ", dimensional_stack)
      print("OTS:", operand_stack)
      print("OS: ", operator_stack, "\n")
      for x in schema:
        print(x)
  else:
    print("zen::grm > syntax error: unexpected end of input")
  
# ---Parser-------------------------------------------------------
lexer = tokenizer()
parser = yacc.yacc()
# ----------------------------------------------------------------