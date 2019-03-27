SECTION .text
	GLOBAL _start 
_start:
	mov eax, 5
	mov ebx, 6
	mov ecx, 7
	cmp ecx, 1
	jne BB2
	cmp eax, 2
	je BB3
	cmp eax, 3
	je BB4
	cmp eax, 4
	je BB5
	
BB2:	mov eax, 5
	mov ebx, 6
	mov ecx, 7
BB3:	mov eax, 8
	mov ebx, 9
	mov ecx, 10
BB4:	mov eax, 11
	mov ebx, 12
	mov ecx, 13
BB5:	mov eax,1            ; 'exit' system call
	mov ebx,0            ; exit with error code 0
	int 80h              ; call the kernel
