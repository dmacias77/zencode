# David Macías (1283419) & Hannia Ortega (1283410)
import zen.code

zen.code.zenlogo()
file = input("\nZen Beta-2 Compiler...\n\nFile: ")

if not file.endswith(".zen"):
  file += ".zen"

zen.code.zazen(file)