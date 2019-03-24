SECTION .text
	GLOBAL _start 
_start:
	mov eax, 5
	mov ebx, 6
	mov ecx, 7
	cmp ecx, 6
	je BB2
	mov eax, 7
	jmp BB3

BB2:	mov eax, 5
	mov ebx, 6
	mov ecx, 7

BB3:	mov eax,1            ; 'exit' system call
	mov ebx,0            ; exit with error code 0
	int 80h              ; call the kernel

