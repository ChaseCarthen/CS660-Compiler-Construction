main:
		addiu $sp,$sp,-36
		sw $ra,0($sp)
		sw $s0,4($sp)
		sw $s1,8($sp)
		sw $s2,12($sp)
		sw $s3,16($sp)
		sw $s4,20($sp)
		sw $s5,24($sp)
		sw $s6,28($sp)
		sw $s7,32($sp)
		move $s0,$t0
		sw $s0,36($sp)
		move $s0,$zero
		sw $s0,36($sp)
		j label_100000
	label_100000:
		move $a0,$s0
jal printint
	label_100001:
		addi $t1,$s0,1
		move $s0,$t1
		sw $s0,36($sp)
		slt $t2,$s0,10
		bne $zero,$t2,label_100000
		lw $ra,0($sp)
		lw $s0,4($sp)
		lw $s1,8($sp)
		lw $s2,12($sp)
		lw $s3,16($sp)
		lw $s4,20($sp)
		lw $s5,24($sp)
		lw $s6,28($sp)
		lw $s7,32($sp)
		addiu $sp,$sp,36
		jr $ra


#Adding Generated print functions

.data
nl:   .asciiz "\n"
.text

.globl printint
printint:
  li    $v0, 1
  syscall
  la    $a0, nl
  li    $v0, 4
  syscall
  j $ra

.globl printchar
printchar:
  li    $v0, 11
  syscall
  la    $a0, nl
  li    $v0, 4
  syscall
  j $ra
