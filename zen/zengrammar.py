# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅] Grammar and Semantics

# To Do:
# • La máquina virtual
import zen.ply.yacc as yacc

from zen.zenlexicon import tokens, tokenizer
from zen.zenmind import MasterMind
import zen.zensemantics as zs

# ---ZenMind (Memory Allocators)----------------------------------
zenmind = {}
mastermind = []

# ---Directories--------------------------------------------------
function_dir = []
table_dir = []

# ---Pins---------------------------------------------------------
calling_function = -1
const_temporal = None
current_function = 0
current_type = -1
function_def = False
invert_result = False
read_write = -1
special_addr = -1
tablecols = 0

# ---Auxiliary Functions------------------------------------------
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

def fd_update(fdID, element, new_value):
  temp = list(function_dir[fdID])
  temp[element] = new_value
  function_dir[fdID] = tuple(temp)

def quad_update(quad_ID, element, new_value):
  temp = list(schema[quad_ID])
  temp[element] = new_value
  schema[quad_ID] = tuple(temp)

def rewind():
  mastermind[1].drop_func()

def searchconst(mmind_index, value):
  mm = 1 if mmind_index != 0 else 0
  bottom, top = mastermind[mm].dir_range(8)
  for key in range(bottom, top):
    if zenmind[key] == value:
      return key
      break
  else:
    newk = mastermind[mm].alloc(0, "constant")
    zenmind.update({newk: value})
    return newk

# ---Functional Stacks--------------------------------------------
dimensional_stack = []
jump_stack = []
operand_stack = []
operator_stack = []
par_limit_stack = []
parameter_stack = []

# ---Program's Schema---------------------------------------------
# -----Contains the program in quadruples-------------------------
schema = []

# ---Grammar Definitions & Semantics------------------------------

# Program
def p_program(p):
  '''program : n0101 auxa auxb mains'''
  pass

def p_n0101(p):
  '''n0101 : '''
  global special_addr
  schema.append(zs.quad("goto",None,None,None))
  jump_stack.append(0)
  function_dir.append(("#", None, 0, 0, [], [], None))
  mastermind.append(MasterMind(1))
  mastermind.append(MasterMind(0))
  special_addr = mastermind[0].alloc(1, "variable")

def p_auxa(p):
  '''auxa : vars auxa
          | '''
  pass

def p_auxb(p):
  '''auxb : functiondef auxb
          | '''
  pass

# Statements
def p_statement(p):
  '''statement : assign
               | conds
               | console
               | datadist
               | dataset
               | dowhiles
               | loops
               | vfunction
               | whiles'''
  pass

# Variable definition
def p_vars(p):
  '''vars : SET type var SMCLN vars
          | CREATE datatable SMCLN vars
          | '''
  pass

# Type definition
def p_type(p):
  '''type : INT
          | CHAR
          | DEC
          | BOOL
          | TEXT'''
  global current_type
  if p[1] == r'int':
    current_type = 0
  elif p[1] == r'dec':
    current_type = 1
  elif p[1] == r'char':
    current_type = 2
  elif p[1] == r'bool':
    current_type = 3
  elif p[1] == r'text':
    current_type = 4

# Custom variable name
def p_datatable(p):
  '''datatable : DATA ID n0501 BOX_L BRACE_L type COLON STRING n0502 BRACE_R auxc BOX_R BOX_L INTEGER BOX_R'''
  for x in function_dir[current_function][5]:
    if x[0] == p[2]:
      raise zs.ZenRedefinedID(f"zen::cmp > {p[2]} is already defined.")
      break
  else:
    mm = 0 if current_function == 0 else 1
    for _ in range(p[14]):
      for i in range(tablecols):
        addr = mastermind[mm].alloc(8, "variable")
        zenmind.update({addr: 1})
    function_dir[current_function][5].append((p[2], 5, (addr+1)-tablecols*p[14], [p[14], tablecols], table_dir))

def p_n0501(p):
  '''n0501 : '''
  if function_dir[current_function][3] == 0:
    global tablecols
    fd_update(current_function, 3, 1)
    tablecols = 0
  else:
    raise zs.ZenDataTableRedefinition("zen::cmp > data table is a single-definition class.")

def p_n0502(p):
  '''n0502 : '''
  global tablecols
  name = p[-1]
  for x in table_dir:
    if name == x[0]:
      raise zs.ZenRedefinedID("zen::cmp > attempting to declare two columns with the same identifier in data.")
      break
  else:
    table_dir.append((name, current_type))
    tablecols += 1

def p_auxc(p):
  '''auxc : COMMA BRACE_L type COLON STRING n0502 BRACE_R auxc
          | '''
  pass

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
    zenmind.update({addr: 1})
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
      zenmind.update({addr: 1})
      function_dir[current_function][5].append((p[2], current_type, addr))

def p_auxf(p):
  '''auxf : LIST ID BOX_L INTEGER BOX_R auxg'''
  for x in function_dir[current_function][5]:
    if x[0] == p[2]:
      raise zs.ZenRedefinedID(f"zen::cmp > {p[2]} is already defined.")
      break
  else:
    mm = 0 if current_function == 0 else 1
    for _ in range(p[4]):
      addr = mastermind[mm].alloc(current_type, "variable")
      zenmind.update({addr: 1})
    function_dir[current_function][5].append((p[2], current_type, (addr+1)-p[4], [p[4]]))

