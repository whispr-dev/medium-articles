
Criteria for Viral Selection in EXE Files
(Saved responses are view only)
To determine if an EXE file is suitable for infection, specific architectural criteria must be met to ensure the virus can execute without crashing the host program or being easily detected. According to the sources, the following five criteria are used by viruses like Intruder-B to identify infectable EXE files:
1. Genuine EXE Signature
The file must be a true EXE program, which is identified by the "MZ" signature at the very beginning of the file header. If these characters are missing, the operating system may attempt to treat the file as a COM file instead.
2. Zero Overlay Number
The Overlay Number field in the EXE header must be set to zero. Viruses often avoid infecting overlays because the main program calling them may have highly specific expectations about their contents, and an infection could cause the system to fail.
3. Space in the Relocation Pointer Table
The host file must have enough room in its relocation pointer table to accommodate additional pointers required by the virus. This is determined by a calculation involving the header size, the number of existing relocatables, and the table offset. If there is no room to add these pointers without enlarging the header, some viruses will skip the file to avoid the time-consuming and obvious chore of moving the entire load module.
4. Standard DOS Format
The file must be a purely DOS EXE rather than an extended Windows or OS/2 EXE. These extended formats can be identified by the location of the relocation pointer table; if the table is at offset 40H or higher, it is not a standard DOS EXE and is typically avoided to prevent compatibility issues.
5. Absence of Previous Infection
To prevent re-infecting the same file, the virus checks the Initial IP field in the EXE header. A virus will often set this field to a specific unique value (such as 0057H) upon infection. If a potential host already contains this specific value, the virus assumes it is already present and skips the file.
Would you like to know more about how viruses manipulate the EXE header to ensure they gain control of the system before the host program executes?
NotebookLM can be inaccurate; please double-check its responses.
Video Overview 'A Relic's Security Lessons' is ready.
