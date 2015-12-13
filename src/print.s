.data
nl:   .asciiz "\n"
.text

.globl printint
printint:
  li    $v0, 1
  syscall

  addi $sp,$sp,-4
  sw $a0, ($sp)

  la    $a0, nl
  li    $v0, 4
  syscall

  lw $a0,($sp)
  addi $sp,$sp,4

  jr $ra

.globl printchar
printchar:
  li    $v0, 11
  syscall

  addi $sp,$sp,-4
  sw $a0, ($sp)

  la    $a0, nl
  li    $v0, 4
  syscall

  lw $a0,($sp)
  addi $sp,$sp,4

  jr $ra


# a0 - sleep duration
.globl sleep
sleep:
la $v0,32
syscall
jr $ra

# a0 - pitch
# a1 - duration
# a2 - instrument
# a3 - volume
.globl playsound
# Play Sound
playsound:
la $v0, 31
syscall
#move $a0,$a1
#la $v0,32
#syscall
jr $ra