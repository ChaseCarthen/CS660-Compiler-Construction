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
  jr $ra

.globl printchar
printchar:
  li    $v0, 11
  syscall
  la    $a0, nl
  li    $v0, 4
  syscall
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