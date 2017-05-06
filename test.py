#Example of program for the Small programming language

import small

# Enable the debuging information
small.getGlobalContext().debug = True

# Hello world

small.execString("Hello println")

# Simple expressions

small.execString("10 5 + println")
small.execString("4 5 6 7 8 * / + - 1 + println")

# Simple variables

small.execString("5 a set 10 b set a get b get + println")


# Simple execution

small.execString("{ Hello println } f set f get exec")

# Call the function "test" in the standard library

small.execString("std.sml load exec test get exec")

# Recursion

small.execString("5 i set { i get println i get 1 - i set i get 0 > { h get exec } { } if } h set h get exec")

# Play with lists

small.execString("{ 10 11 12 13 } length println")
small.execString("{ 10 11 12 13 } { 14 15 16 } merge println")
small.execString("{ 10 11 12 13 } tail println")

# For from the standard library

small.execString("std.sml load exec i 2 8 { i: print i get println } for get exec")

# Factorial from the standard library

small.execString("std.sml load exec 5 factorial get exec println")

# Execute the program in test.sml

small.execString("test.sml load exec")

print("done")