def p_auxg(p):
  '''auxg : COMMA ID BOX_L INTEGER BOX_R auxg
          | '''
  if len(p) > 2:
    for x in function_dir[current_function][5]:
      if x[0] == p[2]:
        raise zs.ZenRedefinedID(f"zen::cmp > {p[2]} is already defined.")
        break
    else:
      mm = 0 if current_function == 0 else 1
      for _ in range(p[4]):
        addr = mastermind[mm].alloc(current_type, "variable")
        zenmind.update({addr: 1})
      function_dir[current_function][5].append((p[2], current_type, (addr+1)-p[4], [p[4]]))

def p_auxh(p):
  '''auxh : MATRIX ID BOX_L INTEGER COMMA INTEGER BOX_R auxi'''
  for x in function_dir[current_function][5]:
    if x[0] == p[2]:
      raise zs.ZenRedefinedID(f"zen::cmp > {p[2]} is already defined.")
      break
  else:
    mm = 0 if current_function == 0 else 1
    for _ in range(p[4]*p[6]):
      addr = mastermind[mm].alloc(current_type, "variable")
      zenmind.update({addr: 1})
    function_dir[current_function][5].append((p[2], current_type, (addr+1)-p[4]*p[6], [p[4], p[6]]))

def p_auxi(p):
  '''auxi : COMMA ID BOX_L INTEGER COMMA INTEGER BOX_R auxi
          | '''
  if len(p) > 2:  
    for x in function_dir[current_function][5]:
      if x[0] == p[2]:
        raise zs.ZenRedefinedID(f"zen::cmp > {p[2]} is already defined.")
        break
    else:
      mm = 0 if current_function == 0 else 1
      for _ in range(p[4]*p[6]):
        addr = mastermind[mm].alloc(current_type, "variable")
        zenmind.update({addr: 1})
      function_dir[current_function][5].append((p[2], current_type, (addr+1)-p[4]*p[6], [p[4], p[6]]))

# Assignation
def p_assign(p):
  '''assign : ID ASSIGN n0701 expression SMCLN
            | direction ASSIGN n0701 expression SMCLN'''
  if operator_stack[-1] == 0:
    operator_stack.pop()
    if p[1] is not None:
      for x in function_dir[current_function][5]:
        if p[1] == x[0]:
          if zs.check_compatible(x[1], 0, operand_stack[-1][1]) != -1:
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
                schema.append(zs.quad(0,operand_stack[-1][0],None,x[2]))
                operand_stack.pop()
                break
          else:
            raise zs.ZenUndefinedID(f"zen::cmp > '{p[1]}' is never defined.")
        else:
          raise zs.ZenUndefinedID(f"zen::cmp > '{p[1]}' is never defined.")
    else:
      asigned, a2type = operand_stack[-1]
      operand_stack.pop()
      asignee, a1type = operand_stack[-1]
      operand_stack.pop()
      if zs.check_compatible(a1type, 0, a2type) != -1:
        schema.append(zs.quad(0, asigned, None, asignee))
  else:
    raise OSError()

def p_n0701(p):
  '''n0701 : '''
  operator_stack.append(0)

# Conditional statement (if-else)
def p_conds(p):
  '''conds : IF PARNT_L condition PARNT_R n0801 auxk n0802
           | IF PARNT_L condition PARNT_R n0801 auxk ELSE n0803 auxk n0802'''
  pass

def p_n0801(p):
  '''n0801 : '''
  cond, ctype = operand_stack[-1]
  operand_stack.pop()
  if ctype != 3:
    if ctype == 5: wrong_type = "whole data table"
    elif ctype == 4: wrong_type = "text"
    elif ctype == 2: wrong_type = "char"
    elif ctype == 1: wrong_type = "dec"
    elif ctype == 0: wrong_type = "int"
    raise zs.ZenTypeMismatch(f"zen::cmp > if-statement expected boolean, received {wrong_type}")
  else:
    schema.append(zs.quad("goto-f", cond, None, None))
    jump_stack.append(len(schema)-1)

def p_n0802(p):
  '''n0802 : '''
  quad_update(jump_stack[-1], 3, len(schema))
  jump_stack.pop()

def p_n0803(p):
  '''n0803 : '''
  schema.append(zs.quad("goto", None, None, None))
  quad_update(jump_stack[-1], 3, len(schema))
  jump_stack.pop()
  jump_stack.append(len(schema)-1)

def p_auxk(p):
  '''auxk : statement
          | BRACE_L statement auxl BRACE_R'''
  pass

def p_auxl(p):
  '''auxl : statement auxl
          | '''
  pass

# Condition defining
def p_condition(p):
  '''condition : auxm comparison n0901 logicop condition
               | auxm comparison n0901'''
  pass

def p_n0901(p):
  '''n0901 : '''
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
        if len(operator_stack) > 0:
          if operator_stack[-1] == 18:
            schema.append(zs.quad(operator_stack[-1], None, None, temp))
            operator_stack.pop()
        zenmind.update({temp: 1})
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
        zenmind.update({temp: 1})
        operand_stack.append((temp, btype))

def p_auxm(p):
  '''auxm : TILDE
          | '''
  if len(p) > 1: operator_stack.append(18)

# Comparisons in condition
def p_comparison(p):
  '''comparison : expression compop expression'''
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
    zenmind.update({temp: 1})
    operand_stack.append((temp, otype))
  else:
    raise zs.ZenTypeMismatch("zen::cmp > type mismatch: condition expected boolean result")

# While statement
def p_whiles(p):
  '''whiles : WHILE n1101 PARNT_L condition PARNT_R n1102 auxk'''
  temp = jump_stack[-1]
  jump_stack.pop()
  schema.append(zs.quad("goto", None, None, jump_stack[-1]))
  jump_stack.pop()
  quad_update(temp, 3, len(schema))

def p_n1101(p):
  '''n1101 : '''
  jump_stack.append(len(schema))

