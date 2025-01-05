# Virtualization

    - [Helpful article](https://www.brendangregg.com/blog/2017-11-29/aws-ec2-virtualization-2017.html)
    - [Video](https://learn.cantrill.io/courses/1101194/lectures/27026221)

### Virtualization defined

- The process of running more than one operating system on a piece of hardware

### Historical/Traditional Architecture (before Virtualization)

- Traditionally, part of the OS known as the Kernel operates in Privileged mode with special access to the hardware components of the computer (memory, storage, etc)
  - The Kernel is the only software in the OS that can directly interact with hardware
- Other software like Applications run in User mode (Unprivileged mode) and needs to make a System call through the Kernel to access hardware

## Virtualization solution

- Only one part of an OS can run in privileged mode
- Virtualization allows multiple OS's to run on the same system with access to privileged commands.
- Traditional/old Virtualization methods primarily relied on an inefficient software layer to "trick" the different Operating Systems on a device
- Hardware Virtualization was the breakthrough and more efficient solution, while SR-IOV Hardware Aware Virtualization is the fastest most efficient

### Emulated Virtualization

- Old way of virtualization and not as efficient - had to be done via software
- Guest Operating systems ran in Virtual Containers given fake emulated mappings to real hardware by Hypervisor software
- Still an OS with Kernel but with software known as a Hypervisor
  - The hypervisor software layer ran in privileged mode
  - The hypervisor provided fake emulated device information (i.e. storage, memory locations, devices) to each guest Operating System (The guest OS believed that the devices were real and not emulated)
    - The guest OS's use privileged system calls to read and write to what they think are real hardware devices (they are really just areas of physical disk allocated to them by the Hypervisor)
- To prevent guest Operating Systems overwriting memory of each other, etc., the Hypervisor performs **Binary Translation**
  - Any system calls that the guest OS's make are intercepted and translated by software in the Hypervisor
  - This process is very inefficient and slow

### Para-Virtualization

- Works on a small subset of operating systems, only OSs that can be modified
  - modifies the areas of guest operating systems that make system calls
  - The actual source code of the operating system is modified!
- The modified parts of the guest OSs make privileged calls to the Hypervisor software layer instead of calling the hardware
- Modifications were dependent on and modified for the specific Hypervisor in use
  - **Not Generalized Virtualization as with Emulated Virtualization - meant for a particular vendor!**
- Massive improvement in performance compared to Emulated Virtualization

### Hardware Virtualization (Hardware Assisted Virtualization)

- Virtualization Aware Hardware
- Major improvement in virtualization was moving away from above software methods into those where the physical hardware was aware of the virtualization
- The CPU was aware of virtualization (instead of just a software layer on the device)
  - The CPU expects privileged system calls from guest operating systems and traps them and does not halt
  - The guest OSs still think they are directing the calls directly to the hardware, but the hardware redirects them to the Hypervisor since they can't be run as-is. The Hypervisor handles how they are executed

#### The major performance impact is I/O

- Each virtual container uses logical devices, not actual physical ones, so there has to be a software layer in between for operations against the hard disk, network cards, etc. which consumes more CPU cycles on the host machine

### SR-IOV (Signal route I/O Virtualization)

- The hardware devices themselves become Virtualization Aware
- Allows a network or any other add-on card in a computer to present itself as several mini cards instead of one single card.
  - Supported in hardware, not software, and are seen as fully unique hardware cards from the guest OS perspective dedicated for its use
  - No translation is needed by the Hypervisor software which increases performance even more. The guest OS can directly use it's card
  - Known as Enhanced Networking in AWS
