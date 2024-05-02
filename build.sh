#!/bin/bash

# Assembly build
nasm -f elf64 float_to_int.asm -g
gcc -m64 -o main float_to_int.o main.c -g

# Shared library build
gcc -c -Wall -Werror -fpic lib_float_to_int.c
gcc -shared -o lib_float_to_int.so lib_float_to_int.o float_to_int.o

rm -f *.o