def p_n1102(p):
  '''n1102 : '''
  cond, ctype = operand_stack[-1]
  operand_stack.pop()
  if ctype != 3:
    if ctype == 5: wrong_type = "whole data table"
    elif ctype == 4: wrong_type = "text"
    elif ctype == 2: wrong_type = "char"
    elif ctype == 1: wrong_type = "dec"
    elif ctype == 0: wrong_type = "int"
    raise zs.ZenTypeMismatch(f"zen::cmp > while-statement expected boolean, received {wrong_type}")
  else:
    schema.append(zs.quad("goto-f", cond, None, None))
    jump_stack.append(len(schema)-1)

# Do-while statement
def p_dowhiles(p):
  '''dowhiles : DO n1201 auxk WHILE PARNT_L condition PARNT_R'''
  cond, ctype = operand_stack[-1]
  operand_stack.pop()
  if ctype != 3:
    if ctype == 5: wrong_type = "whole data table"
    elif ctype == 4: wrong_type = "text"
    elif ctype == 2: wrong_type = "char"
    elif ctype == 1: wrong_type = "dec"
    elif ctype == 0: wrong_type = "int"
    raise zs.ZenTypeMismatch(f"zen::cmp > do-while-statement expected boolean, received {wrong_type}")
  else:
    schema.append(zs.quad("goto-t", cond, None, jump_stack[-1]))
    jump_stack.pop()

def p_n1201(p):
  '''n1201 : '''
  jump_stack.append(len(schema))

# Loop statement
def p_loops(p):
  '''loops : LOOP ID n1301 IN RANGE PARNT_L expression n1302 COLON expression n1303 COLON condition n1304 PARNT_R auxk n1305'''
  pass

def p_n1301(p):
  '''n1301 : '''
  if current_function != 0:
    for x in function_dir[current_function][5]:
      if x[0] == p[-1]:
        if x[1] == 0: 
          operand_stack.append((x[2], x[1]))
        else:
          if x[1] == 5: wrong_type = "whole data table"
          elif x[1] == 4: wrong_type = "text"
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
          if x[1] == 5: wrong_type = "whole data table"
          elif x[1] == 4: wrong_type = "text"
          elif x[1] == 3: wrong_type = "bool"
          elif x[1] == 2: wrong_type = "char"
          elif x[1] == 1: wrong_type = "dec"
          raise zs.ZenTypeMismatch(f"zen::cmp > for-statement expected int iterator, received {wrong_type}")
        break
    else:
      raise zs.ZenUndefinedID(f"zen::cmp > {p[-1]} is not defined.")

def p_n1302(p):
  '''n1302 : '''
  begin, bgtype = operand_stack[-1]
  operand_stack.pop()
  iter, itype = operand_stack[-1]
  operand_stack.pop()
  if bgtype != 0:
    raise zs.ZenTypeMismatch("zen::cmp > for-statement start clause expected int.")
  if zs.check_compatible(itype, 0, bgtype) != -1:
    schema.append(zs.quad(0, begin, None, iter))
    schema.append(zs.quad("goto", None, None, None))
    jump_stack.append(len(schema))
    jump_stack.append(len(schema)-1)
    operand_stack.append((iter, itype))
  else:
    raise zs.ZenTypeMismatch(f"zen::cmp > type mismatch: can't operate {bgtype} {0} {itype}")

def p_n1303(p):
  '''n1303 : '''
  update, utype = operand_stack[-1]
  operand_stack.pop()
  iter, itype = operand_stack[-1]
  operand_stack.pop()
  if utype != 0:
    raise zs.ZenTypeMismatch("zen::cmp > for-statement update clause expected int.")
  else:
    if zs.check_compatible(itype, 0, utype) == 0:
      if current_function == 0: temp = mastermind[0].alloc(0, "temporal")
      else: temp = mastermind[1].alloc(0, "temporal")
      schema.append(zs.quad(1, update, iter, temp))
      schema.append(zs.quad(0, temp, None, iter))
      temp = jump_stack[-1]
      quad_update(temp, 3, len(schema))
      jump_stack.pop()
    else:
      raise zs.ZenTypeMismatch(f"zen::cmp > type mismatch: can't assign {itype} to {utype}")

def p_n1304(p):
  '''n1304 : '''
  compare, ctype = operand_stack[-1]
  operand_stack.pop()
  if ctype != 3:
    raise zs.ZenTypeMismatch("zen::cmp > for-statement compare clause expected boolean.")
  else:
    schema.append(zs.quad("goto-t", compare, None, None))
    jump_stack.append(len(schema)-1)

def p_n1305(p):
  '''n1305 : '''
  quad_update(jump_stack[-1], 3, len(schema)+1)
  jump_stack.pop()
  schema.append(zs.quad("goto", None, None, jump_stack[-1]))
  jump_stack.pop()

# Console interaction statement
def p_console(p):
  '''console : CREAD n1401 ASSIGN expression auxn SMCLN
             | CWRITE n1401 ASSIGN expression auxn SMCLN'''
  global read_write
  schema.append(zs.quad(16 + read_write, None, None, operand_stack[-1][0]))
  operand_stack.pop()
  read_write = -1

def p_n1401(p):
  '''n1401 : '''
  global read_write
  if p[-1] == r'cread': read_write = 0
  else: read_write = 1
  
def p_auxn(p):
  '''auxn : ASSIGN expression auxn
          | '''
  pass

# Constant element usage
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
  elif type(p[1]) is str and len(p[1]) == 1: this_type = 2
  elif p[1] == "True" or p[1] == "False": this_type = 3
  else: this_type = -1
  const_temporal = (p[1], this_type)

