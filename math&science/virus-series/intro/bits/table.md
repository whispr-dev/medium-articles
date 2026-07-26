\# Computer Virus Architecture: Comprehensive Reference

\*Based on 9 sources\*


Part I covers the mechanisms table with all the viral techniques, their functions, targets, and trade-offs
Part II breaks down into:

Core architectural components (search, copy, anti-detection, payloads)
EXE infection criteria (signature checks, infection markers)
File manipulation methods (overwriting, prepending, appending, stealth)
Cybersecurity literature references


---



\## Part I: Characteristics and Mechanisms of Computer Virus Architectures



| Viral Component/Technique | Primary Function | Target File Type | Architecture/Mechanism Details | Stealth or Detection Avoidance Strategy | Associated Trade-offs (Inferred) | Source |

|--------------------------|------------------|------------------|-------------------------------|----------------------------------------|----------------------------------|--------|

| Search Routine | Locates new files or disks for infection | COM, EXE, SYS, Batch, etc. | Uses wildcards like `\*.com`; logic determines efficiency and scope of replication across disks. | Limited scope to avoid unusual disk activity and user suspicion. | Increased sophistication improves reproduction but increases viral size and risk of detection through high activity. | \[1, 2] |

| Copy Routine | Reproduces viral code into a target program | COM, EXE | Smaller for COM files; larger/complex for EXE due to file structure requirements and internal complexity. | Minimal code size to avoid being noticed; attaches to host programs without immediate detection. | Simplicity reduces detection risk but limits target compatibility; complex routines are harder to implement. | \[1, 2] |

| EXE Header Manipulation / Architectural Verification | Directs execution flow and identifies suitable infection targets | EXE | Modifies Initial CS:IP and SS:SP; checks for "MZ" signature at 00H, zero Overlay Number at 1AH, and DOS format (table offset < 40H). | Maintains original header values or avoids non-standard files (Windows/OS2) to prevent system crashes and maintain host control. | Complex coding required; risk of trashing non-standard formats; limits the range of potential targets to ensure reliability. | \[1, 2] |

| Parasitic Appending or Prepending | Attaches to file without destroying host | COM, EXE | Virus body at end or start of file; prepares `INT 3→5` bytes with a jump (E9H) or modifies header (Initial IP) to run virus first. | Restores original bytes in memory or masks file growth and date changes to run host normally. | Larger file size compared to overwriting; slower infection; more complex than overwriting but more successful at remaining hidden. | \[1-3] |

| Interrupt Hooking (Stealth) | Intercepts system calls to hide presence | Boot Sector, Files | Hooks INT 21H or INT 13H; redirects calls to original handlers while filtering processing to shortcut OS calls. | Reports original file size (Scan INT/4EH), original date/time, or original boot sector data (INT 13H/02H). | Must remain memory resident; detectable by behavior checkers or software scanning for illegal interrupt hooks. | \[1, 2, 4] |

| Encryption and Polymorphism / VME | Evades signature-based scanners using varying code | COM, EXE, All files | Visible Mutation Engine (VME) generates unique decryption routines and encrypted bodies for every new infection. | No constant scan string exists; uses random instructions like NOP, PUSH/POP to ensure no two copies look alike. | Increases viral size and complexity; potential for decryption errors; can be detected by heuristic or spectral analysis. | \[1, 2] |

| Companion Infection | Executes virus before host program | COM, EXE | Renames host (e.g., to .CON or .EXE) and creates virus with original host name (.COM). | Sets hidden attributes on files; calls the renamed original host to maintain the appearance of functionality. | Relies on DOS search order (COM before EXE); requires maintaining two files which can be spotted during file system audits. | \[1, 2] |

| Overwriting Infection | Infection by replacement | COM, EXE | Replaces the beginning of a program (e.g., first 44 bytes) with viral code, destroying original content. | Often lacks stealth; can use "overlays" to avoid increasing file size. | Easiest to program but highly obvious to the user because the host file is destroyed or fails to run. | \[1, 2, 4, 5] |

| Self-Identification Flags | Avoids re-infection | EXE | Checks Initial IP field for specific values (e.g., 0057H) or sets file date far into the future. | Prevents redundant file growth and unnecessary disk activity to alert the user. | Required for stability, but the unique flag itself can become a signature for anti-virus programs to track. | \[2] |

| Genetic Mutation | Evolves gene sequence to evade scanners | Encrypted Viruses | Uses bit-flipping (MUTATE) on a 100-byte gene; replaces LCG32 random seed. | Descent-with-modification allows children to inherit traits that evaded detection. | Requires many generations and replications to become effective against specific scanners. | \[1] |

| Protected Mode Stealth | Ultimate hardware-level cloaking | All (Resident) | V86 mode monitor; Interrupt Descriptor Table (IDT) manipulation; Paging. | Hooks I/O ports (1F0H-1F7H) to redirect hardware reads; pages virus out of memory. | Extremely difficult to program and debug; hardware-dependent and causes OS conflicts. | \[1] |



---



\## Part II: Architecture Components, Infection Criteria and Literature



\### Viral Architecture - Core Components



| Subject Area | Component or Requirement | Description | Technical Specifications | Functionality or Impact | Source |

|--------------|-------------------------|-------------|-------------------------|------------------------|--------|

