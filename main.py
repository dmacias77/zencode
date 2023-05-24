# David Macías (1283419) & Hannia Ortega (1283410)
import zen.code

args = input("Zen Beta Compiler...\n\nFile: ")

if not args.endswith(".zen"):
  args += ".zen"

zen.code.zazen(args, False, False)