# Function definition    
def p_functiondef(p):
  '''functiondef : FUNCTION type ID n1701 PARNT_L args PARNT_R BRACE_L vars auxl RETURN expression n1702 SMCLN BRACE_R
                 | voidfdef'''
  global current_function, function_def
  function_dir[current_function][5].clear()
  fd_update(current_function, 6, mastermind[1].func_range(-1))
  mastermind[1].drop_func()
  schema.append(zs.quad(99, None, None, None))
  current_function = function_dir[current_function][3]
  function_def = False
  rewind()

def p_n1701(p):
  '''n1701 : '''
  global current_function
  for x in function_dir:
    if x[0] == p[-1]:
      raise zs.ZenRedefinedID(f"zen::cmp > a function named {p[-1]} is already defined.")
      break
  else:
    global function_def
    function_def = True
    function_dir.append((p[-1], current_type, len(schema), current_function, [], [], None))
    addr = mastermind[0].alloc(current_type, "function")
    zenmind.update({addr: 1})
    function_dir[0][5].append((f"#{p[-1]}", current_type, addr))
    mastermind[1].alloc_func()
    current_function = len(function_dir) - 1

def p_n1702(p):
  '''n1702 : '''
  if operand_stack[-1][1] == function_dir[current_function][1]:
    schema.append(zs.quad("return", None, None, operand_stack[-1][0]))
    operand_stack.pop()
  else:
    raise zs.ZenTypeMismatch(f"zen::cmp > returning element for {function_dir[current_function][0]}() does not match its type.")

# Void function definition
def p_voidfdef(p):
  '''voidfdef : FUNCTION VOID ID n1801 PARNT_L args PARNT_R BRACE_L vars statement auxl BRACE_R'''
  pass

def p_n1801(p):
  '''n1801 : '''
  global current_function, current_type
  current_type = -1
  for x in function_dir:
    if x[0] == p[-1]:
      raise zs.ZenRedefinedID(f"zen::cmp > a function named {p[-1]} is already defined.")
      break
  else:
    global function_def
    function_def = True
    function_dir.append((p[-1], -1, len(schema), current_function, [], [], None))
    mastermind[1].alloc_func()
    current_function = len(function_dir) - 1

# Function call
def p_function(p):
  '''function : ID n1901 PARNT_L params PARNT_R'''
  global calling_function
  if len(parameter_stack) == par_limit_stack[-1][1]:
    schema.append(zs.quad("gosub", None, None, calling_function))
    par_limit_stack.pop()
    if len(par_limit_stack) > 0:
      calling_function = par_limit_stack[-1][0]
    else:
      calling_function = -1
  else:
    raise zs.ZenFunctionCallError(f"zen::cmp > incorrect number of parameters on call to {function_dir[calling_function][0]}.")
  auxfvar = "#" + p[1]
  for x in function_dir[0][5]:
    if x[0] == auxfvar:
      auxfvar = (x[2], x[1])
      operand_stack.append((x[2], x[1]))
      break
  if len(operator_stack) > 0:
    if operator_stack[-1] != 0:
      operand_stack.pop()
      mm = 1 if current_function == 0 else 0
      temp = mastermind[mm].alloc(auxfvar[1], "temporal")
      schema.append(zs.quad(0, auxfvar[0], None, temp))
      operand_stack.append((temp, auxfvar[1]))
  else:
    operand_stack.pop()
    mm = 1 if current_function == 0 else 0
    temp = mastermind[mm].alloc(auxfvar[1], "temporal")
    schema.append(zs.quad(0, auxfvar[0], None, temp))
    operand_stack.append((temp, auxfvar[1]))

def p_n1901(p):
  '''n1901 : '''
  i = 0
  for x in function_dir:
    if p[-1] == x[0]:
      if x[1] != -1:
        global calling_function
        calling_function = i
        schema.append(zs.quad("arx", None, None, i))
        par_limit_stack.append((calling_function, len(parameter_stack)))
        if len(function_dir[calling_function][4]) > 0:
          j = len(function_dir[calling_function][4])
          for y in reversed(function_dir[calling_function][4]):
            parameter_stack.append((y, j))
            j -= 1
      else:
        zs.ZenFunctionCallError(f"zen::cmp > function {p[-1]} is void and expected to return.")
    else:
      i += 1
  else:
    zs.ZenFunctionCallError(f"zen::cmp > function {p[-1]} is not defined.")

# Void function call
def p_vfunction(p):
  '''vfunction : ID n2001 PARNT_L params PARNT_R SMCLN'''
  global calling_function
  if len(parameter_stack) == par_limit_stack[-1][1]:
    schema.append(zs.quad("gosub", None, None, calling_function))
    par_limit_stack.pop()
    if len(par_limit_stack) > 0:
      calling_function = par_limit_stack[-1][0]
    else:
      calling_function = -1
  else:
    raise zs.ZenFunctionCallError(f"zen::cmp > incorrect number of parameters on call to {function_dir[calling_function][0]}.")

def p_n2001(p):
  '''n2001 : '''
  i = 0
  for x in function_dir:
    if p[-1] == x[0]:
      if x[1] == -1:
        global calling_function
        calling_function = i
        schema.append(zs.quad("arx", None, None, i))
        par_limit_stack.append((calling_function, len(parameter_stack)))
        if len(function_dir[calling_function][4]) > 0:
          j = len(function_dir[calling_function][4])
          for y in reversed(function_dir[calling_function][4]):
            parameter_stack.append((y, j))
            j -= 1
      else:
        zs.ZenFunctionCallError(f"zen::cmp > function {p[-1]} is not void.")
    else:
      i += 1
  else:
    zs.ZenFunctionCallError(f"zen::cmp > function {p[-1]} is not defined.")

# Arguments definition statement
def p_args(p):
  '''args : type ID n2101 auxp
          | '''
  pass

