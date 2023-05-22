# David Macías (1283419) & Hannia Ortega (1283410)
import argparse
import zen.code

parser = argparse.ArgumentParser(prog='zen', description="Zencode [禅] Compiler")
parser.add_argument('file', help='Zencode file to compile.')
parser.add_argument('-v', '--verbose', action='store_true', 
                   help='Print additional information.')
parser.add_argument('-sf', '--specs_file', metavar='file', 
                   help='Print additional information to the specified file.')

args = parser.parse_args()

zen.code.zazen(args.file, args.verbose, args.specs_file)