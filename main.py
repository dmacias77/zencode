# David Macías (1283419)
import zen.code

zen.code.zenlogo()
file = input("\nZen Compiler...\n\nFile: ")

if not file.endswith(".zen"):
  file += ".zen"

zen.code.zazen(file)