def p_n2101(p):
  '''n2101 : '''
  if function_def:
    function_dir[current_function][4].append(current_type)
    mm = 0 if current_function == 0 else 1
    addr = mastermind[mm].alloc(current_type, "variable")
    zenmind.update({addr: 1})
    function_dir[current_function][5].append((p[-1], current_type, addr))

def p_auxp(p):
  '''auxp : COMMA args auxp
          | '''
  pass

# Parameter definition statement
def p_params(p):
  '''params : expression n2201 auxq
            | '''
  pass

def p_n2201(p):
  '''n2201 : '''
  auxfvar = "#" + function_dir[calling_function][0]
  for x in function_dir[0][5]:
    if x[0] == auxfvar:
      auxfvar = x[2]
      break
  else: auxfvar = -1
  if auxfvar != operand_stack[-1][0]:
    par, ptype = operand_stack[-1]
    operand_stack.pop()
    if ptype == parameter_stack[-1][0]:
      schema.append(zs.quad("param", par, None, parameter_stack[-1][1]))
      parameter_stack.pop()
    else:
      raise zs.ZenFunctionCallError(f"zen::cmp > invalid parameter on call to {function_dir[calling_function][0]}.")

def p_auxq(p):
  '''auxq : COMMA expression n2201 auxq
          | '''
  pass

# Array, Matrix or Datatable direction
def p_direction(p):
  '''direction : ID BOX_L expression BOX_R
               | ID BOX_L expression COMMA expression BOX_R
               | ID COLON ID BOX_L expression BOX_R'''
  if p[4] == ']':
    for x in function_dir[current_function][5]:
      if p[1] == x[0]:
        if len(x) > 2:
          if len(x[3]) == 1:
            index, itype = operand_stack[-1]
            operand_stack.pop()
            if itype == 0:
              schema.append(zs.quad("check", index, 0, x[3][0]))
              mm = 0 if current_function == 0 else 1
              addr = mastermind[mm].alloc(0, "constant")
              temp = mastermind[mm].alloc(0, "temporal")
              zenmind.update({addr: x[2]})
              schema.append(zs.quad(1, index, addr, temp))
              operand_stack.append(("&"+str(temp), x[1]))
              break
            else: raise zs.ZenTypeMismatch("zen::cmp > cannot use non-integer index for list.")
          else: raise zs.ZenTypeMismatch(f"zen::cmp > {x[0]} is not a list.")
        else: raise zs.ZenSegmentationFault(f"zen::cmp > {x[0]} is not subscriptable.")
    else:
      if current_function != 0:
        for x in function_dir[0][5]:
          if p[1] == x[0]:
            if len(x) > 2:
              if len(x[3]) == 1:
                index, itype = operand_stack[-1]
                operand_stack.pop()
                if itype == 0:
                  schema.append(zs.quad("check", index, 0, x[3][0]))
                  mm = 0 if current_function == 0 else 1
                  addr = mastermind[mm].alloc(0, "constant")
                  temp = mastermind[mm].alloc(0, "temporal")
                  zenmind.update({addr: x[2]})
                  schema.append(zs.quad(1, index, addr, temp))
                  operand_stack.append(("&"+str(temp), x[1]))
                  break
                else: raise zs.ZenTypeMismatch("zen::cmp > cannot use non-integer index for list.")
              else: raise zs.ZenTypeMismatch(f"zen::cmp > {x[0]} is not a list.")
            else: raise zs.ZenSegmentationFault(f"zen::cmp > {x[0]} is not subscriptable.")
        else: raise zs.ZenUndefinedID(f"zen::cmp > '{p[-1]}' is never defined.")
      else: raise zs.ZenUndefinedID(f"zen::cmp > '{p[-1]}' is never defined.")
  elif p[4] == ',':
    for x in function_dir[current_function][5]:
      if p[1] == x[0]:
        if len(x) > 2:
          if len(x[3]) == 2:
            col, ctype = operand_stack[-1]
            operand_stack.pop()
            row, rtype = operand_stack[-1]
            operand_stack.pop()
            if ctype == 0 and rtype == 0:
              schema.append(zs.quad("check", row, 0, x[3][0]))
              mm = 0 if current_function == 0 else 1
              addr = mastermind[mm].alloc(0, "constant")
              temp = mastermind[mm].alloc(0, "temporal")
              zenmind.update({addr: x[3][1]})
              schema.append(zs.quad(3, row, addr, temp))
              schema.append(zs.quad("check", col, 0, x[3][1]))
              temp2 = mastermind[mm].alloc(0, "temporal")
              schema.append(zs.quad(1, temp, col, temp2))
              temp = mastermind[mm].alloc(0, "temporal")
              addr = mastermind[mm].alloc(0, "constant")
              zenmind.update({addr: x[2]})
              schema.append(zs.quad(1, temp2, addr, temp))
              operand_stack.append(("&"+str(temp), x[1]))
              break
            else: raise zs.ZenTypeMismatch("zen::cmp > cannot use non-integer index for list.")
          else: raise zs.ZenTypeMismatch(f"zen::cmp > {x[0]} is not a matrix.")
        else: raise zs.ZenSegmentationFault(f"zen::cmp > {x[0]} is not subscriptable.")
    else:
      if current_function != 0:
        for x in function_dir[0][5]:
          if p[1] == x[0]:
            if len(x) > 2:
              if len(x[3]) == 2:
                col, ctype = operand_stack[-1]
                operand_stack.pop()
                row, rtype = operand_stack[-1]
                operand_stack.pop()
                if ctype == 0 and rtype == 0:
                  schema.append(zs.quad("check", row, 0, x[3][0]))
                  mm = 0 if current_function == 0 else 1
                  addr = mastermind[mm].alloc(0, "constant")
                  temp = mastermind[mm].alloc(0, "temporal")
                  zenmind.update({addr: x[3][1]})
                  schema.append(zs.quad(3, row, addr, temp))
                  schema.append(zs.quad("check", col, 0, x[3][1]))
                  temp2 = mastermind[mm].alloc(0, "temporal")
                  schema.append(zs.quad(1, temp, col, temp2))
                  temp = mastermind[mm].alloc(0, "temporal")
                  addr = mastermind[mm].alloc(0, "constant")
                  zenmind.update({addr: x[2]})
                  schema.append(zs.quad(1, temp2, addr, temp))
                  operand_stack.append(("&"+str(temp), x[1]))
                  break
                else: raise zs.ZenTypeMismatch("zen::cmp > cannot use non-integer index for list.")
              else: raise zs.ZenTypeMismatch(f"zen::cmp > {x[0]} is not a matrix.")
            else: raise zs.ZenSegmentationFault(f"zen::cmp > {x[0]} is not subscriptable.")
        else: raise zs.ZenUndefinedID(f"zen::cmp > '{p[-1]}' is never defined.")
      else: raise zs.ZenUndefinedID(f"zen::cmp > '{p[-1]}' is never defined.")
  else:
    pass

