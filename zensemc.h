#include <iostream>
using namespace std;

/* K   TYPE      OPERATION
----------------------------
   0   INT    ADDITION
   1   DEC    SUBTRACTION
   2   CHAR   MULTIPLICATION
   3   BOOL   DIVISION
   4          EXPONENTIATION
   5          MODULO
*/
// Enum variations:
const int tk = 4, ok = 6;
// Semantic prism:
bool zen_scube[tk][tk][ok] = {
  //  +, -, *, /, ^, %
  { { 1, 1, 1, 1, 1, 1 },   // int  -  int
    { 1, 1, 1, 1, 1, 0 },   //         dec
    { 1, 1, 0, 0, 0, 0 },   //         char
    { 1, 1, 1, 1, 0, 0 } }, //         bool
  { { 1, 1, 1, 1, 1, 0 },   // dec  -  int
    { 1, 1, 1, 1, 1, 0 },   //         dec
    { 0, 0, 0, 0, 0, 0 },   //         char
    { 1, 1, 1, 1, 0, 0 } }, //         bool
  { { 1, 1, 1, 1, 1, 0 },   // char -  int
    { 1, 1, 0, 0, 0, 0 },   //         dec
    { 1, 1, 0, 0, 0, 0 },   //         char
    { 0, 0, 0, 0, 0, 0 } }, //         bool
  { { 0, 0, 0, 0, 0, 0 },   // bool -  int
    { 0, 0, 0, 0, 0, 0 },   //         dec
    { 0, 0, 0, 0, 0, 0 },   //         char
    { 0, 0, 0, 0, 0, 1 } }, //         bool
};

unsigned interpret(string name, bool istype) {
  if (istype) {
    if (name == "int") return 1;
    if (name == "dec") return 2;
    if (name == "char") return 3;
    if (name == "bool") return 4;
  } else {
    if (name.substr(0,3) == "add") return 1;
    if (name.substr(0,3) == "sub") return 2;
    if (name.substr(0,4) == "mult") return 3;
    if (name.substr(0,3) == "div") return 4;
    if (name.substr(0,3) == "exp") return 5;
    if (name.substr(0,3) == "mod") return 6;
  }
  return 0;
}

bool zsc_check(string left_type, string right_type, string operation) {
  unsigned ult, uop, urt;

  ult = interpret(left_type, 1);
  urt = interpret(right_type, 1);
  uop = interpret(operation, 0);

  try {
    if (ult < 1) throw(1);
    if (urt < 1) throw(2);
    if (uop < 1) throw(3);
    return zen_scube[ult-1][urt-1][uop-1];
  }
  catch (unsigned field) {
    cerr << "Error: On call to bool zsc_check: Couldn't interpret field " << field << endl;
    abort();
  }
}

bool zsc_check(unsigned left_type, unsigned right_type, unsigned operation) {
  try {
    if (left_type < 0 || left_type >= tk) throw(1);
    if (right_type < 0 || right_type >= tk) throw(2);
    if (operation < 0 || operation >= ok) throw(3);
    return zen_scube[left_type][right_type][operation];
  }
  catch (unsigned field) {
    cerr << "Error: On call to bool zsc_check: Couldn't interpret field " << field << endl;
    abort();
  }
}