# Machine Level Representations of Programs

- Computers execute machine code, sequences of bytes encoding the low-level op-
  erations that manipulate data, manage memory, read and write data on storage
  devices, and communicate over networks. A compiler generates machine code
  through a series of stages, based on the rules of the programming language, the
  instruction set of the target machine, and the conventions followed by the operat-
  ing system. The gcc C compiler generates its output in the form of assembly code,
  a textual representation of the machine code giving the individual instructions in
  the program. gcc then invokes both an assembler and a linker to generate the exe-
  cutable machine code from the assembly code.

many of the ways programs can be attacked,
allowing worms and viruses to infest a system, involve nuances of the way pro-
grams store their run-time control information. Many attacks involve exploiting
weaknesses in system programs to overwrite information and thereby take control
of the system.

#### Examples of Machine Languages

- Intel IA32
- x86-64 (extension that runs on 64 bit machines)

### Type sizes:

Type | Size (bytes)
char | 1
short | 2
int | 4
long | 4
long | 4
char | 4
float | 4 *single precision
double | 8 (double presicion)
long | 10/12 (extended precision)

### Instructions:
- %edp can be a way of signifying a register (using percent)
- instructions can have size suffixes: `movl` means move a long word (a larger sized data type with more bytes), `movb` means move byte etc.
