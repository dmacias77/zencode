# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅] Lexicon
import zen.ply.lex as lex
import re

# Tokens Definition
tokens = (
  'AND', 'ANG_L', 'ANG_R', 'ASSIGN', 'ASTRK', 'BOOL',
  'BOX_L', 'BOX_R', 'BRACE_L', 'BRACE_R', 'CARET', 'CHAR',
  'CHARACTER', 'COLON', 'COMMA', 'CREAD', 'CWRITE', 'DATA',
  'DEC', 'DECIMAL', 'DO', 'ELSE', 'END', 'EQUAL', 'FALSE',
  'FUNCTION', 'ID', 'IF', 'IN', 'INT', 'INTEGER', 'LIST',
  'LOOP', 'MAIN', 'MATRIX', 'MODULO', 'NDASH', 'NEQUAL',
  'NULL', 'OR', 'PARNT_L', 'PARNT_R', 'PLUS', 'RANGE',
  'RETURN', 'SET', 'SLASH', 'SMCLN', 'STRING', 'TILDE',
  'TRUE', 'VOID', 'WHILE'
)

# Tokens' Regex Definition
t_AND = r'&&'
t_ANG_L = r'<'
t_ANG_R = r'>'
t_ASSIGN = r'<<'
t_ASTRK = r'\*'
t_BOOL = r'bool'
t_BOX_L = r'\['
t_BOX_R = r'\]'
t_BRACE_L = r'{'
t_BRACE_R = r'}'
t_CARET = r'\^'
t_CHAR = r'char'
t_COLON = r':'
t_COMMA = r','
t_CREAD = r'cread'
t_CWRITE = r'cwrite'
t_DATA = r'data'
t_DEC = r'dec'
t_DO = r'do'
t_ELSE = r'else'
t_END = r'end'
t_EQUAL = r'='
t_FALSE = r'False'
t_FUNCTION = r'function'
t_IF = r'if'
t_IN = r'in'
t_INT = r'int'
t_LIST = r'list'
t_LOOP = r'loop'
t_MAIN = r'main'
t_MATRIX = r'matrix'
t_MODULO = r'%'
t_NDASH = r'-'
t_NEQUAL = r'><'
t_NULL = r'Null'
t_OR = r'\|\|'
t_PARNT_L = r'\('
t_PARNT_R = r'\)'
t_PLUS = r'\+'
t_RANGE = r'range'
t_RETURN = r'return'
t_SET = r'set'
t_SLASH = r'/'
t_SMCLN = r';'
t_TILDE = r'~'
t_TRUE = r'True'
t_VOID = r'void'
t_WHILE = r'while'

t_ignore = ' \t'

# Reserved Words
reswords = {
  'bool': 'BOOL', 'char': 'CHAR',
  'cread': 'CREAD', 'cwrite': 'CWRITE', 'data': 'DATA',
  'dec': 'DEC', 'do': 'DO', 'else': 'ELSE', 'end': 'END',
  'endl': 'ENDL', 'False': 'FALSE', 'function': 'FUNCTION',
  'if': 'IF', 'in': 'IN', 'int': 'INT',
  'list': 'LIST', 'loop': 'LOOP', 'main': 'MAIN',
  'matrix': 'MATRIX', 'Null': 'NULL',
  'range': 'RANGE', 'return': 'RETURN', 'set': 'SET',
  'True': 'TRUE', 'void': 'VOID', 'while': 'WHILE',
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
  t.type = 'ID' if t.value not in reswords else t.value.upper()
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