# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅]
from zengrammar import parser

def zazen(file, verbose=False, specs_file=None):
  outfile = None

  if verbose: print(f"{file} zazen:\n")
  if specs_file:
    if specs_file.endswith('.txt'):
      outfile = specs_file
    else:
      outfile = f"{file[:-4]}_zazen_info.txt"

    with open(outfile, 'w') as of:
      of.write(f"{file[:-4].title()} Compilation Info")

  parser.parse(file)