ANSI C to MIPS Compiler
========================================
*Institution: University of Nevada, Reno*<br/>
*Course: CS660: Compiler Construction*<br/>
*Author: Chase Carthen*<br/>
*Author: Nolan Burfield*<br/>
*Author: Vinh Le*<br/>
*Date: 12/15/15*

========================================

To run this compiler
---------------------

*On ubuntu it can be installed with these commands*

>$ sudo apt-get install python-pip spim <br/>
>$ sudo pip install ply bintrees strconv termcolor <br/>

To run this compiler:

>$ python driver.py input_file<br/>
>$ spim a input_asm<br/>
The spim command will verify the results<br/><br/>
Flags offered by this compiler can be referenced using the <br/>
>$ python driver.py -h<br/>

Dependencies
========================================
**Python - Main Language of this Compiler Project**<br>
**PiP - This module allows for easy of use in installing these python modules. **<br>
**PLY - This module mimics the C equivalent of Flex and Yacc **<br>
**Bintrees - This module allows for an easy of use Red-Black Tree **<br>
**StrConv - This module allows for the type inference needed for type checking **<br>
**TermColor - Chase has OCD for coloring text **<br>


Features
==================================================
**Type Definitions - Capable of handling simple variable types(char, int).**<br>
**N-Arrays - Fully Functional.**<br>
**Functions - Fully Functional.**<br>
**Constants - Fully Functional.**<br>
**Recognize Syntax Errors - Can locate errors and provide IMPROVED feedback.**<br>
**Constant Value Arithmetic - Capable of optimizing simple arithmetic.**<br>
**For Loop - Fully Functional.**<br>
**While Loop - Fully Functional.**<br>
**Function Declarations - Fully Functional.**<br>
**Function Definitions - Fully Functional.**<br>
**Variable Declarions/Calls - Fully Functional.**<br>
**If/Else - Fully Functional.**<br>
**Simple Assignment - Fully Functional.**<br>
**Type Checking - Fully Functional.**<br>
**Pointer - Simple 1D Pointers **<br>
**Structs - No Array of Structs **<br>


Additional Notes
=========================================
**Assignment Completed in Python 2.7** <br/>
<br/>
Extra credit: 1D Pointers, Structs, Multiple Dimensions, Recursion<br/>
<br/>

