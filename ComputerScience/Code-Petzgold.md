Foundation for mechanics and operation of computer s came from relays in telegrams (original electricomputers from relays made for the telephone system to control routing of calls) combined with binary  boolean algebra and logic.
Inputs(ex existence or lack of voltage/current), outputs and logic gates are the main elements.

Current flowing represents a 1 output, no current is a 0 output.
Transistors are used in place of relays. A


Bit - binary digit (0 or 1)

Voltage- potential
Current- actual in amps
Resistance - measured in ohms, increases with distance and thinned of wire, less the thicker/wider the diameter of the wire

(Pg 90)
Boolean algebra, + is union (something is either of two classes)
x is intersection (everything is in both classes)
1 everything, 0 nothing
x is and, + is or, - is not.

Gates
Came from telegraph relays which were used to amplify signals over long distances to counter resistance in the wires which weakened the original signal. They're created based originally on which contact you place the relay bar initially and are manipulated based on the electromagnetic iron bars charged when signal is sent.
AND, OR, NAND ( outputs 1 for any inputs that are not both 1),  NOR (output is 1 if both inputs are 0), XOR (exclusive or - output is 1 if either of 2 inputs is 1 but not if both inputs are 1, excludes and condition)


Invertor, uses other contact for relay to touch when metal piece is at rest not touching iron bar so that it still sends current (inverts a on switch to be off and off to be on). 0 (no voltage) becomes a 1 (no voltage)
(Really is wires around an iron bar.  When electricity flows causes bar to become electromagnetic and pull down a near by circuit to close it.

De Morgan's law in electrical circuits:
AND gate with two inverted inputs is same as a nor gate.
Or gate with two inverted inputs is same as a mand gate.
Iow: not A and not B = not (A or B)
Not A or not B = not (A and B)
-purpose was to simplify boolean logic.

Computers use transistors in place of relays today (function the same but are smaller and cheaper)

Basics of making sound, a buzzer with a circuit on pg 156.  OSCILLATOR - runs by itself alternating between on and off voltage. (An output circles back to become an input causing ba feedback cycle)

Pg 160, flip-flop circuit.  Retains information 
Level triggered flip flop: 2 inputs, clock and data.  When clock input is 0 any changes to data input does not affect output.
Edge triggered flip flop: difference is changes to data input also don't affect output when clock input is 1.  Data input affects output only at the instance the clock input changes from 0 to 1.
Summary of level triggered d type flip flop circuit is on p 191.
P 192 also called a "latch" as it latches onto data to store it.  
level triggered. In a level-triggered latch, the Clock input has to go to 1 and then back to 0 in order for the latch to store something. During the time the Clock input is 1, the data inputs of the inch can change and these changes will affect the stored output. Later in that chapter, I introduced edge-triggered latches. These latches save their values in the brief moment that the Clock input goes from 0 to 1. Edge-triggered latches are often somewhat easier to use, so I want to assume that all the latches in this chapter are edge triggered.

Page 176, combining frequency dividers to make an incrementing counter of 4 to 8 bit numbers.

Instruction codes or operation codes (opcodes) - instruct circuitry to perform a certain operation based on a numeric code. P 213

Byte ( misspelled bite, as in a biteful of bits).  8 bits.
P182-3, explanation of hex numbers for shortening byte numbers.  
A hexadecimal digit is in base 16, represents 4 bits (numbers from 1-16).  
**1 byte is represented by a pair of hexadecimal digits.

Memory: p 192, basic level trigger flip flop circuit to store 1 bit of data.  Change clock/write input to 1 and then back to 0 to store data input.
P 198, concept of a memory address.
P 205 - explanation of how RAM is volatile and requires electrical signal and power.  If power is lost so is the memory.

P220: more complex accumulator - op codes do 3 bytes, the op code itself and the memory address of where to read or write data for the operation. Key is adding more instructions to the ram array involves using the memory address to use the data.  Now one ram array instead of two can be used as well.(before the two arrays had to be sequenced so the instruction lined up with the data in order)


P222: instruction fetch - process of retrieving instructions from ram memory.  Retrieves one bye at a time, one cycle per part.

TANSTAAFL - tans toffle - there ain't no such thing as a free lunch.  Usually whenever you make a machine better in some way, something else tends to suffer as a result.

P225-226: jump or go-to instruction to add on instructions in a ram array.

Conditional jump on p 230-231
What separates a computer from a calculator is controlled repitition or looping.

4 parts to a digital computer: processor, memory, input device, output device

Electronic computer: replaced relays with vacuum tubes which change state much faster.
Von Neumann architecture: stored program concept: data and instructions are speed in memory.
Von Neumann bottleneck: time spent fetching instructions limited speed of program.

P247
Transistor: development that replaced vacuum tubes and relays made in research by staff at bell telephone company for the purpose of improving the telephone system, namely the problem of more cheaply and effectively transmitting signal and eliminating noise.
Was originally an amplifier constructed from germanium (a semiconductor) with gold foil.

Semiconductors p247: have 4 electrons in outer shell and not like conductors, but can be manipulated (electrons can be added or impurities can be introduced).  Modern transistors are usually made from silicon.

Primary combinations of transistors:
Gates
Selectors
Decoders
Flip flops
Adders

Integrated circuit, page 250: think silicon wafers doped(added electrons or impurities) and etched to maker microscopic components.  Common configuration s of transistors and gates as listed above in prepackaged form.

Memory a processor has affects speed since retrieving and reading data from an outside source takes more time.

Stack memory: p 273.  Purpose is to store jobs sequentially.

Call and return instruction.  P 277.  The call instruction is like a jump but it saves the address where it jumped from to the stack.  The return instruction pops that saved address from the stack for the program to return to.
A subroutine saves the place or needed to return to 

Input/keyboard interrupt p 280
Restart command goes to address with coffee to read bytes from the keyboard.

Little endian and big endian -p 283, least significant byte of address that follows op code is lfirst or last.  Intel is little endian.

P 285 - pipelining in cpus: loading next instruction while executing another instruction.
Cache- very fast ram to store recent executed instructions to prevent having to reload them repetitively.  

BCD - binary coded decimal, 4 bit code for digits 0-9.

ASCII characters are 8 bits (1 byte), so 1000 characters is 1000 bytes.

P 291 - sorting of nums caps and lowercase chars

Unicode was invented in 1988 to account for more characters.  It is a 16 bit code as opposed to ASCIIs 8 bits. Every character requires two bytes instead of one so Unicode takes twice the space.

Bus definition p 301: collection of digital signals that are provided to every board in a computer.

Open architecture as an explanation for higher pc market share over macintosh closed architecture.  P303.

DMA request (direct memory access), can be used to bypass microprocessor for reading and writing to memory (used by storage for example)

Difference between SRAM and DRAM.  P 308-309

P 327 - binary file: not a text file, contains machine code.
ASCII or text file: contains ASCII codes that corresponds to human readable text characters.

P 328 - booting the os. Bootstrap loader loads instructions into memory to l load the rest of the operating system.

Utility programs: small and designed to do simpler chores.

P 333 evolution and beginnings of unix operating system.

P 334 virtual memory, blocks of memory stored in temporary files when not needed and retrieved when needed to free up ram.

P 339 - fixed point format numbers- decimal point is fixed at a particular number of places.
The program must know where the decimal place is, the number does not store this or indicate that in it's bytes.
Fixed point fails when numbers are ranting from extremely small to extremely big for memory space constraints.

Floating point notation, p 340.  Alternative to fixed point notation for dealing with large and small numbers based on scientific notation. 
P 342 - single precision (4 bytes) vs double precision format (8 bytes)

Floating point only accurate to a certain degree. P 345-346.  Adding extremely high number with an extremely low number would result in no difference  in the sum for example.  Or the difference between two very long floats would be none. I'm

Fixed point format used for banking.

P 351  how a basic assembler works to concert mnemonics to machine code.   

P 353 - compiler and difference from an assembler.  Assembler is one to one text to machine code instruction.  Compiler is more complicated and must break down text to multiple machine code instructions.

Interpreter - p 362, reads source code and executes as reading instead of creating a executable file like a compiler.

Oop origins and principles, p 372, object oriented programming

P 374, vector graphics (lines, circles etc for designing) vs raster(bitmap) graphics-computer for pictures.

Run length encoding compression for bitmap images.  Encode the number of repeating pixels too reduce size (RLE usually involves numbers representing value presence or repitition.  Can be used in database column compression as well with bitmaps of distinct values - see p 98 of designing data driven programs)

LZW is more sophisticated and used in gif files - detects patterns of repetition of differently values pixels.

Main idea of compression: use when values and data is repetitive.

Sound conversion in computers and CDs: p 376-377

Serial interface: bytes are sent one after the other rather than all at once. (Not parallel)

Light i.e. in fiber optic cables is the future of sending signals instead of electrons for the transmission of energy.  It is much faster than electricity.




