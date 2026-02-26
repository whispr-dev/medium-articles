Studio
Note
Mechanisms of Computer Virus Infection and Stealth Tactics
(Saved responses are view only)
Computer viruses manipulate files through several primary methods, ranging from basic overwriting to sophisticated architectural modifications. To remain hidden, they employ stealth techniques, encryption, and polymorphism to deceive scanners and system monitors.
Primary File Manipulation Methods
Viruses generally use the following techniques to integrate themselves into a host system:
• Overwriting: This is the simplest and most destructive method where the virus replaces the beginning of a program with its own code. While easy to program, it effectively destroys the original file, making the infection obvious once the programme fails to run.
• Companion Infections: A virus renames the target programme to a non-standard name and then replaces the original file name with itself. When the user attempts to run the programme, the virus executes first and then calls the renamed original host.
• Parasitic Appending or Prepending: These viruses attach themselves to the end or beginning of a file without destroying the original code. By modifying the file header, the virus ensures it runs first and then jumps back to the host programme, making the file appear functional while hidden.
• Boot Sector Infection: These viruses replace the first sector of a disk (the boot sector or master boot record). Because this code is the first to execute upon starting the computer, the virus gains control before the operating system even loads.
• Source Code Infection: More advanced viruses target source files (such as .C or .PAS files) by inserting #include statements or function calls. The virus then becomes a permanent part of the executable once the programmer recompiles their code.
Methods for Avoiding System Detection
To bypass anti-virus software and system integrity checks, viruses utilise a range of deceptive tactics:
• Stealth Programming: This is the art of returning only original, unchanged values when the operating system requests information about a file, such as its size or creation date. By hooking Interrupt 21H, a virus can subtract its own size from the reported file length, convincing the user that nothing has changed.
• Encryption and Polymorphism: Many viruses encrypt their main body so that scanners cannot find a fixed "scan string" of code. Polymorphic viruses go further by using a code generator to create a different decryption routine every time they replicate, ensuring no two copies look exactly alike.
• Memory Stealthing: Resident viruses often hide in "memory holes"—unused segments of RAM—to avoid being detected by memory scanners. Some utilize protected mode paging to map themselves into physical memory that is entirely hidden from the virtual machine running the operating system.
• Self-Identification Flags: To avoid re-infecting the same file (which might cause noticeable file growth), viruses often set a specific flag. For example, a virus might set the file's "seconds" count or creation date far into the future (e.g., the year 2037), which the resident virus recognizes but masks from the user.
• Genetic Evolution: Advanced viruses can use a "gene"—a fixed array of bytes—to make decisions on how to mutate. Through Darwinian evolution, the virus population learns over several generations which mutations successfully evade specific scanners, eventually producing a strain that is nearly invisible to detection.
• Retaliation: Some viruses actively scan memory for anti-virus programmes. If a monitor is found, the virus may attempt to uninstall or disable the anti-virus, or even trigger a logic bomb to simulate hardware failure as a diversion.
Operating System Vulnerabilities
Viruses can also exploit covert channels in the operating system to leak information across security levels. By manipulating shared resources, such as disk space availability or global memory buffers, a virus can transmit data from a high-security process to a low-security capture programme without using standard file systems.
Would you like to explore how specific operating systems, such as Windows 95 or Unix, differ in their vulnerability to these stealth tactics?
