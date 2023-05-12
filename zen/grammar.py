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
  '''program : auxa auxb auxc auxd main'''
  # Semantics:

def p_auxa(p):
  '''auxa : imports auxa
          | empty'''
  # Semantics:

def p_auxb(p):
  '''auxb : customdef auxb
          | empty'''
  # Semantics:

def p_auxc(p):
  '''auxc : vars auxc
          | empty'''
  # Semantics:

def p_auxd(p):
  '''auxd : functiondef auxd
          | empty'''
  # Semantics:

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
  # Semantics

# Variable definition
def p_vars(p):
  '''vars : type var SMCLN'''
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
  '''var : auxe
         | auxg
         | auxi'''
  # Semantics

def p_auxe(p):
  '''auxe : ID auxf'''
  # Semantics

def p_auxf(p):
  '''auxf : COMMA ID auxf
          | empty'''
 # Semantics

def p_auxg(p):
  '''auxg : LIST ID BOX_L INTEGER BOX_R auxh'''
  # Semantics

def p_auxh(p):
  '''auxh : COMMA ID BOX_L INTEGER BOX_R auxh
          | empty'''
  # Semantics

def p_auxi(p):
  '''auxi : MATRIX ID BOX_L INTEGER COMMA INTEGER BOX_R auxj'''
  # Semantics

def p_auxj(p):
  '''auxj : COMMA ID BOX_L INTEGER COMMA INTEGER BOX_R auxj
          | empty'''
  # Semantics

# Assignation
def p_assign(p):
  '''assign : ID ASSIGN auxk auxl SMCLN'''
  # Semantics

def p_auxk(p):
  '''auxk : ID ASSIGN auxk
          | empty'''
  # Semantics

def p_auxl(p):
  '''auxl : ID
          | constant
          | expression'''
  # Semantics

# Conditional statement (if-else)
def p_conds(p):
  '''conds : IF condition auxm auxo'''
  # Semantics

def p_auxm(p):
  '''auxm : statement
          | BRACE_L statement auxn BRACE_R'''
  # Semantics

def p_auxn(p):
  '''auxn : statement auxn
          | empty'''
  # Semantics

def p_auxo(p):
  '''auxo : ELSE auxm
          | empty'''
  # Semantics

# Condition defining
def p_condition(p):
  '''condition : PARNT_L auxp comparison auxq PARNT_R'''
  # Semantics

def p_auxp(p):
  '''auxp : TILDE
          | empty'''
  # Semantics

def p_auxq(p):
  '''auxq : logicop auxp comparison auxq
          | empty'''
  # Semantics

# Comparisons in condition
def p_comparison(p):
  '''comparison : auxl compop auxl'''
  # Semantics

# While statement
def p_whiles(p):
  '''whiles : WHILE condition auxm'''
  # Semantics

# Do-while statement
def p_dowhiles(p):
  '''dowhiles : DO auxm WHILE condition'''
  # Semantics

# Loop statement
def p_loops(p):
  '''loops : LOOP ID auxr UNTIL condition auxm'''
  # Semantics

def p_auxr(p):
  '''auxr : BY expression
          | empty'''
  # Semantics

# Foreach statement
def p_foreachs(p):
  '''foreachs : FOREACH ID IN ID auxm'''
  # Semantics

# Switch statement
def p_switchs(p):
  '''switchs : SWITCH PARNT_L auxs PARNT_R BRACE_L cases auxt BRACE_R'''
  # Semantics

def p_auxs(p):
  '''auxs : ID
          | expression'''
  # Semantics

def p_auxt(p):
  '''auxt : cases auxt
          | empty'''
  # Semantics

# Case statement
def p_cases(p):
  '''cases : CASE COLON auxu BREAK SMCLN
           | DEFAULT COLON auxu BREAK SMCLN'''
  # Semantics

def p_auxu(p):
  '''auxu : statement auxu
          | empty'''
  # Semantics

# Jump statement (next/break/return)
def p_jumps(p):
  '''jumps : NEXT SMCLN
           | BREAK SMCLN
           | RETURN auxl SMCLN'''
  # Semantics

# Function call as statement
def p_funccall(p):
  '''funccall : function SMCLN'''
  # Semantics

# Function call as part of an expression
def p_function(p):
  '''function : auxv ID PARNT_L args PARNT_R'''
  # Semantics

def p_auxv(p):
  '''auxv : ID COLON
          | empty'''
  # Semantics

# HOF apply statement
def p_applys(p):
  '''applys : APPLY auxw INTO ID SMCLN'''
  # Semantics

def p_auxw(p):
  '''auxw : function
          | lambdacall'''
  # Semantics

# HOF fold statement
def p_folds(p):
  '''folds : FOLDL ID INTO ID USING auxw SMCLN
           | FOLDR ID INTO ID USING auxw SMCLN'''
  # Semantics

# Lambda function call
def p_lambdacall(p):
  '''lambdacall : LAMBDA PARNT_L args PARNT_R BRACE_L auxu RETURN auxl BRACE_R'''
  # Semantics

# Console interaction statement
def p_console(p):
  '''console : CREAD ASSIGN auxy auxx SMCLN
             | CWRITE ASSIGN auxy auxx SMCLN'''
  # Semantics

def p_auxx(p):
  '''auxx : ASSIGN auxy auxx
          | empty'''
  # Semantics

def p_auxy(p):
  '''auxy : ID
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
  '''functiondef : "FUNCTION" type "ID" "PARNT_L" args "PARNT_R" "BRACE_L" auxu "RETURN" auxl "BRACE_R"
                 | voidfdef'''
  # Semantics

# Void function definition
def p_voidfdef(p):
  '''voidfdef : "FUNCTION" "VOID" "ID" "PARNT_L" args "PARNT_R" "BRACE_L" statement auxu "BRACE_R"'''
  # Semantics

# Custom variable type definition
def p_customdef(p):
  '''customdef : "CUSTOM" "ID" "PARNT_L" auxz "PARNT_R" "SMCLN"'''
  # Semantics

def p_auxz(p):
  '''auxz : priv pub
          | pub priv'''
  # Semantics

# Private section of custom variable definition
def p_priv(p):
  '''priv : "PRIVATE" "COLON" structstat auxaa
          | empty'''
  # Semantics

# Public section of custom variable definition
def p_pub(p):
  '''pub : "PUBLIC" "COLON" structstat auxaa
         | empty'''
  # Semantics

def p_auxaa(p):
  '''auxaa : structstat auxaa
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
  '''cnstrdef : "CONSTR" "PARNT_L" args "PARNT_R" "BRACE_L" statement auxu "BRACE_R"'''
  # Semantics

# Arguments definition statement
def p_args(p):
  '''args : type var args
          | empty'''

# Arithmetic expression
def expression(p):
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
def term(p):
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
def base(p):
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
def factor(p):
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
def logicop(p):
  '''logicop : "AND"
             | "OR"
             | "TILDE"'''
  # Semantics

# Comparative operator appearance
def compop(p):
  '''compop : "ANG_L" auxab
            | "ANG_R" auxab
            | "EQUAL"
            | "NEQUAL"'''
  # Semantics

def auxab(p):
  '''auxab : "EQUAL"
           | empty'''
  # Semantics

# Main section
def mains(p):
  '''mains : "MAIN" "BRACE_L" vars statement auxu "END" "BRACE_R"'''
  # Semantics

# ---Parser-------------------------------------------------------
parser = yacc.yacc()
# ----------------------------------------------------------------