# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅] Lexicon
import zen.ply.lex as lex
import re

# Tokens Definition
tokens = (
  'AND', 'ANG_L', 'ANG_R', 'ASSIGN', 'ASTRK', 'BINOMIAL', 'BOOL',
  'BOX_L', 'BOX_R', 'BRACE_L', 'BRACE_R', 'CARET', 'CHAR',
  'CHARACTER', 'COLON', 'COMMA', 'CORR', 'CREAD', 'CREATE',
  'CWRITE', 'DATA', 'DEC', 'DECIMAL', 'DO', 'ELSE', 'END', 'EQUAL',
  'FALSE', 'FIT', 'FUNCTION', 'ID', 'IF', 'IN', 'INT', 'INTEGER',
  'LIST', 'LOOP', 'MAIN', 'MATRIX', 'MAX', 'MEAN', 'MIN', 'MODULO',
  'NDASH', 'NDIST', 'NEQUAL', 'NULL', 'OR', 'PARNT_L', 'PARNT_R',
  'PASS', 'PLUS', 'RANGE', 'RETURN', 'SD', 'SET', 'SLASH', 'SMCLN',
  'STRING', 'SUM', 'TEXT', 'TILDE', 'TRUE', 'VALUES', 'VAR', 'VOID',
  'WHILE', 'WITH', 'WRITE'
)

# Tokens' Regex Definition
t_AND = r'&&'
t_ANG_L = r'<'
t_ANG_R = r'>'
t_ASSIGN = r'<<'
t_ASTRK = r'\*'
t_BINOMIAL = r'binomial'
t_BOOL = r'bool'
t_BOX_L = r'\['
t_BOX_R = r'\]'
t_BRACE_L = r'{'
t_BRACE_R = r'}'
t_CARET = r'\^'
t_CHAR = r'char'
t_COLON = r':'
t_COMMA = r','
t_CORR = r'CORR'
t_CREAD = r'cread'
t_CREATE = r'create'
t_CWRITE = r'cwrite'
t_DATA = r'data'
t_DEC = r'dec'
t_DO = r'do'
t_ELSE = r'else'
t_END = r'end'
t_EQUAL = r'='
t_FALSE = r'False'
t_FIT = r'fit'
t_FUNCTION = r'function'
t_IF = r'if'
t_IN = r'in'
t_INT = r'int'
t_LIST = r'list'
t_LOOP = r'loop'
t_MAIN = r'main'
t_MATRIX = r'matrix'
t_MAX = r'MAX'
t_MEAN = r'MEAN'
t_MIN = r'MIN'
t_MODULO = r'%'
t_NDASH = r'-'
t_NDIST = r'ndist'
t_NEQUAL = r'><'
t_NULL = r'Null'
t_OR = r'\|\|'
t_PARNT_L = r'\('
t_PARNT_R = r'\)'
t_PASS = r'pass'
t_PLUS = r'\+'
t_RANGE = r'range'
t_RETURN = r'return'
t_SD = r'SDEV'
t_SET = r'set'
t_SLASH = r'/'
t_SMCLN = r';'
t_SUM = r'SUM'
t_TEXT = r'text'
t_TILDE = r'~'
t_TRUE = r'True'
t_VALUES = r'values'
t_VAR = r'VAR'
t_VOID = r'void'
t_WHILE = r'while'
t_WITH = r'with'
t_WRITE = r'write'

t_ignore = ' \t'

# Reserved Words
reserved_words = {
  'binomial': 'BINOMIAL', 'bool': 'BOOL', 'char': 'CHAR',
  'CORR': 'CORR', 'cread': 'CREAD', 'create': 'CREATE',
  'cwrite': 'CWRITE', 'data': 'DATA', 'dec': 'DEC', 'do': 'DO',
  'else': 'ELSE', 'end': 'END', 'False': 'FALSE', 'fit': 'FIT',
  'function': 'FUNCTION', 'if': 'IF', 'in': 'IN', 'int': 'INT',
  'list': 'LIST', 'loop': 'LOOP', 'main': 'MAIN',
  'matrix': 'MATRIX', 'MAX': 'MAX', 'MEAN': 'MEAN', 'MIN': 'MIN',
  'ndist': 'NDIST', 'Null': 'NULL', 'pass': 'PASS',
  'range': 'RANGE', 'return': 'RETURN', 'SDEV': 'SD', 'set': 'SET',
  'SUM': 'SUM', 'text': 'TEXT', 'True': 'TRUE', 'values': 'VALUES',
  'void': 'VOID', 'with': 'WITH', 'while': 'WHILE',
  'write': 'WRITE'
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

def t_ID(t):
  r'[a-z][a-zA-Z0-9_]*'
  t.type = 'ID' if t.value not in reserved_words else t.value.upper()
  return t

def t_DECIMAL(t):
  r'\d+\.\d+'
  t.value = float(t.value)
  return t

def t_INTEGER(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_STRING(t):
  r'"([^"\\]*(\\.[^"\\]*)*)"'
  t.value = re.sub(r'\\(.)', r'\1', t.value[1:-1])
  return t

# Lex Required Functions
def t_comment(t):
  r'\#.*?(?=\#|$)|\#.*'
  pass

def t_error(t):
  if not t.value[0].isspace():
    print(f"zen::lex > invalid character: '{t.value[0]}'")
  t.lexer.skip(1)

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

# ---Tokenizer----------------------------------------------------
def tokenizer():
  return lex.lex()
# ----------------------------------------------------------------