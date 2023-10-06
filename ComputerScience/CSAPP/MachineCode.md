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
float | 4 \*single precision
double | 8 (double presicion)
long | 10/12 (extended precision)

### Instructions:

- %edp can be a way of signifying a register (using percent)
- instructions can have size suffixes: `movl` means move a long word (a larger sized data type with more bytes), `movb` means move byte etc.
- Instructions can be categorized into classes - i.e. MOV instructions can be move operations for various sizes as noted above.

#### Registers

- There are registers dedicated to various word sizes or reserved for certain operations.
- Memory locations are different than registers (registers are a reserved space separate from memory locations)
- indicated in assembly as `%{id}`: ex, %esp (top of the stack register)

#### MOV instructions

- Copying a value from one
  memory location to another requires two instructions—the ﬁrst to load the source
  value into a register, and the second to write this register value to the destination.
  Exampls:
  ```
   movl $0x4050,%eax Immediate--Register, 4 bytes
   movw %bp,%sp Register--Register, 2 bytes
   movb (%edi,%ecx),%ah Memory--Register, 1 byte
   movb $-17,(%esp) Immediate--Memory, 1 byte
   movl %eax,-12(%ebp) Register--Memory, 4 bytes
  ```
- `movl 8(%ebp), %eax` : store parameter x at an offset of 8 relative to the memory location at %ebp

### Arithmetic

- Unary (single operand serves as both source and dest) or Binary operations

#### LEAL (Load Effective Address)

- variant of the movl instruction.
- Does not actually reference memory, instead of reading from a memory location it copies the effective address to the destination.
- Computation can be indicated by the C address operator `&S`
- Instruction can be used to generate pointers for later memory references.
  - or can be used to compactly describe common arithmetic operations.
- destination must be a register
- `leal {first arg}, {destination register}`: leal 6(%eax), %edx

#### Shifting

- Left Shift `SAL` and `SHL` - fill from the right with zeroes.
- Right Shift: two kinds
  - `SAR` - Arithmetic shift - fills with copies of the sign bit
  - `SHR` - logical shift (fill with zeros)
