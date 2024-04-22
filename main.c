#include <stdio.h>
#include <stdlib.h>
#include "lib_float_to_int.c"

int main_asm(float);

int main() {
    char input[100];
    float float_num;
    int int_num;

    printf("Enter a float number: ");
    fgets(input, sizeof(input), stdin);

    float_num = strtod(input, NULL);

    int_num = float_to_int(float_num);
    
    printf("The integer number is: %d\n", int_num);
    return 0;
}
