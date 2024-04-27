#include <stdio.h>

extern int asm_main(float);

int float_to_int(float num) {
    int int_num = 0;
    int_num = asm_main(num);
    return int_num;
}