# Arithmetic expression
def p_expression(p):
  '''expression : term n2401 PLUS n2402 expression
                | term n2401 NDASH n2402 expression
                | term n2401'''
  pass

def p_n2401(p):
  '''n2401 : '''
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
        zenmind.update({temp: 1})
        operand_stack.append((temp, otype))
      else:
        raise zs.ZenTypeMismatch(f"zen::cmp > type mismatch: can't operate {ltype} {operator} {rtype}")
      
def p_n2402(p):
  '''n2402 : '''
  if p[-1] == '+': operator_stack.append(1)
  elif p[-1] == '-': operator_stack.append(2)

# Arithmetic term
def p_term(p):
  '''term : base n2501 ASTRK n2502 term
          | base n2501 SLASH n2502 term
          | base n2501'''
  pass

def p_n2501(p):
  '''n2501 : '''
  if len(operator_stack) > 0:
    if operator_stack[-1] == 3 or operator_stack[-1] == 4:
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
        zenmind.update({temp: 1})
        operand_stack.append((temp, otype))
      else:
        raise zs.ZenTypeMismatch(f"zen::cmp > type mismatch: can't operate {ltype} {operator} {rtype}")
        
def p_n2502(p):
  '''n2502 : '''
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
      zenmind.update({temp: 1})
      schema.append(zs.quad(op, base, relation, temp))
    else:
      raise zs.ZenTypeMismatch(f"zen::cmp > type mismatch: can't operate {btype} {op} {rtype}")

# Arithmetic factor
def p_factor(p):
  '''factor : ID n2701
            | constant n2702
            | NDASH constant n2703
            | direction
            | function
            | datacalc
            | PARNT_L expression PARNT_R'''
  pass

def p_n2701(p):
  '''n2701 : '''
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

def p_n2702(p):
  '''n2702 : '''
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

def p_n2703(p):
  '''n2703 : '''
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

# Logical operator appearance
def p_logicop(p):
  '''logicop : AND
             | OR'''
  if p[1] == '||':
    operator_stack.append(zs.storef("or"))
  else: operator_stack.append(zs.storef("and"))

# Comparative operator appearance
def p_compop(p):
  '''compop : ANG_L n2901
            | ANG_R n2902
            | EQUAL
            | NEQUAL'''
  if len(p) == 2:
    operator_stack.append(zs.storef(p[1]))

def p_n2901(p):
  '''n2901 : EQUAL
           | '''
  if len(p) > 1:
    operator_stack.append(12)
  else: operator_stack.append(8)

def p_n2902(p):
  '''n2902 : EQUAL
           | '''
  if len(p) > 1:
    operator_stack.append(11)
  else: operator_stack.append(7)

# Datatable Row Definition
def p_dataset(p):
  '''dataset : WRITE IN ID BOX_L INTEGER BOX_R VALUES n3001 PARNT_L auxr auxs PARNT_R SMCLN'''
  for x in function_dir[current_function][5]:
    if p[3] == x[0]:
      if x[1] == 5:
        schema.append(zs.quad("chkrow", p[5], 0, x[3][0]))
        schema.append(zs.quad("chklen", tablecols, -1, x[3][1]))
        addr = []
        for i in range(tablecols):
          addr.append(operand_stack[-1])
          operand_stack.pop()
        mm = 0 if current_function == 0 else 1
        point = searchconst(mm, x[2]+p[5]*x[3][1])
        plus = searchconst(mm, 1)
        while addr:
          if addr[-1][0] != "pass":
            schema.append(zs.quad(0, addr[-1][0], None, point))
            addr.pop()
            next = searchconst(mm, zenmind[point]+1)
            if len(addr) > 0:
              schema.append(zs.quad(1, point, plus, next))
              point = next
          else:
            addr.pop()
      else:
        raise zs.ZenInvalidType(f"zen::cmp > variable {x[0]} is not a data table.")
  else:
    if current_function != 0:
      for x in function_dir[0][5]:
        if p[3] == x[0]:
          if x[1] == 5:
            schema.append(zs.quad("chkrow", p[5], 0, x[3][0]))
            schema.append(zs.quad("chklen", tablecols, -1, x[3][1]))
            addr = []
            for i in range(tablecols):
              addr.append(operand_stack[-1])
              operand_stack.pop()
            point = searchconst(0, x[2]+p[5]*x[3][1])
            plus = searchconst(0, 1)
            while addr:
              if addr[-1][0] != "pass":
                schema.append(zs.quad(0, addr[-1][0], None, point))
                addr.pop()
                next = searchconst(0, zenmind[point]+1)
                if len(addr) > 0:
                  schema.append(zs.quad(1, point, plus, next))
                  point = next
              else:
                addr.pop()
          else:
            raise zs.ZenInvalidType(f"zen::cmp > variable {p[3]} is not a data table.")
    else: 
      raise zs.ZenUndefinedID(f"zen::cmp > variable {p[3]} is not defined.")
        
