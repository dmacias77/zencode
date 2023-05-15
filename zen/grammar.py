# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅] Grammar
import ply.yacc as yacc
import zen.lexicon
import zen.semantics as zs

# ---Generate Zen Lexer-------------------------------------------
zenlx = zen.lexicon.tokenizer()

# ---Grammar Definitions & Semantics------------------------------

# Program
def p_program(p):
  '''program : auxa auxb vars auxc main'''
  zs.fd_init() # Initialization of Function Directory
  p_auxa(p[1])
  p_auxb(p[2])
  p_auxc(p[3])
  p_auxd(p[4])
  p_mains(p[5])

def p_auxa(p):
  '''auxa : imports auxa
          | empty'''
  if len(p) == 3:
    p_imports(p[1])
    p_auxa(p[2])

def p_auxb(p):
  '''auxb : customdef auxb
          | empty'''
  if len(p) == 3:
    p_customdef(p[1])
    p_auxb(p[2])

def p_auxc(p):
  '''auxc : functiondef auxc
          | empty'''
  if len(p) == 3:
    p_functiondef(p[1])
    p_auxc(p[2])

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
  if p[1][1] == "IF": p_conds(p[1])
  elif p[1][1] == "WHILE": p_whiles(p[1])
  elif p[1][1] == "DO": p_dowhiles(p[1])
  elif p[1][1] == "LOOP": p_loops(p[1])
  elif p[1][1] == "FOREACH": p_foreachs(p[1])
  elif p[1][1] == "SWITCH": p_switchs(p[1])
  elif p[1][1] == "NEXT" or p[1][1] == "BREAK" or p[1][1] == "RETURN":
    p_jumps(p[1])
  elif p[1][1] == "APPLY": p_applys(p[1])
  elif p[1][1] == "FOLDL" or p[1][1] == "FOLDR":
    p_folds(p[1])
  elif p[1][1] == "CREAD" or p[1][1] == "CWRITE":
    p_console(p[1])
  elif p[1][1] == "POUND": p_comment(p[1])
  elif p[1][2] == "ASSIGN": p_assign(p[1])
  else: p_funccall(p[1])

# Variable definition
def p_vars(p):
  '''vars : type var SMCLN vars
          | empty'''
  type = p_type(p[1])
  varq = p_var(p[2])

  #for i in varq:
  #  [insertar variable en tabla de variables de función actual]

# Type definition
def p_type(p):
  '''type : INT
          | CHAR
          | DEC
          | BOOL
          | TEXT
          | customkey'''
  if p[1] in zs.basic_types:
    p[0] = ('type', p[1])
  else:
    p_customkey(p)

# Custom variable name
def p_customkey(p):
  '''customkey : ID'''
  if p[1] not in zs.customReg:
    raise zs.ZenUndefinedID(f"zen::cmp > error: Undefined custom type {p[1]}.")
  else:
    p[0] = ('type', p[1])

# Variable naming
def p_var(p):
  '''var : auxd
         | auxf
         | auxh'''
  if p[1][1] == "LIST": p_auxf(p[1])
  elif p[1][1] == "MATRIX": p_auxh(p[1])
  else: p_auxd(p[1])

def p_auxd(p):
  '''auxd : ID auxe'''
  # Semantics

def p_auxe(p):
  '''auxe : COMMA ID auxe
          | empty'''
 # Semantics

def p_auxf(p):
  '''auxf : LIST ID BOX_L INTEGER BOX_R auxg'''
  # Semantics

def p_auxg(p):
  '''auxg : COMMA ID BOX_L INTEGER BOX_R auxg
          | empty'''
  # Semantics

def p_auxh(p):
  '''auxh : MATRIX ID BOX_L INTEGER COMMA INTEGER BOX_R auxi'''
  # Semantics

def p_auxi(p):
  '''auxi : COMMA ID BOX_L INTEGER COMMA INTEGER BOX_R auxi
          | empty'''
  # Semantics

# Assignation
def p_assign(p):
  '''assign : ID ASSIGN auxj auxk SMCLN'''
  # Semantics

def p_auxj(p):
  '''auxj : ID ASSIGN auxj
          | empty'''
  # Semantics

def p_auxk(p):
  '''auxk : ID
          | constant
          | expression'''
  p[0] = p[1]

