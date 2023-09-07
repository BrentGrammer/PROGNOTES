# Computer Systems A Programmers Perspective by Randal Bryant and David O'Hallaron

### Binary Filesiles that consist exclusivelyof ASCII characters are known as text files.ll other files are known as binary files.

### Compilation:

The programs that perform the four phases (preprocessor, compiler, assembler, and linker) are known collectively as thompilation system.

Linking phase.Notice that our hello program calls the printf function, whics part of the standard C library provided by every C compiler. The printunction resides in a separate precompiled object file called printf.o, whicust somehow be merged with our hello.o program. The linker (ld) handlehis merging. The result is the hello file, which is an executable object file (oimply executable) that is ready to be loaded into memory and executed bhe system.

GCC is one of many useful tools developed by the GNU (short for GNU's Not Unix) project. ThNU project is a tax-exempt charity started by Richard Stallman in 1984, with the ambitious goal oeveloping a complete Unix-like system whose source code is unencumbered by restrictions on hot can be modified or distributedhe gcc compiler harown to support many different languages, with the ability to generate code for many differenachines.

### The Shellhe shell is a command-line interpreter that prints a prompt, waits for you to type ommand line, and then performs the command. If the first word of the commanine does not correspond to a built-in shell command, then the shell assumes that is the name of an executable file that it should load and run.

### System Busunning throughout the computer hardware system is a collection of electrical conduits called busehat carry bytes of information back and forth between the components. Busere typically designed to transfer fixed-sized chunks of bytes known as words. The number of bytes or bits in a word (the word size) is a fundamental system parameter that varies across systems. Most machines today have word sizes of either 4 bytes (32 bits) or 8 bytes (64 bits)

Main Memory (where programs are loaded, run and manipulated - RAM, not hard disk)
The main memory is a temporary storage device that holds both a program anhe data it manipulates while the processor is executing the program. Physicallyain memory consists of a collection of dynamic random access memory (DRAM)
When a program is executed by the system, the executable code(binary) is copied from hard disk and loaded into RAM for running.

### CPU Processing of a Programinstructions executn strict sequence, and executing a single instruction involves performing a serief steps. The processor reads the instruction from memory pointed at by throgram counter (PC), interprets the bits in the instruction, performs some simplperation dictated by the instruction, and then updates the PC to point to the nexnstruction, which may or may not be contiguous in memory to the instruction thaas just executed.

L1,L2 CPU caches (Exploiting Locality for performance gains)eading from main memory is slower than reading from the register file (where current program data is stored and accessed by the CPU). To deal with the processor-memory gap, system designers include smalleaster storage devices called cache memories (or simply caches) that serve aemporary staging areas for information that the processor is likely to need ihe near future. L1 is fastest and smallest cache, while L2 is larger and slower (but still fast It might take imes longer for the process to access the L2 cache than the L1 cache, but this itill 5 to 10 times faster than accessing the main memory. The L1 and L2 caches armplemented with a hardware technology known as static random access memorSRAM). Newer and more powerful systems even have three levels of cache: L12, and L3. The idea behind caching is that a system can get the effect of bot very large memory and a very fast one by exploiting locality, the tendency forograms to access data and code in localized regions. By setting up caches to holata that is likely to be accessed often, we can perform most memory operationsing the fast caches

Memory Heirarchy (intermediary caches)his notion of inserting a smaller, faster storage device (e.g., cache memory) between the processor and a larger slower device (e.g., main memory) turns ouo be a general idea. In fact, the storage devices in every computer system arrganized as a memory hierarchy similar to Figure 1.9. As we move from the tof the hierarchy to the bottom, the devices become slower, larger, and less costler byte. The register file occupies the top level in the hierarchy, which is knows level 0, or L0. We show three levels of caching L1 to L3, occupying memorierarchy levels 1 to 3. Main memory occupies level 4, and so onhe main idea of a memory hierarchy is that storage at one level serves as ache for storage at the next lower level. Thus, the register file is a cache for th1 cache. Caches L1 and L2 are caches for L2 and L3, respectively.

The OS as a layer between the program and hardwareWe can think of the operating system a layer of software interposed between the application program and the hardwares shown in Figure 1.10. All attempts by an application program to manipulate thardware must go through the operating system.

The operating system has two primary purposes: (1) to protect the hardwarrom misuse by runaway applications, and (2) to provide applications with simplnd uniform mechanisms for manipulating complicated and often wildly differenow-level hardware devices.

POSIX origin (standard for Unix)endors started making various derivatives of the Unix OS.rouble arose in the mid 1980s as Unix vendors tried to differentiate themselves by adding nend often incompatible features. To combat this trend, IEEE (Institute for Electrical and Electronicngineers) sponsored an effort to standardize Unix, later dubbed CPosix" by Richard Stallman. Thesult was a family of standards, known as the Posix standards, that cover such issues as the C languagnterface for Unix system calls, shell programs and utilities, threads, and network programming. Aore systems comply more fully with the Posix standards, the differences between Unix versions arradually disappearing.

### PROCESS definition process is the operating system's abstraction for a running program. Multile processes can run concurrently on the same system, and each process appearo have exclusive use of the hardwarehe operating system performs this interleaving with a mechanism known as context switchinghe operating system keeps track of all the state information that the proceseeds in order to run. This state is known as the context.

Threads: a process can actually consist of multiple execution units, called threadsach running in the context of the process and sharing the same code and globaata.

Information inside the computer is represented aroups of bits that are interpreted in different ways, depending on the context.

### FILE definition file is a sequence of bytes, nothing more and nothing less. Every I/O devicencluding disks, keyboards, displays, and even networks, is modeled as a file. Alnput and output in the system is performed by reading and writing files, using mall set of system calls known as Unix I/O.

### UNIXhe 1960s was an era of huge, complex operating systems, such as IBMCs OS/360 and Honeywell'ultics systems. While OS/360 was one of the most successful software projects in history, Multicragged on for years and never achieved wide-scale use. Bell Laboratories was an original partner in thultics project, but dropped out in 1969 because of concern over the complexity of the project and thack of progress. In reaction to their unpleasant Multics experience, a group of Bell Labs researchersen Thompson, Dennis Ritchie, Doug McIlroy, and Joe Ossanna-began work in 1969 on a simpleperating system for a DEC PDP-7 computer, written entirely in machine language. Many of the idean the new system, such as the hierarchical file system and the notion of a shell as a user-level processere borrowed from Multics but implemented in a smaller, simpler package. In 1970, Brian Kernighaubbed the new system "Unix" as a pun on the complexity of "Multics." The kernel was rewritten i in 1973, and Unix was announced to the outside world in 1974 [89].

### LINUXthe Linux project has developed a complete, Posix-complianersion of the Unix operating system, including the kernel and all of the supporting infrastructureinux is available on a wide array of computers, from hand-held devices to mainframe computers

### CONCURENCY: We use the term concurrency to refer to the general concept of a system witultiple, simultaneous activities.

Traditionally, concurrent execution wanly simulated, by having a single computer rapidly switch among its executinrocesses, much as a juggler keeps multiple balls flying through the air. This forf concurrency allows multiple users to interact with a system at the same timeuch as when many people want to get pages from a single Web server.

Multi-core processors have several CPUs (referred to as "cores") integratento a single integrated-circuit chip. (implemenmts hyperthreading, i.e. more than one core that juggled threads)

Hyperthreading, sometimes called simultaneous multi-threading, is a techique that allows a single CPU to execute multiple flows of control. It involveaving multiple copies of some of the CPU hardware, such as program counternd register files, while having only single copies of other parts of the hardwareuch as the units that perform floating-point arithmetic

a hyperthreaded processor decides which of its threads to execute on a cycley-cycle basis. It enables the CPU to make better advantage of its processinesources. For example, if one thread must wait for some data to be loaded int cache, the CPU can proceed with the execution of a different thread. As an exmple, the Intel Core i7 processor can have each core executing two threads, ano a four-core system can actually execute eight threads in parallel.

modern processors can execute multiplnstructions at one time, a property known as instruction-level parallelism.

### PARALELLISM: parallelism to refers to the use of concurrency to make a system run faster

---

SECTION 2:

### Bit: Binary Digit

In isolation, a single bit is not very useful. When we group bits together anpply some interpretation that gives meaning to the different possible bit patternsowever, we can represent the elements of any finite set.

## Integers and Floats:

Computer representations use a limited number of bits to encode a number,
and hence some operations can oveflow when the results are too large to be rep-
resented. This can lead to some surprising results. For example, on most of today's
computers (those using a 32-bit representation of data type int), computing the
expression
200 \* 300 \* 400 \* 500
yields -884,901,888.

integer representations can encode a comparatively small range of values, but do so precisely, while floating-point representations can encode a wide range of values, but only approximately.

## Memory Definition:

A machine-level program views memory as a very large array of bytes, referred to as virtual
memory. Every byte of memory is identified by a unique number, known as its address, and the set of all possible addresses is known as the virtual address space.

As indicated by its name, this virtual address space is just a conceptual image presented to the machine-level program.
The actual implementation (presented
in Chapter 9) uses a combination of random-access memory (RAM), disk storage,
special hardware, and operating system software to provide the program with what
appears to be a monolithic byte array.

### C Pointer:

the value of a pointer in C, whether it points to an integer, a structure, or some other program object, is the virtual address of the first byte
of some block of storage.

They provide the mechanism for referencing elements of data structures, including arrays. Just like a variable, a pointer has two aspects: its value and its type. The value indicates the location of some object, while its type indicates what kind of object (e.g., integer or floating-point number) is stored at that location.

Although the C compiler maintains type information, the actual
machine-level program it generates has no information about data types. It simply
treats each program object as a block of bytes, and the program itself as a sequence

The C "address of" operator `&` creates a pointer. On all three lines, the expression `&x` creates a pointer to the location holding the object indicated by variable x
of bytes.

### Hexadecimal Numbers:

In C, numeric constants starting with 0x or 0X are interpreted as being in hexadecimal. The characters 'A' through 'F' may be written in either upper or lower case

Split each hexadecimal number into 4 bits.

One simple trick for doing the conversion in your head is to memorize the decimal equivalents of hex digits A, C, and F.
The hex values B, D, and E can be translated to decimal by computing their values
relative to the first three.

given a binary number 1111001010110110110011, you convert it
to hexadecimal by first splitting it into groups of 4 bits each. Note, however, that if
the total number of bits is not a multiple of 4, you should make the leftmost group
be the one with fewer than 4 bits, effectively padding the number with leading
zeros.

0x39A7F8 (skip the 0x and start translating at 3)

001110011010011111111000

A single byte can be represented by two hexadecimal digits:
0 = 0x00

### Word Size (32 64 bit etc.):

Every computer has a word size, indicating the nominal size of integer and pointer
data. Since a virtual address is encoded by such a word, the most important system
parameter determined by the word size is the maximum size of the virtual address
space.

Most personal computers today have a 32-bit word size. This limits the virtual
address space to 4 gigabytes (written 4 GB). 64 bit is more common now.

### Data Sizes:

The C language supports multiple data formats for both integer and floating-
point data. The C data type char represents a single byte. Although the name
"char" derives from the fact that it is used to store a single character in a text
string, it can also be used to store integer values. The C data type int can also be
prefixed by the qualifiers short, long, and recently long long, providing integer
representations of various sizes

"short" integers have 2-byte allocations, while an unqualified int is 4 bytes. A
"long" integer uses the full word size of the machine.

Most machines also support
two different floating-point formats: single precision, declared in C as float,
and double precision, declared in C as double. These formats use 4 and 8 bytes,
respectively

### Memory Addressing:

In virtually all machines, a multi-byte object is stored as a contiguous sequence
of bytes, with the address of the object given by the smallest address of the bytes
used. For example, suppose a variable x of type int has address 0x100, that is, the
value of the address expression &x is 0x100. Then the 4 bytes of x would be stored
in memory locations 0x100, 0x101, 0x102, and 0x103.

The int 0x01234567 will have it's binary split into bytes (2 x 4 bits) and placed at each memory address starting at 0x100, for example, and proceeding to 0x103 address.
The int takes up 4 bytes in total (4 \* 8 bits) and 4 memory address slots.

#### Big Endian vs. Little Endian:

Big endian (most significant digit first) vs. Little Endian (least significant digit first)
Little-Endian: In little-endian byte order, the least significant byte (LSB) of a multi-byte value is stored at the lowest memory address, and subsequent bytes are stored in increasing order of significance. This means that the bytes are ordered from least significant to most significant, and when you read the bytes from memory sequentially, you are effectively reading the value from right to left.

Big-Endian: In big-endian byte order, the most significant byte (MSB) of a multi-byte value is stored at the lowest memory address, and subsequent bytes are stored in decreasing order of significance. The bytes are ordered from most significant to least significant, and when you read the bytes from memory sequentially, you are effectively reading the value from left to right.

- Can cause issues when machines transfer ints over a network if machines do not adhere to one - they must take into account the network standard to avoid reversing the bytes of the int.

- 0 index: in C (using pointers), the reference `some_array[i]` indicates that we want to read the byte that is i positions beyond the location pointed to by start. so i = 0 represents 0 positions beyond the start of the memory block (i.e. the first byte at the memory address)

Note: term comes from Gulliver's Travels classic novel.

## Strings

A string in C is encoded by an array of characters terminated by the null (having
value 0) character.

Observe that the ASCII code for decimal digit
x happens to be 0x3x, and that the terminating byte has the hex representation
0x00. This same result would be obtained on any system using ASCII as its
character code, independent of the byte ordering and word size conventions. As
a consequence, text data is more platform-independent than binary data

the UTF-8 representation encodes each character as a
sequence of bytes, such that the standard ASCII characters use the same single-byte encodings as they
have in ASCII, implying that all ASCII byte sequences have the same meaning in UTF-8 as they do in
ASCII.

### Representing Code

Binary code is seldom portable across different combinations of machine and operating system.

A fundamental concept of computer systems is that a program, from the
perspective of the machine, is simply a sequence of bytes

### Bit Vectors (see p 49 or pdf p 84) and Bit Wise Operators:

We can extend the four Boolean operations to also operate on bit vectors,
strings of zeros and ones of some fixed length w.

As examples, consider the case where w = 4, and with arguments a = [0110]
and b = [1100]. Then the four operations a & b, a | b, a ^ b, and ~b yield

When given hexidecimal, convert them to binary and then run the bitwise operations to get a result which you can convert back to hexidecimal:

```
0x69 & 0x55 -> [0110 1001] & [0101 0101] -> [0100 0001] -> 0x41
```

Ex: (apply the operation on the left to each column of pairs of bits vertically)

```
  0110    0110    0110
& 1100  | 1100  ^ 1100  ~ 1100
  0100    1110    1010    0011
```

Symbols:
The Boolean operation ~ corresponds to the logical op-
eration Not, denoted by the symbol ¬ . That is, we say that ¬ P is true when P
is not true, and vice versa. Correspondingly, ~p equals 1 when p equals 0, and
vice versa. Boolean operation & corresponds to the logical operation And, de-
noted by the symbol ∧ . We say that P ∧ Q holds when both P is true and Q is
true. Correspondingly, p & q equals 1 only when p = 1 and q = 1. Boolean opera-
tion | corresponds to the logical operation Or, denoted by the symbol ∨ . We say
that P ∨ Q holds when either P is true or Q is true. Correspondingly, p | q equals
1 when either p = 1 or q = 1. Boolean operation ^ corresponds to the logical op-
eration Exclusive-Or, denoted by the symbol ⊕ . We say that P ⊕ Q holds when
either P is true or Q is true, but not both. Correspondingly, p ^ q equals 1 when
either p = 1 and q = 0, or p = 0 and q = 1

#### Shift Operations:

As examples, the following table shows the effect of applying the different
shift operations to some sample 8-bit data:

```
(Argument x         [01100011] [10010101])

Operation           Values

x << 4              [00110000] [01010000]
x >> 4 (logical)    [00000110] [00001001]
x >> 4 (arithmetic) [00000110] [11111001] - adds 1s
```

Observe that all but one entry involves filling with zeros. The exception
is the case of shifting [10010101] right arithmetically. Since its most significant bit
is 1, this will be used as the fill value.

An arithmetic right shift fills the left end with k repetitions of the most significant bit, giving a result [x n − 1, . . . , x n − 1, x n − 1, x n − 2, . . . x k ].
This convention might seem peculiar, but as we will see it is useful for operating
on signed integer data.

### Masking

One common use of bit-level operations is to implement masking operations,
where a mask is a bit pattern that indicates a selected set of bits within a word. As
an example, the mask 0xFF (having ones for the least significant 8 bits) indicates
the low-order byte of a word. The bit-level operation x & 0xFF yields a value
consisting of the least significant byte of x, but with all other bytes set to 0.
For example, with x = 0x89ABCDEF, the expression would yield 0x000000EF.

### Logical Operators:

- Not to be confused with bit wise operators and they function different:
  The logical operations treat any
  nonzero argument as representing True and argument 0 as representing False.
  They return either 1 or 0, indicating a result of either True or False, respectively.
  Here are some examples of expression evaluation:

```
Expression Result
!0x41 0x00
!0x00 0x01
!!0x41 0x01
0x69 && 0x55 0x01
0x69 || 0x55 0x01
```

logical operators do not evaluate their second argument if the result of the expression can be determined by evaluat-
ing the first argument. Thus, for example, the expression a && 5/a will never cause
a division by zero, and the expression p && \*p++ will never cause the dereferencing
of a null pointer.

## Numbers (Integral Data Types)

integral data types: ones that represent finite ranges of integers.

The most significant bit x
w − 1 is also called the sign bit. Its “weight” is − 2 w − 1
, the
negation of its weight in an unsigned representation. When the sign bit is set to
1, the represented value is negative, and when set to 0 the value is nonnegative

```c
//B2T4
([0101]) = 5
//B2T4
([1011]) = -5
```

### Signed vs. Unsigned:

Note on signed negative integrals:
the two’s-complement range is asymmetric: | TMin | = | TMax | + 1, that is, there is no positive counterpart to TMin.
Ex: -128 thourgh 127 for the range of signed integers.

- almost all modern machines use two’s complement.

  - Note the different position of apostrophes: Two’s complement versus Ones’ complement. The term
    “two’s complement” arises from the fact that for nonnegative x we compute a w-bit representation
    of − x as 2 w − x (a single two). The term “ones’ complement” comes from the property that we can
    compute − x in this notation as [111 . . . 1] − x (multiple ones).

- In two's complement, the Most Significant Bit is the sign bit. If the MSB is 0, the number is positive or zero. If the MSB is 1, the number is negative.
  - Most Significant means it holds the highest value, i.e. the left most slot in a number

### IMPORTANT NUMBERS IN SYSTEMS (Most common compatible ranges):

```
                        Word size w
Value     8       16         32                 64
UMax w  0xFF    0xFFFF  0xFFFFFFFF      0xFFFFFFFFFFFFFFFF
        255     65,535  4,294,967,295   18,446,744,073,709,551,615

TMin w  0x80    0x8000  0x80000000      0x8000000000000000
        −128    −32,768 −2,147,483,648  −9,223,372,036,854,775,808

TMax w  0x7F    0x7FFF  0x7FFFFFFF      0x7FFFFFFFFFFFFFFF
        127     32,767  2,147,483,647   9,223,372,036,854,775,807

−1     0xFF    0xFFFF  0xFFFFFFFF      0xFFFFFFFFFFFFFFFF

0       0x00    0x0000  0x00000000      0x0000000000000000
```

#### Compatible Ranges:

- The C standards do not require signed integers to be represented in two’s-
  complement form, but nearly all machines do so
- Different systems support potentially different ranges of numeric data types (i.e. a long can be a different range on one system vs. another).
- The ISO C99 standard introduces another class of integer types in the file stdint.h. This file
  defines a set of data types with declarations of the form intN_t and uintN_t, specifying N-bit signed
  and unsigned integers, for different values of N. The exact values of N are implementation dependent,
  but most compilers allow values of 8, 16, 32, and 64. Thus, we can unambiguously declare an unsigned,
  16-bit variable by giving it type uint16_t, and a signed variable of 32 bits as int32_t.

  - For example, if you need an integer that is exactly 2 bytes, you can use int16_t. If you need an integer that is exactly 4 bytes, you can use int32_t. And if you need an integer that is exactly 8 bytes, you can use int64_t. These types provide size guarantees across different systems.

  many programs are written assuming a two’s-complement
  representation of signed numbers, and the “typical” ranges shown in Figures 2.8
  and 2.9, and these programs are portable across a broad range of machines and
  compilers. The file <limits.h> in the C library defines a set of constants delim-
  iting the ranges of the different integer data types for the particular machine on
  which the compiler is running. For example, it defines constants INT*MAX, INT*
  MIN, and UINT_MAX describing the ranges of signed and unsigned integers.

  - JAVA numbers: The Java standard is quite specific about integer data type ranges and repre-
    sentations. It requires a two’s-complement representation with the exact ranges
    shown for the 64-bit case (Figure 2.9). In Java, the single-byte data type is called
    byte instead of char, and there is no long long data type. These detailed require-
    ments are intended to enable Java programs to behave identically regardless of
    the machines running them.

#### Note on Casting (i.e. unsigned to signed etc):

- In casting from unsigned int to int, the underlying bit representation stays the same.

```c
unsigned u = 4294967295u; /* UMax_32 max 32 bit number */
int tu = (int) u;
printf("u = %u, tu = %d\n", u, tu);

// When run on a two’s-complement machine, it generates the following output:
u = 4294967295, tu = -1

short int v = -12345;
unsigned short uv = (unsigned short) v;
printf("v = %d, uv = %u\n", v, uv);
//When run on a two’s-complement machine, it generates the following output:
v = -12345, uv = 53191
```

In other words, That is, the 16-bit pattern written in
hexadecimal as 0xCFC7 is both the two’s-complement representation of − 12,345
and the unsigned representation of 53,191. Similarly, from Figure 2.13, we see that
T2U32
( − 1) = 4,294,967,295, and U2T32
(4,294,967,295) = − 1. That is, UMax has
the same bit representation in unsigned form as does − 1 in two’s-complement form.
These are the effects you need to keep in mind when casting between unsigned and two's compliment numbers in most C implementations.

- Signed to Unsigned: the values that are negative in a two’s-complement representation increase by 2^4(exponent is word size i.e. 4,16,32 etc) = 16 with an unsigned representation. Thus, − 5 becomes + 11, and − 1 becomes + 15.

#### C specific considerations:

**_Careful with comparisons using unsigned and signed numbers_**

#### Never use unsigned numbers:

One way to avoid bugs is to never use unsigned
numbers. In fact, few languages other than C support unsigned integers. Appar-
ently these other language designers viewed them as more trouble than they are
worth.

NOTE: Generally, in C most numbers are signed by default. For example, when declaring a
constant such as 12345 or 0x1A2B, the value is considered signed. Adding charac-
ter ‘U’ or ‘u’ as a suffix creates an unsigned constant, e.g., 12345U or 0x1A2Bu.

When an operation is performed where one operand is signed and the other is unsigned, C implicitly
casts the signed argument to unsigned and performs the operations assuming
the numbers are nonnegative. As we will see, this convention makes little dif-
ference for standard arithmetic operations, but it leads to nonintuitive results
for relational operators such as < and >.
Ex:

```c
-1 < 0U => False // -1 cast to unsigned automatically
// *** When either operand of a comparison is unsigned, the other operand is implicitly cast to unsigned. ***
// UMax (Max number given a word size) has the same bit representation in unsigned form as does -1 in two's-complement form, so here -1 could = 4294967295 for example
```

### Converting Integers (i.e. to different word sizes, 16 bit to 32 bit sizes etc.):

- Converting from a smaller to a larger data type, however, should always be possible.
- for a positive number, we can simply add leading zeros to the
  representation; this operation is known as **zero extension**.
- For converting a two’s-complement number to a larger data type, the rule is to perform a **sign extension**,
  adding copies of the most significant bit to the representation (i.e. could be adding a series of 1's).

- Bit vector [101] represents the value
  − 4 + 1 = − 3. Applying sign extension gives bit vector [1101] representing the
  value − 8 + 4 + 1 = − 3. We can see that, for w = 4, the combined value of the
  two most significant bits is − 8 + 4 = − 4, matching the value of the sign bit for
  w = 3. Similarly, bit vectors [111] and [1111] both represent the value − 1.

- Casting to a smaller value (int to short for ex): Truncating a number can alter its value—a form of overflow

```c
int x = 53191;
2 short sx = (short) x; /* -12345 */
3 int y = sx; /* -12345 */
```

- NOTE: security vulnerabilities and unexpected bugs can arise from implicit casting of negative numbers to unsigned number types. Important to ensure that types line up:

ex:

```c
void *memcpy(void *dest, void *src, size_t n);
int copy_from_kernel(void *user_dest, int maxlen) {
  int len = KSIZE < maxlen ? KSIZE : maxlen;
  memcpy(user_dest, kbuf, len); // if maxlen is passed as a negative signed int, it will be cast to unsigned (and positive number) when passed to memcpy expecting an unsigned num.
  return len;
}
```

#### When to use unsigned numbers:

- Generally you should avoid unsigned numbers, but Unsigned values are very useful when we want to think of words as just col-
  lections of bits with no numeric interpretation. This occurs, for example, when
  packing a word with flags describing various Boolean conditions. Addresses are
  naturally unsigned, so systems programmers find unsigned types to be helpful.
  Unsigned values are also useful when implementing mathematical packages for
  modular arithmetic and for multiprecision arithmetic, in which numbers are rep-
  resented by arrays of words.

## INTEGER ARITHMETIC

- The result of arithmetic us unbounded (i.e. the result or sum can be max number of bits)

  - to maintain the sum as a w + 1-bit number and add it to another value, we may re-
    quire w + 2 bits (_each addition of two x bit nums require a result of potentially x+1 bits_), and so on. This continued “word size inflation” means we cannot
    place any bound on the word size required to fully represent the results of arith-
    metic operations.

  - More commonly, programming languages support fixed-precision arithmetic

  - Unsigned arithmetic can be viewed as a form of modular arithmetic. Unsigned
    addition is equivalent to computing the sum modulo 2 w . This value can be com-
    puted by simply discarding the high-order bit in the w + 1-bit representation of
    x + y. For example, consider a 4-bit number representation with x = 9 and y = 12,
    having bit representations [1001] and [1100], respectively. Their sum is 21, having
    a 5-bit representation [10101]. But if we discard the high-order bit, we get [0101],
    that is, decimal value 5. This matches the value 21 mod 16 = 5.
    With a 4-bit word size, addition is performed modulo 16 (2^4).

- An arithmetic operation is said to overflow when the full integer result cannot
  fit within the word size limits of the data type. As Equation 2.11 indicates, overflow
  occurs when the two operands sum to 2 w or more

  ### Multiplication

  - Multiplication requires more clock cycles than arithmetic and is more expensive.
  - Compilers will optomize by using bit shifting, addition and subtraction to make an equivalent calculation - Ex: suppose a program contains the expression x \* 14. Recognizing that 14 =2^3 + 2^2 + 2^1, the compiler can rewrite the multiplication as (x<<3) + (x<<2) + (x<<1), replacing one multiplication with three shifts and two additions. - x<<3 adds 3 0s to the right and shifts the binary to the left three places.
    ```
    Original x: 11001010
    After shifting left by 3 positions: 01010000
    The << operator effectively adds three zero bits to the right of the binary representation of x. This has the effect of multiplying x by 2^3 (which is 8 in decimal). So, x << 3 is equivalent to x * 8.
    ```
    - Most compilers only perform this optimization when a small number of shifts, adds, and subtractions suffice.

### Division

- Integer division on most machines is even slower than integer multiplication - requiring 30 or more clock cycles (multiplication is 10).
- Integer division always rounds toward zero

```
(result = rounded): 3.14 = 3, 3.14 = -4
```

- right shifting: When you shift a bit to the right, the rightmost bits "fall off," and new bits are added on the left side.
- similar to dividing a decimal number by a power of 2, where you move the decimal point to the left.
- 11001100 shift 1 bit to right is 01100110

### General Integer arithmetic

- operations such as addition, subtraction, multiplication, and even division have either identical or
  very similar bit-level behaviors whether the operands are in unsigned or two’s-
  complement form

- Integer Overflow ex: the result wraps around, and the leftmost bit is lost
  - Unsigned Integer Overflow: 11111111 (255 in decimal) + 00000001 (1 in decimal) = 00000000 (0 in decimal). The leftmost bit is not lost but wraps around, resulting in a value of 0.
    - when the value of an integer exceeds the maximum value that can be represented with the available number of bits, it starts again from the minimum value. It's as if the number "wraps around" from the highest possible value to the lowest possible value.
  - Signed Integer Overflow: 01111111 (127 in decimal) + 00000001 (1 in decimal) = 10000000 (-128 in decimal). The leftmost bit is not lost but wraps around, resulting in a negative value.

## Floating Point Numbers

- Nowadays, virtually all computers support what has become known as IEEE ﬂoating point. This has greatly improved the portability of scientiﬁc application programs across different machines.

- **The Institute of Electrical and Electronic Engineers** (**IEEE**—pronounced “Eye-Triple-Eee”) is a pro-
  fessional society that encompasses all of electronic and computer technology. It publishes journals,
  sponsors conferences, and sets up committees to deﬁne standards on topics ranging from power trans-
  mission to software engineering.

  - negative exponents:
    2^-3 is the same as 1 / 2^3, which is 1 / 8 or 0.125.
    5^-2 is the same as 1 / 5^2, which is 1 / 25 or 0.04.

- The 'decimal point' becomes a 'binary point' in binary floating point representations.
  - digits to the left of the point have weights of 2^i, and weights to the right are 1 / 2^i
  - shifting the binary point one position to the left has the effect of dividing the number by 2, shifting it to the right has the effect of multiplying the number by 2

### Accuracy of Floating Points

- Some rational numbers cannot be represented in binary due to the finite bits. 1/3,5/7,1/5 (0.20 - 0.001100110011..., where the 0011 sequence repeats indefinitely)

- Float (Single Precision) - 32 bit representation of a fraction 0 - 255
- Double (Double Precision) - 64 bit representation of a fraction 0 - 2047

A second function of denormalized numbers is to represent numbers that are
very close to 0.0. They provide a property known as gradual underﬂow in which
possible numeric values are spaced evenly near 0.0.

#### NaN

- . Inﬁnity can represent results that overﬂow, as when we
  multiply two very large numbers, or when we divide by zero. When the fraction
  ﬁeld is nonzero, the resulting value is called a “NaN,” short for “Not a Number.”
- can be useful for representing an uninitialized value in some applications.

### Rounding

- Floating-point arithmetic can only approximate real arithmetic, since the repre-
  sentation has limited range and precision
- for a value x, we generally want
  a systematic method of ﬁnding the “closest” matching value x, so that can be rep-
  resented in the desired ﬂoating-point format. This is the task of the rounding
  operation
  - Rounding up or down? we could determine representable values x− and x+ such that the value x is guaranteed to lie between them: x− ≤ x ≤ x+
- The IEEE ﬂoating-point format deﬁnes
  four different rounding modes. The default method ﬁnds a closest match, while
  the other three can be used for computing upper and lower bounds.

#### Rounding Methods:

1.  Round-to-even (also
    called round-to-nearest) is the default mode. It attempts to ﬁnd a closest match.
    Thus, it rounds $1.40 to $1 and $1.60 to $2, since these are the closest whole dollar
    values - rounding from the middle up or down: rounds the number either upward or downward such that the
    least signiﬁcant digit of the result is even. Thus, it rounds both $1.50 and $2.50
    to $2 (since 3 is odd). - Why round to even, why not round up? rounding a set of data values would then introduce a statistical bias into the computation of an average of the values. The average would be slightly higher than the average of the numbers themselves. if we always rounded numbers halfway between downward, the average of a set of rounded numbers would be slightly lower than the average of the numbers themselves. Rounding toward even numbers avoids this statistical bias in most real-life situations. It will round upward about 50% of the time and round downward about 50% of the time.
    - Note: Round-to-even rounding can be applied even when we are not rounding to
      a whole number. We simply consider whether the least signiﬁcant digit is even
      or odd. we would round both 1.2350000 and 1.2450000 to 1.24, since 4 is even.
1.  Round-toward-zero mode rounds positive numbers downward and negative numbers upward, giving a value ˆ x such that | ˆ x | ≤ | x | .
1.  Round-down mode rounds both positive and negative numbers downward, giving a value x− such that x− ≤ x.
1.  Round-up mode rounds both positive and negative numbers upward, giving a value x+ such that x ≤ x+

#### Floating Point Arithmetic:

- Rounding is applied to the result of operation/expression on real numbers (not the individual numbers in the calculation). i.e. Round(x + y) and not Round(x) + Round(y)
  - with single-precision ﬂoating point the expression (3.14+1e10)-1e10 evaluates to 0.0—the value 3.14 is lost due to rounding. On the other hand, the expression 3.14+(1e10 - 1e10) evaluates to 3.14
- **Use Floating Point Arithmetic with caution since does not obey some common mathematical properties such as associativity**

#### Floating Points in C

All versions of C provide two different ﬂoating-point data types: float and
double. On machines that support IEEE ﬂoating point, these data types corre-
spond to single- and double-precision ﬂoating point and use round-to-even mode rounding.

##### Underflow:

Floating-point values can underﬂow, when they are so close to 0.0 that they are changed to zero.

### Casting Floating Point numbers:

When casting values between int, float, and double formats, the program
changes the numeric values and the bit representations as follows (assuming a
32-bit int):
. From int to float, the number cannot overﬂow, but it may be rounded.
. From int or float to double, the exact numeric value can be preserved be-
cause double has both greater range (i.e., the range of representable values),
as well as greater precision (i.e., the number of signiﬁcant bits).
. From double to float, the value can overﬂow to +∞ or −∞ , since the range
is smaller. Otherwise, it may be rounded, because the precision is smaller.
. From float or double to int the value will be rounded toward zero. For
example, 1.999 will be converted to 1, while − 1.999 will be converted to
− 1. Furthermore, the value may overﬂow. The C standards do not specify
a ﬁxed result for this case. Intel-compatible microprocessors designate the
