# David Macías (1283419) & Hannia Ortega (1283410)
# ZENCODE [禅]
from zen.zenmaster import parser

def zazen(file):
  print("\n\n\n")
  zen_program = open(file, "r")
  parser.parse(zen_program.read())

def zenlogo():
  print("\n          *%@@        %(                                                                  ")
  print("     @@@@@@@@@            @@@/                                                            ")
  print("  /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                          ")
  print(" @@@@@@@@@@@@@/    .//.       @@@        _____________      _______        ____   ____    ")
  print("*@@@@@@@@@@@                  @@@@       @@@@@@@@@@@@%    .@@@@@@@@@@      @@@@,@@@@@@@@  ")
  print("@@@@@@@@@@@@@& /@@@@@@@     ,@@@@@              &@@@@    @@@@(    #@@@%    @@@@@@   &@@@@ ")
  print("@@@@@@@@@@@@@@@@@@@@@     .@@@@@@@            &@@@@.    /@@@@      @@@@    @@@@      @@@@.")
  print("@@@@@@@@@@@@@@@@@@#     (@@@@@@@@@          #@@@@,      %@@@@@@@@@@@@@@    @@@@      @@@@.")
  print("@@@@@@@@@@@@@&                 @@@        /@@@@/        ,@@@@              @@@@      @@@@.")
  print("&@@@@@@                       *@@@      .@@@@/..../&@@   #@@@@%    @@@     @@@@      @@@@,")
  print(" @@@@@@@&       ./@@@,===@@@@@@@@(      .@@@@@@@@@@@@&     #@@@@@@@@@/     @@@@      @@@@@")
  print("  @@@@@@@@@@@@@@@@@@.    @@@@@@@(                                                         ")
  print("   ,@@@@@@@@@@@@@@@@     @@@@@&                                                           ")
  print("       @@@@@@@@@@@@@     @@,                                                              \n\n")