# Conditional statement (if-else)
def p_conds(p):
  '''conds : IF condition auxl auxn'''
  if p[2]:
    p_auxl(p[3])       # Execute if-clause
  elif len(p) == 5:    # Check for an else-clause
    p_auxn(p[4])       # Execute else-clause

def p_auxl(p):
  '''auxl : statement
          | BRACE_L statement auxm BRACE_R'''
  if len(p) == 2:
    p_statement(p[1])
  elif len(p) == 4:
    p_statement(p[2])
    p_auxm(p[3])

def p_auxm(p):
  '''auxm : statement auxm
          | empty'''
  if len(p) == 3:
    p_statement(p[1])
    p_auxm(p[2])
  elif len(p) == 2: pass

def p_auxn(p):
  '''auxn : ELSE auxl
          | empty'''
  if len(p) == 3:
    p_auxl(p[2])
  elif len(p) == 2: pass

# Condition defining
def p_condition(p):
  '''condition : PARNT_L auxo comparison auxp PARNT_R'''
  # p[0] = evaluate("cond", p[2], p[3], p[4])

def p_auxo(p):
  '''auxo : TILDE
          | empty'''

def p_auxp(p):
  '''auxp : logicop auxo comparison auxp
          | empty'''
  # if len(p) == 5:
  #   p[0] = evaluate("logic", p[1], p[2], p[3], p[4])
  # elif len(p) == 2: pass

# Comparisons in condition
def p_comparison(p):
  '''comparison : auxk compop auxk'''
  # p[0] = evaluate("comp", p[1], p[2], p[3])

# While statement
def p_whiles(p):
  '''whiles : WHILE condition auxl'''
  # Semantics

# Do-while statement
def p_dowhiles(p):
  '''dowhiles : DO auxl WHILE condition'''
  # Semantics

# Loop statement
def p_loops(p):
  '''loops : LOOP ID auxq UNTIL condition auxl'''
  # Semantics

def p_auxq(p):
  '''auxq : BY expression
          | empty'''
  # Semantics

# Foreach statement
def p_foreachs(p):
  '''foreachs : FOREACH ID IN ID auxl'''
  # Semantics

# Switch statement
def p_switchs(p):
  '''switchs : SWITCH PARNT_L auxr PARNT_R BRACE_L cases auxs BRACE_R'''
  # Semantics

def p_auxr(p):
  '''auxr : ID
          | expression'''
  # Semantics

def p_auxs(p):
  '''auxs : cases auxs
          | empty'''
  # Semantics

# Case statement
def p_cases(p):
  '''cases : CASE COLON auxt BREAK SMCLN
           | DEFAULT COLON auxt BREAK SMCLN'''
  # Semantics

def p_auxt(p):
  '''auxt : statement auxt
          | empty'''
  # Semantics

# Jump statement (next/break/return)
def p_jumps(p):
  '''jumps : NEXT SMCLN
           | BREAK SMCLN
           | RETURN auxk SMCLN'''
  # Semantics

# Function call as statement
def p_funccall(p):
  '''funccall : function SMCLN'''
  # Semantics

# Function call as part of an expression
def p_function(p):
  '''function : auxu ID PARNT_L args PARNT_R'''
  # Semantics

def p_auxu(p):
  '''auxu : ID COLON
          | empty'''
  # Semantics

# HOF apply statement
def p_applys(p):
  '''applys : APPLY auxv INTO ID SMCLN'''
  # Semantics

def p_auxv(p):
  '''auxv : function
          | lambdacall'''
  # Semantics

# HOF fold statement
def p_folds(p):
  '''folds : FOLDL ID INTO ID USING auxv SMCLN
           | FOLDR ID INTO ID USING auxv SMCLN'''
  # Semantics

# Lambda function call
def p_lambdacall(p):
  '''lambdacall : LAMBDA PARNT_L args PARNT_R BRACE_L auxt RETURN auxk BRACE_R'''
  # Semantics

# Console interaction statement
def p_console(p):
  '''console : CREAD ASSIGN auxx auxw SMCLN
             | CWRITE ASSIGN auxx auxw SMCLN'''
  # Semantics

def p_auxw(p):
  '''auxw : ASSIGN auxx auxw
          | empty'''
  # Semantics

