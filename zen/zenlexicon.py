# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅] Lexicon
import ply.lex as lex
import re

# Tokens Definition
tokens = (
  'AND', 'ANG_L', 'ANG_R', 'APPLY', 'AS', 'ASSIGN', 'ASTRK', 'BOOL',
  'BOX_L', 'BOX_R', 'BRACE_L', 'BRACE_R', 'BREAK', 'BY', 'CARET',
  'CASE', 'CHAR', 'CHARACTER', 'COLON', 'COMMA', 'CONSTR',
  'CREAD', 'CUSTOM', 'CWRITE', 'DEC', 'DECIMAL', 'DEFAULT', 'DO',
  'DOT', 'ELSE', 'END', 'ENDL', 'EQUAL', 'FALSE', 'FOLDL',
  'FOLDR', 'FOREACH', 'FUNCTION', 'ID', 'IF', 'IMPORT', 'IN',
  'INT', 'INTO', 'INTEGER', 'LAMBDA', 'LIST', 'LOOP', 'MAIN',
  'MATRIX', 'MODULO', 'NDASH', 'NEQUAL', 'NEXT', 'NULL', 'OR',
  'PARNT_L', 'PARNT_R', 'PLUS', 'POUND', 'PRIVATE', 'PUBLIC',
  'RETURN', 'SLASH', 'SMCLN', 'STRING', 'SWITCH', 'TAB', 'TILDE',
  'TRUE', 'UNTIL', 'USING', 'VOID', 'WHILE',
)

# Tokens' Regex Definition
t_AND = r'&&'
t_ANG_L = r'<'
t_ANG_R = r'>'
t_APPLY = r'apply'
t_AS = r'as'
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
t_POUND = r'\#'
t_PRIVATE = r'private'
t_PUBLIC = r'public'
t_RETURN = r'return'
t_SLASH = r'/'
t_SMCLN = r';'
t_SWITCH = r'switch'
t_TAB = r'tab'
t_TILDE = r'~'
t_TRUE = r'True'
t_UNTIL = r'until'
t_USING = r'using'
t_VOID = r'void'
t_WHILE = r'while'

# Reserved Words
reswords = {
  'and': 'AND', 'apply': 'APPLY', 'as': 'AS', 'bool': 'BOOL',
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
def t_error(t):
  print(f"zen::lex > invalid character: '{t.value[0]}'")
  t.lexer.skip(1)

# ---Tokenizer----------------------------------------------------
def tokenizer():
  return lex.lex()
# ----------------------------------------------------------------