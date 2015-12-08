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