def p_auxx(p):
  '''auxx : ID
          | constant
          | expression
          | TAB
          | ENDL'''
  # Semantics

# Comment section delimitation statement
def p_comment(p):
  '''comment : POUND STRING POUND'''
  # Semantics

# Constant appearance
def p_constant(p):
  '''constant : "INTEGER"
              | "DECIMAL"
              | "CHARACTER"
              | "TRUE"
              | "FALSE"
              | "STRING"
              | "NULL"'''
  # Semantics

# Function definition    
def p_functiondef(p):
  '''functiondef : "FUNCTION" type "ID" "PARNT_L" args "PARNT_R" "BRACE_L" auxt "RETURN" auxk "BRACE_R"
                 | voidfdef'''
  # Semantics

# Void function definition
def p_voidfdef(p):
  '''voidfdef : "FUNCTION" "VOID" "ID" "PARNT_L" args "PARNT_R" "BRACE_L" statement auxt "BRACE_R"'''
  # Semantics

# Custom variable type definition
def p_customdef(p):
  '''customdef : "CUSTOM" "ID" "PARNT_L" auxy "PARNT_R" "SMCLN"'''
  # Semantics

def p_auxy(p):
  '''auxy : priv pub
          | pub priv'''
  # Semantics

# Private section of custom variable definition
def p_priv(p):
  '''priv : "PRIVATE" "COLON" structstat auxz
          | empty'''
  # Semantics

# Public section of custom variable definition
def p_pub(p):
  '''pub : "PUBLIC" "COLON" structstat auxz
         | empty'''
  # Semantics

def p_auxz(p):
  '''auxz : structstat auxz
           | empty'''
  # Semantics

# Custom variable's structure statement
def p_structstat(p):
  '''structstat : vars
                | functiondef
                | cnstrdef'''
  # Semantics

# Custom variable's constructor definition
def p_cnstrdef(p):
  '''cnstrdef : "CONSTR" "PARNT_L" args "PARNT_R" "BRACE_L" statement auxt "BRACE_R"'''
  # Semantics

# Arguments definition statement
def p_args(p):
  '''args : type var args
          | empty'''

# Arithmetic expression
def p_expression(p):
  '''expression : expression "PLUS" term
                | expression "NDASH" term
                | term'''
  if len(p) == 2:
    p[0] = p[1]
  elif p[2] == '+':
    p[0] = p[1] + p[3]
  elif p[2] == '-':
    p[0] = p[1] - p[3]

# Arithmetic term
def p_term(p):
  '''term : term "ASTRK" base
          | term "SLASH" base
          | base'''
  if len(p) == 2:
    p[0] = p[1]
  elif p[2] == '*':
    p[0] = p[1] * p[3]
  elif p[2] == '/':
    p[0] = p[1] / p[3]

# Numerical base
def p_base(p):
  '''base : factor "MODULO" factor
          | factor "CARET" factor
          | factor'''
  if len(p) == 2:
    p[0] = p[1]
  elif p[2] == '%':
    p[0] = p[1] % p[3]
  elif p[2] == '^':
    p[0] = p[1] ** p[3]

# Arithmetic factor
def p_factor(p):
  '''factor : constant
            | "PLUS" constant
            | "NDASH" constant
            | "PARNT_L" expression "PARNT_R"'''
  if len(p) == 2:
    p[0] = p[1]
  elif p[1] == '+':
    p[0] = p[2]
  elif p[1] == '-':
    p[0] = -p[2]
  elif p[1] == '(':
    p[0] = p[2]

# Logical operator appearance
def p_logicop(p):
  '''logicop : "AND"
             | "OR"
             | "TILDE"'''
  # Semantics

# Comparative operator appearance
def p_compop(p):
  '''compop : "ANG_L" auxaa
            | "ANG_R" auxaa
            | "EQUAL"
            | "NEQUAL"'''
  # Semantics

def p_auxaa(p):
  '''auxaa : "EQUAL"
           | empty'''
  # Semantics

# Main section
def p_mains(p):
  '''mains : "MAIN" "BRACE_L" vars statement auxt "END" "BRACE_R"'''
  # Semantics

# ---Parser-------------------------------------------------------
parser = yacc.yacc()
# ----------------------------------------------------------------