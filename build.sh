#!/bin/bash

gcc -c -Wall -Werror -fpic lib_float_to_int.c
gcc -shared -o lib_float_to_int.so lib_float_to_int.o

nasm -f elf32 float_to_int.asm -g
gcc -m32 -o main float_to_int.o main.c -g

rm -f *.o