def p_n3001(p):
  '''n3001 : '''
  global tablecols
  tablecols = 0

def p_auxr(p):
  '''auxr : expression
          | PASS'''
  global tablecols
  tablecols += 1
  if p[1] == r'pass':
    operand_stack.append(("pass",-1))

def p_auxs(p):
  '''auxs : COMMA auxr auxs
          | '''

def p_datacalc(p):
  '''datacalc : MAX PARNT_L ID COLON STRING PARNT_R
              | MIN PARNT_L ID COLON STRING PARNT_R
              | SUM PARNT_L ID COLON STRING PARNT_R
              | MEAN PARNT_L ID COLON STRING PARNT_R
              | VAR PARNT_L ID COLON STRING PARNT_R
              | SD PARNT_L ID COLON STRING PARNT_R
              | CORR PARNT_L ID COLON STRING COMMA STRING PARNT_R'''
  mm = 0 if current_function == 0 else 1
  temp = mastermind[mm].alloc(1, "temporal")
  for x in function_dir[current_function][5]:
    if p[3] == x[0]:
      if x[1] == 5:
        i = 0
        for y in x[4]:
          if str(p[5]) == y[0]:  
            if y[1] == 0 or y[1] == 1:
              if p[1] == r'MAX':
                schema.append(zs.quad("max", None, x[2], i))
                schema.append(zs.quad(0, special_addr, None, temp))
                operand_stack.append((temp, 1))
                return
              elif p[1] == r'MIN':
                schema.append(zs.quad("min", None, x[2], i))
                schema.append(zs.quad(0, special_addr, None, temp))
                operand_stack.append((temp, 1))
                return
              elif p[1] == r'SUM':
                schema.append(zs.quad("sum", None, x[2], i))
                schema.append(zs.quad(0, special_addr, None, temp))
                operand_stack.append((temp, 1))
                return
              elif p[1] == r'MEAN':
                schema.append(zs.quad("mean", None, x[2], i))
                schema.append(zs.quad(0, special_addr, None, temp))
                operand_stack.append((temp, 1))
                return
              elif p[1] == r'VAR':
                schema.append(zs.quad("var", None, x[2], i))
                schema.append(zs.quad(0, special_addr, None, temp))
                operand_stack.append((temp, 1))
                return
              elif p[1] == r'SDEV':
                schema.append(zs.quad("sdev", None, x[2], i))
                schema.append(zs.quad(0, special_addr, None, temp))
                operand_stack.append((temp, 1))
                return
              elif p[1] == r'CORR':
                j = 0
                for z in x[4]:
                  if str(p[7]) == z[0]:
                    if z[1] == 0 or z[1] == 1:
                      schema.append(zs.quad("corr", x[2], i, j))
                      schema.append(zs.quad(0, special_addr, None, temp))
                      operand_stack.append((temp, 1))
                      return
                    else: raise zs.ZenTypeMismatch(f"zen::cmp > column {p[7]} is not numerical.")
                  j += 1
                else: raise zs.ZenTypeMismatch(f"zen::cmp > data table has no column {p[7]}.")
            else: raise zs.ZenTypeMismatch(f"zen::cmp > column {p[5]} is not numerical.")
          i += 1
        else: raise zs.ZenUndefinedID(f"zen::cmp > data table has no column {p[5]}.")
      else: raise zs.ZenInvalidType(f"zen::cmp > variable {p[3]} is not a data table.")
  else: 
    if current_function != 0:
      for x in function_dir[0][5]:
        if p[3] == x[0]:
          if x[1] == 5:
            i = 0
            for y in x[4]:
              if p[5] == y[0]:  
                if y[1] == 0:
                  if p[1] == r'MAX':
                    schema.append(zs.quad("max", None, x[2], i))
                    schema.append(zs.quad(0, special_addr, None, temp))
                    operand_stack.append((temp, 1))
                    return
                  elif p[1] == r'MIN':
                    schema.append(zs.quad("min", None, x[2], i))
                    schema.append(zs.quad(0, special_addr, None, temp))
                    operand_stack.append((temp, 1))
                    return
                  elif p[1] == r'SUM':
                    schema.append(zs.quad("sum", None, x[2], i))
                    schema.append(zs.quad(0, special_addr, None, temp))
                    operand_stack.append((temp, 1))
                    return
                  elif p[1] == r'MEAN':
                    schema.append(zs.quad("mean", None, x[2], i))
                    schema.append(zs.quad(0, special_addr, None, temp))
                    operand_stack.append((temp, 1))
                    return
                  elif p[1] == r'VAR':
                    schema.append(zs.quad("var", None, x[2], i))
                    schema.append(zs.quad(0, special_addr, None, temp))
                    operand_stack.append((temp, 1))
                    return
                  elif p[1] == r'SDEV':
                    schema.append(zs.quad("sdev", None, x[2], i))
                    schema.append(zs.quad(0, special_addr, None, temp))
                    operand_stack.append((temp, 1))
                    return
                  elif p[1] == r'CORR':
                    j = 0
                    for z in x[4]:
                      if p[7] == z[0]:
                        if z[1] == 0:
                          schema.append(zs.quad("corr", 0, i, j))
                          schema.append(zs.quad(0, special_addr, None, temp))
                          operand_stack.append((temp, 1))
                          return
                        else: raise zs.ZenTypeMismatch(f"zen::cmp > column {p[7]} is not int.")
                      j += 1
                    else: raise zs.ZenTypeMismatch(f"zen::cmp > data table has no column {p[7]}.")
                else: raise zs.ZenTypeMismatch(f"zen::cmp > column {p[5]} is not int.")
              i += 1
            else: raise zs.ZenUndefinedID(f"zen::cmp > data table has no column {p[5]}.")
          else: raise zs.ZenInvalidType(f"zen::cmp > variable {p[3]} is not a data table.")
      else: raise zs.ZenUndefinedID(f"zen::cmp > variable {p[3]} is not defined.")
    else: raise zs.ZenUndefinedID(f"zen::cmp > variable {p[3]} is not defined.")

