# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅] Grammar and Semantics
import ply.yacc as yacc

from zenlexicon import tokens, tokenizer
import zensemantics as zs

# ---Directories--------------------------------------------------
function_dir = []
custom_dir = []

# ---Pins---------------------------------------------------------
const_temporal = None
current_function = 0
current_type = -1
temps = -1

# ---Generate Functional Stacks-----------------------------------
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
  schema.append(zs.to_quad("goto",None,None,None))
  jump_stack.append(len(schema)-1)
  function_dir.append(("#", None, 0, 0, None, [], []))

def p_auxa(p):
  '''auxa : imports auxa
          | empty'''
  pass

def p_auxb(p):
  '''auxb : customdef auxb
          | empty'''
  pass

def p_auxc(p):
  '''auxc : functiondef auxc
          | empty'''
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
               | console
               | comment'''
  pass

# Variable definition
def p_vars(p):
  '''vars : type var SMCLN vars
          | empty'''
  pass

# Type definition
def p_type(p):
  '''type : INT
          | CHAR
          | DEC
          | BOOL
          | customkey'''
  global current_type
  if p[-1] == r'int':
    current_type = 0
  elif p[-1] == r'dec':
    current_type = 1
  elif p[-1] == r'char':
    current_type = 2
  elif p[-1] == r'bool':
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
  for x in function_dir[current_function][6]:
    if x[0] == p[1]:
      raise zs.ZenRedefinedID(f"zen::cmp > {p[1]} is already defined.")
      break
  else:
    function_dir[current_function][6].append((p[1], current_type))

def p_auxe(p):
  '''auxe : COMMA ID auxe
          | empty'''
  if len(p) > 2:
    for x in function_dir[current_function][6]:
      if x[0] == p[2]:
        raise zs.ZenRedefinedVariable(f"zen::cmp > {p[2]} is already defined.")
        break
    else:
      function_dir[current_function][6].append((p[2], current_type))

def p_auxf(p):
  '''auxf : LIST ID BOX_L INTEGER BOX_R auxg'''
  pass

def p_auxg(p):
  '''auxg : COMMA ID BOX_L INTEGER BOX_R auxg
          | empty'''
  pass

def p_auxh(p):
  '''auxh : MATRIX ID BOX_L INTEGER COMMA INTEGER BOX_R auxi'''
  pass

def p_auxi(p):
  '''auxi : COMMA ID BOX_L INTEGER COMMA INTEGER BOX_R auxi
          | empty'''
  pass

# Assignation
def p_assign(p):
  '''assign : ID ASSIGN auxj auxk SMCLN'''
  pass

def p_auxj(p):
  '''auxj : ID ASSIGN auxj
          | empty'''
  pass

def p_auxk(p):
  '''auxk : ID
          | constant
          | expression'''
  pass

# Conditional statement (if-else)
def p_conds(p):
  '''conds : IF condition n0901 auxl auxn'''
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
    schema.append(zs.to_quad("goto-f", cond, None, None))
    jump_stack.append(len(schema)-1)

def p_auxl(p):
  '''auxl : statement n6101
          | BRACE_L statement auxm BRACE_R n6101'''
  pass

def p_n6101(p):
  '''n6101 : '''
  schema[jump_stack[-1]][3] = len(schema)
  jump_stack.pop()

def p_auxm(p):
  '''auxm : statement auxm
          | empty'''
  pass

def p_auxn(p):
  '''auxn : ELSE n6301 auxl
          | empty'''
  pass

def p_n6301(p):
  '''n6301 : '''
  schema.append(zs.to_quad("goto", None, None, None))
  schema[jump_stack[-1]][3] = len(schema)
  jump_stack.pop()
  jump_stack.append(len(schema)-1)

# Condition defining
def p_condition(p):
  '''condition : PARNT_L auxo comparison auxp PARNT_R'''
  pass

def p_auxo(p):
  '''auxo : TILDE
          | empty'''
  pass

def p_auxp(p):
  '''auxp : logicop auxo comparison auxp
          | empty'''
  pass

# Comparisons in condition
def p_comparison(p):
  '''comparison : auxk compop auxk'''
  pass

# While statement
def p_whiles(p):
  '''whiles : WHILE n1201 condition n1202 auxl n1203'''
  pass

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
    schema.append(zs.to_quad("goto-f", cond, None, None))
    jump_stack.append(len(schema)-1)

def p_n1203(p):
  '''n1203 : '''
  temp = jump_stack[-1]
  jump_stack.pop()
  schema.append(zs.to_quad("goto", None, None, jump_stack[-1]))
  jump_stack.pop()
  schema[temp][3] = len(schema)

# Do-while statement
def p_dowhiles(p):
  '''dowhiles : DO n1301 auxl WHILE condition n1302'''
  pass

def p_n1301(p):
  '''n1301 : '''
  jump_stack.append(len(schema))

def p_n1302(p):
  '''n1302 : '''
  cond, ctype = operand_stack[-1]
  operand_stack.pop()
  if ctype != 3:
    if ctype > 3: wrong_type = custom_dir[ctype-4][0]
    elif ctype == 2: wrong_type = "char"
    elif ctype == 1: wrong_type = "dec"
    elif ctype == 0: wrong_type = "int"
    raise zs.ZenTypeMismatch(f"zen::cmp > do-while-statement expected boolean, received {wrong_type}")
  else:
    schema.append(zs.to_quad("goto-t", cond, None, jump_stack[-1]))
    jump_stack.pop()

# Loop statement
def p_loops(p):
  '''loops : LOOP ID n1401 auxq UNTIL condition auxl'''
  pass

def p_n1401(p):
  '''n1401 : '''
  if current_function != 0:
    for x in function_dir[current_function][6]:
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
    for x in function_dir[0][6]:
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

def p_auxq(p):
  '''auxq : BY expression
          | empty'''
  pass

# Foreach statement
def p_foreachs(p):
  '''foreachs : FOREACH AS ID IN ID auxl'''
  pass

# Switch statement
def p_switchs(p):
  '''switchs : SWITCH PARNT_L auxr PARNT_R BRACE_L cases auxs BRACE_R'''
  pass

def p_auxr(p):
  '''auxr : ID
          | expression'''
  pass

def p_auxs(p):
  '''auxs : cases auxs
          | empty'''
  pass

# Case statement
def p_cases(p):
  '''cases : CASE COLON auxt BREAK SMCLN
           | DEFAULT COLON auxt BREAK SMCLN'''
  pass

def p_auxt(p):
  '''auxt : statement auxt
          | empty'''
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
  '''function : auxu ID PARNT_L args PARNT_R'''
  pass

def p_auxu(p):
  '''auxu : ID DOT
          | empty'''
  pass

# HOF apply statement
def p_applys(p):
  '''applys : APPLY auxv INTO ID SMCLN'''
  pass

def p_auxv(p):
  '''auxv : function
          | lambdacall'''
  pass

# HOF fold statement
def p_folds(p):
  '''folds : FOLDL ID INTO ID USING auxv SMCLN
           | FOLDR ID INTO ID USING auxv SMCLN'''
  pass

# Lambda function call
def p_lambdacall(p):
  '''lambdacall : LAMBDA PARNT_L args PARNT_R BRACE_L vars auxt RETURN auxk BRACE_R'''
  pass

# Console interaction statement
def p_console(p):
  '''console : CREAD ASSIGN auxx auxw SMCLN
             | CWRITE ASSIGN auxx auxw SMCLN'''
  pass

def p_auxw(p):
  '''auxw : ASSIGN auxx auxw
          | empty'''
  pass

def p_auxx(p):
  '''auxx : ID
          | constant
          | expression
          | TAB
          | ENDL'''
  pass

# Comment section delimitation statement
def p_comment(p):
  '''comment : POUND STRING POUND'''
  pass

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
  if type(p[-1]) is int: this_type = 0
  elif type(p[-1]) is float: this_type = 1
  elif type(p[-1]) is str and len(p[-1]) == 1: this_type = 2
  elif type(p[-1]) is bool: this_type = 3
  else: this_type = -1
  const_temporal = (p[-1], this_type)

# Function definition    
def p_functiondef(p):
  '''functiondef : FUNCTION type ID n2701 PARNT_L args PARNT_R BRACE_L auxt RETURN auxk BRACE_R n2702
                 | voidfdef'''
  pass

def p_n2701(p):
  '''n2701 : '''
  global current_function, temps
  temps = 0
  for x in function_dir:
    if x[0] == p[-1]:
      raise zs.ZenRedefinedID(f"zen::cmp > a function named {p[-1]} is already defined.")
      break
  else:
    function_dir.append((p[-1], current_type, len(schema) + 1, "", current_function, [], []))
    function_dir[0][6].append((f"zf#{p[-1]}", current_type))
    current_function = len(function_dir) - 1

def p_n2702(p):
  '''n2702 : '''
  function_dir[current_function][6].clear()

# Void function definition
def p_voidfdef(p):
  '''voidfdef : FUNCTION VOID ID n2801 PARNT_L args PARNT_R BRACE_L vars statement auxt BRACE_R n2802'''
  pass

def p_n2801(p):
  '''n2801 : '''
  global current_function, current_type, temps
  current_type = -1
  temps = 0
  for x in function_dir:
    if x[0] == p[-1]:
      raise zs.ZenRedefinedID(f"zen::cmp > a function named {p[-1]} is already defined.")
      break
  else:
    function_dir.append((p[-1], -1, len(schema) + 1, (0,0,0,0,0,0,0,0), current_function, [], []))
    current_function = len(function_dir) - 1

def p_n2802(p):
  '''n2802 : '''
  function_dir[current_function][6].clear()

# Custom variable type definition
def p_customdef(p):
  '''customdef : CUSTOM ID n2901 PARNT_L auxy PARNT_R SMCLN n2902'''
  pass

def p_n2901(p):
  '''n2901 : '''
  pass

def p_n2902(p):
  '''n2902 : '''
  pass

def p_auxy(p):
  '''auxy : priv pub
          | pub priv'''
  pass

# Private section of custom variable definition
def p_priv(p):
  '''priv : PRIVATE COLON structstat auxz
          | empty'''
  pass

# Public section of custom variable definition
def p_pub(p):
  '''pub : PUBLIC COLON structstat auxz
         | empty'''
  pass

def p_auxz(p):
  '''auxz : structstat auxz
          | empty'''
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
  '''args : type var n3401 args
          | empty'''
  pass

def p_n3401(p):
  '''n3401 : '''
  function_dir[current_function][5].append(current_type)

# Arithmetic expression
def p_expression(p):
  '''expression : expression n3501 PLUS n3502 term
                | expression n3501 NDASH n3502 term
                | term'''
  pass

def p_n3501(p):
  '''n3501 : '''
  if operator_stack[-1] == '+' or operator_stack[-1] == '-':
    right, rtype = operand_stack[-1]
    operand_stack.pop()
    left, ltype = operand_stack[-1]
    operand_stack.pop()
    operator = operator_stack[-1]
    operator_stack.pop()

    otype = zs.check_compatible(ltype, operator, rtype)
    if otype != -1:
      if current_function != 0:
        function_dir[current_function][3][4+otype] += 1
        # Memory handling function for temporals:
        # schema.append(zs.to_quad(len(schema)+1,operator,left,right,None))
        # operand_stack.push((..., otype))
      else:
        function_dir[0][3] += 1
        # Memory handling function for temporals:
        # schema.append(zs.to_quad(len(schema)+1,operator,left,right,None))
        # operand_stack.push((..., otype))
    else:
      raise zs.ZenTypeMismatch(f"zen::cmp > type mismatch: can't operate {ltype} {operator} {rtype}")
      
def p_n3502(p):
  '''n3502 : '''
  if p[-1] == '+': operator_stack.push(1)
  elif p[-1] == '-': operator_stack.push(2)

# Arithmetic term
def p_term(p):
  '''term : term n3601 ASTRK n3602 base
          | term n3601 SLASH n3602 base
          | base'''
  pass

def p_n3601(p):
  '''n3601 : '''
  if operator_stack[-1] == '*' or operator_stack[-1] == '/':
    right, rtype = operand_stack[-1]
    operand_stack.pop()
    left, ltype = operand_stack[-1]
    operand_stack.pop()
    operator = operator_stack[-1]
    operator_stack.pop()

    otype = zs.check_compatible(ltype, operator, rtype)
    if otype != -1:
      if current_function != 0:
        function_dir[current_function][3][4+otype] += 1
        # Memory handling function for temporals:
        # schema.append(zs.to_quad(len(schema)+1,operator,left,right,None))
        # operand_stack.push((..., otype))
      else:
        function_dir[0][3] += 1
        # Memory handling function for temporals:
        # schema.append(zs.to_quad(len(schema)+1,operator,left,right,None))
        # operand_stack.push((..., otype))
    else:
      raise zs.ZenTypeMismatch(f"zen::cmp > type mismatch: can't operate {ltype} {operator} {rtype}")
      
def p_n3602(p):
  '''n3602 : '''
  if p[-1] == '*': operator_stack.push(3)
  elif p[-1] == '/': operator_stack.push(4)

# Numerical base
def p_base(p):
  '''base : factor MODULO n3701 factor
          | factor CARET n3701 factor
          | factor'''
  pass

def p_n3701(p):
  '''n3701 : '''
  if p[-1] == '%': operator_stack.push(5)
  elif p[-1] == '^': operator_stack.push(6)

# Arithmetic factor
def p_factor(p):
  '''factor : ID n3801
            | constant n3802
            | NDASH constant n3803
            | funccall
            | PARNT_L expression PARNT_R'''
  pass

def p_n3801(p):
  '''n3801 : '''
  for x in function_dir[current_function][6]:
    if p[-1] == x[0]:
      operand_stack.append((x[0], x[1]))
      break
  else:
    if current_function != 0:
      for x in function_dir[0][6]:
        if p[-1] == x[0]:
          operand_stack.append((x[0], x[1]))
        break
      else:
        raise zs.ZenUndefinedID(f"zen::cmp > {p[-1]} is never defined.")
    else:
      raise zs.ZenUndefinedID(f"zen::cmp > {p[-1]} is never defined.")

def p_n3802(p):
  '''n3802 : '''
  operand_stack.append(const_temporal)

def p_n3803(p):
  '''n3803 : '''
  global const_temporal
  const_temporal[0] = -(const_temporal[0])
  operand_stack.append(const_temporal)

# Logical operator appearance
def p_logicop(p):
  '''logicop : AND
             | OR
             | TILDE'''
  pass

# Comparative operator appearance
def p_compop(p):
  '''compop : ANG_L auxaa
            | ANG_R auxaa
            | EQUAL
            | NEQUAL'''
  pass

def p_auxaa(p):
  '''auxaa : EQUAL
           | empty'''
  pass

# Main section
def p_mains(p):
  '''mains : MAIN BRACE_L vars statement auxt END n4101 BRACE_R'''
  pass

def p_n4101(p):
  '''n4101 : '''
  function_dir.clear()

# YACC required functions
def p_empty(p):
  '''empty : '''
  pass

def p_error(p):
  if p:
    print(f"zen::grm > syntax error at token {p.type} ({p.value}) at line {p.lineno} : {p.lexpos}")
  else:
    print("zen::grm > syntax error: unexpected end of input")
  pass

# ---Parser-------------------------------------------------------
lexer = tokenizer()
parser = yacc.yacc(start = 'program')
# ----------------------------------------------------------------
print("Compiled lexicon and grammar.")