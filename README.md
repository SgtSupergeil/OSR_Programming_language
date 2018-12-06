# OSR_Programming_language

OSR stands for "Only six registers!" and
is a dynamically interpreted assembly like
language. Instead of variables it has a stack
and 6 registers which 4 of them are multi purpose,
1 (ACC) being the register for math operations and
the last one (CMP) being for comparison operations.
The code is read line by line and because of that,
syntax errors will only be detected at runtime
when the interpreter arrives at the line. Debugging 
and exception handling is implemented.

Currently OSR features 24 instrucions

## Todo

- [ ] Better stack handling