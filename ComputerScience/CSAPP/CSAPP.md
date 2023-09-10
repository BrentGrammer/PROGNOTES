# Computer Systems A Programmers Perspective by Randal Bryant and David O'Hallaron

Binary Files that consist exclusively of ASCII characters are known as text files.
other files are known as binary files.

### Compilation:

The programs that perform the four phases (preprocessor, compiler, assembler, and linker) are known collectively as the compilation system.

Linking phase.Notice that our hello program calls the printf function, whics part of the standard C library provided by every C compiler. The printunction resides in a separate precompiled object file called printf.o, whicust somehow be merged with our hello.o program. The linker (ld) handlehis merging. The result is the hello file, which is an executable object file (oimply executable) that is ready to be loaded into memory and executed bhe system.

GCC is one of many useful tools developed by the GNU (short for GNU's Not Unix) project. ThNU project is a tax-exempt charity started by Richard Stallman in 1984, with the ambitious goal oeveloping a complete Unix-like system whose source code is unencumbered by restrictions on hot can be modified or distributedhe gcc compiler harown to support many different languages, with the ability to generate code for many differenachines.

### The Shell

the shell is a command-line interpreter that prints a prompt, waits for you to type ommand line, and then performs the command. If the first word of the commanine does not correspond to a built-in shell command, then the shell assumes that is the name of an executable file that it should load and run.

### System Bus

running throughout the computer hardware system is a collection of electrical conduits called busehat carry bytes of information back and forth between the components. Busere typically designed to transfer fixed-sized chunks of bytes known as words. The number of bytes or bits in a word (the word size) is a fundamental system parameter that varies across systems. Most machines today have word sizes of either 4 bytes (32 bits) or 8 bytes (64 bits)

Main Memory (where programs are loaded, run and manipulated - RAM, not hard disk)
The main memory is a temporary storage device that holds both a program anhe data it manipulates while the processor is executing the program. Physicallyain memory consists of a collection of dynamic random access memory (DRAM)
When a program is executed by the system, the executable code(binary) is copied from hard disk and loaded into RAM for running.

### CPU

- Processing of a Program instructions executing in strict sequence, and executing a single instruction involves performing a series of steps. The processor reads the instruction from memory pointed at by throgram counter (PC), interprets the bits in the instruction, performs some simplperation dictated by the instruction, and then updates the PC to point to the nexnstruction, which may or may not be contiguous in memory to the instruction thaas just executed.

L1,L2 CPU caches (Exploiting Locality for performance gains)eading from main memory is slower than reading from the register file (where current program data is stored and accessed by the CPU). To deal with the processor-memory gap, system designers include smalleaster storage devices called cache memories (or simply caches) that serve aemporary staging areas for information that the processor is likely to need ihe near future. L1 is fastest and smallest cache, while L2 is larger and slower (but still fast It might take imes longer for the process to access the L2 cache than the L1 cache, but this itill 5 to 10 times faster than accessing the main memory. The L1 and L2 caches armplemented with a hardware technology known as static random access memorSRAM). Newer and more powerful systems even have three levels of cache: L12, and L3. The idea behind caching is that a system can get the effect of bot very large memory and a very fast one by exploiting locality, the tendency forograms to access data and code in localized regions. By setting up caches to holata that is likely to be accessed often, we can perform most memory operationsing the fast caches

Memory Heirarchy (intermediary caches)his notion of inserting a smaller, faster storage device (e.g., cache memory) between the processor and a larger slower device (e.g., main memory) turns ouo be a general idea. In fact, the storage devices in every computer system arrganized as a memory hierarchy similar to Figure 1.9. As we move from the tof the hierarchy to the bottom, the devices become slower, larger, and less costler byte. The register file occupies the top level in the hierarchy, which is knows level 0, or L0. We show three levels of caching L1 to L3, occupying memorierarchy levels 1 to 3. Main memory occupies level 4, and so onhe main idea of a memory hierarchy is that storage at one level serves as ache for storage at the next lower level. Thus, the register file is a cache for th1 cache. Caches L1 and L2 are caches for L2 and L3, respectively.

The OS as a layer between the program and hardwareWe can think of the operating system a layer of software interposed between the application program and the hardwares shown in Figure 1.10. All attempts by an application program to manipulate thardware must go through the operating system.

The operating system has two primary purposes: (1) to protect the hardwarrom misuse by runaway applications, and (2) to provide applications with simplnd uniform mechanisms for manipulating complicated and often wildly differenow-level hardware devices.

POSIX origin (standard for Unix)endors started making various derivatives of the Unix OS.rouble arose in the mid 1980s as Unix vendors tried to differentiate themselves by adding nend often incompatible features. To combat this trend, IEEE (Institute for Electrical and Electronicngineers) sponsored an effort to standardize Unix, later dubbed CPosix" by Richard Stallman. Thesult was a family of standards, known as the Posix standards, that cover such issues as the C languagnterface for Unix system calls, shell programs and utilities, threads, and network programming. Aore systems comply more fully with the Posix standards, the differences between Unix versions arradually disappearing.

### PROCESS

definition: process is the operating system's abstraction for a running program. Multile processes can run concurrently on the same system, and each process appearo have exclusive use of the hardwarehe operating system performs this interleaving with a mechanism known as context switchinghe operating system keeps track of all the state information that the proceseeds in order to run. This state is known as the context.

Threads: a process can actually consist of multiple execution units, called threadsach running in the context of the process and sharing the same code and globaata.

Information inside the computer is represented aroups of bits that are interpreted in different ways, depending on the context.

### FILE

definition: file is a sequence of bytes, nothing more and nothing less. Every I/O devicencluding disks, keyboards, displays, and even networks, is modeled as a file. Alnput and output in the system is performed by reading and writing files, using mall set of system calls known as Unix I/O.

### UNIX

The 1960s was an era of huge, complex operating systems, such as IBMCs OS/360 and Honeywell'ultics systems. While OS/360 was one of the most successful software projects in history, Multicragged on for years and never achieved wide-scale use. Bell Laboratories was an original partner in thultics project, but dropped out in 1969 because of concern over the complexity of the project and thack of progress. In reaction to their unpleasant Multics experience, a group of Bell Labs researchersen Thompson, Dennis Ritchie, Doug McIlroy, and Joe Ossanna-began work in 1969 on a simpleperating system for a DEC PDP-7 computer, written entirely in machine language. Many of the idean the new system, such as the hierarchical file system and the notion of a shell as a user-level processere borrowed from Multics but implemented in a smaller, simpler package. In 1970, Brian Kernighaubbed the new system "Unix" as a pun on the complexity of "Multics." The kernel was rewritten i in 1973, and Unix was announced to the outside world in 1974 [89].

### LINUX

the Linux project has developed a complete, Posix-complianersion of the Unix operating system, including the kernel and all of the supporting infrastructureinux is available on a wide array of computers, from hand-held devices to mainframe computers

### CONCURENCY:

We use the term concurrency to refer to the general concept of a system witultiple, simultaneous activities.

Traditionally, concurrent execution wanly simulated, by having a single computer rapidly switch among its executinrocesses, much as a juggler keeps multiple balls flying through the air. This forf concurrency allows multiple users to interact with a system at the same timeuch as when many people want to get pages from a single Web server.

Multi-core processors have several CPUs (referred to as "cores") integratento a single integrated-circuit chip. (implemenmts hyperthreading, i.e. more than one core that juggled threads)

Hyperthreading, sometimes called simultaneous multi-threading, is a techique that allows a single CPU to execute multiple flows of control. It involveaving multiple copies of some of the CPU hardware, such as program counternd register files, while having only single copies of other parts of the hardwareuch as the units that perform floating-point arithmetic

a hyperthreaded processor decides which of its threads to execute on a cycley-cycle basis. It enables the CPU to make better advantage of its processinesources. For example, if one thread must wait for some data to be loaded int cache, the CPU can proceed with the execution of a different thread. As an exmple, the Intel Core i7 processor can have each core executing two threads, ano a four-core system can actually execute eight threads in parallel.

modern processors can execute multiplnstructions at one time, a property known as instruction-level parallelism.

#### PARALELLISM: parallelism to refers to the use of concurrency to make a system run faster

Concurrency vs. Parallelism: Concurrency is running multiple processes over a given span of time, paralellism is running two or more processes at the same time.
(Concurrency can include running in parallel, simultaneously, or in multiple threads that interleave and processing is jumping back and forth between then, i.e. not simultaneous execution)

---


