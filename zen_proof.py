# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅]
import ply.lex as lex
import ply.yacc as parse
import re

# --Zencode Lexicon-----------------------------------------------
# Tokens Definition
tokens = (
  'AND', 'ANG_L', 'ANG_R', 'APPLY', 'ASSIGN', 'ASTRK', 'BOOL',
  'BOX_L', 'BOX_R', 'BRACE_L', 'BRACE_R', 'BREAK', 'BY', 'CARET',
  'CASE', 'CHAR', 'CHARACTER', 'COLON', 'COMMA', 'CONSTR',
  'CREAD', 'CUSTOM', 'CWRITE', 'DEC', 'DECIMAL', 'DEFAULT', 'DO',
  'DOT', 'ELSE', 'END', 'ENDL', 'EQUAL', 'FALSE', 'FOLDL',
  'FOLDR', 'FOREACH', 'FUNCTION', 'ID', 'IF', 'IMPORT', 'IN',
  'INT', 'INTO', 'INTEGER', 'LAMBDA', 'LIST', 'LOOP', 'MAIN',
  'MATRIX', 'MODULO', 'NDASH', 'NEQUAL', 'NEXT', 'NULL', 'OR',
  'PARNT_L', 'PARNT_R', 'PLUS', 'POUND', 'PRIVATE', 'PUBLIC',
  'RETURN', 'SLASH', 'SMCLN', 'STRING', 'SWITCH', 'TAB', 'TEXT',
  'TILDE', 'TRUE', 'UNTIL', 'USING', 'VOID', 'WHILE',
)

# Tokens' Regex Definition
t_AND = r'&&'
t_ANG_L = r'<'
t_ANG_R = r'>'
t_APPLY = r'apply'
t_ASSIGN = r'<<'
t_ASTRK = r'\*'
t_BOOL = r'bool'
t_BOX_L = r'\['
t_BOX_R = r'\]'
t_BRACE_L = r'{'
t_BRACE_R = r'}'
t_BREAK = r'break'
t_BY = r'by'
t_CARET = r'\^'
t_CASE = r'case'
t_CHAR = r'char'
t_COLON = r':'
t_COMMA = r','
t_CONSTR = r'constructor'
t_CREAD = r'cread'
t_CUSTOM = r'custom'
t_CWRITE = r'cwrite'
t_DEC = r'dec'
t_DEFAULT = r'default'
t_DO = r'do'
t_DOT = r'\.'
t_ELSE = r'else'
t_END = r'end'
t_ENDL = r'endl'
t_EQUAL = r'='
t_FALSE = r'False'
t_FOLDL = r'foldleft'
t_FOLDR = r'foldright'
t_FOREACH = r'foreach'
t_FUNCTION = r'function'
t_IF = r'if'
t_IMPORT = r'import'
t_IN = r'in'
t_INT = r'int'
t_INTO = r'into'
t_LAMBDA = r'lambda'
t_LIST = r'list'
t_LOOP = r'loop'
t_MAIN = r'main'
t_MATRIX = r'matrix'
t_MODULO = r'%'
t_NDASH = r'-'
t_NEQUAL = r'><'
t_NEXT = r'next'
t_NULL = r'Null'
t_OR = r'\|\|'
t_PARNT_L = r'\('
t_PARNT_R = r'\)'
t_PLUS = r'\+'
t_POUND = r'#'
t_PRIVATE = r'private'
t_PUBLIC = r'public'
t_RETURN = r'return'
t_SLASH = r'/'
t_SMCLN = r';'
t_SWITCH = r'switch'
t_TAB = r'tab'
t_TEXT = r'text'
t_TILDE = r'~'
t_TRUE = r'True'
t_UNTIL = r'until'
t_USING = r'using'
t_VOID = r'void'
t_WHILE = r'while'

# Reserved Words
reswords = {
  'and': 'AND', 'apply': 'APPLY', 'bool': 'BOOL',
  'break': 'BREAK', 'by': 'BY', 'case': 'CASE', 'char': 'CHAR',
  'constructor': 'CONSTR', 'cread': 'CREAD', 'custom': 'CUSTOM',
  'cwrite': 'CWRITE', 'dec': 'DEC', 'default': 'DEFAULT',
  'do': 'DO', 'else': 'ELSE', 'end': 'END', 'endl': 'ENDL',
  'False': 'FALSE', 'foldleft': 'FOLDL', 'foldright': 'FOLDR',
  'foreach': 'FOREACH', 'function': 'FUNCTION', 'if': 'IF',
  'import': 'IMPORT', 'in': 'IN', 'int': 'INT', 'into': 'INTO',
  'lambda': 'LAMBDA', 'list': 'LIST', 'loop': 'LOOP',
  'main': 'MAIN', 'matrix': 'MATRIX', 'next': 'NEXT',
  'Null': 'NULL', 'private': 'PRIVATE', 'public': 'PUBLIC',
  'return': 'RETURN', 'switch': 'SWITCH', 'tab': 'TAB',
  'text': 'TEXT', 'True': 'TRUE', 'until': 'UNTIL',
  'using': 'USING', 'void': 'VOID', 'while': 'WHILE',
}

# Special Tokens' Regex Definition
def t_CHARACTER(t):
    r"'(\\'|\\\\|\\\"|\\\\\\\\|\\n|\\t|[^'\\\\\\n\\t\\\"])'"
    t.value = t.value[1:-1]
    if t.value == r"\'":
        t.value = "'"
    elif t.value == r'\"':
        t.value = '"'
    elif t.value == r"\\":
        t.value = "\\"
    elif t.value == r"\\n":
        t.value = "\n"
    elif t.value == r"\\t":
        t.value = "\t"
    return t

def t_DECIMAL(t):
  r'\d+(\.\d+)?'
  t.value = float(t.value)
  return t

def t_ID(t):
  r'[a-z][a-zA-Z0-9_]*'
  t.type = 'ID' if t.value not in reswords else t.value.upper()
  return t

def t_INTEGER(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_STRING(t):
  r'"([^"\\]*(\\.[^"\\]*)*)"'
  t.value = re.sub(r'\\(.)', r'\1', t.value[1:-1])
  return t

# Error Definition
def t_ERROR(t):
  print(f"zen::lex > invalid character: '{t.value[0]}'")
  t.lexer.skip(1)

# Tokenizer
lexer = lex.lex()
# ----------------------------------------------------------------
# --ZenCode Grammar & Semantics-----------------------------------

# Program
def p_program(p):
  '''program : auxa auxb auxc auxd main'''
  # Semantics:

def p_auxa(p):
  '''auxa : imports
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
  # Semantics

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
    # Do something.

# Define the type rule.
def p_type(p):
  '''type : INT
          | CHAR
          | DEC
          | BOOL
          | TEXT
          | customkey'''
  # Semantics

# Custom variable name
def p_customkey(p):
  '''customkey : ID'''
  # Semantics

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
  # Do something.

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

parser = yacc.yacc()
# ----------------------------------------------------------------