def p_datadist(p):
  '''datadist : NDIST FIT ID COLON STRING WITH PARNT_L expression COMMA expression PARNT_R SMCLN
              | BINOMIAL FIT ID COLON STRING WITH PARNT_L expression COMMA expression PARNT_R SMCLN'''
  for x in function_dir[current_function][5]:
    if p[3] == x[0]:
      if x[1] == 5:
        i = 0
        for y in x[4]:
          if str(p[5]) == y[0]:  
            if y[1] == 0 or y[1] == 1:
              if p[1] == r'ndist':
                stdev, sdtype = operand_stack[-1]
                operand_stack.pop()
                mean, mtype = operand_stack[-1]
                operand_stack.pop()
                if (mtype == 0 or mtype == 1) and (sdtype == 0 or sdtype == 1):
                  schema.append(zs.quad("prepare", mean, stdev, "ndist"))
                  schema.append(zs.quad("ndist", None, x[2], i))
                  return
                else: raise zs.ZenInvalidType("zen::cmp > call to normal distribution fitting requires numerical attributes.")
              elif p[1] == r'binomial':
                prob, ptype = operand_stack[-1]
                operand_stack.pop()
                tests, ttype = operand_stack[-1]
                operand_stack.pop()
                if (ttype == 0) and (ptype == 1):
                  schema.append(zs.quad("prepare", tests, prob, "binom"))
                  schema.append(zs.quad("binom", None, x[2], i))
                  return
                else: raise zs.ZenInvalidType("zen::cmp > call to binomial distribution fitting requires numerical attributes.")
            else: raise zs.ZenTypeMismatch(f"zen::cmp > column {p[5]} is not numerical.")
          i += 1
        else: raise zs.ZenUndefinedID(f"zen::cmp > data table has no column {p[5]}.")
      else: raise zs.ZenInvalidType(f"zen::cmp > variable {p[3]} is not a data table.")
  else:
    if current_function != 0:
      for x in function_dir[current_function][5]:
        if p[3] == x[0]:
          if x[1] == 5:
            i = 0
            for y in x[4]:
              if str(p[5]) == y[0]:
                if y[1] == 0 or y[1] == 1:
                  if p[1] == r'ndist':
                    stdev, sdtype = operand_stack[-1]
                    operand_stack.pop()
                    mean, mtype = operand_stack[-1]
                    operand_stack.pop()
                    if (mtype == 0 or mtype == 1) and (sdtype == 0 or sdtype == 1):
                      schema.append(zs.quad("prepare", mean, stdev, "ndist"))
                      schema.append(zs.quad("ndist", None, x[2], i))
                      return
                    else: raise zs.ZenInvalidType("zen::cmp > call to normal distribution fitting requires numerical attributes.")
                  elif p[1] == r'binomial':
                    prob, ptype = operand_stack[-1]
                    operand_stack.pop()
                    tests, ttype = operand_stack[-1]
                    operand_stack.pop()
                    if (ttype == 0) and (ptype == 1):
                      schema.append(zs.quad("prepare", tests, prob, "binom"))
                      schema.append(zs.quad("binom", None, x[2], i))
                      return
                    else: raise zs.ZenInvalidType("zen::cmp > call to binomial distribution fitting requires numerical attributes.")
                else: raise zs.ZenTypeMismatch(f"zen::cmp > column {p[5]} is not numerical.")
              i += 1
            else: raise zs.ZenUndefinedID(f"zen::cmp > data table has no column {p[5]}.")
          else: raise zs.ZenInvalidType(f"zen::cmp > variable {p[3]} is not a data table.")
      else: raise zs.ZenUndefinedID(f"zen::cmp > variable {p[3]} is not defined.")
    else: raise zs.ZenUndefinedID(f"zen::cmp > variable {p[3]} is not defined.")
      
# Main section
def p_mains(p):
  '''mains : MAIN BRACE_L n0001 vars statement auxl END n0002 BRACE_R'''
  pass

def p_n0001(p):
  '''n0001 : '''
  global current_function
  quad_update(jump_stack[-1], 3, len(schema))
  jump_stack.pop()
  function_dir.append(("main", None, len(schema), 0, None, [], None))
  current_function = len(function_dir) - 1

def p_n0002(p):
  '''n0002 : '''
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
  # ----------------------------------
  function_dir.clear()

# YACC required error function
def p_error(p):
  if p:
    if p.type != 'COMMENT':
      print(f"zen::grm > syntax error at token {p.type} ({p.value}) at line {p.lineno} : {p.lexpos}\n")
  else:
    print("zen::grm > syntax error: unexpected end of input")
  
# ---Parser-------------------------------------------------------
lexer = tokenizer()
parser = yacc.yacc()
# ----------------------------------------------------------------