| Viral Architecture | Search Routine | Subroutine that identifies potential target files or disks for infection. | Uses DOS Search First (`1E H`) and Search Next (`4F H`) functions; results in 43-byte Disk Transfer Area (DTA). Trade-off between code complexity and instruction size. | Determines reproduction speed and scope, such as whether it infects multiple disks or specific disk areas. | \[1, 2] |

| Viral Architecture | Copy Routine | Routine responsible for duplicating viral code into a target identified by the search routine. | Binary write operations; complexity depends on target file type (e.g., higher for complex EXE structures compared to COM). | Essential for the physical spread of the virus; ensures the virus replicates and attaches to host programs. | \[1, 2] |

| Viral Architecture | Anti-detection Routines | Structures used to camouflage the virus or deceive anti-virus monitors. | Preservation of original file date/time stamps; hooking Interrupt 21 H. | Improves longevity by hiding the presence of the infection from users and software. | \[2] |

| Viral Architecture | Payloads | Routines unrelated to reproduction, such as logic bombs. | Can perform mischievous, beneficial, or destructive actions. | Executes specific tasks like displaying messages or destroying data. | \[2] |



\### EXE Infection Criteria



| Subject Area | Component or Requirement | Description | Technical Specifications | Functionality or Impact | Source |

|--------------|-------------------------|-------------|-------------------------|------------------------|--------|

| EXE Infection Criteria | Signature Check | Verification of the file header to ensure the target is a valid executable. | Check for hexadecimal bytes "MZ" (`4D 5A`) at offset 0 of the file header. | Ensures the virus only attempts to infect compatible executable formats, preventing system crashes and OS errors. | \[1, 2] |

| EXE Infection Criteria | Infection Marker Check | Check for existing viral signatures to prevent multiple redundant infections. | Comparison of Initial IP field at offset `14H` in the EXE header; for Intruder-B, the marker is `0057H`. | Prevents file size bloating and instability caused by repeatedly re-infecting the same file. | \[1, 2] |



\### File Manipulation - Infection Methods



| Subject Area | Component or Requirement | Description | Technical Specifications | Functionality or Impact | Source |

|--------------|-------------------------|-------------|-------------------------|------------------------|--------|

| File Manipulation Methods | Overwriting | The simplest infection method where the virus replaces part of the host file's virus code. | Writes viral code (e.g., 44 bytes for MINI-44) directly to the start of the file (offset `100H` for COM) using DOS calls (AH `40H`). | Easiest to program but highly destructive, as the original host program functionality is destroyed. | \[1-3] |

| File Manipulation Methods | Parasitic (Prepending) | Inserting the virus at the beginning of the host while shifting original code further down. | Reads host into memory, writes virus at offset `100H`, then appends original host code. | Non-destructive; allows the virus to execute first and then pass control to the original program. | \[1] |

| File Manipulation Methods | Parasitic (Appending) | Body of the virus is added to the end of the host file. | Modifies the first few bytes of the host with a NEAR JMP (`E9` Hex); header modified to jump to end; final jump returns to host start. | Faster infection as only viral code is written; ensures virus runs first while maintaining host functionality. | \[1, 2, 4] |

| File Manipulation Methods | Stealth Programming | Intercepting OS requests to hide changes made to files. | Hooking Interrupt `21 H` to subtract viral size from reported file length. | Deceives users and scanners by returning original file size, date/time, or original boot sector data (INT `13H/02H`). | \[2, 5] |



\### Cybersecurity Literature



| Subject Area | Component or Requirement | Description | Technical Specifications | Functionality or Impact | Source |

|--------------|-------------------------|-------------|-------------------------|------------------------|--------|

| Cybersecurity Literature | The Giant Black Book of Computer Viruses | A technical guide focused on the mechanics of virus programming and defence. | Authored by Mark Ludwig; includes source code for COM, EXE, and Boot Sector viruses; ISBN 0-929408-33-0. | Intended to educate professionals on viral defence, military applications, and computational artificial life. | \[1] |

| Cybersecurity Literature | The Happy Hacker | Educational material regarding hacking techniques and internet security. | Fourth Edition released December 2001; authored by Carolyn P. Meinel. | Provides updates on hacking websites, Windows operating systems, and internet back doors. | \[1] |

| Cybersecurity Literature | Hacking: The Art of Exploitation | Book covering technical aspects of hacking including programming and memory. | Author: Jon Erickson; includes Linux environment on CD. | Teaches technical exploitation, shellcode, and buffer (e.g., overflows. | \[6] |

| Cybersecurity Literature | A Bug Hunter's Diary | Case studies of software vulnerabilities and real-world flaws. | Author: Tobias Klein; published October 2011. | Provides insights into the thought process behind finding vulnerabilities. | \[6] |

| Cybersecurity Literature | Assembler Inside and Out | Recommended reading for learning Assembly language for virus research. | Not in source | Provides the necessary coding knowledge for foundational virus construction. | \[3] |



---



\## References



\[1] The Giant Black Book of Computer Viruses.pdf  

\[2] All notes 1/01/2026  

\[3] overwriting\_virus\_tutorial\_#1.md  

\[4] viral\_code\_addition.md  

\[5] file\_infecting\_vir.md  

\[6] hacking\_books.pdf  



---



\*Compiled for research and educational purposes in cybersecurity defence\*

